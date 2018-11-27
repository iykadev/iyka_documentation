import math
import urllib
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse

import simplejson as json

from node import Node


class atdict(dict):
    def __getattr__(self, item):
        return self.get(item)


root = Node.make_root("root", "Documentation Web-Service Docs", "This documentation web-service is designed to isolate the documentation structure creation and maintenance from the root project that it is describe. Hierarchical(tree-like) design is embedded into this utility and is its intended use case.")

# overview = root.add("overview", "Overview")

nodes = root.add("nodes", "Nodes", "The nodes module is the centerpiece of this package. It is designed with the idea that each node represents a directory in a file-system, with each parent child relation of nodes representing the relative paths to each directory.")
creating = nodes.add("creating", "Creating a root node", "A root node can be created by invoking the Node class method Node.make_root(name, label, description).")
adding = nodes.add("adding", "Adding children nodes", "The child node can be created and added to a parent node by invoking the Node instance method parent.add(name, label, description). A child node can alternatively be created, although discouraged, by invoking the Node class method Node.make(name, label, description). Then the child node can be added by invoking the Node class method parent._add(child)")
rendering = nodes.add("rendering", "Rendering a node structure", "In order to generate the designed file-structure, the node-structure must be rendered. The node structure can be rendered by invoking the Node instance method render(memo=dict(<tags go here>). Additional options can be passed as memos to the render function to specify how to render the node-structure.")
debug = rendering.add("debug", "Debug Mode", "Enable/Disable Debug Output. tag: debug type: boolean")
custom_rendering = rendering.add("custom_rendering", "Custom Renderer", "Specify a custom render function. tag: custom_renderer type: function")
templates = rendering.add("templates", "Overriding Default Templates", "Override the directory of the base doc page and base link template. tag: template_page  type: string tag: template_sublink type: string")
overriding = rendering.add("overriding", "Overriding Existing index.html files", "Override existing index.html files. tag: override_files type: boolean")
starting_from_scratch = rendering.add("starting_from_scratch", "Starting from Scratch", "Erase root and children directories and regenerate from scratch. tag: start_from_scratch type: boolean")
syncing = nodes.add("syncing", "Loading and Syncing existing node structures", "Node structures can also be loaded from json strings and dictionary object via the corresponding functions: Node.load_from_json(data) and Node.load_from_dict(data)")
other = nodes.add("other", "Other information about nodes", "Nodes cache the label and description located within the index.html file within their respective directory. Node do not maintain a list of \"known\" files within their corresponding directory, other than of course index.html.")

func_class_defs = root.add("func_class_defs", "Function/Class Definitions")

node = func_class_defs.add("node", "Node")
make_root = node.add("make_root", "make_root")
make = node.add("make", "make")
load_from_dict = node.add("load_from_dict", "load_from_dict")
load_from_json = node.add("load_from_json", "load_from_json")
to_dict = node.add("to_dict", "to_dict")
to_json = node.add("to_json", "to_json")
add = node.add("add", "add")
get_path = node.add("get_path", "get_path")
get_tokenized_path = node.add("get_tokenized_path", "get_tokenized_path")
render = node.add("render", "render")
scan = node.add("scan", "scan")
find = node.add("find", "find")
get_file = node.add("get_file", "get_file")

file = func_class_defs.add("file", "File")

html_parser = func_class_defs.add("html_parser", "HTMLParser")
html_parser.add("make", "make")
html_parser.add("parse", "parse")

root.render(memo={"start_from_scratch": True})


# root = Node.make_root("documentation", "Documentation", "This is the documentation's root page. This is where you can find all of the top-level concepts outlined.")
# root.scan()
#
# getting_started = root.add("getting_started", "Getting Started")
# getting_started.add("signing_up", "Signing Up")
# getting_started.add("overview", "Overview")
# settings = getting_started.add("settings", "Settings")
# settings.add("profile_and_account", "Profile and Account")
# collaborators = settings.add("collaborators", "Collaborators")
# collaborators.add("group_actions", "Group Actions")
# collaborators.add("member_actions", "Member Actions")
# settings.add("inbox", "Inbox")
#
# dashboard = root.add("dashboard", "Dashboard")
# dashboard.add("watchlist", "Watchlist")
# dashboard.add("symbol_pouch", "Symbol Pouch")
# dashboard.add("symbol_details", "Symbol Details")
#
# strategies = root.add("strategies", "Strategies")
# strategies.add("creating_a_strategy", "Creating a Strategy")
# strategies.add("coding_a_strategy_in_open_close_position_criteria", "Coding a Strategy in Open-Close Position Criteria")
# strategies.add("coding_a_strategy_in_python", "Coding a Strategy in Python")
# strategies.add("verifying_a_strategy", "Verifying a Strategy")
# strategies.add("backtesting_a_strategy", "Backtesting a Strategy")
# strategies.add("trading_with_a_strategy", "Trading with a Strategy")
# strategies.add("sharing_a_strategy", "Sharing a Strategy")
# other_strategy_actions = strategies.add("other_strategy_actions", "Other Strategy Actions")
# other_strategy_actions.add("strategy_status", "Strategy Status")
# other_strategy_actions.add("cloning_a_strategy", "Cloning a Strategy")
# other_strategy_actions.add("archiving_a_strategy", "Archiving a Strategy")
# other_strategy_actions.add("viewing_all_backtests_and_trading_sessions", "Viewing all Backtests and Trading Sessions")
#
# backtesting = root.add("backtesting", "Backtesting")
# backtesting.add("backtest_dashboard", "Backtest Dashboard")
# backtesting.add("backtest_results", "Backtest Results")
# backtesting.add("backtest_actions", "Backtest Actions")
#
# trading = root.add("trading", "Trading")
# trading.add("trading_accounts", "Trading Accounts")
# trading.add("trading_sessions", "Trading Sessions")
# trading.add("trading_information", "Trading Information")
#
# selectors = root.add("selectors", "Selectors")
# selectors.add("creating_a_selector", "Creating a Selector")
# selectors.add("static_list", "Static List")
# selectors.add("dynamic_list", "Dynamic List")
# selectors.add("selector_actions", "Selector Actions")
#
# factors = root.add("factors", "Factors")
# factors.add("creating_a_factor", "Creating a Factor")
# factors.add("coding_a_factor_in_open_close_position_criteria", "Coding a Factor in Open-Close Position Criteria")
# factors.add("coding_a_factor_in_python", "Coding a Factor in Python")
# factors.add("using_factors", "Using Factors")
# factors.add("making_factors_available", "Make Factors Available")
#
# data = root.add("data", "Data")
# data.add("data", "Data")
# data_browser = data.add("data_browser", "Data Browser")
# data_browser.add("selection_criteria", "Selection Criteria")
#
# root.add("keyword_reference", "Keyword Reference")
#
# root.render(memo={"start_from_scratch": True})


class WebServer(BaseHTTPRequestHandler):

    def parse_query(self):
        d = atdict()

        try:
            parsed_path = parse.urlparse(self.path)
            q = parsed_path.query
        except Exception as e:
            q = ""

        if not q:
            return d
        for v in q.split('&'):
            vals = v.split('=')
            k = vals[0]
            if len(vals) > 1:
                V = vals[1]

                try:
                    V = urllib.parse.unquote(V)
                except:
                    pass
                v = V
                try:
                    V = json.loads("{'x':" + V + '}')

                    v = V['x']
                except:
                    v = V
                if type(v) is str and v.isdigit():
                    v = float(v)
                    if v == math.floor(v):
                        v = int(v)
            d[k] = v

        return d

    def read_message(self):
        parsed_path = parse.urlparse(self.path)

        if '/' in self.path:
            path = self.path.split("/")

            if '.' in path[-1]:
                file = path[-1]

                if '?' in file:
                    file = file.replace('?', '')

                ext = file[file.index('.') + 1:]
            else:
                file = ""
                ext = ""

        d = atdict(command=self.command,
                   path=self.path,
                   file=file,
                   ext=ext,
                   real_path=parsed_path.path,
                   query=parsed_path.query,
                   request_version=self.request_version
                   )
        d["CLIENT VALUES"] = atdict(client_address=self.client_address, address_string=self.address_string())
        d["SERVER VALUES"] = atdict(server_version=self.server_version, sys_version=self.sys_version, protocol_version=self.protocol_version)
        d["HEADERS"] = atdict(self.headers)
        d["QUERY"] = self.parse_query()

        return d

    # OPTIONS
    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", '*')
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")

    # GET
    def do_GET(self):
        # Send response status code
        message = self.read_message()
        self.send_response(200)

        content = self.process_request(message)

        if not content:
            content = json.dumps({"error": "invalid criteria"})

        if not isinstance(content, bytes):
            content = bytes(content, "utf-8")

        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-length", str(len(content)))
        # self.send_header("Content-Encoding", "gzip")
        # self.send_header("Content-type", "text/x-json")
        self.end_headers()

        self.wfile.write(content)

    # @staticmethod
    # def rreplace(s, old, new, occurrence):
    #     li = s.rsplit(old, occurrence)
    #     return new.join(li)

    def process_request(self, msg):
        result = ""
        error = ""

        q = msg.QUERY

        if not q:
            path = msg.path
            file = msg.file
            ext = msg.ext

            print(path, file, ext)

            if path == '/':
                return "Main Page"
            elif ext == "html":
                path = msg.path[1:msg.path.rindex('/')].replace('/', '.')

                if path:
                    node = root.find(path)

                    if node:
                        return node.get_file(file).content
                    else:
                        with open("templates/error_404.html", "r") as f:
                            data = f.read()
                            return data
            elif ext in ("ico", "png", "jpg"):
                if file == "favicon.ico":
                    path = "static" + path
                else:
                    path = "static/images" + path

                with open(path, "rb") as f:
                    data = f.read()
                    return data

            return ""

        render_format = q.renderas if "renderas" in q else ""

        if "search" in q:
            node = root.find(q.search)

            if not render_format:
                if node:
                    result = node.get_file("index.html").content
                else:
                    error = "Invalid token: {token}".format(token=q.search)
            elif render_format == "html":
                if node:
                    return node.get_file("index.html").content
                else:
                    error = "Invalid token: {token}".format(token=q.search)
            else:
                error = "Invalid Render Format!"

        return json.dumps(atdict(query=str(msg.path), result=result, error=error))


def run():
    server_address = ("192.168.1.9", 8080)
    httpd = HTTPServer(server_address, WebServer)
    print(datetime.now(), "Server Starts - %s:%s" % server_address)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(datetime.now(), "Server Stops - %s:%s" % server_address)


if __name__ == "__main__":
    run()
