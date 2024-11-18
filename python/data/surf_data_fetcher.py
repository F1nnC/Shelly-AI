# surf_data_fetcher.py
import pysurfline
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from models.spot_forecast import SpotForecastData
import os

# Your existing code here


# Set up the database engine and session (reuse your previous code for this part)
DATABASE_URL = "sqlite:///volumes/surf_data.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

from datetime import datetime, timedelta, time

def fetch_and_store_surf_conditions(spot_id):
    session = Session()
    today = datetime.now().date()

    # Find the most recent forecast time in the database for this spot
    latest_entry = session.query(SpotForecastData).filter_by(spot_id=spot_id).order_by(SpotForecastData.time.desc()).first()
    
    if latest_entry and latest_entry.time.date() >= today:
        print(f"Data for {spot_id} is up-to-date.")
        session.close()
        return  # No need to fetch if data is up-to-date

    # Fetch data using pysurfline, using the adjusted range if needed
    spot_forecasts = pysurfline.get_spot_forecasts(
        spotId=spot_id,
        days=2,  # Adjust the number of days as needed
        intervalHours=3,
    )

    # Extract and store new data only
    for wave, wind in zip(spot_forecasts.waves, spot_forecasts.wind):
        timestamp = wave.timestamp.dt if isinstance(wave.timestamp, pysurfline.api.models.spots.Time) else wave.timestamp

        # Skip if the timestamp is older than the latest entry's timestamp
        if latest_entry and timestamp <= latest_entry.time:
            continue

        # Add or update new data
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

    session.commit()
    session.close()
    print(f"Forecast data for spot {spot_id} updated successfully.")


# Had to take methods from surf.py and put them here to make the shelly_bp work cause I didn't want to fetch the results from another endpoint
def spot_data_time(spot_id, time_period):
    # Validate the input parameters
    if not spot_id:
        return {"error": "spot_id parameter is required"}

    if time_period not in ["morning", "noon", "afternoon"]:
        return {"error": "Invalid time_period. Must be 'morning', 'noon', or 'afternoon'."}

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

    # Format the results as a list of dictionaries
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

    return result  # Return raw list of dictionaries


def get_shelly_spots(spots, time_period):
    spot_data = []
    for spot_id in spots:
        data = spot_data_time(spot_id, time_period)
        if isinstance(data, dict) and "error" in data:  # Handle potential errors from spot_data_time
            return data  # Return the error response if there's an issue
        spot_data.extend(data)  # Use .extend() to flatten the list of lists
    return spot_data  # Return the full, flattened list of data