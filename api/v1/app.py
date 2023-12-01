#!/usr/bin/python3
"""
Flask App
"""
from flask import Flask, Blueprint, render_template, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down():
    """closes the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def error_page():
    """handles 404 errors"""
    return (jsonify({"error": "Not Found"}), 404)


if __name__ == "__main__":
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    else:
        host = '0.0.0.0'
    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    else:
        port = 5000
    app.run(host=host, port=port, threaded=True)
