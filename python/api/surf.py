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

def get_surf_conditions_time(time_period):
    try:
        # Get today's date
        today = datetime.now().date()

        # Determine the target time based on the provided time period
        if time_period == "morning":
            target_time = time(8, 0)  # 8:00 AM
        elif time_period == "noon":
            target_time = time(11, 0)  # 11:00 AM
        elif time_period == "afternoon":
            target_time = time(16, 0)  # 4:00 PM
        else:
            raise ValueError("Invalid time_period. Must be 'morning', 'noon', or 'afternoon'.")

        # Query the database for entries at the specified time for today and all spots
        data = SpotForecastData.query.filter(
            SpotForecastData.time >= datetime.combine(today, target_time),
            SpotForecastData.time < datetime.combine(today, target_time.replace(hour=target_time.hour + 1))
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

        return result
    
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return {"error": str(ve)}
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return {"error": "An unexpected error occurred while retrieving surf conditions."}
