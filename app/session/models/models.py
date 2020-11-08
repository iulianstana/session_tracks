from flask_restful_swagger_2 import Schema


SessionActionTypeEnum = ['login', 'logout', 'buy', 'review', 'shopping-cart']


class SessionAction(Schema):
    type = 'object'
    title = 'Session Action'
    properties = {
        'ip': {
            'type': 'string',
            'description': 'client IP',
        },
        'resolution': {
            'type': 'object',
            'description': 'Current resolution',
            'required': ['width', 'height'],
            'properties': {
                'width': {
                    'type': 'integer'
                },
                'height': {
                    'type': 'integer'
                }
            }
        }
    }
    required = ['ip']


class SessionActionType(Schema):
    type = 'string'
    title = 'Session Action Type'
    enum = SessionActionTypeEnum


class SessionLocation(Schema):
    type = 'object'
    title = 'Session Location Details'
    properties = {
        'longitude': {
            'type': 'number',
            'format': 'float'
        },
        'latitude': {
            'type': 'number',
            'format': 'float'
        },
        'city': {
            'type': 'string'
        },
        'region': {
            'type': 'string'
        },
        'country': {
            'type': 'string'
        },
        'country_iso2': {
            'type': 'string'
        },
        'continent': {
            'type': 'string'
        },
    }
    required = [
        'longitude', 'latitude', 'city', 'region', 'country', 'country_iso2', 'continent'
    ]


class SessionActionDetails(Schema):
    type = 'object'
    properties = {
        'action': SessionActionType,
        'info': SessionAction,
        'location': SessionLocation,
        'action_date': {
            'type': 'string',
            'description': "ISO 8601 representation of current date/time with timezone information (using client's timezone)"
        },
    }
    required = [
        'action', 'info', 'location', 'action_date'
    ]
