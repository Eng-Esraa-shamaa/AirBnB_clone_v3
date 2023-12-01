#!/usr/bin/python3
"""Create a new view for State objects"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Request, abort, jsonify
from models.state import State


@app_views.route('/states', methods=['GET'])
def all_states():
    """Retrieves all states"""
    states = [state.to_json() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a state by id"""
    state = storage.get("State", state_id)
    if state:
        return jsonify(state.to_json())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id=None):
    """Deletes a state by id"""
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a state"""
    req = Request.get_json()
    if req is None:
        abort(400, 'Not a JSON')
    if req.get("name") is None:
        abort(400, 'Missing name')

    new_state = State(**req)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a state"""
    req = Request.get_json()
    if req is None:
        abort(400, 'Not a JSON')
    state = storage.get("State", state_id)
    if state is None:
        abort(404, "State not found")
    for key, value in req.items():
        if key not in ['id','created_at','updated_at']:
            setattr(state, key, value)

    storage.save()
    return jsonify(state.to_json()), 200

