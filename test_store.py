from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''


@pytest.fixture
def create_pet():
    import uuid
    endpoint = "/pets/"
    data = {"id": int(uuid.uuid4().int % 1000000),
            "name": "test_pet", "type": "dog", "status": "available"}
    response = api_helpers.post_api_data(endpoint, data)
    assert response.status_code == 201
    pet = response.json()
    yield pet['id']


@pytest.fixture
def create_order(create_pet):
    pet_id = create_pet
    endpoint = "/store/order"
    data = {"pet_id": pet_id}
    response = api_helpers.post_api_data(endpoint, data)
    assert response.status_code == 201
    order = response.json()
    yield order['id']


def test_patch_order_by_id(create_order):
    order_id = create_order
    endpoint = f"/store/order/{order_id}"
    data = {"status": "sold"}
    response = api_helpers.patch_api_data(endpoint, data)
    assert response.status_code == 200
    assert response.json()['message'] == "Order and pet status updated successfully"
