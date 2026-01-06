from flask import Flask
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Import and register routes
    from app import routes
    app.register_blueprint(routes.main_routes)
    
    return app