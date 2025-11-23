import pytest
import requests
from config.constants import BASE_URL


@pytest.fixture
def create_item():
    """Фикстура создаёт объявление и возвращает его ID и тело ответа."""
    payload = {
        "sellerID": 123456,
        "name": "Тестовый товар",
        "price": 1000,
        "statistics": {"likes": 1, "viewCount": 5, "contacts": 0}
    }

    response = requests.post(f"{BASE_URL}/api/1/item", json=payload)
    return response.json()
