from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import connect_to_database

# Define the Blueprint
players_bp = Blueprint('players', __name__, template_folder='templates')

@players_bp.route('/', methods=['GET', 'POST'])
def manage_players():
    connection = connect_to_database()
    cursor = connection.cursor()

    if request.method == 'POST':
        # Handle form submission for adding a player
        name = request.form.get('name')
        number = request.form.get('number')
        position = request.form.get('position')
        team_id = request.form.get('team_id')

        try:
            query = """
                INSERT INTO players (name, number, position, team_id)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, number, position, team_id))
            connection.commit()
            flash("Player added successfully!", "success")
        except Exception as e:
            connection.rollback()
            flash(f"Error adding player: {e}", "danger")
        finally:
            cursor.close()
            connection.close()
            return redirect(url_for('players.manage_players'))

    # Handle sorting
    sort_by = request.args.get('sort_by', 'name')  # Default sort by name
    order = request.args.get('order', 'asc')  # Default order ascending
    valid_sort_columns = {
        'name': 'name',
        'number': 'number',
        'position': 'position'
    }
    valid_order = {'asc': 'ASC', 'desc': 'DESC'}

    sort_column = valid_sort_columns.get(sort_by, 'name')
    sort_order = valid_order.get(order, 'ASC')

    try:
        query = f"SELECT player_id, name, number, position, team_id FROM players ORDER BY {sort_column} {sort_order}"
        cursor.execute(query)
        players = cursor.fetchall()
    except Exception as e:
        players = []
        flash(f"Error fetching players: {e}", "danger")
    finally:
        cursor.close()
        connection.close()

    return render_template('players.html', players=players)
