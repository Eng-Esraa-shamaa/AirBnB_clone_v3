#!/usr/bin/python3
"""view for users objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves list of all usrs"""
    users = []
    for user in storage.all("User").values():
        user.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/user_id', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves user with specified id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/user_id', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """deletes a user based on specified id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """creates a new user"""
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in req:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in req:
        return jsonify({'error': 'Missing password'}), 400
    user = User(**req)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/user_id', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """updates a user"""
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Not a JSON'}), 400
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    for attr, val in req.items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    user.save()
    return jsonify(user.to_dict())
