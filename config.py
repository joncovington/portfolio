import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Set Flask configuration vars from .env file."""
    SECRET_KEY = os.getenv('SECRET_KEY')

    # configuration of mail
    MAIL_SERVER = os.getenv('SMTP_SERVER')
    MAIL_PORT = os.getenv('SMTP_PORT')
    MAIL_USERNAME = os.getenv('SMTP_USERNAME')
    MAIL_PASSWORD = os.getenv('SMTP_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True