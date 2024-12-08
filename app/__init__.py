from flask import Flask
from app.db_connect import get_db

# Initialize the Flask app
app = Flask(__name__)

# Set the secret key (replace with a strong secret key in production)
app.secret_key = 'your_secret_key'

# Register Blueprints
from app.blueprints.leagues import leagues_bp


# Import routes
from app import routes

