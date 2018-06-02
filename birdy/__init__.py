import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    app.db = db

    app.config.update(
    	DEBUG = True,
    	MAIL_SERVER = 'smtp.gmail.com',
    	MAIL_PORT = 465,
    	MAIL_USE_SSL = True,
    	MAIL_USERNAME = env_variables()['gmail_username'],
    	MAIL_PASSWORD = env_variables()['gmail_password']
	)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from birdy.controllers import auth
    app.register_blueprint(auth.bp)

    from birdy.controllers import dashboard
    app.register_blueprint(dashboard.bp)
    app.add_url_rule('/', endpoint='index')

    from birdy.controllers import favorites
    app.register_blueprint(favorites.bp)
    app.add_url_rule('/favorites/<int:id>/delete', endpoint='favorites.delete', methods=['POST',])

    from birdy.controllers import favorites_endpoints
    app.register_blueprint(favorites_endpoints.bp)

    from birdy.controllers import bird_search
    app.register_blueprint(bird_search.bp)

    return app

def env_variables():
    APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
    dotenv_path = os.path.join(APP_ROOT, '.env')
    load_dotenv(dotenv_path)
    ebird_api_key = os.getenv('EBIRD_API_KEY')
    gmail_username = os.getenv('MAIL_USERNAME')
    gmail_password = os.getenv('MAIL_PASSWORD')
    return {'ebird_api_key': ebird_api_key,
            'gmail_username': gmail_username,
            'gmail_password': gmail_password}
