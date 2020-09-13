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
            if not re.search(pattern,y, re.IGNORECASE) and not y == "":
                #debug(y.strip())
                tokens = tokenize(y.strip())
                for t in tokens:
                    #print(f'"{t.text}":\tclass="{t.token_class}", start="{t.start}", end="{t.end}"')
                    insertData = (t.text, t.token_class, t.start, t.end, ID)
                    c.execute("""
                    INSERT INTO Monstertoken (Token, Class, Start, End, ID) 
                    VALUES (?,?,?,?,?)""", insertData)

    db.commit()

def tokenize_with_nltk():
    import nltk
    import sqlite3

    #nltk.download() #Vor dem ersten Verwenden unbedingt downloaden
    #nltk.download('averaged_perceptron_tagger')
    #nltk.download('maxent_ne_chunker')

    db = sqlite3.connect("Monster.db")
    c = db.cursor()

    c.execute("SELECT Beschreibung, ID FROM Monster WHERE NOT Beschreibung = 'No information available.' AND NOT Beschreibung = ''")
    monstertable = c.fetchmany(3)
    pattern = r'\d+d\d+|initiative|challenge rating|CR\d+|advantage|disadvantage|saving throw| DC |lair action'

    for monster in monstertable:
        description = monster[0]
        ID = monster[1]
        #print(description)

        lines = description.split(".")
        for y in lines:
            if not re.search(pattern, y, re.IGNORECASE) and not y == "":
                tokens = nltk.word_tokenize(y)
                #print(y.strip())
                #print(tokens)
                tagged = nltk.pos_tag(tokens)
                print(tagged)
                #entities = nltk.chunk.ne_chunk(tagged)
                #print(entities)



def tokenize_with_stanza(homebrew):
    import stanza
    import sqlite3
    import os
    from stanza.utils.conll import CoNLL
    #stanza.download("en") #Beim ersten Ausführen unbedingt einmal Laufen lassen (benötigt Internetverbindung)
    nlp = stanza.Pipeline("en")

    db = sqlite3.connect("Monster.db") #Verbindet die DB
    c = db.cursor()

    folder = "./tagged_stanza" #Erstellt einen Ordner um die TSVs zu speichern
    if not os.path.exists(folder):
        os.makedirs(folder)

    if homebrew == True: #Nur für den filenamen wichtig
        fname_part = "/homebrew_"
        c.execute("SELECT DISTINCT Beschreibung FROM Homebrew")

    else:
        fname_part = "/5eTools_"
        c.execute(
            "SELECT Beschreibung, ID FROM Monster WHERE NOT Beschreibung = 'No information available.' AND NOT Beschreibung = ''")  # Wählt nur relevante Einträge aus der Tabelle

    monstertable = c.fetchall()
    pattern = r'\d+d\d+|initiative|challenge rating|CR\d+|advantage|disadvantage|saving throw| DC |lair action|Enter a description for your Monster here' #Schmeißt Zeilen raus die offensichtlich keine Beschreibung enthalten

    ID = 0
    for monster in monstertable: #Looped über die Ergebnisse des fetchall
        if homebrew:
            if len(monster[0]) > 4:
                #print(len(monster[0]))
                description = monster[0][2:-2]
            else:
                continue
        else:
            description = monster[0]
            ID = monster[1]
        forstanza = ""

        lines = description.split(".")
        for y in lines:
            if not re.search(pattern, y, re.IGNORECASE) and not y == "":
                temp = y.replace(u'\\xa0', ' ').encode('utf-8').decode('utf-8', errors='replace')
                #temp = "".join(y.split())
                forstanza = forstanza + temp

        file = folder + fname_part + str(ID) + ".tsv"
        with open(file,"w",encoding="UTF-8") as f:
            if len(forstanza) > 0 and not forstanza == " ":
                print(forstanza)
                doc = nlp(forstanza)
                conll = CoNLL.convert_dict(doc.to_dict())
                for sentence in conll:
                    for token in sentence:
                        print("\t".join(token), file=f)
        ID = ID +1

tokenize_with_stanza(True)