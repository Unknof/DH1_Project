from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os
from time import sleep

#Bei jedem neuen Durchlauf muss das geöffnete Browser Fenster wieder geschlossen werden

start_url = "https://5e.tools/bestiary.html#aarakocra_mm"
gecko = os.path.normpath(os.path.join(os.path.dirname(__file__), 'geckodriver'))  #legt den driver in PATH ab
binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe') #hier müsst ihr den Pfad zu eurer firefox.exe angeben
driver = webdriver.Firefox()    # über diesen driver wird die Seite mit dynamischen Content aufgerufen
driver.get(start_url)           
wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='onetrust-accept-btn-handler']"))).click()   #lässt den driver 15 sek die Seite laden und klickt dann die Datenschutzhinweise weg
wait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='stat-tab  btn btn-default stat-tab-gen']"))).click()   #wartet bis die seite geladen ist und klickt auf den Info-Block
sleep(10)   #manchmal bekomme ich die Fehlermeldung, dass etwas noch nicht gefunden werden kann, hier pausiert das programm um sicher zu gehen, dass die seite geladen ist

p_element = driver.find_element_by_xpath("//div[@class='rd__b  rd__b--2']//descendant-or-selfc::*")   #xpath holt das gesuchte element



print(p_element.text)
#driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#"//div[@class='rd__b  rd__b--2']/p[1]"
####