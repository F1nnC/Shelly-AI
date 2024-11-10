# spotForcast.py
from data.surf_data_fetcher import fetch_and_store_surf_conditions  # Import the new method
from model import SpotForecastData

# List of Southern California spots with their spot IDs
spot_ids = [
    '5842041f4e65fad6a77088af',  # Del Mar
    '5842041f4e65fad6a7708841',  # Pacific Beach
    '5842041f4e65fad6a77088cc',  # Blacks Beach
    '5842041f4e65fad6a77088c4',  # Tourmaline
    '5842041f4e65fad6a77088cc',  # La Jolla Shores
    '5842041f4e65fad6a770883d',  # Horseshoe
    '5842041f4e65fad6a770883c',  # Windansea
]

# if __name__ == "__main__":
#     for spot_id in spot_ids:
#         fetch_and_store_surf_conditions(spot_id)  # Call the method from the new file
def fetch_all_spots():
    for spot_id in spot_ids:
        fetch_and_store_surf_conditions(spot_id)  # Call the method from the new file