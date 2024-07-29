from app import db

class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    free_shipping = db.Column(db.Boolean, nullable=False)
