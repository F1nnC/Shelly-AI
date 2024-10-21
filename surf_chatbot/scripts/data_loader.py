import pandas as pd
import numpy as np

def load_data(file_path):
    """
    Load surf condition data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the surf condition data.
    """
    try:
        data = pd.read_csv(file_path)
        print(f"Data loaded successfully with shape: {data.shape}")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def preprocess_data(data):
    """
    Preprocess the surf condition data:
    - Handle missing values
    - Normalize numerical columns (e.g., wave height, wind speed)
    
    Args:
        data (pd.DataFrame): The raw surf condition data.

    Returns:
        pd.DataFrame: Preprocessed data.
    """
    # Drop rows with missing values (optional, based on your data)
    data = data.dropna()

    # Normalize numerical features (wave height, wind speed, etc.)
    numerical_cols = ['wave_height', 'wind_speed', 'tide_height']  # Example columns
    data[numerical_cols] = (data[numerical_cols] - data[numerical_cols].mean()) / data[numerical_cols].std()

    print("Data preprocessing complete.")
    return data

# For testing
if __name__ == "__main__":
    # Load and preprocess data
    file_path = "../data/surf_conditions.csv"
    raw_data = load_data(file_path)
    
    if raw_data is not None:
        processed_data = preprocess_data(raw_data)
        print(processed_data.head())
