import requests
import pytest

@pytest.fixture
def url(request):
    return request.config.getoption('--url')

@pytest.fixture
def status_code(request):
    return request.config.getoption('--status-code')

def test_check_status_code(url, status_code):
    response = requests.get(url)
    assert response.status_code == status_code, f'Статус код {response.status_code} ' \
                                                    f'не соответствует ожидаемому {status_code} для URL: {url}'

