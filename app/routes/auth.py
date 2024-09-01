from flask import Blueprint, request, jsonify, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from app.models.db import execute_query, insert_user
from app.utils.jwt_helpers import blacklist

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username, email, password = data.get(
        'user'), data.get('email'), data.get("password")
    if not username or not email or not password:
        return jsonify({'message': 'All fields are required!'}), 400
    if insert_user(username, email, password):
        return redirect(url_for('auth.signup_success'))
    else:
        return jsonify({'message': 'Username already exists. Please choose a different one.'}), 409


@auth_bp.route('/signup_success')
def signup_success():
    return "Signup request submitted successfully!"


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON data received!"}), 400
    username, password = data.get('user'), data.get('password')
    if not username or not password:
        return jsonify({"message": "Username and password required!"})
    user = execute_query(
        'SELECT * FROM login WHERE user = %s', (username,), fetch_one=True)
    if not user or password != user['password']:
        return jsonify({"message": "Invalid username or password!"})
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@auth_bp.route('/dashboard', methods=['Get'])
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"message": "Successfully logged out"}), 200
