class DataProvider:

    @staticmethod
    def valid_item():
        return {
            "sellerID": 123456,
            "name": "Телефон",
            "price": 10000,
            "statistics": {"likes": 10, "viewCount": 100, "contacts": 5}
        }

    @staticmethod
    def invalid_items():
        return [
            {"sellerID": 123456, "name": "Телефон", "price": -100},
            {"sellerID": 100000, "name": "Телефон", "price": 10000},
        ]
