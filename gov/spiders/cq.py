# -*- coding: utf-8 -*-
from scrapy import Request,Spider
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options

from gov.items import GovItem
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

class cqSpider(Spider):
    name = 'chongqing'
    page =500
#这里将webdriver定义在spider文件的好处是，不需要每一次请求url都打开和关闭浏览器。
    def __init__(self):
        # self.item = cqItem()
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.set_page_load_timeout(30)
        self.browser2=webdriver.Chrome(chrome_options=chrome_options)
        self.start_url ='http://www.cq.gov.cn/publicmail/citizen/ReleaseMailListDistrict.aspx'
#其中的closed()方法，是在爬虫程序结束之后，自动关闭浏览器。
    def closed(self, spider):
        print("spider closed")
        self.browser.close()
    def start_requests(self):
        yield Request(self.start_url,self.cq_parse)
    def cq_parse(self,response):
        count =1
        item = GovItem()
        browser =response.browser
        while count<self.page:
            infos = browser.find_elements_by_css_selector('#dgrdMail tbody tr[bgcolor]')
            for info in infos:
                 try:
                         item['title'] = info.find_element_by_css_selector('td a').text
                         detail_url =info.find_element_by_css_selector('td a').get_attribute('href')
                         item['detail_url'] = detail_url
                         item['department'] =info.find_element_by_css_selector('td:nth-child(2)').text
                         item['res_date'] =info.find_element_by_css_selector('td:nth-child(3)').text
                         self.browser2.get(detail_url)
                         self.parse_detail(self.browser2,item)
                         yield item
                 except (NoSuchElementException):
                     pass
            browser.find_element_by_css_selector('#btnNext').click()

    def parse_detail(self,br,item):
        item['reply'] = br.find_element_by_css_selector('span#lblResult').text
        item['raise_date'] = br.find_element_by_css_selector('span#lblSendDate').text
        item['suggestion'] = br.find_element_by_css_selector('span#lblContent1').text




