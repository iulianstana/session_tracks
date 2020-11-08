
from flask import request
from flask_restplus import Resource
from flask_restful.reqparse import RequestParser
from flask_restful_swagger_2 import swagger

from ..models.models import SessionAction, SessionActionDetails, SessionActionType, SessionLocation


class TrackSessionAPI(Resource):

    @swagger.doc({
        'tags': ['Tracking'],
        'summary': 'Session action tracking',
        'description': 'Records session action information.',
        'parameters': [
            {
                'name': 'action',
                'description': ' Session action',
                'in': 'path',
                'type': 'string',
                'required': True,
                'enum': ['login', 'logout', 'buy', 'review', 'shopping-cart']
            },
            {
                'name': 'body',
                'in': 'body',
                'type': 'object',
                'schema': SessionAction
            }
        ],
        'responses': {
            '200': {
                'description': 'Successful response',
                'schema': SessionActionDetails,
            },
            '400': {
                'description': 'Invalid request. Specified request parameters are not valid.',
                'schema': { 
                    'properties': {
                        'errors': { 
                            'type': 'array',
                            'description': 'Message for validation errors.',
                            'items': {
                                'type': 'object'
                            }
                        }
                    }
                }
            }
        }
    })
    def post(self, action):
        actionDetails = SessionActionDetails(
            action=SessionActionType(), 
            info=SessionAction(ip='1.1.1.1'), 
            location=SessionLocation(
                longitude=23.6, 
                latitude=46.7667, 
                city="Cluj-Napoca", 
                region="CJ", 
                country="Romania", 
                country_iso2="RO", 
                continent="Europe"
                ),
            action_date="now"
            )
        return actionDetails, 200
