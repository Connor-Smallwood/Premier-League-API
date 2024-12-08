from app.services.api_football import fetch_league_data
from app.db_connect import insert_league_data
from flask import Flask, request, jsonify

app = Flask(__name__)

if __name__ == "__main__":
    league_id = 39  # Example for Premier League
    season = 2021   # Specify the season year

    # Fetch league data
    league_data = fetch_league_data(league_id, season)

    # Insert into database
    if league_data:
        insert_league_data(league_data, season)
        print("League data inserted successfully!")
    else:
        print("Failed to fetch or insert league data.")

if __name__ == '__main__':
    app.run(debug=True)
