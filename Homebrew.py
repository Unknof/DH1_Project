import csv
import scrapy
from scrapy.crawler import CrawlerProcess
import random
from sqlBase import homebrewTable

homebrewTable()         #nach dem ersten mal ausführen muss die start url geändert werden, siehe kommentare am ende. ausserdem muss diese zeile gelöscht werden, da sonst alte db überschrieben wird
                        #nicht schön aber einen anderen weg finde ich nicht

class homebrew(scrapy.Spider):
    name = "homebrew" 
    cr = "" 
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
    }
    SPIDER_MIDDLEWARES = {
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True,}
    handle_httpstatus_list = [400, 403, 404]
    ROBOTSTXT_OBEY = False
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        ]
    user_agent = random.choice(user_agent_list)
    
    
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
    
            homebrewlist = csv.writer(homebrewlist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if name != "['']":
                homebrewlist.writerow([name, cr, autor, "https://www.dndbeyond.com" + url, description])
            if str(name) != "['']":
                insertData(str(name), str(cr), str(autor), "https://www.dndbeyond.com" + str(url), str(description))


def insertData(Name, CR, Source, URL, Beschreibung):
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    data = (Name, CR, Source, URL, Beschreibung)
    c.execute("""INSERT INTO Homebrew(Name, CR, Source, URL, Beschreibung) 
    VALUES (?,?,?,?,?)""", data)
    c.execute("""SELECT DISTINCT Name, CR, Source, URL, Beschreibung
    FROM Homebrew""")
    
    db.commit()
    db.close()    


process = CrawlerProcess()
process.crawl(homebrew)
process.start()

#https://www.dndbeyond.com/homebrew/monsters?page=10
#https://www.dndbeyond.com/homebrew/monsters?page=20
#https://www.dndbeyond.com/homebrew/monsters?page=30
#https://www.dndbeyond.com/homebrew/monsters?page=40