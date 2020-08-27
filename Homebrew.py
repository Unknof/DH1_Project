
import scrapy
from scrapy.crawler import CrawlerProcess

class homebrew(scrapy.Spider):       #Spider
    name = "homebrew"
    namelist = []
    descriptionlist = []
    def start_requests(self):       #Standard Funktion
        url = "https://www.dandwiki.com/wiki/5e_Monsters"     
        yield scrapy.Request(url=url, callback=self.get_urls)
 
    def get_urls(self, response):         # holt sich alle links und übergibt an nächste funktion
        urls = response.xpath('//table[@style = "width: 100%; text-align: left;"]//child::*//tr//a/@href').getall()
        
        for link in urls:
            yield response.follow(url=link, callback=self.get_all)
        
       # next_page = response.xpath('//tbody//child::*//a/@href').get()
        
      #  if next_page is not None:
         #   yield response.follow(url=next_page, callback=self.get_urls)
        

    def get_all(self, response):        # der xpath befehl funktioniert soweit. leider bekommt man nicht alle beschreibungen. manche sind noch extra verschachtelt in a tags z.b.
        description = response.xpath('normalize-space(//table[@style = "margin: 1em auto 1em auto;"]//following::p//text())').extract() #scrapt definitiv nicht die gesamte Beschreibung
        name = response.xpath('//h2/child::span/text()').extract()
        #join die listen zu einem String
        tempdesc = ''.join(description)
        tempname = ''.join(name)
        #fügt die Strings an die Liste der Klasse an
        homebrew.descriptionlist.append(tempdesc)
        homebrew.namelist.append(tempname)
        #print(homebrew.namelist)

def make_csv(namelist,descriptionlist):
    import csv
    import os
    file_name = "Homebrewliste.csv"     #das funktioniert nicht wie es soll, hab aber heute keinen kopf mehr dafür! trennt jeden buchstaben mit , und überschreibt jedes mal den alten eintrag
    with open(r'.\\' + file_name, mode='w') as homebrewlist:

        writer = csv.DictWriter(homebrewlist, fieldnames = ["Name", "CR", "Source","URL", "Beschreibung"])
        writer.writeheader()
        homebrewlist = csv.writer(homebrewlist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for x in namelist:

            homebrewlist.writerow(namelist[x])
            homebrewlist.writerow(descriptionlist[x])

        # hier müssen noch name, cr, source, url eingefügt werden    

process = CrawlerProcess()
process.crawl(homebrew)
process.start()
make_csv(homebrew.namelist,homebrew.descriptionlist)