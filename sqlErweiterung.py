def addInfosToTable():
    import sqlite3
    from sqlBase import authorTable
    import csv
    

    # Diese Hilfsfunktion holt sich den Wert aus der CSV-Zeile und gibt ihn zurueck. Wenn der Wert leer ist, gibt die Funktion None zurueck.
    def get_attribute_or_none(csvRow, key) :
        result = None
        if key in csvRow :
            value = csvRow[key]

            #diese beiden Zeilen sind wahrscheinlich unnötig, nur noch nicht gelöscht.
            value = value.strip("\"") # Entferne alle Anfuehrungszeichen am Anfang und Ende.
            value = value.strip() # Entferne alle Arten von Whitespace (Leerzeichen, Tabs, etc.) am Anfang und Ende.
            
            if value != "" :
                result = value
        return result

    
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS authorTable")


    with open('books_authors_releasedate.csv', encoding='utf8') as metadataFile:           # Hier oeffne ich die Datei
        csvReader = csv.DictReader(metadataFile, dialect='excel', delimiter=';')  # ... und uebergebe sie an das CSV-Modul
        
        for csvRow in csvReader : # jede Zeile in der CSV-Datei anschauen
            Bookname = get_attribute_or_none(csvRow, "Bookname")
            Author = get_attribute_or_none(csvRow, "Author")
            ReleaseDate = get_attribute_or_none(csvRow, "ReleaseDate")
                        
            insertData = (Bookname, Author, ReleaseDate)
            authorTable()
            # Daten in die Datenbank einsetzen
            cursor = db.cursor()
            cursor.execute("""
            INSERT INTO Author 
            (Bookname, Author, ReleaseDate) 
            VALUES(?, ?, ?)""", insertData)
            
    db.commit()
    db.close()    

import sqlite3
db = sqlite3.connect("Monster.db")
cursor = db.cursor()
cursor.execute("SELECT * FROM Author")
result =cursor.fetchall()
print(result)    

