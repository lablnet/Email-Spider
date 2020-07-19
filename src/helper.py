"""helper.py: Helpers functions for EmailSpider."""
__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Production"

from urllib.parse import urlparse
import os


# Create directory
def create_directory(name):
    if not os.path.exists(name):
        print("Creating the required directory " + name)
        os.makedirs(name)


# Create the file
def create_files(name, url):
    queue = name + '/queue.txt'
    crawled = name + '/crawled.txt'
    if not os.path.isfile(queue):
        write_file(queue, url)
    if not os.path.isfile(crawled):
        write_file(crawled, '')


# Write on file
def write_file(file, data):
    with open(file, 'w') as f:
        f.write(data)


# Append to file.
def append_to_file(file, data):
    with open(file, 'a') as f:
        f.write(data + '\n')


# Delete contents form file.
def delete_from_file(file):
    with open(file, 'w'):
        pass


# Read file and convert to set
def file_to_set(file):
    s = set()
    with open(file, 'r') as f:
        for line in f:
            s.add(line.replace('\n', ''))
    return s


# Convert set to file
def set_to_file(s, file):
    delete_from_file(file)
    for item in sorted(s):
        append_to_file(file, item)


# Get main domain name (example.com)
def get_domain_name(url):
    """
    >>> get_domain_name("https://a.b.c.d/e/f?g=h,i=j#k")
    'c.d'
    >>> get_domain_name("Not a URL!")
    ''
    """
    try:
        u = get_sub_domain_name(url).split('.')
        return u[-2] + '.' + u[-1]
    except:
        return ""


# Get sub domain name (sub.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
