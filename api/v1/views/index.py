#!/usr/bin/python3
"""Flask Route that returns json represnation of status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', methods=['GET'])
def status():
    """function that returns json represnation of status"""
    return (jsonify({'status': 'OK'}))


@app_views.route('/stats', methods=['GET'])
def stats():
    """retrieves number of each object by type"""
    objs = {
        'states': State, 'users': User,
        'amenities': Amenity, 'cities': City,
        'places': Place, 'reviews': Review
    }
    for key in objs:
        objs[key] = storage.count(objs[key])
    return jsonify(objs)
