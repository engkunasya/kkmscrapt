import csv
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup undetected Chrome options for headless mode
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Initialize driver
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# Step 1: Read MAL numbers from CSV
with open('mal_codes.csv') as file:
    reader = csv.reader(file)
    data = list(reader)

mal_numbers = []

# Step 2: Select MAL numbers from rows 1 to 22
for row in data[1:23]:
    for mal in row:
        mal = mal.strip()
        if mal:
            mal_numbers.append(mal)

json_data = []

for mal in mal_numbers:
    url = f"https://quest3plus.bpfk.gov.my/pmo2/detail.php?type=product&id={mal}"
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
        "ingredients": ingredients
    }

    json_data.append(product)
    print(f"✅ Scraped {mal}")

# Write all data to JSONL file
with open('mal_data_headless.jsonl', 'w', encoding='utf-8') as json_file:
    for item in json_data:
        json_file.write(json.dumps(item) + "\n")

print(f"✅ Finished scraping {len(json_data)} records")

driver.quit()
