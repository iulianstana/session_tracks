import json
import unittest
import requests

from mock import patch
from nose.plugins.attrib import attr

from clients.ipAPI.client import IpAPIClient


@attr('unit')
class TestIpAPI(unittest.TestCase):
    
    @patch('clients.ipAPI.client.IpAPIClient.do_request', autospec=True)
    def test_client_error(self, mock_request):
        """ Assert client get requests raise error. """
        content, status = b'{"status":"fail","message":"invalid query","query":"8.8..8"}', 400
        resp = requests.Response()
        resp._content = content 
        resp.status_code = status

        mock_request.return_value = resp
        client = IpAPIClient('test')
        resp_content, resp_code = client.get('8.8..8')

        self.assertEqual(resp_code, 400, 'Wrong status code returned')
        self.assertEqual(resp_content, {'errors': [resp.json()]}, 'Wrong returned conent')

    @patch('clients.ipAPI.client.IpAPIClient.do_request', autospec=True)
    def test_client_error_with_succes_code(self, mock_request):
        """ Assert client get requests raise error. """
        content, status = b'{"status":"fail","message":"invalid query","query":"8.8..8"}', 200
        resp = requests.Response()
        resp._content = content 
        resp.status_code = status

        mock_request.return_value = resp
        client = IpAPIClient('test')
        resp_content, resp_code = client.get('8.8..8')

        self.assertEqual(resp_code, 400, 'Wrong status code returned')
        self.assertEqual(resp_content, {'errors': [resp.json()]}, 'Wrong returned conent')

    @patch('clients.ipAPI.client.IpAPIClient.do_request', autospec=True)
    def test_client_success(self, mock_request):
        """ Assert client get requests return success """
        content, status = b'{"status":"success","continent":"North America","country":"United States","countryCode":"US","region":"VA","regionName":"Virginia","city":"Ashburn","lat":39.03,"lon":-77.5,"timezone":"America/New_York","query":"8.8.8.8"}', 200
        resp = requests.Response()
        resp._content = content 
        resp.status_code = status

        mock_request.return_value = resp
        client = IpAPIClient('test')
        resp_content, resp_code = client.get('8.8.8.8')

        self.assertEqual(resp_code, 200, 'Wrong status code returned')
        self.assertEqual(resp_content, resp.json(), 'Wrong returned conent')
