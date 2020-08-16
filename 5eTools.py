def getDescription():
    from sqlBase import insertData
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait as wait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    from time import sleep
    from fixEncoding import fixString
    import os
    import csv

    start_url = "https://5e.tools/bestiary.html#aarakocra%20simulacra_skt"
    #gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))  #legt den driver in PATH ab
    os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))  # legt den driver in PATH ab edit: Kein Grund dem eine Variable zuzuweisen
    #binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe') #hier müsst ihr den Pfad zu eurer firefox.exe angeben
    FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')  # hier müsst ihr den Pfad zu eurer firefox.exe angeben edit: wie oben
    driver = webdriver.Firefox()    # über diesen driver wird die Seite mit dynamischen Content aufgerufen
    driver.get(start_url)
    sleep(15) #sleep früher plazieren um sicherzustellen, dass die Seite erstmal lädt
    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()#lässt den driver 15 sek die Seite laden und klickt dann die Datenschutzhinweise weg
    sleep(5) #Sonst buggt es manchmal auch
    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='stat-tab  btn btn-default stat-tab-gen']"))).click() #wartet bis die seite geladen ist und klickt auf den Info-Block

    file_name = "Monsterliste_fixedEncoding.csv"
    with open(r'.\\' + file_name, mode='r') as f_in: #Öffne die csv um die an die links zu kommen und eine andere zum Speichern
        spamreader = csv.reader(f_in) #geschachtelte Liste mit allen Tupeln
        for row in spamreader: #Schleife über die Liste
            if not row == []: #Ignoriert leere Spalten die in der csv leider aus "übersichtlichkeitsgründen" auftauchen
                link = row[3] #Zieht die links
                if not link == "URL": #Okay bitte csv zukünftige mit dictwriter erstellen sonst werde ich sauer
                    driver.get(link) #öffnet den link
                    description = driver.find_element_by_xpath('//td[@class="text"]//descendant-or-self::*')   #xpath holt die description
                    #print(fixString(row[0]))
                    insertData(fixString(row[0]), fixString(row[1]), fixString(row[2]), fixString(row[3]), fixString(description.text))
    driver.close() #Schließ das ding

def encoding():
    from fixEncoding import fixEncoding
    file_name = 'Monsterliste.csv'
    fixEncoding(file_name)

def createCSV(namelist,cr_list,source_list,linklist):
    import csv
    import os
    file_name = 'Monsterliste.csv'
    with open(r'.\\' + file_name, mode='w') as monsterlist:
        writer = csv.DictWriter(monsterlist, fieldnames = ["Name", "CR", "Source","URL", "Beschreibung"])
        writer.writeheader()
        monsterlist = csv.writer(monsterlist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for x in range(len(namelist)):
            monsterlist.writerow([namelist[x].text, cr_list[x].text, source_list[x].get_attribute("title"),linklist[x].get_attribute("href")])  #bisher nur die beiden Attribute, bin schon am überlegen ob ich mir ne spider sparen kann :DD
            x += 1

def getAllButDescription():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait as wait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
    import os
    from time import sleep
    import csv

    start_url = "https://5e.tools/bestiary.html#aarakocra%20simulacra_skt"
    gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))  #legt den driver in PATH ab
    binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe') #hier müsst ihr den Pfad zu eurer firefox.exe angeben
    driver = webdriver.Firefox()    # über diesen driver wird die Seite mit dynamischen Content aufgerufen
    driver.get(start_url)
    wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()   #lässt den driver 15 sek die Seite laden und klickt dann die Datenschutzhinweise weg
    sleep(10)   #manchmal bekomme ich die Fehlermeldung, dass etwas noch nicht gefunden werden kann, hier pausiert das programm um sicher zu gehen, dass die seite geladen ist

    namelist = driver.find_elements_by_xpath("//span[@class='ecgen__name bold col-4-2 pl-0']")
    cr_list = driver.find_elements_by_xpath("//span[@class='col-1-7 text-center']")
    source_list = driver.find_elements_by_xpath("//span[starts-with(@class, 'col-2')]")
    linklist = driver.find_elements_by_xpath("//a[@class='lst--border']")
    createCSV(namelist,cr_list,source_list,linklist)
    encoding()
    driver.close()


def addDescription():
    import csv
    import os
    file_name = 'Monsterliste.csv'
    # os.remove('Monsterliste2.csv')
    with open("Monsterliste_fixedEncoding.csv") as f_in, open("Monsterliste_withDescription.csv", 'w') as f_out:
        # Write header unchanged
        header = f_in.readline()
        f_out.write(header)
        f_out = csv.writer(f_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        spamreader = csv.reader(f_in)
        for x in spamreader:
            if not x == []:
                f_out.writerow([x[0], x[1], x[2], x[3], "1"])


import os
if not os.path.exists("Monsterliste_fixedEncoding.csv"):
    getAllButDescription()
getDescription()