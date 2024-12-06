from app.services.api_football import fetch_team_statistics, update_team_statistics_in_db

def test_fetch_and_update():
    # Set parameters for the API request
    team_id = 47  # Tottenham Hotspur's ID
    league_id = 39  # Premier League ID
    season = 2021  # Season year

    # Fetch team statistics from the API
    print("Fetching team statistics...")
    team_data = fetch_team_statistics(team_id, league_id, season)

    # Check if data was fetched successfully
    if team_data:
        print("Team data fetched successfully:")
        print(team_data)

        # Update the database with the fetched data
        print("Updating database with team statistics...")
        update_team_statistics_in_db(team_data)
        print("Database update complete.")
    else:
        print("Failed to fetch team data.")

if __name__ == "__main__":
    test_fetch_and_update()
