import pandas as pd
import os

# Dictionary for spot ID to spot name mapping
spot_id_to_name = {
    "5842041f4e65fad6a77088cc": "La Jolla Shores",
    "5842041f4e65fad6a7708841": "PB",
    "5842041f4e65fad6a77088af": "Del Mar",
    "5842041f4e65fad6a77088c4": "Tourmaline",
    "5842041f4e65fad6a770883b": "Blacks",
    "5842041f4e65fad6a770883d": "Horseshoe",
    "5842041f4e65fad6a770883c": "Windansea"
}

def data_processing():
    # Load data from CSV
    data = pd.read_csv('volumes/san-diego.csv')

    # Handle missing values
    data.replace(-99.9, pd.NA, inplace=True)

    # Map spot_id to spot_name using the dictionary
    data['spot_name'] = data['spot_id'].map(spot_id_to_name)

    # Drop the original 'spot_id' column as it's no longer needed
    data.drop(columns=['spot_id'], inplace=True)

    # Calculate a simple surf quality score based on relevant columns
    data['surf_quality'] = (
        (data['surf_optimalScore'].fillna(0) + data['surf_max'].fillna(0)) / 2
    )

    # Apply surf quality classification
    data['surf_rating'] = data['surf_quality'].apply(classify_surf_quality)

    # Save the preprocessed data to a new CSV file
    processed_file = os.path.join('volumes/', 'processed_san_diego_forecast.csv')
    data.to_csv(processed_file, index=False)  # Save to data directory

    print("Data preprocessing complete. Saved as 'processed_san_diego_forecast.csv'.")

def classify_surf_quality(score):
    if score <= 2:
        return 'Poor'
    elif score <= 4:
        return 'Fair'
    elif score <= 6:
        return 'Good'
    elif score <= 8:
        return 'Very Good'
    else:
        return 'Excellent'
