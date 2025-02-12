from http import HTTPStatus
import json
from client.cat_favorites_client import CatFavoritesClient
import pytest
from assertpy import assert_that
from fixture.authorization_fixture import api_key
from fixture.authorization_fixture import test_logger as logger
from util.parameters_for_tests import invalid_api_keys
from util.constants import AUTHORIZATION_ERROR_MESSAGE, INVALID_ID

client = CatFavoritesClient()

# TODO add contract testing
# TODO create favorite in fixtures???
TEST_VALID_FAVORITES = 232514437

def test_retrieve_favorites(api_key, logger):    
    logger.info("test_retrieve_favorites favorites has started:")
    response = client.get_favorites(api_key)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    assert_that(response.json()).is_not_empty

    favorites_list = json.loads(response.text)
    assert_that(len(favorites_list)).is_greater_than(0)
    for favorite in favorites_list:
        verify_required_fields_are_present(favorite)

def test_retrieve_favorites_by_id(api_key, logger):    
    logger.info("test_retrieve_favorites_by_id favorites has started:")
    response = client.get_favorites_by_id(api_key, id=TEST_VALID_FAVORITES)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    assert_that(response.json()).is_not_empty

    favorite = json.loads(response.text)
    verify_required_fields_are_present(favorite)
    assert_that(favorite['id']).is_equal_to(TEST_VALID_FAVORITES) 

def verify_required_fields_are_present(favorite):
    assert_that(favorite['id']).is_not_none() 
    assert_that(favorite['user_id']).is_not_none() 
    assert_that(favorite['image_id']).is_not_none() 
    assert_that(favorite['sub_id']).is_not_none() 
    assert_that(favorite['created_at']).is_not_none()

#Validation tests

@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_retrieve_favorites_invalid_api_key(api_key, logger):    
    logger.info("test_retrieve_favorites_invalid_api_key favorites has started:")
    response = client.get_favorites(api_key)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_retrieve_favorites_by_id_invalid_api_key(api_key, logger):    
    logger.info("test_retrieve_favorites_by_id_invalid_api_key favorites has started:")
    response = client.get_favorites_by_id(api_key, id=TEST_VALID_FAVORITES)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

def test_retrieve_favorites_by_id_with_invalid_id(api_key, logger):    
    logger.info("test_retrieve_favorites_by_id_with_invalid_id favorites has started:")

    response = client.get_favorites_by_id(api_key, id = INVALID_ID)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.NOT_FOUND) 
    assert_that(response.text).is_equal_to('NOT_FOUND') 

