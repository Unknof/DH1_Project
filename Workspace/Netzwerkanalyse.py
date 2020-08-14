#%%
import networkx as nx
import matplotlib.pyplot as plt
import re
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from itertools import combinations
import pandas as pd
import requests


page = requests.get('https://textgridlab.org/1.0/aggregator/html/textgrid:k93c.0')
response = Selector(text = page.content)
sample = response.xpath('//div[@class = "h4"]')
sample2 = response.xpath('//div[@class = "h4"]').getall()
cleantext = BeautifulSoup(str(sample2), "lxml").text
speakers = sample.xpath('.//div[@class = "speaker"]/text()').getall()
print(cleantext)
splittext = re.sub(pattern='\W+',
                       string=cleantext.lower(),
                       repl=" ").split(" ")


all_speakers = []
for x in speakers:
   y = x.replace(".", "").replace(",", "").lower()
   all_speakers.append(y)

charList = []
k = 0
for x in all_speakers:
    if (len(all_speakers[k]) <= 11):
        charList.append(x)
        k += 1
    else:
        k += 1  

print(list(set(charList)))

paare=[]     
score=[]    
umkreis= 20
for paar in combinations(list(set(charList)),2):
    zw_summe = 0        
    for i in range(len(splittext)):    
        if splittext[i]==paar[0]:         
            for k in [x for x in splittext[i-umkreis:i+umkreis]]:
                if k == paar[1]:    
                    zw_summe+=1     
    paare.append(paar)       
    score.append(zw_summe)  
df = pd.DataFrame({"paare":paare,"score":score})  
print(df.sort_values(by="score",ascending=False)) 


G = nx.Graph()  
edges = list(df.loc[(df.score>0)].paare) 
weights = list(df.loc[(df.score>0)].score)  
G.add_edges_from(edges)     
nx.draw(G,                    
width=[(weight/2)**0.5 for weight in weights],
with_labels=True,edge_color="grey",
node_size= 150,   
node_color="red",
node_shape="o",
font_size=18,
font_color="black",
alpha=1)
plt.show()

# %%
