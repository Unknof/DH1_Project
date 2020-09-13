import pandas as pd
import plotly.graph_objects as go
import statistics as stats
import numpy as np
import os
import chardet



#filename = "/5eTools_Gesamt.tsv"
filename = "/homebrew_fixed.tsv"
dir = "./tagged_stanza"
file = dir + filename



colnames = ['id', 'token', 'lemma', 'upos', 'xpos', 'feats', 'head', 'deprel', 'deps', 'misc']
table = pd.read_table(file, names=colnames, quoting=3)
only_words = table[table['upos'] != 'PUNCT']
#only_words = table.query('upos != "PUNCT"')  # alternativ: table[table['upos'] != 'PUNCT']
only_words = only_words.assign(token_upos=only_words['token'].str.lower() + "/" + only_words['upos'])

def wordlength():
    count = 0
    sumlen = 0
    for x in only_words["token"]:
        if not x == ",":
            count = count + 1
            sumlen = sumlen + len(x)
    print(sumlen/count)



def freq():
    type_freq = table[
        'token'].str.lower().value_counts()  # bei englischen Daten lohnt es sich u.U., alle Tokens in Kleinschreibung zu berücksichtigen – bei deutschen wäre ich vorsichtiger
    type_freq = type_freq.to_frame()
    type_freq = type_freq.reset_index()
    type_freq.columns = ['type', 'count']
    type_freq = type_freq.assign(rel=type_freq['count'] / len(table))
    # print(type_freq)
    type_freq = type_freq.iloc[0:50]
    fig = go.Figure(data=go.Bar(x=type_freq['type'], y=type_freq['count']))
    fig.update_layout(
        title="Häufigkeiten der 50 häufigsten Types",
        xaxis_title="Type",
        yaxis_title="Absolute Häufigkeit",
        template="ggplot2"
    )
    fig.show()


def upos():
    upos_freq = table['upos'].value_counts()
    upos_freq = upos_freq.to_frame()
    upos_freq = upos_freq.reset_index()
    upos_freq.columns = ['upos', 'count']
    upos_freq = upos_freq.assign(rel=upos_freq['count'] / len(table))
    fig = go.Figure(data=go.Bar(x=upos_freq['upos'], y=upos_freq['count']))
    fig.update_layout(
        title="Wortartenhäufigkeiten",
        xaxis_title="UPOS-Tag",
        yaxis_title="Absolute Häufigkeit",
        template="ggplot2"
    )
    fig.show()


def makeHugetsv(fname):
    filedir = "./tagged_stanza/" + fname
    with open(filedir, "a") as afile:
        for f in os.listdir("./tagged_stanza"):
            if not str(f) == fname and not str(f) == "5eTools_Gesamt.tsv":
                with open("./tagged_stanza/" + str(f), "r", encoding='UTF-8') as rfile:
                    rcontent = rfile.readlines()
                    # rcontent = [x.strip() for x in rcontent]
                    for line in rcontent:
                        afile.writelines(line.rstrip() + "\t" + str(f) + "\n")
                # print(rcontent)
            # break


def mtld(tokens, factor_size=.72):
    '''MTLD according to McCarthy & Jarvis (2010)'''
    if isinstance(tokens, pd.Series):
        tokens = tokens.tolist()  # sonst funktioniert .reverse() nicht

    def mtldsub(tokens, factor_size, reverse=False):
        # Startwerte (types ist ein Set, kann also keine Duplikate enthalten):
        factors = 0
        types = set()
        token_count = 0
        if reverse:
            tokens.reverse()
        # Tokens durchgehen und der aktuellen Type-Menge hinzufügen:
        for token in tokens:
            types.add(token)
            token_count += 1
            # Falls TTR-Wert die festgelegte Faktorgröße erreicht oder unterschreitet,
            # Faktorzahl erhöhen und neue Type-Liste beginnen:
            if (len(types) / token_count) <= factor_size:
                factors += 1
                types = set()
                token_count = 0
        # Teilfaktor, falls am Ende noch Tokens übrig sind:
        if token_count > 0:
            TTR = len(types) / token_count
            factors += (1 - TTR) / (1 - factor_size)
        # Gesamttokenzahl durch Faktorzahl teilen und zurückgeben:
        return len(tokens) / factors

    # In beiden Richtungen durch den Text gehen, Mittelwert als Endergebnis zurückgeben:
    mtld_forward = mtldsub(tokens, factor_size)
    mtld_reverse = mtldsub(tokens, factor_size, reverse=True)
    return stats.mean([mtld_forward, mtld_reverse])

#wordlength()
#print('MTLD mit TTR-Schwellenwert 0,72, Text 1:', mtld(only_words['token_upos']))
#makeHugetsv("homebrew_Gesamt.tsv")
upos()
