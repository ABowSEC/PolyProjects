import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title = "LineShift Dashboard", layout = "wide")
st.title("LineShift - NFL ODDS Dashboard")

#connect to generated DBs
conn = sqlite3.connect("nfl_odds.db")

#retrieve latest odds send to dashboard
query = """
SELECT
    g.home_team,
    g.away_team,
    o.spread_details,
    o.over_under,
    o.moneyline_home,
    o.moneyline_away,
    MAX(o.updated_at) AS last_updated
FROM games g
JOIN odds o ON g.game_id = o.game_id
GROUP BY g.game_id
ORDER BY last_updated DESC
"""

df = pd.read_sql_query(query, conn)

# Filter sidebar
team_filter = st.sidebar.text_input("Filter by Team Name:")
if team_filter:
    df = df[df['home_team'].str.contains(team_filter, case=False) |
            df['away_team'].str.contains(team_filter, case=False)]

# Display table
st.dataframe(df, use_container_width=True)

conn.close()