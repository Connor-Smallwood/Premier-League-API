import mysql.connector
from mysql.connector import Error

# Database Configuration
DB_CONFIG = {
    "host": "jw0ch9vofhcajqg7.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
    "user": "or9lfkafm52dnld9",
    "password": "ybq0i39tcg69u170",
    "database": "gq4u8frecn8pgnmq"
}

def connect_to_database():
    """
    Establish a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("Successfully connected to the database.")
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

