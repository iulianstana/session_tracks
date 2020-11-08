
from flask import request
from flask_restplus import Resource
from flask_restful.reqparse import RequestParser
from flask_restful_swagger_2 import swagger

from ..models.models import (
    SessionAction, SessionActionDetails, SessionActionType, SessionLocation, SessionActionTypeEnum
)


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
                'enum': SessionActionTypeEnum
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

        session_action = None
        ip = ''
        if request.json:
            try:
                session_action = SessionAction(**request.json)
            except Exception as exp:
                return {
                    'errors': [str(exp)]
                }, 400
        if action not in SessionActionTypeEnum:
            return {
                'errors': ['{0} is not a valid action.'.format(action)]
            }
        
        if not session_action:
            # default ip to google.com
            ip = '8.8.8.8'
        else:
            ip = session_action['ip']

        actionDetails = SessionActionDetails(
            action=SessionActionType(), 
            info=SessionAction(ip=ip), 
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
