# spotForcast.py
from data.surf_data_fetcher import fetch_and_store_surf_conditions  # Import the new method
from models.spot_forecast import SpotForecastData
from data.surf_data_fetcher import fetch_and_store_surf_conditions
from models.spot import Spot



def fetch_all_spots():
    spot_ids = Spot().get_all_spot_ids()
    for spot_id in spot_ids:
        fetch_and_store_surf_conditions(spot_id)