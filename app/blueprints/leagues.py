from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db_connect import DB_CONFIG
import pandas as pd

leagues_bp = Blueprint('leagues', __name__)

@leagues_bp.route('/show_leagues')
def show_leagues():
    connection = DB_CONFIG()
    query = """
    SELECT league_id, name, country, season, logo, start, end
    FROM leagues
    """
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    df = pd.DataFrame(result)
    if not df.empty:
        # Rename columns to be more user-friendly
        df.rename(columns=lambda x: x.replace('_', ' ').title(), inplace=True)
    if not df.empty:
        # Update the Pandas DataFrame to include Edit and Delete buttons
        df['Actions'] = df['League Id'].apply(lambda id:
            f'<a href="{url_for("leagues.edit_league", league_id=id)}" class="btn btn-sm btn-info">Edit</a> '
            f'<form action="{url_for("leagues.delete_league", league_id=id)}" method="post" style="display:inline;">'
            f'<button type="submit" class="btn btn-sm btn-danger">Delete</button></form>'
        )
    table_html = df.to_html(classes='dataframe table table-striped table-bordered', index=False, header=True, escape=False, justify='left', border=0)

    return render_template("leagues.html", table=table_html)


@leagues_bp.route('/add_league', methods=['GET', 'POST'])
def add_league():
    connection = DB_CONFIG()
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        season = int(request.form['season'])
        start = request.form['start']
        end = request.form['end']
        logo = request.form['logo']

        # Insert into leagues table
        query = """
        INSERT INTO leagues (league_id, name, country, season, logo, start, end)
        VALUES (NULL, %s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, (name, country, season, logo, start, end))
        connection.commit()
        flash("New league added successfully!", "success")
        return redirect(url_for('leagues.show_leagues'))

    return render_template("add_league.html")


@leagues_bp.route('/edit_league/<int:league_id>', methods=['GET', 'POST'])
def edit_league(league_id):
    connection = DB_CONFIG()
    if request.method == 'POST':
        name = request.form['name']
        country = request.form['country']
        season = int(request.form['season'])
        start = request.form['start']
        end = request.form['end']
        logo = request.form['logo']

        # Update leagues table
        query = """
        UPDATE leagues
        SET name = %s, country = %s, season = %s, start = %s, end = %s, logo = %s
        WHERE league_id = %s
        """
        with connection.cursor() as cursor:
            cursor.execute(query, (name, country, season, start, end, logo, league_id))
        connection.commit()
        flash("League updated successfully!", "success")
        return redirect(url_for('leagues.show_leagues'))

    # Fetch the current league data to pre-populate the form
    query = "SELECT * FROM leagues WHERE league_id = %s"
    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query, (league_id,))
        league = cursor.fetchone()

    return render_template("edit_league.html", league=league)


@leagues_bp.route('/delete_league/<int:league_id>', methods=['POST'])
def delete_league(league_id):
    connection = DB_CONFIG()
    query = "DELETE FROM leagues WHERE league_id = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (league_id,))
    connection.commit()
    flash("League deleted successfully!", "success")
    return redirect(url_for('leagues.show_leagues'))
