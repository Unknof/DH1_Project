import csv
import scrapy
from scrapy.crawler import CrawlerProcess

class homebrew(scrapy.Spider):       #Spider
    name = "homebrew"
    namelist = []
    descriptionlist = []
    def start_requests(self):       #Standard Funktion
        url = "https://www.dndbeyond.com/homebrew/monsters"     
        yield scrapy.Request(url=url, callback=self.get_urls)
 
    def get_urls(self, response):         # holt sich alle links und übergibt an nächste funktion
        
        urls = response.xpath('//a[@class = "link"]/@href').getall()
        for link in urls:
            print(link)
            yield response.follow(url=link, callback=self.get_all)
        
        next_page = response.xpath('//a[text()="Next"]/@href').get()       # holt sich den link für die nächte seite und übergibt wieder an sich selbst
        if next_page is not None:
           yield response.follow(url=next_page, callback=self.get_urls)
        
        
        
          
        
    def get_all(self, response):       
        
        name = response.xpath('//div[@class = "mon-stat-block__name"]//a/text()').extract()
        cr = response.xpath('//span[@class = "mon-stat-block__tidbit-label"]/text()').extract()
        description = response.xpath('//div[@class = "mon-details__description-block-content"]//following::p/text()').extract()
        autor = response.xpath('//div[@class = "source source-description"]/text()').extract()
        url = response.xpath('//div[@class = "mon-stat-block__name"]//a/@href').get()
       
        

        file_name = "Homebrewliste.csv"    #header kann nicht geschrieben werden, sonst wäre der zwischen jeder zeile drin
        with open(r'.\\' + file_name, mode='a') as homebrewlist:
    
           # writer = csv.DictWriter(homebrewlist, fieldnames = ["Name", "CR", "Source","URL", "Beschreibung"])
            #writer.writeheader()
            homebrewlist = csv.writer(homebrewlist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            homebrewlist.writerow([name, cr, autor, url.get_attribute("href"), description])
              
                             
process = CrawlerProcess()
process.crawl(homebrew)
process.start()
