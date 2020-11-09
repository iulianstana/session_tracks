import requests


default_fields = 'status,message,continent,country,countryCode,region,regionName,city,lat,lon,timezone,query'


class IpAPIClient(object):
    def __init__(self, origin, fields=None):
        self.origin = origin
        self.base_request = 'http://ip-api.com/json/'
        self.fields = fields if fields else default_fields

    def get(self, ip):
        req = self.do_request(ip)
        
        content = req.json()
        if req.status_code != 200:
            return {
                'errors': [content]
            }, 400
        if content['status'] != 'success':
            return {
                'errors': [content]
            }, 400
        
        return content, 200

    def do_request(self, ip):
        return requests.get('{0}{1}?fields={2}'.format(self.base_request, ip, self.fields))