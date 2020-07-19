"""link_finder.py: Find links from RAW HTML."""
__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Production"

from html.parser import HTMLParser
from urllib import parse


class LinkFinder(HTMLParser):

    def __init__(self, base_url):
        super().__init__()
        self.data = set()
        self.base_url = base_url

    # When we call HTMLParser feed() this function is called when it encounters an opening tag <a>
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
            # Check the list of defined attributes.
            for name, value in attrs:
                # If href is defined, and not empty nor # add it to set.
                if name == "href" and value != "#" and value != '':
                    # If not already in data.
                    if value not in self.data:
                        url = parse.urljoin(self.base_url, value)
                        self.data.add(url)

    # ERROR's
    def error(self):
        pass

    # Get the URL's
    def getURLs(self):
        return self.data
