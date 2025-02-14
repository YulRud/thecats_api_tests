from util.logger_util import Logger
import requests

class BaseClient:     

    logger = None

    def __init__(self, name=__name__):
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if not BaseClient.logger:
            BaseClient.logger = Logger(name=name).get_logger()

    def make_get_request(self, url, api_key, parameters=None):
        if parameters is None:
            parameters = {}
        parameters['api_key'] = api_key
        BaseClient.logger.info(f"Making GET request to: {url} with params: {parameters}")

        response = requests.get(url,
            headers=self.headers, 
            params=parameters)           
        
        BaseClient.logger.info(f"Received response with status code: {response.status_code} and body: {response.text}")
        return response

    def make_get_by_id_request(self, url, api_key, id):     
        parameters = {'api_key': api_key}
        url = url + f'/{id}'
        BaseClient.logger.info(f"Making GET request to: {url} with params: {parameters}")

        response = requests.get(url,
            headers=self.headers, 
            params=parameters)           
        
        BaseClient.logger.info(f"Received response with status code: {response.status_code}, params: {parameters} and body: {response.text}")
        return response

    def make_post_request(self, url, api_key, body=None): 
        parameters = {'api_key': api_key}  
        BaseClient.logger.info(f"Making POST request to: {url} with body: {body}")

        response = requests.post(url,
            headers=self.headers, 
            params= parameters,
            json=body)           
        
        BaseClient.logger.info(f"Received response with status code: {response.status_code} and body: {response.text}")
        return response

    def make_delete_request(self, url, api_key, id, parameters=None):       
        if parameters is None:
            parameters = {}
        parameters['api_key'] = api_key
        url = url + f'/{id}'    
        BaseClient.logger.info(f"Making DELETE request to: {url} with params: {parameters}")

        response = requests.delete(url,
            headers=self.headers, 
            params=parameters)           
        
        BaseClient.logger.info(f"Received response with status code: {response.status_code} and body: {response.text}")
        return response
    