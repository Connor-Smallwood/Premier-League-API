from flask import Blueprint, render_template, flash, redirect, url_for
from app.services.api_football import fetch_team_statistics, update_team_statistics_in_db
from app.db_connect import get_db

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/teams', methods=['GET'])
def show_team():
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
    """)
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

@teams_bp.route('/update_team', methods=['GET'])
def update_team():
    """
    Fetch and update Tottenham's data from API.
    """
    team_id = 47  # Tottenham Hotspur's ID
    league_id = 39  # Premier League ID
    season = 2021   # Season year

    try:
        team_data = fetch_team_statistics(team_id, league_id, season)
        if team_data:
            update_team_statistics_in_db(team_data)
            flash("Tottenham's statistics updated successfully!", "success")
        else:
            flash("Failed to fetch data from API.", "danger")
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")

    return redirect(url_for('teams.show_team'))
