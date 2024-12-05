from flask import Blueprint, jsonify, request
from models.spot import Spot
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from datetime import datetime, time

bp = Blueprint("spot", __name__)


@bp.route("/add_spot", methods=["POST"])
@jwt_required()
def add_spot():
    data = request.get_json()
    name = data.get("name")
    spot_id = data.get("spot_id")

    if not name or not spot_id:
        return jsonify({"msg": "Name and spot_id are required"}), 400

    spot = Spot(name=name, spot_id=spot_id)
    spot.add_spot(name, spot_id)

    return jsonify({"msg": "Spot added successfully"}), 200

@bp.route("/get_all_spots", methods=["GET"])
@jwt_required()
def get_all_spots():
    spot = Spot()
    spots = spot.get_all_spots()

    return jsonify(spots), 200

@bp.route("/get_all_spot_names", methods=["GET"])
@jwt_required()
def get_all_spot_names():
    spot = Spot()
    spots_name = spot.get_all_spot_names()

    return jsonify(spots_name), 200