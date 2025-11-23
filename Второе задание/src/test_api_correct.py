import pytest
import requests
import uuid
from config.constants import BASE_URL


class TestAdvertisementsAPI:

    @pytest.fixture
    def create_item(self):
        url = f"{BASE_URL}/api/1/item"
        payload = {
            "sellerID": 123456,
            "name": "Тестовый товар",
            "price": 5000,
            "statistics": {"likes": 10, "viewCount": 100, "contacts": 5}
        }

        response = requests.post(url, json=payload)
        assert response.status_code == 200
        return response.json()

    @pytest.mark.parametrize(
        "seller_id,name,price,expected_status",
        [
            (123456, "Телефон", 10000, 200),  # Валидные данные
            (123456, "Телефон", -100, 200),  # API принимает отрицательную цену (баг)
            (100000, "Телефон", 10000, 200),  # API принимает sellerID вне диапазона (баг)
            (123456, "", 10000, 400),  # API НЕ принимает пустое название
        ]
    )
    def test_create_item(self, seller_id, name, price, expected_status):
        """Проверка создания объявления"""

        url = f"{BASE_URL}/api/1/item"
        payload = {
            "sellerID": seller_id,
            "name": name,
            "price": price,
            "statistics": {"likes": 10, "viewCount": 100, "contacts": 5}
        }

        response = requests.post(url, json=payload)
        assert response.status_code == expected_status

        if expected_status == 200:
            response_json = response.json()
            assert "status" in response_json
            assert "Сохранили объявление" in response_json["status"]

            # Проверка UUID
            status_text = response_json["status"]
            uuid_part = status_text.split(" - ")[-1]
            try:
                uuid.UUID(uuid_part)
                print(f"Создано объявление: {status_text}")
            except ValueError:
                pytest.fail(f"Некорректный UUID: {uuid_part}")

    def test_create_item_missing_required_field(self): #Проверка создания без обязательного поля sellerID
        url = f"{BASE_URL}/api/1/item"
        payload = {
            "name": "Телефон без sellerID",
            "price": 10000,
            "statistics": {"likes": 10, "viewCount": 100, "contacts": 5}
        }

        response = requests.post(url, json=payload)
        assert response.status_code == 400

    def test_get_item_by_id(self, create_item): #Проверка получения объявления по ID

        created_data = create_item
        item_id = created_data["status"].split(" - ")[-1]

        url = f"{BASE_URL}/api/1/item/{item_id}"
        response = requests.get(url)
        assert response.status_code == 200
        item_data = response.json()
        assert isinstance(item_data, list)
        print(f"GET /api/1/item/{item_id} вернул данные объявления")

    def test_get_statistics_v1(self, create_item): #Проверка получения статистики (v1)

        created_data = create_item
        item_id = created_data["status"].split(" - ")[-1]

        url = f"{BASE_URL}/api/1/statistic/{item_id}"
        response = requests.get(url)

        assert response.status_code == 200
        statistics = response.json()
        assert isinstance(statistics, list)
        assert len(statistics) > 0
        print(f"Статистика v1: {statistics}")

    def test_get_statistics_v2(self, create_item): #Проверка получения статистики (v2)

        created_data = create_item
        item_id = created_data["status"].split(" - ")[-1]

        url = f"{BASE_URL}/api/2/statistic/{item_id}"
        response = requests.get(url)

        assert response.status_code == 200
        statistics = response.json()
        assert isinstance(statistics, list)
        assert len(statistics) > 0
        print(f"Статистика v2: {statistics}")

    def test_delete_item(self, create_item): #Проверка удаления объявления

        created_data = create_item
        item_id = created_data["status"].split(" - ")[-1]

        url = f"{BASE_URL}/api/2/item/{item_id}"
        response = requests.delete(url)

        #  Исправление на корректный возврат статуса = 200!
        assert response.status_code == 200
        print(f" DELETE /api/2/item/{item_id} вернул 200")

    def test_get_items_by_seller_id(self): #Проверка получения всех объявлений продавца
        seller_id = 123456

        url = f"{BASE_URL}/api/1/{seller_id}/item"
        response = requests.get(url)

        assert response.status_code == 200
        items = response.json()
        assert isinstance(items, list)
        print(f"GET /api/1/{seller_id}/item вернул {len(items)} объявлений")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])