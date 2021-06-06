import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_recaptcha import ReCaptcha

db = SQLAlchemy()
csrf = CSRFProtect() # instantiate CSRF protection
recaptcha = ReCaptcha()
mail = Mail()

def create_app():
    """Construct the core application."""
    app = Flask( __name__ , instance_relative_config=False)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///./sqlite3.db'
    db.init_app(app)
    app.config.from_object('config.Config')
    csrf.init_app(app)
    recaptcha.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Imports
        from . import routes

        # Initialize Global db
        db.create_all()

        return app