import json
import requests
from app.db_connect import get_db

# API Configuration
API_KEY = "6e0dfc805474353f8cd2a4e30cda460b"  # Replace with your actual API key
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}


def fetch_team_statistics(team_id, league_id, season):
    """
    Fetch Tottenham's statistics from API-Football.
    """
    url = f"{BASE_URL}/teams/statistics"
    params = {
        "season": season,
        "team": team_id,
        "league": league_id
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        json_data = response.json()
        print("API Response:", json.dumps(json_data, indent=4))  # Print the full API response
        return json_data
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None

def update_team_statistics_in_db(team_data):
    """
    Update Tottenham's statistics in the database.
    :param team_data: Parsed JSON data from API.
    """
    db = get_db()
    cursor = db.cursor()

    processed_data = {
        "team_id": 47,  # Tottenham's ID
        "team_name": team_data['team']['name'],
        "team_logo": team_data['team']['logo'],
        "matches_played": team_data['fixtures']['played']['total'],
        "wins": team_data['fixtures']['wins']['total'],
        "draws": team_data['fixtures']['draws']['total'],
        "losses": team_data['fixtures']['loses']['total'],
        "goals_scored": team_data['goals']['for']['total'],
        "goals_conceded": team_data['goals']['against']['total'],
        "xG": team_data['goals']['for']['average'],
        "possession": team_data['percentage']['possession']['total']
    }

    cursor.execute("""
        INSERT INTO teams (team_id, team_name, team_logo, matches_played, wins, draws, losses,
                           goals_scored, goals_conceded, xG, possession)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            team_name = VALUES(team_name),
            team_logo = VALUES(team_logo),
            matches_played = VALUES(matches_played),
            wins = VALUES(wins),
            draws = VALUES(draws),
            losses = VALUES(losses),
            goals_scored = VALUES(goals_scored),
            goals_conceded = VALUES(goals_conceded),
            xG = VALUES(xG),
            possession = VALUES(possession)
    """, (
        processed_data['team_id'], processed_data['team_name'], processed_data['team_logo'],
        processed_data['matches_played'], processed_data['wins'], processed_data['draws'],
        processed_data['losses'], processed_data['goals_scored'], processed_data['goals_conceded'],
        processed_data['xG'], processed_data['possession']
    ))
    db.commit()
    print("Database updated with Tottenham's statistics.")
