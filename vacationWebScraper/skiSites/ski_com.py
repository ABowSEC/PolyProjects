from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def scrape_ski_com(resort_slug):
    print(f"[Ski.com] Searching for packages at: {resort_slug}")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ski.com")

    time.sleep(5)

    try:
        # Find the destination input
        search_input = driver.find_element(By.ID, "destination-input")  # This ID may change
        search_input.send_keys(resort_slug)
        time.sleep(1)
        search_input.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"[Ski.com] Could not perform search: {e}")
        driver.quit()
        return

    time.sleep(5)

    listings = driver.find_elements(By.CSS_SELECTOR, '.listing-tile')  # This class may vary
    if not listings:
        print("[Ski.com] No listings found or site structure changed.")
        driver.quit()
        return

    for listing in listings[:5]:
        try:
            name = listing.find_element(By.CSS_SELECTOR, '.listing-tile__title').text
        except:
            name = "Unknown Resort"

        try:
            price = listing.find_element(By.CSS_SELECTOR, '.listing-tile__price').text
        except:
            price = "Price N/A"

        print(f"{name} — {price}")

    driver.quit()
