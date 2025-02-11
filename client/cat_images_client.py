import requests
import json
from client.base_client import BaseClient
from config import BASE_URI

class CatImagesClient(BaseClient):
    def __init__(self):
        super().__init__(__name__)
        self.base_url = BASE_URI

    def get_images(self, api_key, size= None, mime_types= None, order= None, limit= None, page= None):
        url = f'{self.base_url}/v1/images/search'
        
        params ={'api_key':api_key,
                 'format':'json'}
        if size is not None:
            params['size'] = size
        if mime_types is not None:
            params['mime_types'] = mime_types
        if order is not None:
            params['order'] = order
        if limit is not None:
            params['limit'] = limit
        if page is not None:
            params['page'] = page
            

        response = super().make_get_request(url, params)

        return response

    def get_image_by_id(self, api_key, id = None):
        url = f'{self.base_url}/v1/images'
        
        params ={'api_key':api_key}            

        response = super().make_get_by_id_request(url, id, params)

        return response