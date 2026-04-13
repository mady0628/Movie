from flask import Flask
from config import Config
from app.models.db import init_db, close_db
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf.init_app(app)

    # Database lifecycle
    init_db(app)
    app.teardown_appcontext(close_db)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.movie import movie_bp
    from app.routes.comment import comment_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(movie_bp)
    app.register_blueprint(comment_bp)

    return app
