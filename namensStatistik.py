#dieses Programm zählt, wie oft ein Buchstabe in einem Namen vorkommt
import csv
from collections import Counter
import re
from operator import itemgetter


def namensStatistikTable():
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS namensStatistikTable")
    c.execute("""CREATE TABLE namensStatistikTable
    (Name TEXT, CR FLOAT, Auswertung TEXT)""")

def insertData(Name, CR, Auswertung):
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    data = (name, CRUmwandler(crString), berechneAuswertung(cleanerName))

    c.execute("""
    INSERT INTO namensStatistikTable (Name, CR, Auswertung) 
    VALUES (?,?,?)""", data)

    db.commit()
    db.close()

def CRUmwandler(crString): #CR-Werte werden von Strings in Zahlen umgewandelt
            
    if re.search(r"/", crString): #Brüche
        CRBruch = crString.split("/")
        CRZahl = float(CRBruch[0]) / float(CRBruch[1])
        return CRZahl

    elif re.search(r"—", crString): #keine Angabe => 0 Wert --> sollen noch raussortiert werden für meine Auswertung
        CRZahl = float(0)
        return CRZahl
    elif re.search(r"Unknown", crString): #keine Angabe => 0 Wert --> sollen noch raussortiert werden für meine Auswertung --> SQL!!!!!!!
        CRZahl = float(0)
        return CRZahl
#sorted(names, key=itemgetter(CRZahl))#sorted(names, key=CRZahl) --> sortieren funktioniert noch nicht
    else: #alle "normalen" Zahlen
        CRZahl = float(crString)
        return CRZahl
            

def berechneAuswertung(cleanerName):
    if re.search(r"\s", name): #alle Namen mit Leerzeichen werden markiert
        u ="unwichtig"
        return u
           
    else: #für die restlichen Namen beginnt die Auswertung Wahrscheinlich Müll: #print(row['Name'], CRUmwandler(crString))  #print (count.most_common(5))       
        count = Counter(cleanerName)
        statistikBuchstaben = str(count.most_common(5))
        return statistikBuchstaben
        
filename = 'Monsterliste.csv'
namensStatistikTable()
with open(r'.\\' + filename, mode='r') as csvfile: #Datei öffnen
    reader = csv.DictReader(csvfile)
    names = []
    
    for row in reader:
        names.append(row["Name"])
        name = row['Name']
        crString = row['CR']
        cleanerName = name.lower() #Großbuchstaben in Kleinbuchstaben umwandeln, damit nicht doppelt gezählt wird
        
        insertData(cleanerName, CRUmwandler(crString), berechneAuswertung(cleanerName)) #hier wird eingefügt
        

import sqlite3
db = sqlite3.connect("Monster.db")
c = db.cursor()
c.execute("DELETE FROM namensStatistikTable WHERE Auswertung='unwichtig'") #sortiert alle Monster aus, deren Namen aus mehr als einem Wort bestehen
c.execute("SELECT * FROM namensStatistikTable")

result =c.fetchall()
print(result)
