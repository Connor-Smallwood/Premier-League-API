from flask import Flask, render_template
from app import app
from app.db_connect import connect_to_database

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')

@app.route('/players')
def players():
    return render_template('players.html')

@app.route('/insights')
def insights():
    return render_template('insights.html')

@app.route('/leagues', methods=['GET'])
def leagues():
    return render_template('leagues.html')