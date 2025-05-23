from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import urllib.parse

def scrape_lodging(resort_slug):
    location_map = {
        'copper-mountain-resort': 'Copper Mountain, CO',
        'vail': 'Vail, CO',
        'breckenridge': 'Breckenridge, CO',
        'aspen-snowmass': 'Aspen, CO'
    }

    query = location_map.get(resort_slug, "Colorado")
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.expedia.com/Hotel-Search?destination={encoded_query}"

    print(f"[Expedia] Searching for lodging at: {query}")
    print(f"[Expedia] URL: {url}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Specify your chromedriver.exe path here
    chromedriver_path = r"C:\Tools\chromedriver\chromedriver.exe"
    service = Service(chromedriver_path)

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    hotels = driver.find_elements(By.CSS_SELECTOR, 'div[data-stid="property-listing"]')

    if not hotels:
        print("No hotels found (Expedia structure may have changed).")
        driver.quit()
        return []

    results = []
    for hotel in hotels[:5]:
        try:
            name = hotel.find_element(By.CSS_SELECTOR, '[data-stid="content-hotel-title"]').text
        except:
            name = "Unknown Hotel"

        try:
            price = hotel.find_element(By.CSS_SELECTOR, '[data-stid="price-lockup-text"]').text
        except:
            price = "Price N/A"

        print(f"{name} — {price}")
        results.append({'name': name, 'price': price})

    driver.quit()
    return results
