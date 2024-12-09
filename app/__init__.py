from flask import Flask
from app.db_connect import connect_to_database
from app.blueprints.players import players_bp

# Create the Flask app
app = Flask(__name__)

# Set the secret key (replace with a strong secret key in production)
app.secret_key = 'your_secret_key'

# Register Blueprints
app.register_blueprint(players_bp, url_prefix='/players')



# Import routes
from app import routes

