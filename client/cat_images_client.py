import requests
import json
from client.base_client import BaseClient
from config import BASE_URI

class CatImagesClient(BaseClient):
    def __init__(self):
        super().__init__(__name__)
        self.base_url = BASE_URI

    def get_images(self, api_key, limit= None, page= None, has_breeds= None, breed_ids= None, order= None, parameter_value = None):
        url = f'{self.base_url}/v1/images/search'
        
        params ={'api_key':api_key,
                 'format':'json',
                 'mime_types':'jpg'}
        if order is not None:
            params['order'] = order
        if limit is not None:
            params['limit'] = limit
        if page is not None:
            params['page'] = page
        if has_breeds is not None:
            params['has_breeds'] = has_breeds
        if breed_ids is not None:
            params['breed_ids'] = breed_ids      
        if parameter_value is not None:
            params[parameter_value[0]] = parameter_value[1]      

        response = super().make_get_request(url, params)

        return response

    def get_image_by_id(self, api_key, id = None):
        url = f'{self.base_url}/v1/images'
        
        params ={'api_key':api_key}            

        response = super().make_get_by_id_request(url, id, params)

        return response