import errno
import json
import os
import pathlib
import re
import shutil

from htmlparser import HTMLParser


class Node(object):
    TEMPLATE_PAGE_PATH = "templates/page.html"
    TEMPLATE_SUBLINK_PATH = "templates/sublink.html"

    TEMPLATE_PAGE = None
    TEMPLATE_SUBLINK = None

    folders_generated = 0
    files_generated = 0

    nodes_generated = 0

    # load default template data
    with open(TEMPLATE_PAGE_PATH, "r") as file:
        TEMPLATE_PAGE = file.read()



    with open(TEMPLATE_SUBLINK_PATH, "r") as file:
        TEMPLATE_SUBLINK = file.read()

    # Class Definition
    def __init__(self, parent, name, label="", description=""):
        self.parent = parent
        self.name = name
        self.label = label
        self.description = description
        self.children = []

        Node.nodes_generated += 1

    def __contains__(self, key):
        path = self.get_path().replace("\\", "/")
        key = key.replace("\\", "/")

        return key == path or key == path + "/index.html"

    @classmethod
    def make_root(cls, name="", label="", description=""):
        return cls(None, name, label=label, description=description)

    @classmethod
    def make(cls, parent, name, label="", description=""):
        return cls(parent, name, label=label, description=description)

    @classmethod
    def load_from_dict(cls, data, parent=None):
        if not parent:
            node = cls.make_root(data["name"], label=data["label"], description=data["description"])
        else:
            node = cls.make(parent, data["name"], label=data["label"], description=data["description"])

        if data["subs"]:
            for child in data["subs"].values():
                node._add(cls.load_from_dict(child, node))

        return node

    @classmethod
    def load_from_json(cls, data):
        try:
            return cls.load_from_dict(json.loads(data))
        except Exception as e:
            print("Invalid data inputted")
            raise e

    def to_dict(self):
        node = dict()

        node["name"] = self.name
        node["label"] = self.label
        node["description"] = self.label
        node["subs"] = dict()

        for c in self.children:
            child_node = c.to_dict()
            node["subs"][c.name] = child_node

        return node

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)

    def _add(self, child):
        self.children.append(child)

    def add(self, name, label="", description=""):
        child = self.make(self, name, label=label, description=description)

        self._add(child)
        return child

    def get_path(self):
        if self.parent:
            return self.parent.get_path() + '/' + self.name
        return self.name

    def get_tokenized_path(self):
        if self.parent:
            return self.parent.get_tokenized_path() + '.' + self.name
        return self.name

    # Path Creation
    def _ensure_path(self, memo):
        path = self.get_path()

        if not self.parent and "start_from_scratch" in memo and memo["start_from_scratch"]:
            try:
                shutil.rmtree(path)

                if "debug" in memo and memo["debug"]:
                    print("The directory <{dir}> has been erased.".format(dir=path))
            except FileNotFoundError as e:
                if "debug" in memo and memo["debug"]:
                    print("The directory <{dir}> does not exist. Proceeding as usual.".format(dir=path))
            except PermissionError as e:
                print("The directory <{dir}> is currently in use. Please stop use and rerun to continue.".format(dir=getattr(e, "filename")))
                exit(1)

        try:
            pathlib.Path(path).mkdir(parents=False, exist_ok=False)
            if "debug" in memo and memo["debug"]:
                print("The directory <{dir}> has been generated".format(dir=path))
            Node.folders_generated += 1
        except FileExistsError as e:
            if "debug" in memo and memo["debug"]:
                print("The directory <{dir}> exists. Proceeding as usual.".format(dir=path))
        except PermissionError as e:
            print("The directory <{dir}> is currently in use. Please stop use and rerun to continue.".format(dir=getattr(e, "filename")))
            exit(1)

        return path

    VAR_REG = r"\$\{(\w+)\}"

    # Rendering
    def _render_sublinks(self, memo):
        if "template_sublink" in memo and memo["template_sublink"]:
            template_path = memo["template_sublink"]
            with open(template_path, "r") as file:
                template = file.read()
        else:
            template = self.TEMPLATE_SUBLINK

        result = []

        for c in self.children:
            data = {
                "path":'/' + c.get_path(),
                "label": c.label
            }

            result.append(re.sub(self.VAR_REG, lambda m: data.get(m.group(1), m.group(0)), template))

        result = "".join(result)
        return result

    def _render_page(self, label, description, subs, memo):
        if "template_page" in memo and memo["template_page"]:
            template_path = memo["template_page"]
            with open(template_path, "r") as file:
                html = file.read()
        else:
            html = self.TEMPLATE_PAGE

        data = {
            "label": label,
            "description": description,
            "parent": ("../index.html" if self.parent else ""),
            "subs": subs,
            "is_root": str(False if self.parent else True)
        }

        return re.sub(self.VAR_REG, lambda m: data.get(m.group(1), m.group(0)), html)

    def _render(self, memo):
        path = self._ensure_path(memo)

        html_file_path = path + "/index.html"

        file = pathlib.Path(html_file_path)

        if file.exists() and not ("override_files" in memo and memo["override_files"]):
            if "debug" in memo and memo["debug"]:
                print("index.html already exists within the path <{dir}>. Skipping file generation.".format(dir=path))
        else:
            if "debug" in memo and memo["debug"]:
                print("Generating index.html in the path <{dir}>".format(dir=path))

            if "custom_renderer" in memo and memo["custom_renderer"]:
                html = memo["custom_renderer"]()
            else:
                subs = self._render_sublinks(memo)
                html = self._render_page(self.label, self.description, subs, memo)

            try:
                with open(html_file_path, 'w') as file:
                    file.write(html)
            except PermissionError as e:
                print("The directory <{dir}> is currently in use. Please stop use and rerun to continue.".format(dir=getattr(e, "filename")))
                exit(1)

            Node.files_generated += 1

    # memo options:
    # debug: (boolean) enable debug output
    # custom_renderer: (function) custom render function
    # template_page: (str) template page file path
    # template_sublink: (str) template sublink file path
    # override_files: (boolean) override existing html files
    # start_from_scratch: (boolean) delete root node directory and regenerate all files in structure
    def render(self, memo={}):
        if not self.parent:
            Node.folders_generated = 0
            Node.files_generated = 0

        self._render(memo)

        for c in self.children:
            c.render(memo)

        if "debug" in memo and memo["debug"]:
            print()

        if not self.parent:
            print("{folders_generated} folders were generated.".format(folders_generated=Node.folders_generated))
            print("{files_generated} files were generated.".format(files_generated=Node.files_generated))
            print("{nodes_generated} nodes were generated.".format(nodes_generated=Node.nodes_generated))

    @staticmethod
    def _normalize_path(a, b):
        result = None

        if a in b:
            result = b.replace(a, '', 1)

            if '.' in result and not result.index('.'):
                result = result[1:]

        elif b in a:
            result = a.replace(b, '', 1)

            if '.' in result and not result.index('.'):
                result = result[1:]

        return result

    @staticmethod
    def _scan_non_indexed_dir(paths_found, dir):
        for file in os.listdir(dir):
            file_path = os.path.join(dir, file)

            if os.path.isfile(file_path):
                paths_found.append(("File", file_path))
            else:
                paths_found.append(("Folder", file_path))
                Node._scan_non_indexed_dir(paths_found, file_path)

    def _scan_indexed_dir(self, paths_found, memo):
        path = self.get_path()

        if not os.path.isdir(path):
            return

        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.isfile(file_path):
                if file_path not in self:
                    paths_found.append(("File", file_path))
            else:
                flag = True
                for c in self.children:
                    if file_path in c:
                        flag = False
                        break

                if flag:
                    paths_found.append(("Folder", file_path))
                    self._scan_non_indexed_dir(paths_found, file_path)

    def _scan_dir(self, paths_found, memo={}):
        self._scan_indexed_dir(paths_found, memo)

        for c in self.children:
            c._scan_dir(paths_found, memo)

    def _scan(self, dir):
        result = self.find(dir)
        node = result.add(Node._normalize_path(dir, result.get_tokenized_path()))
        data = node.get_file("index.html").content

        parser = HTMLParser.make()
        parsed_html = parser.parse(data)

        node.label = parsed_html.find(id="label").string
        node.description = parsed_html.find(id="description").string

    # memo options:
    def scan(self, memo={}):
        result = list()

        self._scan_dir(result, memo)

        for type, dir in result:
            dir = self._tokenize_dir(dir)
            if type == "Folder":
                self._scan(dir)

        if not self.parent:
            print("{nodes_generated} nodes were generated.".format(nodes_generated=Node.nodes_generated))

        return result

    def _tokenize_dir(self, dir):
        return dir[dir.index(self.name):].replace('/', '.').replace('\\', '.') if '/' in dir or '\\' in dir else dir

    def _find(self, path):

        if len(path) == 0 or path[0] != self.name:
            return None
        elif len(path) == 1:
            return self

        for c in self.children:
            result = c._find(path[1:])
            if result:
                return result

        return self

    def find(self, tokens):
        tokens = tokens.split('.')
        return self._find(tokens)

    def get_file(self, file_name):
        path = self.get_path()

        with open(path + '/' + file_name) as f:
            content = f.read()

        file = File(path + '/' + file_name, content)

        return file


class File(object):
    __slots__ = ['path', 'content']

    def __init__(self, path, content):
        self.path = path
        self.content = content
