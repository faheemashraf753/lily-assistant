# app/routes.py
from flask import Blueprint, render_template

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

# Add more routes here if needed
# @main_routes.route('/about')
# def about():
#     return render_template('about.html')