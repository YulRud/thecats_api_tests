from http import HTTPStatus
import json
from client.cat_images_client import CatImagesClient
import pytest
from assertpy import assert_that, soft_assertions
from fixture.common_fixture import api_key, test_logger as logger
from util.parameters_for_tests import invalid_api_keys
from util.constants import AUTHORIZATION_ERROR_MESSAGE, NO_VALID_ID_ERROR_MESSAGE, INVALID_ID

client = CatImagesClient()

@pytest.mark.skip(reason="for some reason started to work without the api key") 
@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_retrieve_images_with_invalid_api_key(api_key, logger):    
    logger.info("test_retrieve_images_with_invalid_api_key favorites has started:")
    response = client.get_images(api_key)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

@pytest.mark.skip(reason="for some reason started to work without the api key")  
@pytest.mark.parametrize('api_key', invalid_api_keys)
def test_retrieve_image_by_id_with_invalid_api_key(api_key, logger):    
    logger.info("test_retrieve_images_with_invalid_api_key favorites has started:")
    response = client.get_image_by_id(api_key, id = INVALID_ID)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.UNAUTHORIZED) 
    assert_that(response.text).is_equal_to(AUTHORIZATION_ERROR_MESSAGE) 

def test_retrieve_image_by_id_with_invalid_id(api_key, logger):    
    logger.info("test_retrieve_image_by_id_with_invalid_id favorites has started:")

    response = client.get_image_by_id(api_key, id = INVALID_ID)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.BAD_REQUEST) 
    assert_that(response.text).is_equal_to(NO_VALID_ID_ERROR_MESSAGE.format(INVALID_ID)) 
    