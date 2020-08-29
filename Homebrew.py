import csv
import scrapy
from scrapy.crawler import CrawlerProcess
import random



class homebrew(scrapy.Spider):
    name = "homebrew"
    SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True,}
    handle_httpstatus_list = [400, 403, 404]
    ROBOTSTXT_OBEY = False
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        ]
    user_agent = random.choice(user_agent_list)
    cr = ""
    
    def set_cr(self, cr):
        self.cr = cr
    
    def get_cr(self):
        return (self.cr)



    def start_requests(self):
        
        user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        ]
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}                #wählt zufällig einen user agent aus um menschliches anfrageverhalten zu simulieren

        url = "https://www.dndbeyond.com/homebrew/monsters" 
        yield scrapy.http.Request(url, callback=self.get_urls, headers=headers)
 
    def get_urls(self, response):         # holt sich alle links und übergibt an nächste funktion
        
        user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        ]
        user_agent = random.choice(user_agent_list)
        headers = {'User-Agent': user_agent}            #auch hier wieder zufälliger user agent, ohne würde der Server die Anfragen blockieren
        
        cr = response.xpath('normalize-space(//div[@class="list-row-primary-text list-row-cr-primary-text"]/text())').extract()
        self.set_cr(cr)         #cr wird auf der ersten Seite gescraped, da nicht auf folgenden vorhanden

        urls = response.xpath('//div[@class="list-row-primary-text list-row-name-primary-text"]/a[@class="link"]/@href').getall()
        for link in urls:
            yield response.follow(url="https://www.dndbeyond.com" + link, callback=self.get_all, headers=headers)
            
        next_page = response.xpath('//a[text()="Next"]/@href').extract_first()      # holt sich den link für die nächte seite und übergibt wieder an sich selbst
        if next_page is not None:
           yield response.follow(url=next_page, callback=self.get_urls, headers=headers)
        
        
        
          
        
    def get_all(self, response):       
        
        cr = self.get_cr()          #cr über getter funktion
        name = response.xpath('normalize-space(//div[@class="mon-stat-block__name"]/a/text())').extract()
        description = response.xpath('normalize-space(//div[@class="mon-details__description-block-content"]/p/text())').extract()
        autor = response.xpath('normalize-space(//div[@class="source source-description"]/text())').extract()
        url = response.xpath('normalize-space(//div[@class="mon-stat-block__name"]/a/@href)').get()
        
        

        file_name = "Homebrewliste.csv"    #header kann nicht geschrieben werden, sonst wäre der zwischen jeder zeile drin
        with open(r'.\\' + file_name, mode='a') as homebrewlist:            # mode='a', damit er nicht überschreibt
    
            #writer = csv.DictWriter(homebrewlist, fieldnames = ["Name", "CR", "Source","URL", "Beschreibung"])
            #writer.writeheader()
            homebrewlist = csv.writer(homebrewlist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            homebrewlist.writerow([name, cr, autor, "https://www.dndbeyond.com" + url, description])
              
                             
process = CrawlerProcess()
process.crawl(homebrew)
process.start()