# A. Bowman LineShift — Custom Proprietary Software License
# Copyright © 2025 A. Bowman. All rights reserved.

from playwright.sync_api import sync_playwright #Attempting to beat DK 
import sqlite3
import json

NFL_URL = "https://sportsbook.draftkings.com/leagues/football/nfl"

conn = sqlite3.connect("nfl_odds.db")
cursor = conn.cursor()

def fetch_dk_data():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            page.goto(NFL_URL, timeout=60000)

            # Wait for data to load - wait for a common game element
            page.wait_for_selector(".event-cell__name-text", timeout=30000)

            # Extract all visible odds data
            games = page.query_selector_all(".sportsbook-event-accordion__wrapper")
            scraped_games = []

            for game in games:
                try:
                    teams = game.query_selector_all(".event-cell__name-text")
                    if len(teams) != 2:
                        continue

                    away_team = teams[0].inner_text().strip()
                    home_team = teams[1].inner_text().strip()

                    start_time_elem = game.query_selector(".event-cell__time")
                    start_time = start_time_elem.inner_text().strip() if start_time_elem else ""

                    # Moneyline odds
                    ml_cells = game.query_selector_all('[data-test="americanOdds"]')                # Be wary for doublequote issues """" vs '""'
                    ml_away = ml_cells[0].inner_text().strip() if len(ml_cells) > 1 else None
                    ml_home = ml_cells[1].inner_text().strip() if len(ml_cells) > 1 else None

                    # Totals (Over/Under)
                    total_elem = game.query_selector('[data-test="americanOdds"]')
                    total = total_elem.inner_text().strip() if total_elem else None

                    # Spreads
                    spread_elems = game.query_selector_all('[data-test="spread"]')
                    spreads = [s.inner_text().strip() for s in spread_elems]
                    spread = " | ".join(spreads)

                    scraped_games.append({
                        "home_team": home_team,
                        "away_team": away_team,
                        "start_time": start_time,
                        "moneyline_home": ml_home,
                        "moneyline_away": ml_away,
                        "spread": spread,
                        "over_under": total
                    })
                except Exception as inner:
                    print("Failed to parse a game block:", inner)

            browser.close()
            return scraped_games
    except Exception as e:
        print("Failed to fetch DraftKings NFL data with Playwright:", e)
        return []

def insert_into_db(games):
    for g in games:
        game_id = f"{g['away_team']}@{g['home_team']} {g['start_time']}"

        cursor.execute('''
            INSERT OR IGNORE INTO games (game_id, start_time, home_team, away_team)
            VALUES (?, ?, ?, ?)
        ''', (game_id, g['start_time'], g['home_team'], g['away_team']))

        cursor.execute('''
            INSERT INTO odds (game_id, provider, spread_details, over_under, moneyline_home, moneyline_away)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (game_id, "DraftKings-Web", g['spread'], g['over_under'], g['moneyline_home'], g['moneyline_away']))

        print(f"Imported odds: {g['away_team']} @ {g['home_team']}")

    conn.commit()

def run_dk_import():
    print("Launching browser to fetch DraftKings NFL odds...")
    scraped = fetch_dk_data()
    if scraped:
        insert_into_db(scraped)
    print("DraftKings NFL import complete.")

if __name__ == "__main__":
    run_dk_import()
