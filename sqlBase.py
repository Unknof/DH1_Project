def createDB():
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS Monster")
    c.execute("""
    CREATE TABLE Monster
    (ID INTEGER PRIMARY KEY autoincrement,
    Name TEXT,
    CR TEXT,
    Source TEXT,
    URL TEXT,
    Beschreibung TEXT)
    """)

def tokenTable():
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS Monstertoken")
    c.execute("""
    CREATE TABLE Monstertoken
    (Token TEXT,
    Class TEXT,
    Start INTEGER,
    End INTEGER,
    ID INTEGER)
    """)

def authorTable():
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    c.execute("DROP TABLE IF EXISTS Author")
    c.execute("""
    CREATE TABLE Author
    (Bookname TEXT PRIMARY KEY,
    Author TEXT,
    ReleaseDate TEXT)
    """)

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

#addPrimaryKey()
#authorTable()
#createDB()
tokenTable()