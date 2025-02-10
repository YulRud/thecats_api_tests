from util.logger_util import Logger
import requests

class BaseClient:     
    def __init__(self, name=__name__):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.logger = Logger(name=name).get_logger()

    def make_get_request(self, url, parameters=None):
        self.logger.info(f"Making request to: {url} with params: {parameters}")

        response = requests.get(url,
            headers=self.headers, 
            params=parameters)           
        
        self.logger.info(f"Received response with status code: {response.status_code} and body: {response.text}")
        return response