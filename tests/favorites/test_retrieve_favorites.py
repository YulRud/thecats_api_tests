from http import HTTPStatus
import json
from assertion.contract_testing_validation import validate_schema
from client.cat_favorites_client import CatFavoritesClient
import pytest
from assertpy import assert_that
from fixture.common_fixture import api_key, test_logger as logger
from factory.favorite_factory import get_random_favorite_body
from util.parameters_for_tests import invalid_api_keys
from util.constants import AUTHORIZATION_ERROR_MESSAGE, INVALID_ID

client = CatFavoritesClient()

@pytest.fixture
def favorite_validation_schema():
    return {
    "id": {'type': 'number'},
    "user_id": {'type': 'string'},
    "image_id": {'type': 'string'},
    "sub_id": {'type': 'string'},
    "created_at": {'type': 'string'},
    "image": {
        'type': 'dict',
        'schema': {
            'id': {'type': 'string', 'required': False},
            'url': {'type': 'string', 'required': False}
        },
        'required': False
    }
}

@pytest.fixture
def create_favorite(api_key):
    body = get_random_favorite_body()
    response = client.create_favorite(api_key, body)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK)
    favorite = json.loads(response.text)
    yield favorite
    client.delete_favorite(api_key, favorite['id'])

def test_retrieve_favorites(api_key, logger, favorite_validation_schema):    
    logger.info("test_retrieve_favorites favorites has started:")
    response = client.get_favorites(api_key)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    assert_that(response.json()).is_not_empty

    favorites_list = json.loads(response.text)
    assert_that(len(favorites_list)).is_greater_than(0)
    for favorite in favorites_list:
        verify_required_fields_are_present(favorite)
        validate_schema(favorite, favorite_validation_schema, logger)

def test_retrieve_favorites_by_id(api_key, logger, create_favorite, favorite_validation_schema):    
    logger.info("test_retrieve_favorites_by_id favorites has started:")
    create_favorite_id = create_favorite['id']
    response = client.get_favorites_by_id(api_key, id=create_favorite_id)
    assert_that(response.status_code).is_equal_to(HTTPStatus.OK) 
    assert_that(response.json()).is_not_empty

    favorite = json.loads(response.text)
    verify_required_fields_are_present(favorite)
    assert_that(favorite['id']).is_equal_to(create_favorite_id) 
    assert_that(favorite['user_id']).is_equal_to(favorite['user_id']) 
    assert_that(favorite['image_id']).is_equal_to(favorite['image_id']) 
    assert_that(favorite['sub_id']).is_equal_to(favorite['sub_id']) 
    validate_schema(favorite, favorite_validation_schema, logger)

def verify_required_fields_are_present(favorite):
    assert_that(favorite['id']).is_not_none() 
    assert_that(favorite['user_id']).is_not_none() 
    assert_that(favorite['image_id']).is_not_none() 
    assert_that(favorite['sub_id']).is_not_none() 
    assert_that(favorite['created_at']).is_not_none()
