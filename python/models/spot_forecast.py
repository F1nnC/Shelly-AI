from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class SpotForecastData(db.Model):  # Use db.Model to enable Flask-SQLAlchemy features
    __tablename__ = "spot_forecast"

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.String, nullable=False)
    spot_name = db.Column(db.String, nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    surf_min = db.Column(db.Float, nullable=True)
    surf_max = db.Column(db.Float, nullable=True)
    wave_height = db.Column(db.Float, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)
    wind_direction = db.Column(db.Float, nullable=True)
    surf_optimalScore = db.Column(db.Float, nullable=True)

    def spot_name_set(self):
        spot_data = {
            "5842041f4e65fad6a77088af": "Del Mar",
            "5842041f4e65fad6a7708841": "Pacific Beach",
            "5842041f4e65fad6a77088cc": "La Jolla Shores",  
            "5842041f4e65fad6a77088c4": "Tourmaline",
            "5842041f4e65fad6a770883d": "Horseshoe",
            "5842041f4e65fad6a770883c": "Windansea"
        }
        self.spot_name = spot_data.get(self.spot_id)
        return self.spot_name