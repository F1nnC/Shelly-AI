from flask import Flask, render_template
from extensions import db  # Import db from extensions
from controllers import bp as controllers_bp
import os

app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'),
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates')
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../volumes/surf_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize db here

app.register_blueprint(controllers_bp)  # Register the Blueprint

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8012")
