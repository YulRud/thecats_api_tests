from http import HTTPStatus
import json
from client.cat_images_client import CatImagesClient
import pytest
from assertpy import assert_that, soft_assertions
from fixture.common_fixture import api_key, test_logger as logger
from util.parameters_for_tests import invalid_api_keys
from util.constants import AUTHORIZATION_ERROR_MESSAGE, NO_VALID_ID_ERROR_MESSAGE, INVALID_ID

client = CatImagesClient()

TEST_IMAGE_ID = 'xnzzM6MBI'
TEST_BREED_IDS = ['beng','abys']
DEFAULT_LIMIT = 10
MAX_LIMIT = 100

def test_retrieve_images(api_key, logger):    
    logger.info("test_retrieve_images test has started:")
    response = client.get_images(api_key, limit=DEFAULT_LIMIT)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    assert_that(response.json()).is_not_empty

    images_list = json.loads(response.text)
    assert_that(len(images_list)).is_greater_than(0)

    for image in images_list:        
        verify_image_required_fields(image)


limit_and_page_combinations = {
    (1,0),    
    (1,10),    
    (MAX_LIMIT,1)
    }

@pytest.mark.parametrize('limit, page', limit_and_page_combinations)
def test_retrieve_images_with_limit_and_page(limit, page, api_key, logger):    
    logger.info("test_retrieve_images_with_limit_and_page test has started:")

    response_one = client.get_images(api_key, limit=limit, page=page)    
    assert_that(response_one.status_code).is_equal_to(HTTPStatus.OK) 
    images_list_one = json.loads(response_one.text)
    assert_that(len(images_list_one)).is_equal_to(limit)

    response_two = client.get_images(api_key, limit=limit, page=page+1)    
    assert_that(response_two.status_code).is_equal_to(HTTPStatus.OK) 
    images_list_two = json.loads(response_two.text)
    assert_that(len(images_list_two)).is_equal_to(limit)
    assert_that(images_list_two).is_equal_to(images_list_two)
    assert_that(images_list_two[:DEFAULT_LIMIT]).is_not_equal_to(images_list_one[:DEFAULT_LIMIT])

def test_retrieve_images_with_max_limit_exceeds(api_key, logger):    
    logger.info("test_retrieve_images_with_max_limit_exceeds test has started:")

    response_one = client.get_images(api_key, limit=MAX_LIMIT+1)    
    assert_that(response_one.status_code).is_equal_to(HTTPStatus.OK) 
    images_list_one = json.loads(response_one.text)
    assert_that(len(images_list_one)).is_equal_to(MAX_LIMIT)

has_breeds_combinations = {
    (0),    
    (1)
    }

@pytest.mark.parametrize('has_breeds', has_breeds_combinations)
def test_retrieve_images_with_has_breeds(has_breeds, api_key, logger):    
    logger.info("test_retrieve_images_with_has_breeds test has started:")

    response = client.get_images(api_key, has_breeds=has_breeds, limit=DEFAULT_LIMIT)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    images_list = json.loads(response.text)
    for image in images_list:
        if has_breeds == 1:
            assert_that(image['breeds']).is_not_empty() 
        else:
            assert_that(image['breeds']).is_empty()

order_combinations = {
    ('RANDOM', 'RANDOM'),    
    ('ASC', 'DESC' ),    
    ('DESC', 'ASC' )
    }

@pytest.mark.parametrize('order_one, order_two', order_combinations)
def test_retrieve_images_with_order(order_one, order_two, api_key, logger):    
    logger.info("test_retrieve_images_with_order test has started:")
    page = 1

    response_one = client.get_images(api_key, limit=DEFAULT_LIMIT, page=page, order=order_one)    
    assert_that(response_one.status_code).is_equal_to(HTTPStatus.OK) 
    images_list_one = json.loads(response_one.text)
    assert_that(len(images_list_one)).is_equal_to(DEFAULT_LIMIT)

    response_two = client.get_images(api_key, limit=DEFAULT_LIMIT, page=page, order=order_two)    
    assert_that(response_two.status_code).is_equal_to(HTTPStatus.OK) 
    images_list_two = json.loads(response_two.text)

    assert_that(images_list_one).is_not_equal_to(images_list_two)

def test_retrieve_images_by_breed_ids(api_key, logger):    
    logger.info("test_retrieve_images_has_breeds test has started:")

    response = client.get_images(api_key, breed_ids=','.join(TEST_BREED_IDS), limit=DEFAULT_LIMIT)    
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    images_list = json.loads(response.text)
    for image in images_list:
        assert_that(image['breeds']).is_not_empty() 
        retrieved_breed_ids = {breed['id'] for breed in image['breeds']}
        assert_that(len(retrieved_breed_ids.intersection(set(TEST_BREED_IDS)))).is_greater_than(0)


def test_retrieve_image_by_id(api_key, logger):    
    logger.info("test_retrieve_image_by_id test has started:")

    response = client.get_image_by_id(api_key, TEST_IMAGE_ID)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 

    image_retrieved = json.loads(response.text)
    image_url = image_retrieved['url']

    # verify required fields are present
    with soft_assertions():
        verify_image_required_fields(image_retrieved)
        assert_that(image_retrieved['id']).is_equal_to(TEST_IMAGE_ID) 
        assert_that(image_retrieved['breeds']).is_not_empty() 
    
    # verify the image is accessible
    image_picture_response = client.get(image_url, api_key)
    assert_that(image_picture_response.status_code).is_equal_to(HTTPStatus.OK)  
    assert_that(image_picture_response.headers.get('Content-Type')).is_equal_to('image/jpeg')

def verify_image_required_fields(image):
    assert_that(image).is_not_none() 
    assert_that(image['id']).is_not_none() 
    assert_that(image['url']).is_not_none() 
    