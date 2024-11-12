from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from sqlalchemy.exc import SQLAlchemyError

auth_bp = Blueprint('auth', __name__)

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        # Verify credentials
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Create JWT token
        access_token = create_access_token(identity=user.id)
        response = jsonify({'login': True})
        set_access_cookies(response, access_token)
        return response, 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500

# Protected route
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        return jsonify({'message': f'Hello, {user.username}! This is a protected route.'}), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500