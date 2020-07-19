"""email_finder.py: Extract email from the raw html."""
__author__ = "Muhammad Umer Farooq"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Muhammad Umer Farooq"
__email__ = "contact@muhammadumerfarooq.me"
__status__ = "Production"

import re


# Extract email from the raw html
def get_email_from_html(html, domain):
    emails = []
    email_regx = '[a-zA-Z0-9]+@' + domain
    email = re.findall(email_regx, html)
    for e in email:
        emails.append(e)
    return emails
