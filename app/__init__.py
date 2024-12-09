from flask import Flask
from app.db_connect import connect_to_database

# Create the Flask app
app = Flask(__name__)

# Set the secret key (replace with a strong secret key in production)
app.secret_key = 'your_secret_key'

# Register Blueprints




# Import routes
from app import routes

