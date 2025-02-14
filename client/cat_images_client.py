from client.base_client import BaseClient
from config import BASE_URI

class CatImagesClient(BaseClient):
    def __init__(self):
        super().__init__(__name__)
        self.base_url = BASE_URI + '/v1/images'

    def get_images(self, api_key, limit= None, page= None, has_breeds= None, breed_ids= None, order= None, parameter_value = None):     
        params ={'format':'json',
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

        response = super().get(self.base_url + '/search', api_key, params)

        return response

    def get_image_by_id(self, api_key, id = None):           
        return super().get_by_id(self.base_url, api_key, id)