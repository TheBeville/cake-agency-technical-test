from typing import List
from models.order_model import OrderModel

def calculate_average_order_value(orders: List[OrderModel]) -> float:
    """Utility function to calculate the average value of all orders"""
    return sum(order.calculate_total_order_value() for order in orders) / len(orders) if orders else 0.0