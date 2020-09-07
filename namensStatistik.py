#dieses Programm zählt, wie oft ein Buchstabe in einem Namen vorkommt
import csv
from collections import Counter
import re

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
                return int(CRBruch[0]) / int(CRBruch[1])
                
            elif re.search(r"—", crString): #keine Angabe => 0 Wert --> sollen noch raussortiert werden für meine Auswertung
                CRNullwert = int(0)
                return CRNullwert

            else: #alle "normalen" Zahlen
                CRZahl = int(crString)
                return CRZahl

        if re.search(r"\s", name): #alle Namen mit Leerzeichen werden aussortiert
            names.remove(name)
       
        #elif re.search(r"—", crString): #alle leeren CR-Werte werden aussortiert --> funktioniert noch nicht
            #names.remove(crString)

        else:
            print(row['Name'], CRUmwandler(crString))            #row['CR']) #für die restlichen Namen beginnt die Auswertung
            c = Counter(cleanerName)
            print (c.most_common(5))


