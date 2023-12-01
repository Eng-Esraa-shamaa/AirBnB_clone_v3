#!/usr/bin/python3
"""view for review objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """reviews of place by its id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get review based on its id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """deletes a review based with its id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a new review"""
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Not a JSON'}), 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if 'user_id' not in req:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get("User", req['user_id'])
    if user is None:
        abort(404)
    if 'text' not in req:
        return jsonify({'error': 'Missing text'}), 400
    req['place_id'] = place_id
    review = Review(**req)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """update a review"""
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Not a JSON'}), 400
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    for key, value in req.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict())
