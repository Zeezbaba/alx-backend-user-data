#!/usr/bin/env python3
"""A basic Flask app
"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    """simple app
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users() -> str:
    """end-point to register a user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """user login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    resp = make_response(jsonify
                         ({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
