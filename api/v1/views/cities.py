#!/usr/bin/python3
"""view for City objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """retrieves all cities with the same state id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """retrieves city with its id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete city its id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """creates a city"""
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in req:
        return jsonify({'error': 'Missing name'}), 400
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    req['state_id'] = state_id
    city = City(**req)
    city.save()
    return (jsonify(city.to_dict()), 201)


@app_views.route('/states/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """updates a city"""
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    for key, value in req.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return (jsonify(city.to_dict()), 201)
