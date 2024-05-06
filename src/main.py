"""main.py: Base."""
__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Production"

from .__config import get_config
import os
import threading
from queue import Queue
from .helper import *
from .email_spider import EmailSpider
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Disable processing if we are running in a GitHub Action
url = "" if os.getenv("GITHUB_ACTIONS") else input("Enter the url to crawl: ")
domain = get_domain_name(url)
project_name = domain
queue_file = project_name + '/queue.txt'
crawled_file = project_name + '/crawled.txt'

# get config
No_of_thread = get_config('threads')
if None is No_of_thread:
    No_of_thread = 4

queue = Queue()
if url:
    EmailSpider(project_name, url, domain)


# Create worker.
def workers():
    for _ in range(No_of_thread):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do the next job in queues.s
def work():
    while True:
        url = queue.get()
        EmailSpider.crawlPage(threading.current_thread().name, url)
        queue.task_done()


# Lets do the job.
def jobs():
    for link in file_to_set(queue_file):
        queue.put(link)

    queue.join()
    crawl()


# If anything left in queue, so crawl then.
def crawl():
    queued_links = file_to_set(queue_file)
    if len(queued_links) > 0:
        # Update the user display
        print(str(len(queued_links)) + ' links in the queue')
        jobs()


def main():
    if url:
        workers()
        crawl()
