import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'birdy.sqlite')
    )
    app.config.update(
    	DEBUG = True,
    	MAIL_SERVER = 'smtp.gmail.com',
    	MAIL_PORT = 465,
    	MAIL_USE_SSL = True,
    	MAIL_USERNAME = 'frankyrocksallday@gmail.com',
    	MAIL_PASSWORD = 'frankisthe5513man'
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
