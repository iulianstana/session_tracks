import requests
import datetime

from flask import request
from flask_restplus import Resource
from flask_restful.reqparse import RequestParser
from flask_restful_swagger_2 import swagger

from app.session.models.models import (
    SessionAction, SessionActionDetails, SessionActionType, SessionLocation, SessionActionTypeEnum
)
from app.session.controllers.constants import default_ip
from clients.ipAPI.client import IpAPIClient


class TrackSessionAPI(Resource):

    def __init__(self, *args, **kwargs):
        self.ip_client = IpAPIClient("TrackSessionAPI")
        super(TrackSessionAPI, self).__init__(*args, **kwargs)

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
        errors = []
        if request.json:
            try:
                session_action = SessionAction(**request.json)
            except Exception as exp:
                errors.append(str(exp))

        if action not in SessionActionTypeEnum:
            errors.append('{0} is not a valid action.'.format(action))
        if errors:
            return {
                'errors': errors
            }, 400

        ip = default_ip if not session_action else session_action['ip']
        content, status = self.ip_client.get(ip)
        if status == 400:
            return content, status

        actionDetails = SessionActionDetails(
            action=action, 
            info=SessionAction(ip=ip), 
            location=SessionLocation(
                longitude=content.get('lon', ''), 
                latitude=content.get('lat', ''), 
                city=content.get('city', ''), 
                region=content.get('region', ''), 
                country=content.get('country', ''), 
                country_iso2=content.get('countryCode', ''), 
                continent=content.get('continent', '')
                ),
            action_date=datetime.datetime.now().isoformat()
            )
        return actionDetails, 200
