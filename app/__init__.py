from flask import Flask
from config import Config
from .extensions import db, login

def create_app(test_config=Config):
    app = Flask(__name__)
    app.debug = True
    app.config.from_object(test_config)
    db.init_app(app)
    login.init_app(app)
    login.init_app(app)
    login.login_view = 'login'

    with app.app_context():
        from . import routes, models, forms
        db.create_all()
        return app