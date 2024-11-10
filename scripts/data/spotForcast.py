import pysurfline
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from pysurfline.api.models.spots import Time

# Define the base class for SQLAlchemy
Base = declarative_base()

# Define the database model for storing surf forecast data
class SpotForecastData(Base):
    __tablename__ = "spot_forecast"
    
    id = Column(Integer, primary_key=True)
    spot_id = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    surf_min = Column(Float, nullable=True)
    surf_max = Column(Float, nullable=True)
    wave_height = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    wind_direction = Column(Float, nullable=True)
    surf_optimalScore = Column(Float, nullable=True)

# Set up the database engine and session
VOLUME_PATH = 'volumes/surf_data.db'  # Adjust path as needed
DATABASE_URL = f"sqlite:///{VOLUME_PATH}"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Creates the table in the database
Session = sessionmaker(bind=engine)

def fetch_and_store_surf_conditions(spot_id):
    # Start session
    session = Session()

    # Fetch data using pysurfline with updated parameters
    spot_forecasts = pysurfline.get_spot_forecasts(
        spotId=spot_id,
        days=2,
        intervalHours=3,
    )

    # Extract relevant data and store it in the SQLAlchemy database
    for wave, wind in zip(spot_forecasts.waves, spot_forecasts.wind):
        
        # Convert pysurfline Time object to a datetime object
        if isinstance(wave.timestamp, Time):
            timestamp_datetime = wave.timestamp.dt
        else:
            # If it's already a datetime or string, use it directly
            timestamp_datetime = wave.timestamp

        # Ensure time is stored in the correct format for SQL (as a datetime object)
        time = timestamp_datetime

        # Creating and adding the forecast entry to the session
        forecast_entry = SpotForecastData(
            spot_id=spot_id,
            time=time,
            surf_min=wave.surf.min,
            surf_max=wave.surf.max,
            wave_height=(wave.surf.max + wave.surf.min) / 2,  # Average wave height
            wind_speed=wind.speed,
            wind_direction=wind.direction,
            surf_optimalScore=wave.surf.optimalScore
        )
        session.add(forecast_entry)

    # Commit all entries to the database and close session
    session.commit()
    session.close()
    print(f"Forecast data for spot {spot_id} saved to database successfully.")

# Example usage for a specific spot ID
if __name__ == "__main__":
    spot_id = '5842041f4e65fad6a7708cfd'  # Replace with actual spot ID
    fetch_and_store_surf_conditions(spot_id)
