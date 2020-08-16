
def createDB():
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS Monster")
    c.execute("""
    CREATE TABLE Monster
    (Name TEXT,
    CR TEXT,
    Source TEXT,
    URL TEXT,
    Beschreibung TEXT)
    """)


def get_attribute_or_none(csvRow, key): #Könnte man hier wiederverwenden um sicherzustellen das "echte leere" Elemente in die DB gespielt werden
    result = None
    if key in csvRow:
        value = csvRow[key]
        value = value.strip("\"")  # Entferne alle Anfuehrungszeichen am Anfang und Ende.
        value = value.strip()  # Entferne alle Arten von Whitespace (Leerzeichen, Tabs, etc.) am Anfang und Ende.

        if value != "":
            result = value
    return result

def insertData(Name, CR, Source, URL, Beschreibung):
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()

    data = (Name,CR,Source,URL,Beschreibung)
    c.execute("""
    INSERT INTO Monster (Name, CR, Source, URL, Beschreibung) 
    VALUES (?,?,?,?,?)""", data)

    db.commit()
    db.close()

#createDB()