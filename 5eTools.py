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
wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='stat-tab  btn btn-default stat-tab-gen']"))).click()   #wartet bis die seite geladen ist und klickt auf den Info-Block
sleep(10)   #manchmal bekomme ich die Fehlermeldung, dass etwas noch nicht gefunden werden kann, hier pausiert das programm um sicher zu gehen, dass die seite geladen ist

description = driver.find_element_by_xpath('//td[@class="text"]//descendant-or-self::*')   #xpath holt das gesuchte element
                
namelist = driver.find_elements_by_xpath("//span[@class='ecgen__name bold col-4-2 pl-0']")
cr_list = driver.find_elements_by_xpath("//span[@class='col-1-7 text-center']")
source_list = driver.find_elements_by_xpath("//span[starts-with(@class, 'col-2')]")


with open(r'.\Monsterliste.csv', mode='w') as monsterlist:
    writer = csv.DictWriter(monsterlist, fieldnames = ["Name", "CR", "Source", "Beschreibung"])
    writer.writeheader()
    monsterlist = csv.writer(monsterlist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    for x in range(len(namelist)):
        monsterlist.writerow([namelist[x].text, cr_list[x].text, source_list[x].get_attribute("title")])  #bisher nur die beiden Attribute, bin schon am überlegen ob ich mir ne spider sparen kann :DD
        x += 1


driver.close()
#driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
