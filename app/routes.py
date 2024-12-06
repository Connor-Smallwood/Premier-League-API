from flask import render_template
from . import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/matches')
def matches():
    return render_template('matches.html')

@app.route('/premier_league_table')
def premier_league_table():
    return render_template('premier_league_table.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/insights')
def insights():
    return render_template('insights.html')
