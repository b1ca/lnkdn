# coding=utf-8
from __future__ import unicode_literals
import requests
from lxml import html


class Company(object):
    def __init__(self, entity_id, name, site, num_of_employees):
        self.entity_id = entity_id
        self.name = name
        self.site = site
        self.num_of_employees = num_of_employees


def get_company(entity_id):
    url = ''.join(['https://www.linkedin.com/company/', entity_id])
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8",
    }
    source = requests.get(url, headers=headers)
    tree = html.document_fromstring(source.content)
    name = tree.cssselect('span[itemprop="name"]')[0].text_content().strip().replace('\'', '')
    num_of_employees = ''
    try:
        num_of_employees = tree.cssselect('.company-size p')[0].text_content().strip()
    except IndexError:
        pass
    site = ''
    try:
        site = tree.cssselect('.website a')[0].text_content()
    except IndexError:
        pass
    return Company(entity_id, name, site, num_of_employees)