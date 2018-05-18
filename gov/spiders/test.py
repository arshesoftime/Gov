from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)
def parse_detail(page):
    browser.get('http://www.cq.gov.cn/publicmail/citizen/ViewReleaseMail.aspx?intReleaseID=1016557')
    reply = browser.find_element_by_css_selector('span#lblResult').text
    raise_date = browser.find_element_by_css_selector('span#lblSendDate').text
    suggestion = browser.find_element_by_css_selector('span#lblContent1').text
    print(raise_date, reply,suggestion)
