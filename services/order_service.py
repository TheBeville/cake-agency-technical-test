import requests
from typing import List
from models.order_model import OrderModel

class OrderService:
    """Service class for fetching orders from API"""

    @staticmethod
    def get_orders() -> List[OrderModel]:
        """Fetches orders from the API and returns a list of OrderModel instances"""
        response = requests.get("https://fauxdata.codelayer.io/api/orders")
        response.raise_for_status()
        return [OrderModel.from_json(order) for order in response.json().get("orders", [])]