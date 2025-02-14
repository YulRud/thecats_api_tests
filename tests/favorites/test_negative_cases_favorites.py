import datetime
import pytest
import pytest_depends
from http import HTTPStatus
import json
from client.cat_favorites_client import CatFavoritesClient
from assertpy import assert_that, soft_assertions
from fixture.authorization_fixture import api_key, test_logger as logger
from factory.favorite_factory import get_favorite_body, get_random_favorite_body
from util.string_utils import generate_random_string
from config import USER_ID
import time
from util.parameters_for_tests import invalid_api_keys
from util.constants import AUTHORIZATION_ERROR_MESSAGE, INVALID_ID

client = CatFavoritesClient()

MAX_IMAGE_ID_LENGTH = 11
MAX_SUB_ID_LENGTH = 255

#Retrieve endpoints

@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_retrieve_favorites_invalid_api_key(api_key, logger):    
    logger.info("test_retrieve_favorites_invalid_api_key favorites has started:")
    response = client.get_favorites(api_key)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_retrieve_favorites_by_id_invalid_api_key(api_key, logger):    
    logger.info("test_retrieve_favorites_by_id_invalid_api_key favorites has started:")
    response = client.get_favorites_by_id(api_key, id=INVALID_ID)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

def test_retrieve_favorites_by_id_with_invalid_id(api_key, logger):    
    logger.info("test_retrieve_favorites_by_id_with_invalid_id favorites has started:")

    response = client.get_favorites_by_id(api_key, id = INVALID_ID)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.NOT_FOUND) 
    assert_that(response.text).is_equal_to('NOT_FOUND') 

#Create endpoints

@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_create_favorite_with_invalid_api_key(api_key, logger):    
    logger.info("test_create_favorite_with_invalid_api_key favorites has started:")
    response = client.create_favorite(api_key, get_random_favorite_body())   
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

def test_create_favorite_with_empty_image_id(api_key, logger):
    logger.info("test_create_favorite_with_empty_image_id has started:")
    body = get_favorite_body('', generate_random_string())
    response = client.create_favorite(api_key, body)
    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    assert_that(response.text).is_equal_to('"image_id" is not allowed to be empty') 
    
def test_create_favorite_without_image_id(api_key, logger):
    logger.info("create_favorite_without_image_id has started:")
    body = get_favorite_body(None, generate_random_string())
    response = client.create_favorite(api_key, body)
    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    assert_that(response.text).is_equal_to('"image_id" must be a string') 
    
def test_create_favorite_with_empty_sub_id(api_key, logger):
    logger.info("test_create_favorite_with_empty_sub_id has started:")
    body = get_favorite_body(generate_random_string(), '')
    response = client.create_favorite(api_key, body)
    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    assert_that(response.text).is_equal_to('"sub_id" is not allowed to be empty') 
    
def test_create_favorite_without_sub_id(api_key, logger):
    logger.info("test_create_favorite_without_sub_id has started:")
    body = get_favorite_body(generate_random_string(), None)
    response = client.create_favorite(api_key, body)
    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    assert_that(response.text).is_equal_to('"sub_id" must be a string') 
 
@pytest.fixture
def create_favorite(api_key, logger):
    logger.info("create favorite with image_id and sub_id with length that exceeds max length as test data:")
    body = get_favorite_body(generate_random_string(MAX_IMAGE_ID_LENGTH + 1), generate_random_string(MAX_SUB_ID_LENGTH + 1))
    response = client.create_favorite(api_key, body)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    favorite = json.loads(response.text)
    yield favorite
    client.delete_favorite(api_key, favorite['id'])   

def test_create_favorite_with_image_id_exceeds_length(api_key, logger, create_favorite):
    logger.info("test_create_favorite_with_empty_image_id has started:")
    createdId = create_favorite['id']

    response_created_favorite = client.get_favorites_by_id(api_key, createdId)
    assert_that(response_created_favorite.status_code).is_equal_to(HTTPStatus.OK)
    
    #Verify that image_id cannot have length bigger than max length
    assert_that(len(json.loads(response_created_favorite.text)['image_id'])).is_equal_to(MAX_IMAGE_ID_LENGTH) 

def test_create_favorite_with_sub_id_exceeds_length(api_key, logger, create_favorite):
    logger.info("test_create_favorite_with_sub_id_exceeds_length has started:")
    createdId = create_favorite['id']

    response_created_favorite = client.get_favorites_by_id(api_key, createdId)
    assert_that(response_created_favorite.status_code).is_equal_to(HTTPStatus.OK)
    
    #Verify that sub_id cannot have length bigger than max length
    assert_that(len(json.loads(response_created_favorite.text)['sub_id'])).is_equal_to(MAX_SUB_ID_LENGTH)

def test_create_favorite_with_duplicated_favorites(api_key, logger, create_favorite):
    logger.info("test_create_favorite_with_duplicated_favorites has started:")
    createdId = create_favorite['id']
    response_created_favorite = client.get_favorites_by_id(api_key, createdId)
    assert_that(response_created_favorite.status_code).is_equal_to(HTTPStatus.OK)
    favorite = json.loads(response_created_favorite.text)     

    body = get_favorite_body(favorite['image_id'], favorite['sub_id'])
    response = client.create_favorite(api_key, body)
    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST)
    assert_that(response.text).is_equal_to('DUPLICATE_FAVOURITE - favourites are unique for account + image_id + sub_id')

#Delete endpoints

@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_delete_favorite_with_invalid_api_key(api_key, logger):    
    logger.info("test_delete_favorite_with_invalid_api_key favorites has started:")
    response = client.delete_favorite(api_key, INVALID_ID)   
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

def test_delete_favorite_with_invalid_id(api_key,logger):    
    logger.info("test_delete_favorite_with_invalid_id favorites has started:")
    response = client.delete_favorite(api_key, INVALID_ID)   
    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST) 
    assert_that(response.text).is_equal_to('INVALID_ACCOUNT') 
    