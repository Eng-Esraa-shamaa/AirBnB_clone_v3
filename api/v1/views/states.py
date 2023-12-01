#!/usr/bin/python3
"""Create a new view for Sate objects"""
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import Flask, Request, abort
from models.state import State


@app_views.route('/states', methods=['GET'])
def all_states():
    """retrieves all states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_json())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """retrieves a state by id"""
    state = storage.get("State", state_id)
    if state:
        return jsonify(state)
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a state by id"""
    state = storage.get("State", state_id)
    if state:
        storage.delete(state)
        return jsonify({}), 200
    else:
        abort(404)


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
