#!/usr/bin/python3
"""Flask Route that returns json represnation of status"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def status():
    """function that returns json represnation of status"""
    return (jsonify({'status': 'OK'}))