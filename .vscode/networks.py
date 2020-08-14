
#%%
import networkx as nx    #import von Networkx zum Graph erstellen
import matplotlib.pyplot as plt     #import matplotlib zum visualisieren
import scrapy                       
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.selector import HtmlXPathSelector
from itertools import combinations      #import combinations zum charakter paaren


#Um den Umgang mit Networkx zu demonstrieren haben wir diesen [Korpus] (https://dracor.org/ger) benutzt. Natürlich könnte man die Texte auch mit Scrapy und einer geeigneten Spider selbst scrapen, jedoch bietet das Korpus auch Charakterlisten im z.B. CSV-Format an. Um das Tool Networkx vorzustellen greifen wir deshalb auf diese Listen zurück.
#%%
class network(scrapy.Spider):       #Spider
    name = "network"
    
    
    def start_requests(self):       #Standard Funktion
        url = "https://textgridlab.org/1.0/aggregator/html/textgrid:jkjb.0"     #dieses link habe ich aus dracor.org, ich habe es nicht fertiggebracht den Text direkt aus draco zu scrapen -.-
        yield scrapy.Request(url=url, callback=self.analysis)
    
    
    def analysis(self, response):
        chars = ["KRAWUTSCHKE","LUDE", "BULLE", "ANGLER", "MIEZE", "ABRAMSEN",
         "MORPHY", "LEHMANN", "HELENE", "HENRIETTE"] #Erstellung der Charakterliste per Hand, alle mit Caps damit die Charaktere im Drama gematcht werden können
        nodes = 0
        hxs = HtmlXPathSelector(response)       #Selectorobjekt um Text von HTML-Tags zu befreien
        sample = hxs.select("/html//body//div//*//text()").extract()[nodes]   #hier Fehler, bekomme nur einen Teil des Textes! Gehe ich noch tiefer in die Tags bekomme ich einen Index out of Range error!
        print(len(sample))  # Zwischentest len=87
        print(sample)
        for x in sample:
            x = hxs.select("/html//body//div//*//text()").extract()[nodes]
            nodes+=1
            print(x)        #for Schleife zum testen

        #in den nächsten Zeilen muss auch noch ein Fehler drin sein, da meine Scores alle bei 0 bleiben, selbst wenn ich den Umkreis erhöhe

        char=[]     # Liste um Charakterpaarungen zu speichern
        score=[]    # Liste um den Score der Paarungen zu speichern
        umkreis= 10   # Der Umkreis in welchem die Paarungen auftreten sollen
        for paar in combinations(chars,2):  # Charakterliste und Anzahl der Paare (also würde auch 3 gehen)
            zw_summe = 0        #Zwischensumme um die Anzahl der Paarungen festzuhalten
            for i in range(len(sample)):    #for-Schleife um über sample zu itterieren
                if sample[i]==paar[0]:         # wenn ein Paar gematcht wurde...
                    for k in [x for x in sample[i-umkreis:i+umkreis]]:  # sucht im Umkreis vor und nach einem Charakter
                        if k == paar[1]:    # wenn es matcht
                            zw_summe+=1     #wird die Zwischensumme erhöht (wiederholt für alle möglichen Paarungen)
            char.append(paar)       #fügt das gefunden Paar an die char-liste
            score.append(zw_summe)  #fügt den errechneten score an die score liste
        df = pd.DataFrame({"char":char,"score":score})  #erstellt eine Liste der Paarungen und deren scores
        df.sort_values(by="score",ascending=False)[:10] #sortiert die liste nach scores
        print(df) #test

        G = nx.Graph()  #erstellt einen leeren Graphen
        edges = list(df.loc[(df.score>=0)].char) # erstellt eine liste mit allen charakterpaaren und scores um die Kanten zu intialisieren
        weights = list(df.loc[(df.score>=0)].score)  # erstellt eine liste mit allen scores um die Gewichtung festzustellen
        G.add_edges_from(edges)         # fügt die Liste der Kanten an den Graphen
        nx.draw(G,                      # stellt den Graphen dar mit gewünschten Effekten
        width=[(weight/2)**0.5 for weight in weights],
        with_labels=True,edge_color="green",
        node_size=[(weight*15000)**0.5 for weight in weights],
        node_color="lightgrey",
        node_shape="o",
        font_size=10,
        font_color="black",
        alpha=0.9)
        plt.show()
         
process = CrawlerProcess()
process.crawl(network)
process.start()





# %%
