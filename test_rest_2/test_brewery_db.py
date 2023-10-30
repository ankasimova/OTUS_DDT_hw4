import pytest
import requests
import random


base_url = 'https://api.openbrewerydb.org'

def test_single_brewery():
    # get brewery ids list
    request = requests.get(f'{base_url}/v1/breweries')
    response_data = request.json()

    # get random brewery id
    id_list = []
    for item in response_data:
        id_value = item.get('id')
        id_list.append(id_value)
    random_id = random.choice(id_list)

    # get single brewery
    request = requests.get(f'{base_url}/v1/breweries/{random_id}')
    response_data = request.json()
    assert response_data['id'] == random_id

@pytest.mark.negative
@pytest.mark.parametrize('brewery_id', [0, 'a', ' ', -1])
def test_single_brewery_negative(brewery_id):
    request = requests.get(f'{base_url}/v1/breweries/{brewery_id}')
    response_data = request.json()
    assert 'message' in response_data \
           and response_data['message'] == "Couldn't find Brewery" \
           and request.status_code == 404

@pytest.mark.negative
@pytest.mark.parametrize('size', [0, 1, 55])
def test_breweries_by_size(size):
    request = requests.get(f'{base_url}/v1/breweries/random?size={size}')
    response_data = request.json()
    if size == 0:
        assert len(response_data) == 1
    elif 1 < size <= 50:
        assert len(response_data) == size
    elif size > 50:
        assert len(response_data) == 50


@pytest.mark.parametrize('type', ['micro', 'nano', 'regional', 'brewpub', 'large',
                                  'planning', 'bar', 'contract', 'proprietor', 'closed'])
def test_breweries_list_by_type(type):
    request = requests.get(f'{base_url}/v1/breweries?by_type={type}')
    response_data = request.json()
    assert request.status_code == 200 and response_data[0]['brewery_type'] == type


@pytest.mark.parametrize('num_per_page', [0, 2, 199, 202, -1])
def test_single_brewery_negative(num_per_page):
    request = requests.get(f'{base_url}/v1/breweries?per_page={num_per_page}')
    response_data = request.json()
    if num_per_page == 0:
        assert len(response_data) == 0
    elif 1 <= num_per_page <= 200:
        assert len(response_data) == num_per_page
    elif num_per_page >= 200:
        assert len(response_data) == 200

