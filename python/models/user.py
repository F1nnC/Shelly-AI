from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    favorite_spots = db.Column(db.JSON, nullable=True)  
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def add_spot(self, spot):
        if self.favorite_spots is None:
            self.favorite_spots = []
        self.favorite_spots.append(spot)
        # Re-assign the updated list back to the column
        self.favorite_spots = self.favorite_spots

    
    def remove_spot(self, spot_id):
        for spot in self.favorite_spots:
            if spot['spot_id'] == spot_id:
                self.favorite_spots.remove(spot)
                return True
        return False
    
    
    def return_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'favorite_spots': self.favorite_spots
        }