#dieses Programm zählt, wie oft ein Buchstabe in einem Namen vorkommt
import csv
from collections import Counter
import re
from operator import itemgetter

filename = 'Monsterliste.csv'

with open(filename) as csvfile: #Datei öffnen
    reader = csv.DictReader(csvfile)
    names = []

    for row in reader:
        names.append(row["Name"])
        name = row['Name']
        crString = row['CR']
        cleanerName = name.lower() #Großbuchstaben in Kleinbuchstaben umwandeln, damit nicht doppelt gezählt wird

        def CRUmwandler(crString): #CR-Werte werden von Strings in Zahlen umgewandelt
            
            if re.search(r"/", crString): #Brüche
                CRBruch = crString.split("/")
                CRZahl = float(CRBruch[0]) / float(CRBruch[1])
                return CRZahl

            elif re.search(r"—", crString): #keine Angabe => 0 Wert --> sollen noch raussortiert werden für meine Auswertung
                CRZahl = float(0)
                return CRZahl
            elif re.search(r"Unknown", crString): #keine Angabe => 0 Wert --> sollen noch raussortiert werden für meine Auswertung
                CRZahl = float(0)
                return CRZahl

            else: #alle "normalen" Zahlen
                CRZahl = float(crString)
                return CRZahl
            #sorted(names, key=itemgetter(CRZahl))#sorted(names, key=CRZahl) --> sortieren funktioniert noch nicht
        if re.search(r"\s", name): #alle Namen mit Leerzeichen werden aussortiert
            names.remove(name)
       
        #elif re.search(r"—", crString): #alle leeren CR-Werte werden aussortiert --> funktioniert noch nicht
            #names.remove(crString)

        else:
            
            #print(row['Name'], CRUmwandler(crString))            #row['CR']) #für die restlichen Namen beginnt die Auswertung
            c = Counter(cleanerName)
            #print (c.most_common(5))


        def namensStatistikTable():
            import sqlite3
            db = sqlite3.connect("Monster.db")
            c = db.cursor()
            c.execute("DROP TABLE IF EXISTS namensStatistikTable")
            c.execute("""CREATE TABLE namensStatistikTable
            (Name TEXT, CR FLOAT)""")

        def insertData(Name, CR):
            import sqlite3
            namensStatistikTable()
            db = sqlite3.connect("Monster.db")
            c = db.cursor()
            data = (name, CRUmwandler(crString))
            c.execute("""
            INSERT INTO namensStatistikTable (Name, CR) 
            VALUES (?,?)""", data)

            db.commit()
            db.close()
    
        import sqlite3
        db = sqlite3.connect("Monster.db")
        c = db.cursor()
        c.execute("SELECT * FROM namensStatistikTable")
        result =c.fetchall()
        print(result)

