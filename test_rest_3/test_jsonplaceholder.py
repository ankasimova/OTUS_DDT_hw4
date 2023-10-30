import pytest
import requests

base_url = 'https://jsonplaceholder.typicode.com'


@pytest.mark.parametrize('id', [0, 2, -1, 100, 101])
def test_posts_by_id(id):
    request = requests.get(f'{base_url}/posts/{id}')
    response = request.json()
    if id <= 0:
        assert response == {}
    if 0 < id <= 100:
        assert response['id'] == id
        assert 'userId' in response and 'userId' != 0
        assert request.status_code == 200
    if id > 100:
        assert response == {}

def test_creating_posts():
    data = {
        'title': 'Test_title_123',
        'body': 'Test_body_123',
        'userId': 12
    }
    url = f'{base_url}/posts'
    request = requests.post(url, json=data)
    response = request.json()
    assert response['title'] == data['title'] and response['body'] == data['body'] \
           and response['userId'] == data['userId']

def test_updating_posts():
    data = {
        'id': 1,
        'title': 'Test_title_12345',
        'body': 'Test_body_12345',
        'userId': 1
    }
    url = f'{base_url}/posts/1'
    request = requests.put(url, json=data)
    response = request.json()
    assert response['title'] == data['title'] and response['body'] == data['body'] \
           and response['userId'] == data['userId']

def test_deleting_posts():
    request = requests.delete(f'{base_url}/posts/1')
    response = request.json()
    assert response == {}

@pytest.mark.parametrize('user_id', [0, 2, -1, 11])
def test_posts_by_id(user_id):
    request = requests.get(f'{base_url}/posts?userId={user_id}')
    response = request.json()
    if user_id <= 0:
        assert response == []
    if 0 < user_id <= 10:
        for element in response:
            assert element['userId'] == user_id
        assert request.status_code == 200
    if user_id > 10:
        assert response == []