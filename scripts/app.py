from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from extensions import db  # Import db from extensions
from controllers import bp as controllers_bp
from data.spotForecast import fetch_all_spots  # Import the function from spotForecast
import os

# Initialize Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates')
)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../volumes/surf_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db and register Blueprints
db.init_app(app)
app.register_blueprint(controllers_bp)

fetch_all_spots()



# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8012")
