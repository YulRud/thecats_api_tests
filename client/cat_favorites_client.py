import requests
import json
from client.base_client import BaseClient
from config import BASE_URI

class CatFavoritesClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.base_url = BASE_URI
  
    def get_favorites(self, api_key):
        print('API KEY !!!! ' + str(api_key))

        response = requests.get(
            f'{self.base_url}/v1/favourites',
            headers=self.headers, 
            params={'api_key':api_key}
        )
        return response