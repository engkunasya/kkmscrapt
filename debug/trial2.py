import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#THEORY
# {
#     "name": name_from_page_for_mal,
#     "malNumber": mal,
#     "dosageForm": dosage_form_from_page_for_mal,
#     "recommendedPrice": 0.0,
#     "manufacturer": manufacturer_from_page_for_mal,
#     "license": "NPRA"
# }

# Setup WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)





url = f"https://quest3plus.bpfk.gov.my/pmo2/detail.php?type=product&id=MAL04125487AZ"
driver.get(url)

try:
        name = wait.until(EC.presence_of_element_located((
            By.XPATH, '//*[@id="information"]/div[1]/table/tbody/tr[1]/td[1]/p/b'
        ))).text.strip()
except:
        name = ""



try:
        manufacturer = driver.find_element(
            By.XPATH, '//*[@id="information"]/div[1]/table/tbody/tr[4]/td[1]/p/b'
        ).text.strip()
except:
        manufacturer = ""



try:
        holder = driver.find_element(
            By.XPATH, '//*[@id="information"]/div[1]/table/tbody/tr[2]/td[1]/p/b'
        ).text.strip()
except:
        holder = ""



try:
        packaging = driver.find_element(
            By.XPATH, '//*[@id="tab2"]/tbody'
        ).text.strip()
except:
        packaging = ""



try:
        ingredients = driver.find_element(
            By.XPATH, '//*[@id="tab1"]/tbody'
        ).text.strip()
except:
        ingredients = ""

