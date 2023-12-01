#!/usr/bin/python3
"""
Flask App
"""
from models import storage
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.teardown_appcontext
def tear_down(self):
    """closes the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handles 404 errors"""
    return jsonify({"error": "Not found"}), 404


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
