from flask import render_template, flash, redirect, url_for
from app import app, db_connect, get_db
from app.services.api_football import update_team_statistics_in_db
from app.services.api_football import fetch_team_statistics


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/teams', methods=['GET'])
def teams():
    """
    Display Tottenham Hotspur's statistics from the database.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT team_name, team_logo, matches_played, wins, draws, losses,
               goals_scored, goals_conceded, xG, possession
        FROM teams
        WHERE team_id = 47
    """)  # Fetching data for Tottenham's team_id (47)
    tottenham_data = cursor.fetchone()

    if tottenham_data:
        stats = {
            "team_name": tottenham_data[0],
            "team_logo": tottenham_data[1],
            "matches_played": tottenham_data[2],
            "wins": tottenham_data[3],
            "draws": tottenham_data[4],
            "losses": tottenham_data[5],
            "goals_scored": tottenham_data[6],
            "goals_conceded": tottenham_data[7],
            "xG": tottenham_data[8],
            "possession": tottenham_data[9],
        }
    else:
        stats = None

    return render_template('teams.html', stats=stats)


@app.route('/update_team', methods=['GET'])
def update_team():
    """
    Fetch and update Tottenham Hotspur's data from API.
    """
    try:
        team_id = 47  # Tottenham Hotspur's team ID
        league_id = 39  # Premier League ID
        season = 2023   # Current season
        update_team_statistics_in_db(team_id, league_id, season)
        flash("Tottenham's statistics updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating Tottenham's statistics: {e}", "danger")

    return redirect(url_for('teams'))

@app.route('/players', methods=['GET'])
def players():
    return render_template('players.html')


@app.route('/matches', methods=['GET'])
def matches():
    return render_template('matches.html')


@app.route('/premier_league_table', methods=['GET'])
def premier_league_table():
    return render_template('premier_league_table.html')


@app.route('/history', methods=['GET'])
def history():
    return render_template('history.html')


@app.route('/insights', methods=['GET'])
def insights():
    return render_template('insights.html')

@app.route('/test_update', methods=['GET'])
def test_update():
    """
    Test fetching and updating Tottenham statistics.
    """
    team_id = 47  # Tottenham Hotspur's ID
    league_id = 39  # Premier League ID
    season = 2021  # Season year

    # Fetch and update team statistics
    try:
        team_data = fetch_team_statistics(team_id, league_id, season)
        if team_data:
            update_team_statistics_in_db(team_data)
            return "Team statistics fetched and database updated successfully!"
        else:
            return "Failed to fetch team statistics from API.", 500
    except Exception as e:
        return f"An error occurred: {e}", 500
