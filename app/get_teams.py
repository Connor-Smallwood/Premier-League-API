import requests
import mysql.connector

# API Configuration
API_URL = "https://v3.football.api-sports.io/teams"
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

def fetch_team_data(league_id, season):
    """
    Fetch team data for a specific league and season using the API.
    """
    params = {"league": league_id, "season": season}
    response = requests.get(API_URL, headers=API_HEADERS, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"API Error: {response.status_code}, {response.text}")
        return None

def store_teams_in_db(teams):
    """
    Store team data in the database and output their details to the console.
    """
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()

    for team in teams:
        try:
            team_id = team["team"]["id"]
            name = team["team"]["name"]
            address = team["venue"]["address"]
            city = team["venue"]["city"]
            logo = team["team"]["logo"]

            # Print team details to the console
            print(f"Team: {name}, Address: {address}, City: {city}, Logo: {logo}")

            # Insert into database
            query = """
                INSERT INTO teams (team_id, name, address, city, logo)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                address = VALUES(address),
                city = VALUES(city),
                logo = VALUES(logo)
            """
            cursor.execute(query, (team_id, name, address, city, logo))
        except KeyError as e:
            print(f"Missing key in team data: {e}")
        except Exception as e:
            print(f"Error inserting team: {e}")

    db.commit()
    cursor.close()
    db.close()

# Main Script
if __name__ == "__main__":
    league_id = 39  # Example: English Premier League
    season = 2022   # Example season

    # Fetch team data from the API
    data = fetch_team_data(league_id, season)

    if data and "response" in data:
        teams = data["response"]

        # Store teams in the database and print to console
        store_teams_in_db(teams)

        print("Team data has been successfully stored in the database and printed to the console.")
