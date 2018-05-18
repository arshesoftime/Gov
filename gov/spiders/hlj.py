# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from gov.items import GovItem
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

class hljSpider(Spider):
    name = 'hlj'
    page =500
    def __init__(self):
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_page_load_timeout(30)
        self.browser2=webdriver.Chrome(chrome_options=chrome_options)
        self.start_url ='http://app.dbw.cn/govzx/zx/zx_more.aspx?t=2'
    def closed(self, spider):
        print("spider closed")
        self.browser.close()
    def start_requests(self):
        yield Request(self.start_url,self.hlj_parse)
    def hlj_parse(self,response):
        count =1
        item = GovItem()
        browser =response.browser
        while count<self.page:
            infos = browser.find_elements_by_css_selector('.td1 tr')
            for info in infos:
                try:
                    if info.find_elements_by_css_selector('td'):
                        item['title'] = info.find_element_by_css_selector('td:nth-of-type(2)').text
                        detail_url =info.find_element_by_css_selector('tr div a').get_attribute('href')
                        item['detail_url'] = detail_url
                        item['department'] =info.find_element_by_css_selector('td:nth-of-type(3)').text
                        item['res_date'] = info.find_element_by_css_selector('td:nth-of-type(4)').text
                        self.browser2.get(detail_url)
                        self.parse_detail(self.browser2,item)
                        yield item
                except StaleElementReferenceException as e:
                    pass

            count +=1
            browser.execute_script("__doPostBack('AspNetPager1','{page}')".format(page=str(count)))
    def parse_detail(self,br,item):
        item['suggestion'] = br.find_element_by_css_selector('.bdbd #Label2').text
        item['raise_date'] = br.find_element_by_css_selector('.bdbd #Label5').text
        item['reply'] = br.find_element_by_css_selector('.bdbd #Label8').text




