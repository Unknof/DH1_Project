
import scrapy
from scrapy.crawler import CrawlerProcess


# erst nur das grundgerüst

class homebrew(scrapy.Spider):       #Spider
    name = "homebrew"
    
    
    def start_requests(self):       #Standard Funktion
        url = "https://www.dandwiki.com/wiki/5e_Monsters"     
        yield scrapy.Request(url=url, callback=self.get_urls)
 
    def get_urls(self, response):        # hier wird der crawling prozess enstehen,  hatte leider nicht so viel zeit
        odd_urls = response.xpath('//tr[@class = "odd"]//a/@href').getall()
        even_urls = response.xpath('//tr[@class = "even"]//a/@href').getall()
        for odd_link in odd_urls:
            for even_link in even_urls:
                yield response.follow(url=even_link, callback=self.get_all)
            
            yield response.follow(url=odd_link, callback=self.get_all)
        
        next_odd_page = response.xpath('//tr[@class = "odd"]//a/@href').get() # statt get() geht auch extract_first()
        next_even_page = response.xpath('//tr[@class = "even"]//a/@href').get()
        if next_odd_page is not None:
            if next_even_page is not None:
                yield response.follow(url=next_even_page, callback=self.get_urls)
            yield response.follow(url=next_odd_page, callback=self.get_urls)
        
        
        
          
        
    def get_all(self, response):
        name = response.xpath('//span[@class = "mw-headline"]')
        print(name)
        description = response.xpath('//table[@class = "5e"]//p//text()')
        
        
        

process = CrawlerProcess()
process.crawl(homebrew)
process.start()
#even_urls = response.xpath('//tr[@class = "even"]//a/@href').getall()
 #       for even_link in even_urls:
#
 #           yield response.follow(url=even_link, callback=self.get_urls) 
#next_even_page = response.xpath('//tr[@class = "even"]//a/@href').get() # statt get() geht auch extract_first()
 #       if next_even_page is not None:
  #          yield response.follow(url=next_even_page, callback=self.get_urls) 