import mysql.connector
from flask import g

# Database connection configuration
DB_CONFIG = {
    "host": "jw0ch9vofhcajqg7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    "user": "or9lfkafm52dnld9",
    "password": "ybq0i39tcg69u170",
    "database": "gq4u8frecn8pgnmq"
}

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DB_CONFIG)
    return g.db

def insert_league_data(league_data, season):
    """
    Insert or update league data in the leagues table.
    """
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        sql = """
            INSERT INTO leagues (league_id, name, country, season, logo, start, end)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                country = VALUES(country),
                logo = VALUES(logo),
                start = VALUES(start),
                end = VALUES(end);
        """

        values = (
            league_data["league"]["id"],        # league_id
            league_data["league"]["name"],      # name
            league_data["country"]["name"],     # country
            season,                             # season
            league_data["league"]["logo"],      # logo
            league_data["seasons"][0]["start"], # start date
            league_data["seasons"][0]["end"]    # end date
        )

        cursor.execute(sql, values)
        db.commit()

        print("League data inserted successfully!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def insert_statistics(statistics, league_id):
    """
    Insert or update team statistics in the statistics table.
    """
    try:
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()

        sql = """
            INSERT INTO statistics (
                team_id, league_id, name, logo, form, total_games, wins, draws, losses,
                goals_for, goals_against, clean_sheets, yellow_cards, red_cards
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                form = VALUES(form),
                total_games = VALUES(total_games),
                wins = VALUES(wins),
                draws = VALUES(draws),
                losses = VALUES(losses),
                goals_for = VALUES(goals_for),
                goals_against = VALUES(goals_against),
                clean_sheets = VALUES(clean_sheets),
                yellow_cards = VALUES(yellow_cards),
                red_cards = VALUES(red_cards);
        """

        values = (
            statistics["team"]["id"],               # team_id
            league_id,                              # league_id
            statistics["team"]["name"],             # name
            statistics["team"]["logo"],             # logo
            statistics["form"],                     # form
            statistics["fixtures"]["played"]["total"],  # total_games
            statistics["fixtures"]["wins"]["total"],    # wins
            statistics["fixtures"]["draws"]["total"],   # draws
            statistics["fixtures"]["loses"]["total"],   # losses
            statistics["goals"]["for"]["total"],        # goals_for
            statistics["goals"]["against"]["total"],    # goals_against
            statistics["clean_sheet"]["total"],         # clean_sheets
            statistics["cards"]["yellow"],              # yellow_cards
            statistics["cards"]["red"]                  # red_cards
        )

        cursor.execute(sql, values)
        db.commit()

        print("Statistics data inserted successfully!")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
