def addBookstoTable():
    import sqlite3
    from sqlBase import authorTable
    authorTable()
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    c.execute("SELECT DISTINCT Source FROM Monster")
    result = c.fetchall()
    for x in result:
        #print(x[0])
        c.execute("""
        INSERT INTO Author (Bookname)
        VALUES (?)""", (x[0],)) #Immer schon Tupel für das Statement nehmen
    db.commit() #Das vergessen nervt
    db.close() #Das ist hübsch


import sqlite3
addBookstoTable()
db = sqlite3.connect("Monster.db")
c = db.cursor()
c.execute("SELECT Bookname FROM Author")
result =c.fetchall()
print(result)

#TODO: Zu den 14 Buchtitel die Autoren (und wenn du Bock hast) auch das Erscheinungsdatum scrapen
#Wichtig: Damit das funktioniert, musst du 1mal vorher 5eTools.py ausgeführt haben, sonst bekommst du nich die Liste mit den Büchernamen
