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