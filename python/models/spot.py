from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import JSON


class Spot(db.Model):
    __tablename__ = 'spot_id'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    spot_id = db.Column(db.String(120), unique=True, nullable=False)

    def get_all_spot_names(self):
        spots_name = [];
        for spot in Spot.query.all():
            print(spot.name)
            spots_name.append(spot.name)
        return spots_name
    
    def add_spot(self, name, spot_id):
        spot = Spot(name=name, spot_id=spot_id)
        db.session.add(spot)
        db.session.commit()
        return spot
    
    def get_all_spots(self):
        spots = Spot.query.all()
        return spots
    
    def get_all_spot_ids(self):
        return [spot.spot_id for spot in Spot.query.all()]
    
    def get_spot_id_name_dict(self):
        return {spot.spot_id: spot.name for spot in Spot.query.all()}