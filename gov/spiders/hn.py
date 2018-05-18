# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

from gov.items import GovItem
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


class hnSpider(Spider):
    name = 'hn'
    page =3075
    offset =0
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_page_load_timeout(30)
        self.browser2=webdriver.Chrome(chrome_options=chrome_options)
        self.basic_url = 'http://hdjl.hunan.gov.cn/webapp/szf/wlwz/index.jsp?orgId=&cflag=1&type=&stype=&ext_5=&ext_6=&emailList.offset={offset}&emailList.desc=false'
    def start_requests(self):
        yield Request(self.basic_url.format(offset = 0),self.hn_parse)
    def closed(self, spider):
        print("spider closed")
        self.browser.close()
    def hn_parse(self, response):
        item = GovItem()
        browser = response.browser
        letters =browser.find_elements_by_css_selector('div.myxjgs-content div table tbody tr')
        for letter in letters:
           try:
               item['title'] = letter.find_element_by_css_selector('td:nth-child(1) a').text
               detail_url = letter.find_element_by_css_selector('td:nth-child(1) a').get_attribute('href')
               item['detail_url'] = detail_url
               item['department'] = letter.find_element_by_css_selector('td:nth-child(2) a').text
               item['raise_date'] = letter.find_element_by_css_selector('td:nth-child(3) span').text
               item['res_date'] = letter.find_element_by_css_selector('td:nth-child(4) span').text  # 可能是none
               self.browser2.get(detail_url)
               self.parse_detail(self.browser2,item)
               yield item
           except (NoSuchElementException,StaleElementReferenceException):
               pass
        if self.offset<self.page:
            self.offset +=15
        yield Request(self.basic_url.format(offset =self.offset),self.hn_parse)
    def parse_detail(self,br,item):
        try:
            item['suggestion'] = br.find_element_by_css_selector('div.content table tbody tr:nth-child(4) td:nth-child(2) p').text
            item['reply'] = br.find_element_by_css_selector('div.content table tbody tr:nth-child(3) td:nth-child(2) p').text
        except NoSuchElementException:
            pass
