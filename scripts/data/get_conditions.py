import pysurfline
from datetime import datetime, timedelta
import pandas as pd
from scripts.data.data_processing import data_processing

# Load your CSV data into a DataFrame
def check_last_update():
    try:
        # Try to read the CSV file
        data = pd.read_csv('volumes/san-diego.csv')

        # Convert the 'timestamp_dt' column to datetime if it's not already
        data['timestamp_dt'] = pd.to_datetime(data['timestamp_dt'])

        # Get the most recent timestamp
        latest_timestamp = data['timestamp_dt'].max()

        # Get the current time
        current_time = datetime.now()

        # Calculate the difference in days
        time_difference = current_time - latest_timestamp

        # Check if it’s been two days or more
        if time_difference >= timedelta(days=2):
            get_conditions()
            data_processing()
            print("get_conditions() has been run.")
        else:
            print("It's not been two days yet since the last update.")
    except FileNotFoundError:
        print("CSV file not found. Running get_conditions() to create it.")
        get_conditions()
        data_processing()
    except pd.errors.EmptyDataError:
        print("CSV file is empty. Running get_conditions() to populate it.")
        get_conditions()
        data_processing()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def get_conditions():
    so_cal_spot_ids = [
        "5842041f4e65fad6a77088cc", # La Jolla shores
        "5842041f4e65fad6a7708841", # PB
        "5842041f4e65fad6a77088af", # Del Mar
        "5842041f4e65fad6a77088c4", # Tourmaline
        "5842041f4e65fad6a770883b", # Blacks
        "5842041f4e65fad6a770883d", # Horseshoe
        "5842041f4e65fad6a770883c" # Windansea
    ]

    # Initialize an empty list to store data
    data_frames = []

    # Loop through each spot ID to fetch and store its forecast data
    for spot_id in so_cal_spot_ids:
        try:
            # Fetch the forecast data for the current spot
            spot_forecasts = pysurfline.get_spot_forecasts(
                spot_id,
                days=2,
                intervalHours=3,
            )
            
            # Get the data as a DataFrame and add an extra column for the spot ID
            df = spot_forecasts.get_dataframe()
            df['spot_id'] = spot_id  # Track which spot the data is from
            
            # Append to the list of DataFrames
            data_frames.append(df)
        
        except Exception as e:
            print(f"Failed to retrieve data for spot ID {spot_id}: {e}")

    # Concatenate all DataFrames into a single DataFrame
    all_data = pd.concat(data_frames, ignore_index=True)

    # Save to CSV
    all_data.to_csv("volumes/san-diego.csv", index=False)

    print("Data collection complete. CSV saved as 'san-diego.csv'.")
