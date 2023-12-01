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
def delete_state(state_id):
    """Deletes a state by id"""
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a state"""
    req = Request.get_json()
    if not req:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in req:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**req)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404, "State not found")

    req = Request.get_json()
    if not req:
        abort(400, 'Not a JSON')

    for key, value in req.items():
        setattr(state, key, value)

    storage.save()
    return jsonify(state.to_json()), 200



@app_views.route('/states', methods=['POST'])
def create_state():
    """creates a state"""
    req = Request.get_json()
    if not req:
        return "Not a Json", 400
    if 'name' not in req:
        return "Missing name", 400
    states = []
    new = State(name=req)
    storage.new(new)
    storage.save()
    states.append(new.to_dict())
    return jsonify(states[0]), 201
    

@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """updates a state"""
    state = storage.get("Sate", state_id)
    if not state:
        abort(404, "State not found")
    req = Request.get_json()
    if req:
        abort(400, 'Not a JSON')
    for key, value in req.items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
