#!/usr/bin/env python3
"""
Module Create a Flask app that has a single GET route ("/")
and use flask.jsonify to return a JSON payload of the form
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def home():
    """return a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def create_user():
    """Create user from post route"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'])
def login():
    """
    implement a login function to respond
    to the POST /sessions route.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email=email, password=password):
        abort(401)
    session_id = AUTH.create_session(email=email)
    response = make_response(jsonify({
        "email": "<user email>", "message": "logged in"
    }))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=['DELETE'])
def logout():
    """
    implement logout function
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        return abort(403)


@app.route("/profile", methods=['GET'])
def profile():
    """
    The request is expected to contain a session_id cookie.
    Use it to find the user. If the user exist,
    respond with a 200 HTTP status and the following JSON payload
    If the session ID is invalid or the user does not exist,
    respond with a 403 HTTP status.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if user:
        response = make_response(jsonify(
            {"email": user.email}
        ))
        return response, 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    The request is expected to contain form data with the "email" field.

    If the email is not registered, respond with a 403 status code.
    Otherwise, generate a token and respond with a 200 HTTP status
    and the following JSON payload
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email=email)
        return make_response(jsonify(
            {"email": email, "reset_token": reset_token}
        )), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
