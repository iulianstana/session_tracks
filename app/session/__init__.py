from flask import Flask
from flask_bcrypt import Bcrypt
from flask_restful_swagger_2 import Api

from .config import config_by_name
from .controllers.track import TrackSessionAPI


flask_bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    api = Api(
        app=app,
        title="Session Tracker", 
        description="Tracks session information",
        api_version="1.0.0", 
        produces=['application/json'], 
        schemes=['http'],
        tags=[{'name':'Tracking', 'description': 'Session Tracking'}], 
        host='127.0.0.1:8000'
        )
    api.add_resource(TrackSessionAPI, '/track/<string:action>')
    flask_bcrypt.init_app(app)

    return app
