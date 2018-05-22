# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

from gov.items import GovItem
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')


class AngovSpider(Spider):
    name = 'bj'
    page =500
    count =0
    def __init__(self,**kwargs):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_page_load_timeout(30)
        self.browser2=webdriver.Chrome(chrome_options=chrome_options)
        self.first_url = 'http://rexian.beijing.gov.cn/default/com.web.index.moreLetterReplyQuery.flow?type=firstPage'
        self.beijing_url = 'http://rexian.beijing.gov.cn/default/com.web.index.moreLetterReplyQuery.flow?PageCond/currentPage={PCon}&type={type}'
    def start_requests(self):
        yield Request(self.first_url,self.bj_parse)
    def closed(self, spider):
        print("spider closed")
        self.browser.close()
    def bj_parse(self, response):
        item = GovItem()
        browser = response.browser
        letters =browser.find_elements_by_css_selector('#newLetterReply li')
        for letter in letters:
           try:
               item['title'] = letter.find_element_by_css_selector('p.font14.mymail_title a span').text
               detail_url = letter.find_element_by_css_selector('p.font14.mymail_title a').get_attribute('href')
               item['detail_url'] = detail_url
               item['department'] = letter.find_element_by_css_selector('.font12.gray .mail_margin[name]').text
               self.browser2.get(detail_url)
               self.parse_detail(self.browser2,item)
               yield item
           except (NoSuchElementException,StaleElementReferenceException):
               pass
        self.count += 1
        yield Request(self.beijing_url.format(PCon =self.count,type='nextPage'),self.bj_parse)
    def parse_detail(self,br,item):
        try:
            item['raise_date'] = br.find_element_by_css_selector('#Dbanner div div:nth-child(2) div div:nth-child(3) p span:nth-child(3)').text
            item['res_date'] =br.find_element_by_css_selector('#Dbanner div div:nth-child(2) div div:nth-child(4) span:nth-child(3)').text#可能是none
            item['suggestion'] = br.find_element_by_css_selector('.font14.mail_problem').text
            item['reply'] = br.find_element_by_css_selector('p.offic_p.font14.leaidx').text
        except NoSuchElementException:
            pass
