try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup


class HTMLParser(object):
    instance = None

    @classmethod
    def make(cls):
        if not cls.instance:
            cls.instance = cls()

        return cls.instance

    def parse(self, html):
        return BeautifulSoup(html, features="html.parser")
