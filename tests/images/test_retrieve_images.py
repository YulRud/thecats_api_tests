import json
from client.cat_images_client import CatImagesClient
import pytest
from assertpy import assert_that, soft_assertions
from fixture.authorization_fixture import api_key
from fixture.authorization_fixture import test_logger as logger

client = CatImagesClient()


def test_retrieve_images(api_key, logger):    
    logger.info("test_retrieve_images test has started:")
    response = client.get_images(api_key)
    assert response.status_code == 200
    assert response.json() != []

    images_list = json.loads(response.text)
    assert len(images_list) > 0

# TODO: add tests with some parameters

def test_retrieve_image_by_id(api_key, logger):    
    logger.info("test_retrieve_image_by_id test has started:")
    response = client.get_image_by_id(api_key, 'BkIEhN3pG')
    assert response.status_code == 200
    assert response.json() != []

    image = json.load(response.text)
    with soft_assertions():
        assert_that(image['id']).is_not_none() 
        assert_that(image['url']).is_not_none() 
        assert_that(image['width']).is_not_none() 
        assert_that(image['height']).is_not_none() 
        assert_that(image['mime_type']).is_not_none() 
