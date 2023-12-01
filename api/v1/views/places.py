#!/usr/bin/python3
"""view for Places objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """retrieves all cities with the same city id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """retrieves place with its id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place based with its id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create a new place"""
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Not a JSON'}), 400
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if 'user_id' not in req:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get("User", req['user_id'])
    if user is None:
        abort(404)
    if 'name' not in req:
        return jsonify({'error': 'Missing name'}), 400
    req['city_id'] = city_id
    place = Place(**req)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update a place"""
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Not a JSON'}), 400

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    for attr, val in req.items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    place.save()
    return jsonify(place.to_dict())
