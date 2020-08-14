from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os
from time import sleep
import csv



start_url = "https://5e.tools/bestiary.html#aarakocra_mm"
gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))  #legt den driver in PATH ab
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe') #hier müsst ihr den Pfad zu eurer firefox.exe angeben
driver = webdriver.Firefox()    # über diesen driver wird die Seite mit dynamischen Content aufgerufen
driver.get(start_url)           
wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()   #lässt den driver 15 sek die Seite laden und klickt dann die Datenschutzhinweise weg
wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='stat-tab  btn btn-default stat-tab-gen']"))).click()   #wartet bis die seite geladen ist und klickt auf den Info-Block
sleep(10)   #manchmal bekomme ich die Fehlermeldung, dass etwas noch nicht gefunden werden kann, hier pausiert das programm um sicher zu gehen, dass die seite geladen ist

description = driver.find_element_by_xpath("//div[@class='rd__b  rd__b--2']//descendant-or-self::*")   #xpath holt das gesuchte element
name = driver.find_element_by_xpath("//span[@class='ecgen__name bold col-4-2 pl-0']/self::*")
cr = driver.find_element_by_xpath("//span[@class='col-1-7 text-center']/self::*")
source_element = driver.find_element_by_xpath("//span[@class='col-2 text-center sourceMM pr-0']")
source = source_element.get_attribute("title")
print(description.text)
print(name.text)
print(cr.text)
print(source)


with open(r'C:\Users\ralfh\Documents\Python Scripts\DH1_Project\DH1_Project\Monsterliste.csv', mode='w') as monsterlist:
    writer = csv.DictWriter(monsterlist, fieldnames = ["Name", "CR", "Source", "Beschreibung"])
    writer.writeheader()
    monsterlist = csv.writer(monsterlist, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    
    monsterlist.writerow([name.text, cr.text, source, description.text])
    


driver.close()
#driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#"//div[@class='rd__b  rd__b--2']/p[1]"
####