from flask import Blueprint, jsonify, request
from model import SpotForecastData
from datetime import datetime



bp = Blueprint("controllers", __name__)

@bp.route("/api/recent/spot-data", methods=["GET"])
def spot_data():
    spot_id = request.args.get("spot_id")
    if not spot_id:
        return jsonify({"error": "spot_id parameter is required"}), 400

    today = datetime.now().date()
    data = SpotForecastData.query.filter_by(spot_id=spot_id).filter(SpotForecastData.time >= today).all()

    result = [
        {
            "spot_id": entry.spot_id,
            "time": entry.time,
            "surf_min": entry.surf_min,
            "surf_max": entry.surf_max,
            "wave_height": entry.wave_height,
            "wind_speed": entry.wind_speed,
            "wind_direction": entry.wind_direction,
            "surf_optimalScore": entry.surf_optimalScore,
        }
        for entry in data
    ]
    return jsonify(result)
