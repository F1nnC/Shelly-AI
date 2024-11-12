# surf_data_fetcher.py
import pysurfline
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from models.spot_forecast import SpotForecastData

# Your existing code here


# Set up the database engine and session (reuse your previous code for this part)
DATABASE_URL = "sqlite:///volumes/surf_data.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

from datetime import datetime, timedelta

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
        session.add(forecast_entry)

    session.commit()
    session.close()
    print(f"Forecast data for spot {spot_id} updated successfully.")

