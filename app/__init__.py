# app/__init__.py
from flask import Flask
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Set a secret key (IMPORTANT for sessions, forms, etc.)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Import and register routes
    from app import routes
    app.register_blueprint(routes.main_routes)
    
    return app