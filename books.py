import scrapy
from scrapy.crawler import CrawlerProcess

class BooksSpider(scrapy.Spider):
    name="books"

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_Dungeons_%26_Dragons_rulebooks#Dungeons_&_Dragons_5th_edition'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.xpath('//*[@id="Dungeons_.26_Dragons_5th_edition"]/following-sibling:://i/@href').getall()#').extract()
        #//*[@id="mw-content-text"]/div[1]/table[24]/tbody/tr[2]/td[1]/i/a
        filepath = 'Books_Authors.csv'
       # with open(filepath, 'w') as f:
        #    f.writelines([link+'/n' for link in links])
         #   #books_writer=csv.writer(Books_Authors, delimiter=',', quotechar='"')
        print(links)

process = CrawlerProcess()
process.crawl(BooksSpider)
process.start()

