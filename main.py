

import csv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Chrome WebDriver
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)

# This function will scrape MAL codes based on the given MAL number prefix
def get_mal_codes(prefix):
    driver.get("https://quest3plus.bpfk.gov.my/pmo2/")
    
    # Select the search criteria
    input_element = driver.find_element(By.ID, "searchBy")
    dropdown = Select(input_element)
    dropdown.select_by_value("2")  # For MAL Number

    # Wait for dropdown and search input to be clickable, then enter the prefix (MAL04, MAL05, etc.)
    dropdown_trigger = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-selection--single')))
    dropdown_trigger.click()
    
    search_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.select2-search__field')))
    search_input.click()
    
    # Send the prefix (MAL04, MAL05, etc.) into the search field
    search_input.send_keys(prefix)
    
    # Wait for the results container to load
    results_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'select2-results__options'))
    )
    
    # Custom wait condition: wait until at least 5 <li> are present
    WebDriverWait(driver, 10).until(
        lambda d: len(results_container.find_elements(By.TAG_NAME, 'li')) >= 5
    )
    
    # Retrieve and print the options
    options = results_container.find_elements(By.TAG_NAME, 'li')
    mal_codes = [option.text for option in options]
    return mal_codes

# Debug: Check if CSV can be written to current directory
print("Working directory for saving CSV:", os.getcwd())

# Write the MAL codes to a CSV file during the loop
with open("mal_codes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    
    # Initialize the header (MAL04, MAL05, ..., MAL25)
    header = [f'MAL{i:02d}' for i in range(4, 26)]  # MAL04 to MAL25
    writer.writerow(header)

    for i in range(4, 26):  # MAL04 to MAL25
        mal_prefix = f"MAL{i:02d}"  # Format to 'MAL04', 'MAL05', etc.
        
        # Scrape MAL numbers for the current prefix
        mal_codes = get_mal_codes(mal_prefix)
        
        # Write the results for this MAL number as a row in the CSV
        writer.writerow(mal_codes)
        
        # Print to console for debugging
        print(f"✅ Finished scraping {mal_prefix} with {len(mal_codes)} results.")

# Close the WebDriver
driver.quit()