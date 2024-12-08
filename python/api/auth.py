from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from sqlalchemy.exc import SQLAlchemyError
import logging
from sqlalchemy.orm.attributes import flag_modified

# Assuming you have a Spot model and a User model with a relationship to spots


auth_bp = Blueprint('auth', __name__)

# Register route
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        favorite_spots = []

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        # Create new user
        new_user = User(username=username, email=email, favorite_spots=favorite_spots)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 501
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
        return jsonify({'error': 'Database error', 'message': str(e)}), 501
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

@auth_bp.route('/add_spot', methods=['POST'])
@jwt_required()
def add_spot():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        name = data.get('name')
        spot_id = data.get('spot_id')
        
        print(data)
        
        if not name or not spot_id:
            return jsonify({'error': 'Name and spot_id are required'}), 400

        if user.favorite_spots is None or user.favorite_spots == []:
            user.favorite_spots = []

        # Add spot and reassign to trigger SQLAlchemy's tracking
        user.add_spot({"name": name, "spot_id": spot_id})
        user.favorite_spots = user.favorite_spots  # Reassign explicitly

        print("Before commit:", user.favorite_spots)
        flag_modified(user, "favorite_spots")
        db.session.commit()
        print("After commit:", user.favorite_spots)
        
        return jsonify({'message': 'Favorite spots updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500

@auth_bp.route('/remove_spot', methods=['DELETE'])
@jwt_required()
def remove_spot():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        spot_id = data.get('spot_id')
        
        if not spot_id:
            return jsonify({'error': 'Spot ID is required'}), 400

        if user.favorite_spots is None or user.favorite_spots == []:
            return jsonify({'error': 'No favorite spots to remove'}), 400

        # Remove spot and reassign to trigger SQLAlchemy's tracking
        if not user.remove_spot(spot_id):
            return jsonify({'error': 'Spot not found in favorites'}), 400

        user.favorite_spots = user.favorite_spots  # Reassign explicitly
        flag_modified(user, "favorite_spots")
        db.session.commit()
        
        return jsonify({'message': 'Favorite spots updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'logout': True})
    response.set_cookie('access_token_cookie', '', expires=0)
    return response, 200

@auth_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.return_dict()), 200
    except SQLAlchemyError as e:
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500

@auth_bp.route('/delete_user', methods=['DELETE'])
@jwt_required()
def delete_self():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Database error', 'message': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occurred', 'message': str(e)}), 500 