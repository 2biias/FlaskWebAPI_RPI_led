from app import db

class LED(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gpionumber = db.Column(db.Integer, unique=True, nullable=False)
    state = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<LED {}>'.format(self.id)

# Create tables from models
db.create_all()