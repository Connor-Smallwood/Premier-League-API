import requests

API_KEY = "6e0dfc805474353f8cd2a4e30cda460b"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

def fetch_league_data(league_id, season):
    """
    Fetch league data from API for a given league ID and season.
    """
    url = f"{BASE_URL}/leagues"
    params = {
        "id": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["response"]:
            return data["response"][0]  # Return the first league response
        else:
            print("No league data found.")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def fetch_team_statistics(team_id, league_id, season):
    """
    Fetch team statistics for a given team, league, and season.
    """
    url = f"{BASE_URL}/teams/statistics"
    params = {
        "team": team_id,
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
