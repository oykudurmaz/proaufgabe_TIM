from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.chrome.options import Options
import time

#optionales Argument, das die Chrome-Fenster (un)sichtbar macht
options = Options()
options.add_argument("--headless")

#es gibt zwei Fenster, Driver dient zum Pagination, Driver2 dient zum Abrufen der Details
driver = webdriver.Chrome(options=options)
driver2 = webdriver.Chrome(options=options)

driver.get('https://bugcrowd.com/programs')
time.sleep(2) #alle "time.(sleep)"-Funktionen, die verwendet werden, um sicherzustellen, dass die Seite geladen wird.

#Links von der ersten Seite zu erhalten
links = driver.find_elements(By.XPATH, '//a[@class="cc-inline-clamp-2"]')
time.sleep(2)

programs_info = dict()  #Erstellen ein Dictionary, um Name, URL für Schritt 2 und Min-Max Bounty für Schritt 3 zu übernehmen
programs_info['name'] = []
programs_info['url'] = []
programs_info['min_bounty'] = []
programs_info['max_bounty'] = []

#the Loop 1 ist nur für die erste Seite. Es loopt die Links auf der ersten Seite und nimmt Details auf
for first_page in links:

    href = first_page.get_attribute('href')   #aus dem Path der Links rufen wir alle Seiten mit href auf
    time.sleep(2)

    driver2.get(href)
    time.sleep(2)
    program_details = driver2.find_element(By.XPATH, '//div[@class="bounty-content col-md-8 col-md-pull-4"]')  #aus jedem href-Link erhalten wir Problemdetails
    time.sleep(2)

    prices = driver2.find_element(By.XPATH, '//span[@class= "bc-stat__fig"]')  #Wir definieren Preise, um die maximale und minimale Prämie zu finden
    time.sleep(2)
    temp = prices.text.split('$')  # Um den max Wert vom min Wert zu trennen, teilen wir den Text vom $-Zeichen.
    if len(temp) == 3: #Wenn sowohl der Min- als auch der Maxwert vorhanden sind, beträgt die Länge 3. Dann nehmen wir den ersten Wert als Min und den zweiten Wert als Max.
        new_temp = "".join(coco for coco in temp[2] if coco.isdigit())
        programs_info['max_bounty'].append(int(new_temp))
        new_temp = "".join(coco for coco in temp[1] if coco.isdigit())
        programs_info['min_bounty'].append(int(new_temp))
    else:
        programs_info['min_bounty'].append(0)  #Wenn es keine 3 Werte gibt, bedeutet dies, dass wir entweder nur den maximalen Wert oder keine Werte haben. Deshalb wird min 0 sein.
        if (len(temp) == 2): #Wenn die Länge 2 ist, bedeutet dies, dass es nur einen maximalen Wert gibt. Der erste Wert ist das Maximum.
            new_temp = "".join(coco for coco in temp[1] if coco.isdigit())
            programs_info['max_bounty'].append(int(new_temp))
        else:
            programs_info['max_bounty'].append(0) #wenn length nicht 2 ist, bedeutet dies, dass beide Werte fehlen, also setzen wir max auch auf 0.

    programs_info['name'].append(first_page.text)
    programs_info['url'].append(href)


#Dies ist die Schleife, um als nächstes auf die Schaltfläche zu klicken und dann Details von der Seite wie in der Loop 1 zu übernehmen
for page in range(12): #we have 13 pages that's why i put range with 12
    time.sleep(1)
    print(page)
    next_button = driver.find_elements(By.XPATH, '//button[@class="bc-pagination__link"]') #xpath of the next button
    time.sleep(1)

    for click in range(len(next_button)):
        if next_button[click].text == "Next":  #Da die anderen Seitenschaltflächen dieselbe Klasse haben, klickt der Code auf die Schaltfläche, wenn der Text "Weiter" lautet.
            next_button2 = next_button[click]
    next_button2.click()

    time.sleep(5)

    links = driver.find_elements(By.XPATH, '//a[@class="cc-inline-clamp-2"]')
    time.sleep(3)
    #gleicher Code mit Loop 1
    for first_page in links:
    #try except wird genutzt, um den Code ununterbrochen laufen zu lassen und falsche Seiten zu überspringen
        try:
            href = first_page.get_attribute('href')
            time.sleep(2)

            driver2.get(href)
            time.sleep(2)
            program_details = driver2.find_element(By.XPATH, '//div[@class="bounty-content col-md-8 col-md-pull-4"]')
            time.sleep(2)

            try:
                prices = driver2.find_element(By.XPATH, '//span[@class= "bc-stat__fig"]')
                time.sleep(2)
                temp = prices.text.split('$')
                if len(temp) == 3:
                    new_temp = "".join(coco for coco in temp[2] if coco.isdigit())
                    programs_info['max_bounty'].append(int(new_temp))
                    new_temp = "".join(coco for coco in temp[1] if coco.isdigit())
                    programs_info['min_bounty'].append(int(new_temp))
                else:
                    programs_info['min_bounty'].append(0)
                    if (len(temp) == 2):
                        new_temp = "".join(coco for coco in temp[1] if coco.isdigit())
                        programs_info['max_bounty'].append(int(new_temp))
                    else:
                        programs_info['max_bounty'].append(0)
            except:
                programs_info['min_bounty'].append(0)
                programs_info['max_bounty'].append(0)


            programs_info['name'].append(first_page.text)
            programs_info['url'].append(href)
        except:
            pass


driver.quit()
df = pd.DataFrame.from_dict(programs_info)   #Erstellen eines Datenrahmens aus dem Verzeichnis programms_info
df.to_csv(r'program_info.csv', index=False, header=True) #Erstellen einer CSV-Datei aus dem Datenrahmen
