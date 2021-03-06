
import scrapy
from scrapy.crawler import CrawlerProcess
import random
from sqlBase import homebrewTable
import sqlite3

homebrewTable()

def insertData(Name, CR, Source, URL, Beschreibung):    
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    data = (Name, CR, Source, URL, Beschreibung)
    c.execute("""INSERT INTO Homebrew(Name, CR, Source, URL, Beschreibung) 
    VALUES (?,?,?,?,?)""", data)
    c.execute("""SELECT DISTINCT Name, CR, Source, URL, Beschreibung
    FROM Homebrew""")
    
    db.commit()
    db.close()            

class homebrew(scrapy.Spider):
    name = "homebrew" 
    cr = "" 
    custom_settings = {'AUTOTHROTTLE_ENABLED': True}
    SPIDER_MIDDLEWARES = {'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True}
    handle_httpstatus_list = [400, 403, 404]
    ROBOTSTXT_OBEY = False
    user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
    user_agent = random.choice(user_agent_list)
     
    def set_cr(self, cr):
        self.cr = cr
    
    def get_cr(self):
        return (self.cr)

    def start_requests(self):
        
        user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}                

        url = "https://www.dndbeyond.com/homebrew/monsters" 
        yield scrapy.http.Request(url, callback=self.get_urls, headers=headers)
 
    def get_urls(self, response):  
        
        user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}           
        
        cr = response.xpath('normalize-space(//div[@class="list-row-primary-text list-row-cr-primary-text"]/text())').extract()
        self.set_cr(cr)

        urls = response.xpath('//div[@class="list-row-primary-text list-row-name-primary-text"]/a[@class="link"]/@href').getall()
        for link in urls:
            yield response.follow(url="https://www.dndbeyond.com" + link, callback=self.get_all, headers=headers)
            
        next_page = response.xpath('//a[text()="Next"]/@href').extract_first()     
        if next_page is not None:
           yield response.follow(url=next_page, callback=self.get_urls, headers=headers)
              
        
    def get_all(self, response):       
        
        cr = self.get_cr() 
        name = response.xpath('normalize-space(//div[@class="mon-stat-block__name"]/a/text())').extract()
        description = response.xpath('normalize-space(//div[@class="mon-details__description-block-content"]/p/text())').extract()
        autor = response.xpath('normalize-space(//div[@class="source source-description"]/text())').extract()
        url = response.xpath('normalize-space(//div[@class="mon-stat-block__name"]/a/@href)').get()
        
        if str(name) != "['']":
            insertData(str(name), str(cr), str(autor), "https://www.dndbeyond.com" + str(url), str(description))

process = CrawlerProcess()
process.crawl(homebrew)
process.start()