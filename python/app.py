from flask import Flask, render_template
# from apscheduler.schedulers.background import BackgroundScheduler
from python.api.auth import auth_bp
from python.api.surf import bp as surf_bp
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
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
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Use a strong secret key

# Initialize db and register Blueprints

db = SQLAlchemy()
jwt = JWTManager()

db.init_app(app)
jwt.init_app(app)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(surf_bp)

@app.before_request
def initialize_database():
    db.create_all()  # This will create all tables based on model definitions if they don’t exist

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
