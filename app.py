from flask import Flask, render_template
import pandas as pd
from scripts.main import main

app = Flask(__name__)

# Load the CSV data from the data folder


@app.route('/')
def index():
    # Display initial data or summary
    main()
    path = "volumes"
    data = pd.read_csv(f"{path}/processed_san_diego_forecast.csv")
    return render_template('index.html', data=data.head().to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8012")
