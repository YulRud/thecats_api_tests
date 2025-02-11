import json
from client.cat_favorites_client import CatFavoritesClient
from assertpy import assert_that
from fixture.authorization_fixture import api_key, test_logger as logger

client = CatFavoritesClient()

# TODO: Implement fixture for create favorites clean up
# TODO: Implement fixture for getting/creation of a valid image_id


def test_retrieve_favorites_2(api_key, logger):    
    logger.info("test_retrieve_favorites favorites has started:")
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