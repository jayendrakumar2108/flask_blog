from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import Config
from extensions import init_extensions, db, login_manager, jwt
from error_handlers import register_error_handlers
from routes.auth_routes import auth_bp
from routes.post_routes import posts_bp
from resources.post_resource import register_api
from models import User, Post


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    init_extensions(app)

    # Register error handlers
    register_error_handlers(app)

    # JWT user identity mapping
    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        return user_id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    # Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)

    # Register API resources
    register_api(app)

    # Main routes
    @app.route('/')
    def index():
        posts = Post.query.filter_by(status='published').order_by(Post.created_at.desc()).limit(5).all()
        return render_template('index.html', posts=posts)

    @app.route('/dashboard')
    @login_required
    def dashboard():
        user_posts = current_user.posts.order_by(Post.created_at.desc()).all()
        return render_template('dashboard.html', posts=user_posts)

    # Create tables and default admin
    with app.app_context():
        db.create_all()

        # Create admin user if not exists
        if not User.query.filter_by(email='admin@blog.com').first():
            admin = User(
                username='admin',
                email='admin@blog.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)