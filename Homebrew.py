import csv
import scrapy
from scrapy.crawler import CrawlerProcess


class homebrew(scrapy.Spider):       #Spider
    name = "homebrew"
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
    }
    user_agent = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0"}
    SPIDER_MIDDLEWARES = {
'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True,
}
    handle_httpstatus_list = [403, 404]
    
    

    def start_requests(self):       #Standard Funktion
        
        url = "https://www.dndbeyond.com/homebrew/monsters" 
        headers =  {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Host': 'www.dndbeyond.com',
            'Referer': 'https://www.dndbeyond.com/homebrew/monsters',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        yield scrapy.http.Request(url, callback=self.get_urls, headers=headers)
 
    def get_urls(self, response):         # holt sich alle links und übergibt an nächste funktion
        #response.request.headers.get('Referer', 'https://www.dndbeyond.com/homebrew/monsters')
        urls = response.xpath('//div[@class="list-row-primary-text list-row-name-primary-text"]/a[@class="link"]/@href').getall()
        for link in urls:
            print(link)
            
            yield response.follow(url="https://www.dndbeyond.com" + link, callback=self.get_all)
        
        next_page = response.xpath('//a[text()="Next"]/@href').extract_first()      # holt sich den link für die nächte seite und übergibt wieder an sich selbst
        if next_page is not None:
           yield response.follow(url=next_page, callback=self.get_urls)
        
        
        
          
        
    def get_all(self, response):       
        
        name = response.xpath('//div[@class="mon-stat-block__name"]/a/text()').extract()
        cr = response.xpath('//span[@class="mon-stat-block__tidbit-label"]/text()').extract()
        description = response.xpath('//div[@class="mon-details__description-block-content"]/following::p/text()').extract()
        autor = response.xpath('//div[@class="source source-description"]/text()').extract()
        url = response.xpath('//div[@class="mon-stat-block__name"]/a/@href').get()
       
        

        file_name = "Homebrewliste.csv"    #header kann nicht geschrieben werden, sonst wäre der zwischen jeder zeile drin
        with open(r'.\\' + file_name, mode='a') as homebrewlist:
    
           # writer = csv.DictWriter(homebrewlist, fieldnames = ["Name", "CR", "Source","URL", "Beschreibung"])
            #writer.writeheader()
            homebrewlist = csv.writer(homebrewlist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            
            homebrewlist.writerow([name, cr, autor, url, description])
              
                             
process = CrawlerProcess()
process.crawl(homebrew)
process.start()
