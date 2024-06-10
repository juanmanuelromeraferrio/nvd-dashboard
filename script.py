import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_nvd_dashboard():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Set up the Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open the NVD dashboard
        url = 'https://nvd.nist.gov/general/nvd-dashboard'
        driver.get(url)

        # Wait until the table is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'tableCveStatusCount'))
        )

        # Locate the table
        table = driver.find_element(By.ID, 'tableCveStatusCount')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        # Extract data
        data = {}
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, 'td')
            title = cols[0].text.strip()
            value = cols[1].text.strip()
            data[title] = value

        # Get current date
        current_date = datetime.now().strftime('%Y-%m-%d')

        # Create a new row with the date and extracted data
        new_row = [
            current_date,
            data.get('Total', 'N/A'),
            data.get('Received', 'N/A'),
            data.get('Awaiting Analysis', 'N/A'),
            data.get('Undergoing Analysis', 'N/A'),
            data.get('Modified', 'N/A'),
            data.get('Rejected', 'N/A')
        ]

        # Define CSV file path
        csv_file = 'nvd_dashboard_data.csv'

        # Check if the file exists to write headers if it's new
        file_exists = os.path.isfile(csv_file)

        # Write data to CSV
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Last Update', 'Total', 'Received', 'Awaiting Analysis', 'Undergoing Analysis', 'Modified', 'Rejected'])
            writer.writerow(new_row)

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_nvd_dashboard()
