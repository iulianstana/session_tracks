from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint

### swagger specific ###
SWAGGER_URL = ''
API_URL = '/api/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Session Tracker"
    }
)