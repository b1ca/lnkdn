# coding=utf-8
from __future__ import unicode_literals
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from db import DBHelper

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/32.0"
)


class Linkedin(object):
    def __init__(self, session_key, session_password):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = USER_AGENT
        self.phantom = webdriver.PhantomJS(
            desired_capabilities=dcap, service_args=['--load-images=yes', '--ssl-protocol=tlsv1'])
        self.phantom.implicitly_wait(20)
        self.homepage_url = 'https://www.linkedin.com/'
        self.search_query = None

        self.db = DBHelper()

        self._login(session_key, session_password)

    def __del__(self):
        self.phantom.quit()
        self.db.close()

    def get_current_url(self):
        return self.phantom.current_url

    def get_current_page(self):
        return self.get_current_url().split('page_num=')[-1]

    def _login(self, session_key, session_password):
        self.phantom.get(self.homepage_url)
        self.phantom.find_element_by_css_selector('#session_key-login').send_keys(session_key)
        self.phantom.find_element_by_css_selector('#session_password-login').send_keys(session_password)
        self.phantom.find_element_by_css_selector('#signin').click()
        self.phantom.find_element_by_css_selector('#signin').click()

        assert len(self.phantom.find_elements_by_xpath('//*[contains(.,"Paul Robben")]')) >= 1

    def set_search_query(self, search_query):
        self.search_query = search_query

    def navigate_search_page(self):
        search_url = ''.join(
            [
                self.homepage_url, self.search_query, '&page_num=1'
            ]
        )
        self.phantom.get(search_url)

    def get_entity_ids_from_current_page(self):
        return [el.get_attribute('data-li-entity-id')
                for el in self.phantom.find_elements_by_css_selector('.mod.result')]

    def navigate_next_page(self):
        self.phantom.find_element_by_css_selector('.next a').click()