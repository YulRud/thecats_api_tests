import requests
import json
from client.base_client import BaseClient
from config import BASE_URI

class CatFavoritesClient(BaseClient):
    def __init__(self):
        super().__init__(__name__)
        self.base_url = BASE_URI
  
    def get_favorites(self, api_key):
        url = f'{self.base_url}/v1/favourites'
        params ={'api_key':api_key}

        response = super().make_get_request(url, params)

        return response

    def get_favorites_by_id(self, api_key, id = None):
        url = f'{self.base_url}/v1/favourites'        
        params ={'api_key':api_key}            

        response = super().make_get_by_id_request(url, id, params)

        return response
  
    def create_favorite(self, api_key, body = None):
        url = f'{self.base_url}/v1/favourites'
        params ={'api_key':api_key}

        response = super().make_post_request(url, params, body)

        return response

    def delete_favorite(self, api_key, id = None):
        url = f'{self.base_url}/v1/favourites'        
        params ={'api_key':api_key}            

        response = super().make_delete_request(url, id, params)

        return response