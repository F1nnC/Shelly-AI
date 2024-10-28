import pandas as pd
import os

# Get the directory of the current script
def data_processing():
    
    data = pd.read_csv('volumes/san-diego.csv')

    # Handle missing values
    data.replace(-99.9, pd.NA, inplace=True)

    # Example: Calculate a simple surf quality score based on relevant columns
    data['surf_quality'] = (
        (data['surf_optimalScore'].fillna(0) + data['surf_max'].fillna(0)) / 2
    )

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