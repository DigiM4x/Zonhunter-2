from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import main

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        from app import models
        db.create_all()

    return app
