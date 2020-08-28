# Imports
import re
import sqlite3

#Tokenizierung wie im Seminar (Code is auch einfach aus der Übung kopiert)

token_classes = {
    'emoasc': r'[:;=][-^]?[DP()c|\[\]{}]|XD+',
    'punct': r'[,.:;()]',
    'word': r'\w+'
}

class Token():
    '''Ein Objekt, das ein Token repräsentiert.
    Jedes Token hat einen `text` und eine `token_class`, welche die Klasse (also Art) des Tokens angibt. Außerdem werden
    seine Start- und Endposition im ursprünglichen Text gespeichert'''

    def __init__(self, text, token_class, start, end):
        self.text = text
        self.token_class = token_class
        self.start = start
        self.end = end

    def __str__(self):
        return self.text

    def __repr__(self):
        return f"'{self.text}'"


def debug(text):
    '''Diese Funktion tokenisiert den gegebenen Text mit `tokenize()` und gibt zu jedem Token alle Informationen aus'''
    tokens = tokenize(text)
    for t in tokens:
        print(f'"{t.text}":\tclass="{t.token_class}", start="{t.start}", end="{t.end}"')


def tokenize(text):
    tokens = []
    sep = ""
    stringtext = sep.join(text)
    emoasc = r'[:;=][-^]?[DP()c|\[\]{}]|XD+'
    punct = r'[,.:;()]'
    word = r'\w+'

    iterd = re.finditer(emoasc,stringtext)
    for match in iterd:
        tokens.append(Token(match.group(),"emoasc",match.start(),match.end()))
    stringtext = re.sub(emoasc,"",stringtext)

    iterd = re.finditer(punct,stringtext)
    for match in iterd:
        tokens.append(Token(match.group(),"punct",match.start(),match.end()))
    stringtext = re.sub(punct, "", stringtext)

    iterd = re.finditer(word, stringtext)
    for match in iterd:
        tokens.append(Token(match.group(), "word", match.start(), match.end()))

    return tokens


def tokenizeMonsterDesc():
    db = sqlite3.connect("Monster.db")
    c = db.cursor()

    c.execute("SELECT Beschreibung, ID FROM Monster WHERE NOT Beschreibung = 'No information available.' AND NOT Beschreibung = ''")
    monstertable = c.fetchall()
    pattern = r'\d+d\d+|initiative|challenge rating|CR\d+|advantage|disadvantage|saving throw| DC |lair action'

    for monster in monstertable:

        description = monster[0]
        ID = monster[1]

        lines = description.split(".")
        for y in lines:
            if not re.search(pattern,y, re.IGNORECASE):
                #debug(y.strip())
                tokens = tokenize(y.strip())
                for t in tokens:
                    #print(f'"{t.text}":\tclass="{t.token_class}", start="{t.start}", end="{t.end}"')
                    insertData = (t.text, t.token_class, t.start, t.end, ID)
                    c.execute("""
                    INSERT INTO Monstertoken (Token, Class, Start, End, ID) 
                    VALUES (?,?,?,?,?)""", insertData)

    db.commit()