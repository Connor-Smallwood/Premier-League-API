from flask import render_template, request, redirect, url_for, flash
from app import app
from app.get_player_data import update_team_players
from app.db_connect import connect_to_database


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/players', methods=['GET'])
def players():
    db = connect_to_database()
    cursor = db.cursor()

    try:
        # Fetch players grouped by teams
        query = """
            SELECT t.name AS team_name, p.name AS player_name, p.number, p.position, p.player_id
            FROM teams t
            LEFT JOIN players p ON t.team_id = p.team_id
            ORDER BY t.name, p.name;
        """
        cursor.execute(query)
        data = cursor.fetchall()

        # Group players by team
        grouped_players = {}
        for row in data:
            team_name, player_name, number, position, player_id = row
            if team_name not in grouped_players:
                grouped_players[team_name] = []
            if player_name:  # Exclude teams with no players
                grouped_players[team_name].append({
                    "player_name": player_name,
                    "number": number,
                    "position": position,
                    "player_id": player_id,
                })
    except Exception as e:
        grouped_players = {}
        flash(f"Error fetching players: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return render_template('players.html', grouped_players=grouped_players)



@app.route('/edit_player/<int:player_id>', methods=['POST'])
def edit_player(player_id):
    db = connect_to_database()
    cursor = db.cursor()

    name = request.form.get('name')
    position = request.form.get('position')
    team_id = request.form.get('team_id')
    number = request.form.get('number')

    try:
        query = """
            UPDATE players
            SET name = %s, position = %s, team_id = %s, number = %s
            WHERE player_id = %s
        """
        cursor.execute(query, (name, position, team_id, player_id, number))
        db.commit()
        flash("Player updated successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating player: {e}", "danger")
    finally:
        cursor.close()
        db.close()
        return redirect(url_for('players'))


@app.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    db = connect_to_database()
    cursor = db.cursor()

    try:
        query = "DELETE FROM players WHERE player_id = %s"
        cursor.execute(query, (player_id,))
        db.commit()
        flash("Player deleted successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting player: {e}", "danger")
    finally:
        cursor.close()
        db.close()
        return redirect(url_for('players'))

@app.route('/add_player', methods=['POST'])
def add_player():
    """
    Add a new player to the database.
    """
    db = connect_to_database()
    cursor = db.cursor()

    # Retrieve form data
    name = request.form.get('name')
    number = request.form.get('number')
    position = request.form.get('position')
    team_id = request.form.get('team_id')

    try:
        # Insert into the database
        query = """
            INSERT INTO players (name, number, position, team_id)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, number, position, team_id))
        db.commit()
        flash("Player added successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error adding player: {e}", "danger")
    finally:
        cursor.close()
        db.close()
        return redirect(url_for('players'))


@app.route('/insights')
def insights():
    return render_template('insights.html')

@app.route('/teams', methods=['GET', 'POST'])
def teams():
    connection = connect_to_database()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Add new team
        name = request.form.get('name')
        address = request.form.get('address')
        city = request.form.get('city')
        logo = request.form.get('logo')

        try:
            query = "INSERT INTO teams (name, address, city, logo) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, address, city, logo))
            connection.commit()
            flash("Team added successfully!", "success")
        except Exception as e:
            connection.rollback()
            flash(f"Error adding team: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
            return redirect(url_for('teams'))

    # Handle sorting
    sort_by = request.args.get('sort_by', 'name')
    order = request.args.get('order', 'asc')
    valid_sort_columns = {'name': 'name', 'city': 'city'}
    valid_order = {'asc': 'ASC', 'desc': 'DESC'}

    sort_column = valid_sort_columns.get(sort_by, 'name')
    sort_order = valid_order.get(order, 'ASC')

    try:
        query = f"SELECT team_id, name, address, city, logo FROM teams ORDER BY {sort_column} {sort_order}"
        cursor.execute(query)
        teams = cursor.fetchall()
    except Exception as e:
        teams = []
        flash(f"Error fetching teams: {e}", "danger")
    finally:
        cursor.close()
        connection.close()

    return render_template('teams.html', teams=teams)

@app.route('/edit_team/<int:team_id>', methods=['POST'])
def edit_team(team_id):
    db = connect_to_database()
    cursor = db.cursor()

    # Retrieve form data
    name = request.form.get('name')
    address = request.form.get('address')
    city = request.form.get('city')
    logo = request.form.get('logo')

    try:
        # Update the team in the database
        query = """
            UPDATE teams
            SET name = %s, address = %s, city = %s, logo = %s
            WHERE team_id = %s
        """
        cursor.execute(query, (name, address, city, logo, team_id))
        db.commit()
        flash("Team updated successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error updating team: {e}", "danger")
    finally:
        cursor.close()
        db.close()
        return redirect(url_for('teams'))

@app.route('/delete_team/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    db = connect_to_database()
    cursor = db.cursor()

    try:
        # Delete the team from the database
        query = "DELETE FROM teams WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        db.commit()
        flash("Team deleted successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error deleting team: {e}", "danger")
    finally:
        cursor.close()
        db.close()
        return redirect(url_for('teams'))

@app.route('/add_team', methods=['POST'])
def add_team():
    db = connect_to_database()
    cursor = db.cursor()

    # Retrieve form data
    name = request.form.get('name')
    address = request.form.get('address')
    city = request.form.get('city')
    logo = request.form.get('logo')

    try:
        # Insert the new team into the database
        query = """
            INSERT INTO teams (name, address, city, logo)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, address, city, logo))
        db.commit()
        flash("Team added successfully!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error adding team: {e}", "danger")
    finally:
        cursor.close()
        db.close()
        return redirect(url_for('teams'))

@app.route('/update_players/<int:team_id>', methods=['POST'])
def update_players_for_team(team_id):
    """
    Update players for a specific team.
    """
    try:
        success = update_team_players(team_id)
        if success:
            flash(f"Players updated successfully for team ID: {team_id}!", "success")
        else:
            flash(f"Failed to update players for team ID: {team_id}.", "danger")
    except Exception as e:
        flash(f"Error updating players for team ID {team_id}: {e}", "danger")

    return redirect(url_for('teams'))

@app.route('/update_players_all', methods=['POST'])
def update_players_all():
    """
    Update players for all teams in the database.
    """
    db = connect_to_database()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT team_id FROM teams")
        teams = cursor.fetchall()

        for team in teams:
            team_id = team[0]
            success = update_team_players(team_id)
            if not success:
                flash(f"Failed to update players for team ID: {team_id}.", "danger")

        flash("Players updated successfully for all teams!", "success")
    except Exception as e:
        flash(f"Error updating players for all teams: {e}", "danger")
    finally:
        cursor.close()
        db.close()

    return redirect(url_for('teams'))