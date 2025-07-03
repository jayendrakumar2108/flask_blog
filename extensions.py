from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail

db = SQLAlchemy()
login_manager = LoginManager()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()  # ✅ Mail instance created

def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)  # ✅ Missing line added

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
