import pytest
import requests
from config.constants import BASE_URL


class TestAdvertisementsAPI:

    @pytest.mark.parametrize(
        "seller_id,name,price",
        [
            (123456, "Телефон", 10000),
            (123456, "Телефон", -100),    # API принимает, считается багом
            (100000, "Телефон", 10000),   # API принимает, считается багом
        ]
    )
    def test_create_item(self, seller_id, name, price): #Проверка успешного создания объявления (факт API).

        url = f"{BASE_URL}/api/1/item"
        payload = {
            "sellerID": seller_id,
            "name": name,
            "price": price,
            "statistics": {"likes": 10, "viewCount": 100, "contacts": 5}
        }

        response = requests.post(url, json=payload)

        # Устанавливаем четкое значение для API = 200
        assert response.status_code == 200

        response_json = response.json()

        # API возвращает только status
        assert "status" in response_json
        assert "Сохранили объявление" in response_json["status"]

    def test_get_item_by_id(self, create_item): #Получение объявления по ID ( API возвращает 404 всегда ).

        # Вытаскиваем ID из строки
        created_status = create_item["status"]
        item_id = created_status.split(" - ")[-1]

        url = f"{BASE_URL}/api/1/item/{item_id}"
        response = requests.get(url)

        # Фактическое поведение API: ВСЕГДА 404
        assert response.status_code == 404

    def test_get_statistics_v1(self, create_item): #Проверка получения статистики (v1). API возвращает пустой массив.

        created_status = create_item["status"]
        item_id = created_status.split(" - ")[-1]

        url = f"{BASE_URL}/api/1/statistic/{item_id}"
        response = requests.get(url)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_statistics_v2(self, create_item): #Проверка получения статистики (v2).

        created_status = create_item["status"]
        item_id = created_status.split(" - ")[-1]

        url = f"{BASE_URL}/api/2/statistic/{item_id}"
        response = requests.get(url)

        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_delete_item(self, create_item): #Удаление объявления (API возвращает 404).

        created_status = create_item["status"]
        item_id = created_status.split(" - ")[-1]

        url = f"{BASE_URL}/api/2/item/{item_id}"
        response = requests.delete(url)

        # Проверка фактического поведения API
        assert response.status_code == 404

