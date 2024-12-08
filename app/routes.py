from flask import render_template, request, redirect, url_for, flash
from app import app
from app.db_connect import get_db

@app.route('/leagues/edit/<int:league_id>', methods=['GET', 'POST'])
def edit_league(league_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    if request.method == 'POST':
        # Handle form submission to update league
        name = request.form['name']
        country = request.form['country']
        season = int(request.form['season'])
        start = request.form['start']
        end = request.form['end']
        logo = request.form['logo']

        query = """
        UPDATE leagues
        SET name = %s, country = %s, season = %s, start = %s, end = %s, logo = %s
        WHERE league_id = %s
        """
        cursor.execute(query, (name, country, season, start, end, logo, league_id))
        db.commit()
        flash('League updated successfully!', 'success')
        return redirect(url_for('leagues'))

    # Fetch league data for the form
    cursor.execute("SELECT * FROM leagues WHERE league_id = %s", (league_id,))
    league = cursor.fetchone()

    return render_template('edit_league.html', league=league)


@app.route('/leagues/delete/<int:league_id>', methods=['POST'])
def delete_league(league_id):
    db = get_db()
    cursor = db.cursor()

    query = "DELETE FROM leagues WHERE league_id = %s"
    cursor.execute(query, (league_id,))
    db.commit()

    flash('League deleted successfully!', 'danger')
    return redirect(url_for('leagues'))
