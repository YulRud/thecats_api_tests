import datetime
import pytest
import pytest_depends
from http import HTTPStatus
import json
from client.cat_favorites_client import CatFavoritesClient
from assertpy import assert_that, soft_assertions
from fixture.common_fixture import api_key, test_logger as logger
from factory.favorite_factory import get_favorite_body, get_random_favorite_body
from config import USER_ID
import time
from util.parameters_for_tests import invalid_api_keys
from util.constants import AUTHORIZATION_ERROR_MESSAGE, INVALID_ID

client = CatFavoritesClient()

@pytest.fixture(scope="module")
def favorite_test_data():
    return {
        "id_created": None,
        "body_to_create": None
    }

@pytest.fixture(scope="module", autouse=True)
def cleanup_favorite(api_key, logger, favorite_test_data):
    yield
    if favorite_test_data["id_created"]:
        logger.info(f"Cleaning up favorite with id: {favorite_test_data['id_created']}")
        response = client.delete_favorite(api_key, id=favorite_test_data["id_created"])

@pytest.mark.dependency(name="test_create_favorite")
def test_create_favorite(api_key, logger, favorite_test_data):    
    logger.info("test_create_favorite favorites has started:")

    favorite_test_data["body_to_create"] = get_random_favorite_body()

    response = client.create_favorite(api_key, favorite_test_data["body_to_create"])
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    assert_that(response.json()).is_not_empty
    
    favorites_created = json.loads(response.text)
    assert_that(favorites_created["message"]).is_equal_to('SUCCESS')     
    assert_that(favorites_created["id"]).is_not_none

    favorite_test_data["id_created"] = favorites_created["id"]

@pytest.mark.dependency(name="test_get_created_favorite", depends=["test_create_favorite"])
def test_get_created_favorite(api_key, logger, favorite_test_data):    
    logger.info("test_get_created_favorite favorites has started:")

    response = client.get_favorites_by_id(api_key, id=favorite_test_data["id_created"])
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    assert_that(response.json()).is_not_empty
    
    favorite = json.loads(response.text)
    with soft_assertions():
        assert_that(favorite['id']).is_equal_to(favorite_test_data["id_created"]) 
        assert_that(favorite['user_id']).is_equal_to(USER_ID) 
        assert_that(favorite['image_id']).is_equal_to(favorite_test_data['body_to_create']['image_id']) 
        assert_that(favorite['sub_id']).is_equal_to(favorite_test_data['body_to_create']['sub_id']) 
        assert_that(favorite['image']).is_empty() 

        current_time = datetime.datetime.now(datetime.UTC)
        favorite_created_at = datetime.datetime.strptime(favorite['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)

        assert_that(favorite_created_at).is_equal_to_ignoring_seconds(current_time)

@pytest.mark.dependency(name = "test_delete_created_favorite", depends=["test_create_favorite", "test_get_created_favorite"])
def test_delete_created_favorite(api_key, logger, favorite_test_data):  
    #we need to make the tests sleep to avoid to much requests situation
    time.sleep(1)
      
    logger.info("test_delete_created_favorite favorites has started:")
    favorite_created_id = favorite_test_data["id_created"]

    response = client.delete_favorite(api_key, id=favorite_created_id)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    assert_that(response.json()).is_not_empty
    
    favorite = json.loads(response.text)
    assert_that(favorite["message"]).is_equal_to('SUCCESS')    
