from flask import Flask
from .extensions import db, bcrypt
from flask_migrate import Migrate
from .models import User
from .routes import bp as routes_bp

migrate = Migrate()  # Initialize Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this in production

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)  # Initialize Migrate with app and db

    # Register blueprints
    app.register_blueprint(routes_bp)

    # Create tables and seed initial data
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('changeme')
            db.session.add(admin)
            db.session.commit()

    return app
