"""email_spider.py: Core of this project."""
__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Production"

from urllib.request import urlopen
from .helper import *
from .link_finder import LinkFinder
from .email_finder import *

class EmailSpider:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        EmailSpider.project_name = project_name
        EmailSpider.base_url = base_url
        EmailSpider.domain_name = domain_name
        EmailSpider.queue_file = EmailSpider.project_name + '/queue.txt'
        EmailSpider.crawled_file = EmailSpider.project_name + '/crawled.txt'
        EmailSpider.boot()
        # EmailSpider.crawlPage('First spider', EmailSpider.base_url)
        print("First spider now crawling ", EmailSpider.base_url)
        EmailSpider.addLinksToQueue(EmailSpider.getLinks(EmailSpider.base_url))
        EmailSpider.updateFiles()

    # Boot the Spider
    @staticmethod
    def boot():
        create_directory(EmailSpider.project_name)
        create_files(EmailSpider.project_name, EmailSpider.base_url)
        EmailSpider.queue = file_to_set(EmailSpider.queue_file)
        EmailSpider.crawled = file_to_set(EmailSpider.crawled_file)


    # Let's Crawl the page
    @staticmethod
    def crawlPage(thread_name, page_url):
        print(EmailSpider.domain_name)
        if page_url in EmailSpider.queue:
            # Update user display.
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(EmailSpider.queue)) + ' | Crawled emails ' + str(len(EmailSpider.crawled)))
            EmailSpider.queue.remove(page_url)
            emails = get_email_from_html(EmailSpider.getHTML(page_url), EmailSpider.domain_name)
            EmailSpider.addEmailsToCrawl(emails)
            EmailSpider.updateFiles()

    # Get the links.
    @staticmethod
    def getLinks(page_url):
        HTML = EmailSpider.getHTML(page_url)
        finder = LinkFinder(EmailSpider.base_url)
        if HTML != "":
            finder.feed(HTML)
            return finder.getURLs()
        else:
            return set()

    # Get the HTML from valid page.
    @staticmethod
    def getHTML(page_url):
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                return html_bytes.decode("utf-8")
        except Exception as e:
            print(str(e))
            return ""
        return ""

    # Saves queue data
    @staticmethod
    def addLinksToQueue(links):
        for url in links:
            if url in EmailSpider.queue:
                continue
            if EmailSpider.domain_name != get_domain_name(url):
                continue

            EmailSpider.queue.add(url)

    # Saves crawl data
    @staticmethod
    def addEmailsToCrawl(emails):
        for email in emails:
            if email not in EmailSpider.crawled:
                EmailSpider.crawled.add(email)

    # Update content in files
    @staticmethod
    def updateFiles():
        set_to_file(EmailSpider.queue, EmailSpider.queue_file)
        set_to_file(EmailSpider.crawled, EmailSpider.crawled_file)
