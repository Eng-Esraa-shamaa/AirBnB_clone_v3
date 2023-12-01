#!/usr/bin/python3
"""Flask Route that returns json represnation of status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """function that returns json represnation of status"""
    return (jsonify({'status': 'OK'}))

@app_views.route('/stats', methods=['GET'])
def stats():
    """retrieves number of each object by type"""
    res = {}
    objs = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"       
    }
    for key, value in objs.items():
        res[value] = storage.count(key)
    return (jsonify(res))