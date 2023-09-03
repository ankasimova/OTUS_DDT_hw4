import pytest
import requests
import random



base_url = 'https://dog.ceo/api'

def test_breeds_list():
    # get breeds list
    request = requests.get(f'{base_url}/breeds/list/all')
    response_data = request.json()
    assert 'status' in response_data and response_data['status'] == 'success'


@pytest.mark.parametrize('cnt', [-1, 0, 3, 20])
def test_image_random(cnt):
    request = requests.get(f'{base_url}/breeds/image/random/{cnt}')
    response_data = request.json()
    assert 'status' in response_data and response_data['status'] == 'success'
    # check we get an image and number of images in response matches with the number in request
    assert response_data.get('message'), 'Value is empty'
    if cnt > 0:
        assert len(response_data.get('message')) == cnt
    else:
        len(response_data.get('message')) == 1


def test_list_images_by_breed():
    # get breeds list
    request = requests.get(f'{base_url}/breeds/list/all')
    response_data = request.json()

    # pick random breed from breeds list
    breed_keys_list = list(response_data['message'].keys())
    print(breed_keys_list)
    random_breed = random.choice(breed_keys_list)

    # check picked images match with the breed
    request = requests.get(f'{base_url}/breed/{random_breed}/images')
    response_data = request.json()
    assert 'status' in response_data and response_data['status'] == 'success'

    for link in list(response_data.get('message')):
        breed = (link.split('/'))[4] # pick breed from the image link
        assert random_breed in breed


def test_random_image_by_breed(breed):
    # get breeds list
    request = requests.get(f'{base_url}/breeds/list/all')
    response_data = request.json()

    # pick random breed from breeds list
    breed_keys_list = list(response_data['message'].keys())
    random_breed = random.choice(breed_keys_list)

    # check picked image match with the breed
    request = requests.get(f'{base_url}/breed/{random_breed}/images/random')
    response_data = request.json()
    assert 'status' in response_data and response_data['status'] == 'success'
    link = response_data.get('message')
    breed = (link.split('/'))[4] # pick breed from the image link
    assert random_breed in breed


@pytest.mark.negative
@pytest.mark.parametrize('breed', ['a', 1])
def test_random_image_by_breed(breed):
    # check picked image match with the breed
    request = requests.get(f'{base_url}/breed/{breed}/images/random')
    response_data = request.json()
    assert request.status_code == 404
    assert 'status' in response_data and response_data['status'] == 'error'
    assert 'message' in response_data and response_data['message'] == 'Breed not found (master breed does not exist)'


def test_subbreed_list():
    # get breeds list
    request = requests.get(f'{base_url}/breeds/list/all')
    response_data = request.json()

    # pick random breed from breeds list
    breeds_list = list(response_data['message'].keys())
    random_breed = random.choice(breeds_list)

    subbreeds_list = list(response_data['message'][random_breed])

    # get subbreed_list and check subbreed_list matches with the main breeds list
    url_subbreeds_list = f'{base_url}/breed/{random_breed}/list'
    request = requests.get(url_subbreeds_list)
    response_data = request.json()
    assert response_data['message'] == subbreeds_list