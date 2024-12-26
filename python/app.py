from flask import Flask, render_template
# from apscheduler.schedulers.background import BackgroundScheduler
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
from flask import redirect, url_for, jsonify
from api.auth import auth_bp
from api.surf import bp as surf_bp
from api.shelly import shelly_bp
from api.spot import bp as spot_bp
from extensions import db, jwt
from data.spotForecast import fetch_all_spots  # Import the function from spotForecast
import os

# Initialize Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates')
)

# Configure SQLAlchemy
db_path = os.path.join(os.path.dirname(__file__), '..', 'volumes', 'surf_data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_secret_key')  # Use a strong secret key in production

# Configure JWT
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in production
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Set to True if you want CSRF protection

db.init_app(app)
jwt.init_app(app)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(shelly_bp, url_prefix="/ShellyAI")
app.register_blueprint(spot_bp, url_prefix="/spot")
app.register_blueprint(surf_bp)

with app.app_context():
    db.create_all()  # This will create all tables based on model definitions if they don’t exist
    fetch_all_spots()

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    try:
        verify_jwt_in_request(optional=True)
        if get_jwt_identity():  # Check if the user is already logged in
            return redirect(url_for('account'))
    except:
        pass
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/spots')
@jwt_required()
def spots():
    return render_template('spots.html')

@app.route('/account')
@jwt_required()
def account():
    return render_template('account.html')

@app.route('/about')
def about():
    return render_template('account.html')

@app.route('/chat')
@jwt_required()
def chat():
    return render_template('chat.html')

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return redirect(url_for('login'))

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return redirect(url_for('login'))

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8012")
