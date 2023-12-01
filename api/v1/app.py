#!/usr/bin/python3
"""
Flask App
"""
from flask import Flask, Blueprint, render_template, jsonify
from models import storage
from api.v1.views import app_views
import os


host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down():
    """closes the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def error_page():
    """handles 404 errors"""
    return (jsonify({"error": "Not Found"}))


if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
