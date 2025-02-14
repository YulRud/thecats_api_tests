from client.base_client import BaseClient
from config import BASE_URI

class CatFavoritesClient(BaseClient):
    def __init__(self):
        super().__init__(__name__)
        self.base_url = BASE_URI + '/v1/favourites'
  
    def get_favorites(self, api_key):
        return super().get(self.base_url, api_key)

    def get_favorites_by_id(self, api_key, id = None):        
        return super().get_by_id(self.base_url, api_key, id)
  
    def create_favorite(self, api_key, body = None):
        return super().post(self.base_url, api_key, body)

    def delete_favorite(self, api_key, id = None): 
        return super().delete(self.base_url, api_key, id)