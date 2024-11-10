# surf_data_fetcher.py
import pysurfline
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from model import SpotForecastData

# Your existing code here


# Set up the database engine and session (reuse your previous code for this part)
DATABASE_URL = "sqlite:///volumes/surf_data.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def fetch_and_store_surf_conditions(spot_id):
    """Fetch and store surf conditions for a given spot_id."""
    # Start session
    session = Session()

    # Fetch data using pysurfline with updated parameters
    spot_forecasts = pysurfline.get_spot_forecasts(
        spotId=spot_id,
        days=2,
        intervalHours=3,
    )

    # Check if the latest forecast data is less than 24 hours old
    latest_entry = session.query(SpotForecastData).filter_by(spot_id=spot_id).order_by(SpotForecastData.time.desc()).first()

    if latest_entry:
        # Calculate the time difference between now and the latest data
        time_difference = datetime.now() - latest_entry.time
        if time_difference < timedelta(hours=24):
            print(f"Data for {spot_id} is up-to-date.")
            session.close()
            return  # Skip fetching new data if it's less than 24 hours old

    # Extract relevant data and store it in the SQLAlchemy database
    for wave, wind in zip(spot_forecasts.waves, spot_forecasts.wind):
        
        # Convert pysurfline Time object to a datetime object
        if isinstance(wave.timestamp, pysurfline.api.models.spots.Time):
            timestamp_datetime = wave.timestamp.dt
        else:
            timestamp_datetime = wave.timestamp

        # Ensure time is stored in the correct format for SQL (as a datetime object)
        time = timestamp_datetime

        # Check if we already have the data for this time for the current spot
        existing_data = session.query(SpotForecastData).filter_by(spot_id=spot_id, time=time).first()
        if existing_data:
            # If data already exists for this time, replace it with new data
            existing_data.surf_min = wave.surf.min
            existing_data.surf_max = wave.surf.max
            existing_data.wave_height = (wave.surf.max + wave.surf.min) / 2
            existing_data.wind_speed = wind.speed
            existing_data.wind_direction = wind.direction
            existing_data.surf_optimalScore = wave.surf.optimalScore
        else:
            # Otherwise, add new data
            forecast_entry = SpotForecastData(
                spot_id=spot_id,
                time=time,
                surf_min=wave.surf.min,
                surf_max=wave.surf.max,
                wave_height=(wave.surf.max + wave.surf.min) / 2,
                wind_speed=wind.speed,
                wind_direction=wind.direction,
                surf_optimalScore=wave.surf.optimalScore
            )
            session.add(forecast_entry)

    # Commit all entries to the database and close session
    session.commit()
    session.close()
    print(f"Forecast data for spot {spot_id} saved to database successfully.")

