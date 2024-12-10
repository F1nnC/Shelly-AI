# surf_data_fetcher.py
import pysurfline
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import create_engine
from models.spot_forecast import SpotForecastData
import os
from flask import jsonify

DATABASE_URL = "sqlite:///volumes/surf_data.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def fetch_and_store_surf_conditions(spot_id):
    session = Session()
    today = datetime.now().date()
    latest_entry = session.query(SpotForecastData).filter_by(spot_id=spot_id).order_by(SpotForecastData.time.desc()).first()
    
    try: 
        if latest_entry and latest_entry.time.date() >= today:
            print(f"Data for {spot_id} is up-to-date.")
            session.close()
            return

        spot_forecasts = pysurfline.get_spot_forecasts(
            spotId=spot_id,
            days=2,
            intervalHours=3,
        )

        for wave, wind in zip(spot_forecasts.waves, spot_forecasts.wind):
            timestamp = wave.timestamp.dt if isinstance(wave.timestamp, pysurfline.api.models.spots.Time) else wave.timestamp
            if latest_entry and timestamp <= latest_entry.time:
                continue

            forecast_entry = SpotForecastData(
                spot_id=spot_id,
                time=timestamp,
                surf_min=wave.surf.min,
                surf_max=wave.surf.max,
                wave_height=(wave.surf.max + wave.surf.min) / 2,
                wind_speed=wind.speed,
                wind_direction=wind.direction,
                surf_optimalScore=wave.surf.optimalScore
            )
            forecast_entry.spot_name_set()
            session.add(forecast_entry)
    except Exception as e:
        ## Print Error
        print(e)
        print(f"Failed to fetch forecast data for spot {spot_id}.")
        session.close()
        return

    session.commit()
    session.close()
    print(f"Forecast data for spot {spot_id} updated successfully.")

def spot_data_shelly(spot_id):
    if not spot_id:
        return jsonify({"error": "spot_id parameter is required"}), 400

    today = datetime.now().date()
    data = SpotForecastData.query.filter_by(spot_id=spot_id).filter(SpotForecastData.time >= today).all()

    result = [
        {
            "spot_name": entry.spot_name,
            "time": entry.time,
            "wave_height": entry.wave_height,
            "wind_direction": entry.wind_direction,
            "surf_optimalScore": entry.surf_optimalScore,
        }
        for entry in data
    ]
    return jsonify(result)