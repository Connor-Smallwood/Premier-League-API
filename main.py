from app.db_connect import connect_to_database
from app.services.api_football import fetch_api_data

def main():
    # Fetch API data
    params = {
        'id': 39,
        'name': 'Premier League',
        'country': 'England',
        'season': 2021
    }
    data = fetch_api_data(params)
    if not data:
        return

    # Connect to the database
    connection = connect_to_database()
    if not connection:
        return

    try:
        # Insert data into the database
        cursor = connection.cursor()

        # Update schema with additional fields
        create_table_query = """
        CREATE TABLE IF NOT EXISTS leagues (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            country VARCHAR(255),
            season INT,
            start_date DATE,
            end_date DATE,
            logo VARCHAR(255)
        );
        """
        cursor.execute(create_table_query)

        # Extract relevant data from the API response
        league_info = data['response'][0]['league']
        country = data['response'][0].get('country', {}).get('name', 'Unknown')
        start_date = data['response'][0]['seasons'][0]['start']
        end_date = data['response'][0]['seasons'][0]['end']
        logo = league_info.get('logo', None)

        # Insert or update the data in the database
        query = """
        INSERT INTO leagues (id, name, country, season, start_date, end_date, logo) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            name = VALUES(name),
            country = VALUES(country),
            season = VALUES(season),
            start_date = VALUES(start_date),
            end_date = VALUES(end_date),
            logo = VALUES(logo);
        """
        cursor.execute(query, (
            league_info['id'],
            league_info['name'],
            country,
            params['season'],
            start_date,
            end_date,
            logo
        ))
        connection.commit()
        print(f"Data for league '{league_info['name']}' inserted/updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
