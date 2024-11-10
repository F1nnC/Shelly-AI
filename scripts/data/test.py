import pysurfline

def inspect_wave_timestamp(spot_id):
    spot_forecasts = pysurfline.get_spot_forecasts(
        spotId=spot_id,
        days=2,
        intervalHours=3,
    )

    # Just inspect the first wave for attributes
    wave = spot_forecasts.waves[0]
    print("Wave timestamp type:", type(wave.timestamp))
    print("Wave timestamp:", wave.timestamp)
    print("Wave timestamp attributes:", dir(wave.timestamp))

# Example usage for a specific spot ID
if __name__ == "__main__":
    spot_id = '5842041f4e65fad6a7708cfd'  # Replace with actual spot ID
    inspect_wave_timestamp(spot_id)
