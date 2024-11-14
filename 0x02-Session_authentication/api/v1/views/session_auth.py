#!/usr/bin/env python3
""" Module of Session views
"""
from os import getenv
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ POST  /api/v1/auth_session/login
    Return:
      - 
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({ "error": "email missing" }), 400
    if password is None or password == '':
        return jsonify({ "error": "password missing" }), 400
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({ "error": "no user found for this email" }), 404
    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password" }), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response