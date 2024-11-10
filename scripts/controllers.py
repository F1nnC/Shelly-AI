from flask import Blueprint, jsonify, request
from model import SpotForecastData

bp = Blueprint("controllers", __name__)

@bp.route("/api/spot-data", methods=["GET"])
def spot_data():
    spot_id = request.args.get("spot_id")
    if spot_id:
        data = SpotForecastData.query.filter_by(spot_id=spot_id).all()
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
    else:
        return jsonify({"error": "spot_id parameter is required"}), 400
