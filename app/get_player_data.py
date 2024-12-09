import requests
import mysql.connector

# API Configuration
API_URL = "https://v3.football.api-sports.io/players/squads"
API_HEADERS = {
    "x-rapidapi-key": "6e0dfc805474353f8cd2a4e30cda460b",  # Replace with your API key
    "x-rapidapi-host": "v3.football.api-sports.io"
}

# Database Configuration
DB_CONFIG = {
    "host": "jw0ch9vofhcajqg7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    "user": "or9lfkafm52dnld9",
    "password": "ybq0i39tcg69u170",
    "database": "gq4u8frecn8pgnmq"
}

def fetch_squad_data(team_id):
    """
    Fetch squad data for a specific team using the API.
    """
    params = {"team": team_id}
    response = requests.get(API_URL, headers=API_HEADERS, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"API Error: {response.status_code}, {response.text}")
        return None

def store_squad_in_db(squad, team_id):
    """
    Store the squad data in the database.
    """
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()

    for player in squad:
        try:
            player_id = player["id"]
            name = player["name"]
            position = player["position"]
            number = player.get("number", None)

            # Insert into database
            query = """
                INSERT INTO players (player_id, name, position, team_id, number)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                position = VALUES(position),
                number = VALUES(number)
            """
            cursor.execute(query, (player_id, name, position, team_id, number))
        except Exception as e:
            print(f"Error inserting player: {e}")

    db.commit()
    cursor.close()
    db.close()

def update_team_players(team_id):
    """
    Fetch and store players for a specific team in the database.
    """
    data = fetch_squad_data(team_id)

    if data and "response" in data and len(data["response"]) > 0:
        squad = data["response"][0]["players"]
        store_squad_in_db(squad, team_id)
        return True
    return False

# Main Script
if __name__ == "__main__":
    team_id = 47  # Tottenham Hotspur

    # Fetch squad data from the API
    data = fetch_squad_data(team_id)

    if data and "response" in data and len(data["response"]) > 0:
        squad = data["response"][0]["players"]

        # Store squad in the database and print to console
        store_squad_in_db(squad, team_id)

        print("Squad data has been successfully stored in the database and printed to the console.")
