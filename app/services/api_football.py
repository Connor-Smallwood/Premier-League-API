import requests

# API Configuration
API_URL = "https://v3.football.api-sports.io/leagues"
API_HEADERS = {
    "x-rapidapi-key": "6e0dfc805474353f8cd2a4e30cda460b",  # Replace with your API key
    "x-rapidapi-host": "v3.football.api-sports.io"
}

def fetch_api_data(params):
    """
    Fetch data from the API.
    """
    response = requests.get(API_URL, headers=API_HEADERS, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"API Error: {response.status_code}, {response.text}")
        return None
