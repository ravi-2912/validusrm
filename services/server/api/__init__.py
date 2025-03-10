import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS


# instantiate the extensions
db = SQLAlchemy()
toolbar = DebugToolbarExtension()
cors = CORS()


# new
def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    toolbar.init_app(app)
    cors.init_app(app)

    # register blueprints
    from api.auth.users import auth_blueprint
    app.register_blueprint(auth_blueprint)
    from api.capital_call import capital_call_blueprint
    app.register_blueprint(capital_call_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
