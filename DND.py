from bs4 import BeautifulSoup
from scrapy.selector import Selector
import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os

gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))
binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
#driver = webdriver.Firefox(firefox_binary=binary, executable_path=gecko+'.exe')
driver = webdriver.Firefox()
driver.get("https://5e.tools/bestiary.html#aarakocra_mm")

userName = driver.find_element_by_xpath("//div[@class = 'flex-v-center']")

#driver.execute_script("arguments[0].click();", userName)
#driver.find_element_by_css_selector('span.stat-tab btn btn-default stat-tab-gen stat-tab-sel[onclick*="Info"]').click()
#page = requests.get('https://5e.tools/bestiary.html#aarakocra%20simulacra_skt')
#sleep(5)
#response = Selector(text = page.content)

#sample = response.xpath('normalize-space(//div[@class="wrp-stats-table ecgen__hidden"])').extract()
#sample2 = response.xpath('//span[@class="rd__h rd__h--3"]').extract()
#cleantext = BeautifulSoup(str(sample), "lxml").text
#print(sample2)
print(userName)