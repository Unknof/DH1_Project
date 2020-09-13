import requests
from bs4 import BeautifulSoup
import csv
import pathlib


class book:
    def __init__(self):
        self.title = None
        self.author = None
        self.date = None
        self.pages = None
        self.isbn = None
        self.levels = None


def createbook(bookAsLine):
    newbook = book()
    for i,spalte in enumerate(bookAsLine):
        if(i == 0):
            newbook.title = spalte.text.strip()
        elif(i == 1):
            newbook.author = spalte.text.strip()
        elif(i==2):
            newbook.date = spalte.text.strip()
        elif(i ==3):
            newbook.pages = spalte.text.strip()
        elif(i ==4):
            newbook.isbn = spalte.text.strip()
        elif(i==5):
            newbook.levels = spalte.text.strip()

    print('Title : %s Author %s date %s pages %s ' %(newbook.title, newbook.author, newbook.date,newbook.pages))
    return newbook
    
def createOneTableOfBooks(books,htmltype):
    booksSeperateEdition = []
    for index,book in enumerate(books):
        if(index > 0): #index 0 => Table Header
            spalten = book.find_all(htmltype) # 'td' or 'th'
            booksSeperateEdition.append(createbook(spalten))
    return booksSeperateEdition

def scrapeWikipediaPage():
    URL = 'https://en.wikipedia.org/wiki/List_of_Dungeons_%26_Dragons_rulebooks'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    bookTables = soup.find_all('tbody') 
    FifthEditionBooks = []
    for y,bookTable in enumerate(bookTables): 
        if(y > 22 and y <= 31): # der Rest ist unrelevant, da Bücher anderer Editionen
            books = bookTable.find_all('tr')
            booksOfthisTable = createOneTableOfBooks(books,'td')
            FifthEditionBooks.append(booksOfthisTable)
    FifthEditionBooks.remove(FifthEditionBooks[5])
    return createOneArray(FifthEditionBooks)

def createOneArray(twoDimensionalArray):
    result = []
    for dim1 in twoDimensionalArray:
        for dim2 in dim1:
            result.append(dim2)
    return result

def make_csv(bookList):
    with open('result.csv', 'w') as csv_file:
        wr = csv.writer(csv_file, delimiter=';',lineterminator='\r')
        wr.writerow(['Titel','Author','Erscheinungsdatumsdatum','isbn','Seiten','Level-Vorgabe'])
        for _book in bookList:
            wr.writerow([_book.title,_book.author,_book.date,_book.isbn,_book.pages,_book.levels])

booksWeNeed = scrapeWikipediaPage() # Array aus Tabellen [] -> [] aus Büchern
make_csv(booksWeNeed)



