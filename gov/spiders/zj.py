# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from gov.items import GovItem
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

class zjSpider(Spider):
    name = 'zj'
    page = 500
    count = 1
    def __init__(self,**kwargs):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_page_load_timeout(30)
        self.browser2=webdriver.Chrome(chrome_options=chrome_options)
        self.start_url ='http://www.zjzxts.gov.cn/pageSplit.do?page={page}&buzinessType=null'

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        yield Request(self.start_url.format(page=self.count), self.zj_parse)
    def zj_parse(self,response):
        item = GovItem()
        browser = response.browser
        infos=browser.find_elements_by_css_selector('tr[valign=top]')
        for info in infos:
            try:
                if info.find_element_by_css_selector('a'):#如果元素中含有a
                    item['title'] = info.find_element_by_css_selector('.text').text
                    detail_url =info.find_element_by_css_selector('a').get_attribute('href')
                    item['detail_url']=detail_url
                    self.browser2.get(detail_url)
                    self.parse_detail(self.browser2,item)
                    yield item
            except (StaleElementReferenceException,NoSuchElementException):
                pass
        self.count+=1
        yield Request(self.start_url.format(page=self.count), self.zj_parse)
    def parse_detail(self,br,item):
        item['department'] =br.find_element_by_css_selector('#content tbody tr:nth-child(6) td:nth-child(2)').text
        item['reply'] = br.find_element_by_css_selector('.scollct').text
        item['res_date'] = br.find_element_by_css_selector('#content table tbody tr:nth-child(7) td:nth-child(2) span').text
        item['raise_date'] = br.find_element_by_css_selector('#content table tbody tr:nth-child(10) td:nth-child(2) span').text
        item['suggestion'] = br.find_element_by_css_selector('#qcontent').text




