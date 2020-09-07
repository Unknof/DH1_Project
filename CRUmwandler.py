def CRUmwandler(CR):
    CRBruch = CR.split("/")
    return int(CRBruch[0]) / int(CRBruch[1])


print(CRUmwandler("1/7"))