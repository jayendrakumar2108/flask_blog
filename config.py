import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:hemanth@localhost/flask_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    WTF_CSRF_ENABLED = True

    # ✅ Email Config for Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bunnyyadav1005@gmail.com'         # <--- Replace with your email
    MAIL_PASSWORD = 'gkkh rctq udsj cnlk'            # <--- Replace with Gmail App Password
    MAIL_DEFAULT_SENDER = ('BlogiVerse', 'bunnyyadav1005@gmail.com')
