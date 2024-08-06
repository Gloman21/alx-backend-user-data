#!/usr/bin/env python3
from os import getenv
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.auth import Auth
from flask_cors import (CORS, cross_origin)
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

if os.environ.get('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
if os.environ.get('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def before_request() -> str:
    """
        This function is a before request hook that is executed before each
        request to the Flask application.

        :return: None
    """
    if auth is None:
        return
    forbidden_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/', '/api/v1/forbidden/'
    ]
    if auth.require_auth(request.path, forbidden_paths) is False:
        return
    if auth.authorization_header(request) is None:
        abort(401)
    if auth.current_user(request) is None:
        abort(403)

@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403



@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)

