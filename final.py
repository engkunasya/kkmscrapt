
#THEORY
# {
#     "name": name_from_page_for_mal,
#     "malNumber": mal,
#     "dosageForm": dosage_form_from_page_for_mal,
#     "recommendedPrice": 0.0,
#     "manufacturer": manufacturer_from_page_for_mal,
#     "license": "NPRA"
# }


import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Helper: Wait until an element's text is non-empty
def wait_for_non_empty_text(driver, xpath, timeout=10):
    return WebDriverWait(driver, timeout).until(
        lambda d: d.find_element(By.XPATH, xpath).text.strip() != ""
    )

# Setup WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)



# Step 1: Read selected MAL numbers from CSV
with open('break1.csv') as file:
    reader = csv.reader(file)
    data = list(reader)

mal_numbers = []

# Step 2: Only select MAL numbers from rows 1 to 22
for row in data[1:23]:  # rows 1 to 22
    for mal in row:
        mal = mal.strip()
        if mal:
            mal_numbers.append(mal)

# Step 3: Scrape and save details immediately per MAL number
with open('mal_data.jsonl', 'a', encoding='utf-8') as json_file:
    for mal in mal_numbers:
        url = f"https://quest3plus.bpfk.gov.my/pmo2/detail.php?type=product&id={mal}"
        driver.get(url)

        # Optional delay or additional wait if necessary
        time.sleep(1.5)

        try:
            name_xpath = '//*[@id="information"]/div[1]/table/tbody/tr[1]/td[1]/p/b'
            wait_for_non_empty_text(driver, name_xpath)
            name = driver.find_element(By.XPATH, name_xpath).text.strip()
        except:
            name = ""

        print (mal, name)

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

        

        product = {
            "name": name,
            "malNumber": mal,
            "packaging": packaging,
            "recommendedPrice": 0.0,
            "manufacturer": manufacturer,
            "holder": holder,
            "ingredients": ingredients
        }

        json_file.write(json.dumps(product) + "\n")
        print(f"✅ Scraped and saved {mal} {name}")

# Step 4: Clean up
driver.quit()