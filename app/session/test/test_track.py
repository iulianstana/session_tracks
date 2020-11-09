import json

from flask_testing import TestCase
from mock import patch
from nose.plugins.attrib import attr

from app.session.models.models import SessionActionDetails
from app.session.controllers.constants import default_ip 
from manage import app


@attr('unit')
class TestTrack(TestCase):

    def create_app(self):       
        app.config.from_object('app.session.config.TestingConfig')
        return app

    @patch('clients.ipAPI.client.IpAPIClient.get', autospec=True)
    def test_post_default_ip(self, client_mock):
        """ Assert session track is successful with default ip and no ip on body. """

        action = 'review'
        client_mock.return_value = {
                'status': 'success', 
                'continent': 'North America', 'region': 'VA', 
                'country': 'United States', 'countryCode': 'US', 
                'regionName': 'Virginia', 'city': 'Ashburn', 
                'lat': 39.03, 'lon': -77.5, 'timezone': 
                'America/New_York', 'query': '8.8.8.8'}, 200
        
        with self.client:
            response = self.post_track(action, {})
            
            data = json.loads(response.data.decode())
            session_track = SessionActionDetails(**data)
            self.assertEqual(session_track['action'], action, 'Action was alterated')
            self.assertEqual(response.content_type, 'application/json', 'Different content type returned')
            self.assertEqual(response.status_code, 200, '200 status code should be returned for a successfull call')
            self.assertEqual(session_track['info'], {'ip': default_ip}, 'Default IP was expected')

        self.assertEqual(client_mock.call_count, 1, 'Different number of calls to IpAPIClient')
        self.assertEqual(client_mock.mock_calls[0][1][1], default_ip, 'IpAPIClient was called with a different IP')

    @patch('clients.ipAPI.client.IpAPIClient.get', autospec=True)
    def test_post_body(self, client_mock):
        """ Assert session track is successful with ip on body. """

        action = 'review'
        ip = '89.137.101.73'
        client_mock.return_value = {
                'status': 'success', 
                'continent': 'North America', 'region': 'VA', 
                'country': 'United States', 'countryCode': 'US', 
                'regionName': 'Virginia', 'city': 'Ashburn', 
                'lat': 39.03, 'lon': -77.5, 'timezone': 
                'America/New_York', 'query': '8.8.8.8'}, 200
        
        with self.client:
            response = self.post_track(action, {'ip': ip})
            
            data = json.loads(response.data.decode())
            session_track = SessionActionDetails(**data)
            self.assertEqual(session_track['action'], action, 'Action was alterated')
            self.assertEqual(response.content_type, 'application/json', 'Different content type returned')
            self.assertEqual(response.status_code, 200, '200 status code should be returned for a successfull call')
            self.assertEqual(session_track['info'], {'ip': ip}, 'Default IP was expected')

        self.assertEqual(client_mock.call_count, 1, 'Different number of calls to IpAPIClient')
        self.assertEqual(client_mock.mock_calls[0][1][1], ip, 'IpAPIClient was called with a different IP')

    @patch('clients.ipAPI.client.IpAPIClient.get', autospec=True)
    def test_post_wrong_action(self, client_mock):
        """ Assert session track return error when a wrong action is used. """

        action = 'wrong_action'
        with self.client:
            response = self.post_track(action, {})
            
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400, '400 status code should be returned')
            self.assertIn('errors', data, 'errors field should be present in response')
            self.assertEqual(response.content_type, 'application/json', 'Different content type returned')
            self.assertEqual(data['errors'], ['wrong_action is not a valid action.'], 'Wrong error list returned')

        self.assertEqual(client_mock.call_count, 0, 'Different number of calls to IpAPIClient')

    @patch('clients.ipAPI.client.IpAPIClient.get', autospec=True)
    def test_post_wrong_ip(self, client_mock):
        """ Assert session track return error when a wrong ip is used.  """

        action = 'review'
        with self.client:
            response = self.post_track(action, {'ip': 8888})
            
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400, '400 status code should be returned')
            self.assertIn('errors', data, 'errors field should be present in response')
            self.assertEqual(response.content_type, 'application/json', 'Different content type returned')
            self.assertEqual(data['errors'], ['The attribute "ip" must be a string, but was "<class \'int\'>"'], 'Wrong error list returned')

        self.assertEqual(client_mock.call_count, 0, 'Different number of calls to IpAPIClient')

    @patch('clients.ipAPI.client.IpAPIClient.get', autospec=True)
    def test_post_api_client_error(self, client_mock):
        """ Assert session track return error IpAPIClient return error .  """

        action = 'review'
        ip = '89.137.101.73'
        client_mock.return_value =  {
            'errors': ["APIClient error"]
        }, 400

        with self.client:
            response = self.post_track(action, {'ip': ip})
            
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400, '400 status code should be returned')
            self.assertIn('errors', data, 'errors field should be present in response')
            self.assertEqual(response.content_type, 'application/json', 'Different content type returned')
            self.assertEqual(data['errors'], ['APIClient error'], 'Wrong error list returned')

        self.assertEqual(client_mock.call_count, 1, 'Different number of calls to IpAPIClient')

    def post_track(self, action, body):
        return self.client.post('/track/%s' % action, data=json.dumps(body),
                content_type='application/json'
            )
