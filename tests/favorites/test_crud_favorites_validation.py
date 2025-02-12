import datetime
import pytest
import pytest_depends
from http import HTTPStatus
import json
from client.cat_favorites_client import CatFavoritesClient
from assertpy import assert_that, soft_assertions
from fixture.authorization_fixture import api_key, test_logger as logger
from util.factory.favorite_factory import get_favorite_body, get_random_favorite_body
from util.string_utils import generate_random_string
from config import USER_ID
import time
from util.parameters_for_tests import invalid_api_keys
from util.constants import AUTHORIZATION_ERROR_MESSAGE, INVALID_ID

client = CatFavoritesClient()


@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_create_favorite_with_invalid_api_key(api_key, logger):    
    logger.info("test_create_favorite_with_invalid_api_key favorites has started:")
    response = client.create_favorite(api_key, get_random_favorite_body())   
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

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

#TODO: Add more tests for duplicated favorites
#TODO: Add tests for exeeds max length image_id and sub_id
