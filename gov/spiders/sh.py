# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

from gov.items import GovItem

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

class shSpider(Spider):
    name = 'sh'
    page = 500
    count = 1
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_page_load_timeout(30)
        self.browser2=webdriver.Chrome(chrome_options=chrome_options)
        self.start_url ='http://wsxf.sh.gov.cn/xf_swldxx/feedback_list.aspx?PageName=hfxd&CurrentPage={page}'

    def closed(self, spider):
        print("spider closed")
        self.browser.close()

    def start_requests(self):
        yield Request(self.start_url.format(page=self.count), self.sh_parse)
    def sh_parse(self,response):
        item = GovItem()
        browser=response.browser
        infos=browser.find_elements_by_css_selector('#FBList tr')
        for info in infos:
            try:
                if info.find_element_by_css_selector('a'):#如果元素中含有a标签
                    item['title'] = info.find_element_by_css_selector('td a').text
                    detail_url =info.find_element_by_css_selector('td a').get_attribute('href')
                    item['detail_url'] =detail_url
                    item['department'] =info.find_element_by_css_selector('span').text
                    item['res_date'] = info.find_element_by_css_selector('td:nth-of-type(6)').text
                    self.browser2.get(detail_url)
                    self.parse_detail(self.browser2,item)
                    yield item
            except NoSuchElementException as e:
                pass
        self.count+=1
        yield Request(self.start_url.format(page=self.count), self.sh_parse)
    def parse_detail(self,br,item):
        item['raise_date'] = br.find_element_by_css_selector('#mailboxForm #MainContent_LaDate').text
        item['suggestion'] = br.find_element_by_css_selector('#mailboxForm #MainContent_LaContent').text
        item['reply'] = br.find_element_by_css_selector('#mailboxForm #MainContent_LaDisposition').text




