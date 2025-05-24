import requests
from bs4 import BeautifulSoup

def scrape_lift_tickets(resort_slug):
    url = f"https://www.onthesnow.com/colorado/{resort_slug}/lift-tickets.html"
    print(f"[OnTheSnow] Scraping: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    ticket_sections = soup.select(".lift-ticket-table tbody tr")
    if not ticket_sections:
        print("No ticket info found — structure may have changed.")
        return

    for row in ticket_sections:
        cells = row.find_all("td")
        if len(cells) >= 2:
            ticket_type = cells[0].get_text(strip=True)
            price = cells[1].get_text(strip=True)
            print(f"{ticket_type}: {price}")