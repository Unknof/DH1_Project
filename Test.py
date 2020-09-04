
def insertData(Bookname, Author, ReleaseDate):
    import sqlite3
    db = sqlite3.connect("Monster.db")
    c = db.cursor()
    data = (Bookname, Author, ReleaseDate)
    c.execute('''DROP TABLE IF EXISTS Author''')
    c.execute('''INSERT INTO Author(Bookname, Author, ReleaseDate) 
    VALUES(?,?,?)''', data)
    db.commit()
    db.close()


def get_attribute_or_none(csvRow, key) :
    result = None
    if key in csvRow :
        value = csvRow[key]
            
        if value != "" :
            result = value
    return result


def fillDB():
    import csv
 
    with open('books_authors_releasdate.csv') as authorlist:
        authorlist = csv.reader(authorlist, delimiter= ';')
    for csvRow in authorlist:
        Bookname = get_attribute_or_none(csvRow, "Bookname")
        Author = get_attribute_or_none(csvRow, "Author")
        ReleaseDate = get_attribute_or_none(csvRow, "ReleaseDate")
        insertData(Bookname, Author, ReleaseDate)

