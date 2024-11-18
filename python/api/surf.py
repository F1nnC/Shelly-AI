from flask import Blueprint, jsonify, request
from models.spot_forecast import SpotForecastData
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, set_access_cookies
from datetime import datetime, time



bp = Blueprint("surf-data", __name__)

@bp.route("/api/recent/spot-data", methods=["GET"])
@jwt_required()
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


@bp.route("/api/recent/spot-data-time", methods=["GET"])
@jwt_required()
def spot_data_time():
    spot_id = request.args.get("spot_id")
    time_period = request.args.get("time_period")

    # Validate the input parameters
    if not spot_id:
        return jsonify({"error": "spot_id parameter is required"}), 400

    if time_period not in ["morning", "noon", "afternoon"]:
        return jsonify({"error": "Invalid time_period. Must be 'morning', 'noon', or 'afternoon'."}), 400

    # Get today's date
    today = datetime.now().date()

    # Determine the target time range based on the provided time_period
    if time_period == "morning":
        start_time = time(8, 0)  # 8:00 AM
    elif time_period == "noon":
        start_time = time(11, 0)  # 11:00 AM
    elif time_period == "afternoon":
        start_time = time(16, 0)  # 4:00 PM

    # Define the end time as one hour later
    end_time = start_time.replace(hour=start_time.hour + 1)

    # Query the database for entries at the specified time for today and the given spot_id
    data = SpotForecastData.query.filter(
        SpotForecastData.spot_id == spot_id,
        SpotForecastData.time >= datetime.combine(today, start_time),
        SpotForecastData.time < datetime.combine(today, end_time)
    ).all()

    # Format the results
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
