
from scrapy import selector
from scrapy.crawler import CrawlerProcess


# erst nur das grundgerüst

class homebrew(scrapy.Spider):       #Spider
    name = "homebrew"
    
    
    def start_requests(self):       #Standard Funktion
        url = "https://www.dandwiki.com/wiki/5e_Monsters"     
        yield scrapy.Request(url=url, callback=self.analysis)
    
    def get_all(self, response):        # hier wird der crawling prozess enstehen,  hatte leider nicht so viel zeit
        # die tags in der liste haben abwechselns den namen "even" und "odd", muss mal kucken wie wir das regeln
        
        return