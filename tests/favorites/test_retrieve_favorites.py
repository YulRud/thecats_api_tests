import json
from client.cat_favorites_client import CatFavoritesClient
import pytest
from assertpy import assert_that
from fixture.authorization_fixture import api_key

client = CatFavoritesClient()


#TODO: Add contract testing

def test_retrieve_favorites(api_key):    
    response = client.get_favorites(api_key)
    assert response.status_code == 200
    assert response.json() != []

    favorites_list = json.loads(response.text)
    assert len(favorites_list) > 0

    for dict in favorites_list:
        assert_that(dict['id']).is_not_none() 
        assert_that(dict['user_id']).is_not_none() 
        assert_that(dict['image_id']).is_not_none() 
        assert_that(dict['sub_id']).is_not_none() 
        assert_that(dict['created_at']).is_not_none() 



def test_retrieve_favorites_without_api_key():    
    response = client.get_favorites("")
    assert response.status_code == 401

    
def test_retrieve_favorites_with_invalid_api_key():    
    response = client.get_favorites("Invalid_API_Key")
    assert response.status_code == 401