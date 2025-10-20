from typing import List, Dict, Any
from order_model import OrderModel

class OrderService:
    """Service class for handling order data processing and business logic."""
    
    @staticmethod
    def parse_orders(data: Dict[str, Any]) -> str:
        """Parse orders data and return formatted average value."""

        if not isinstance(data, dict) or "orders" not in data:
            raise ValueError("Invalid data format: expected dict with 'orders' key")
        
        orders = []
        
        for item in data.get("orders", []):
            if not isinstance(item, dict):
                continue
                
            items_list = item.get("items", [])
            if not isinstance(items_list, list):
                items_list = []
                
            items_value = 0
            for order_item in items_list:
                if isinstance(order_item, dict):
                    try:
                        price = float(order_item.get("price", 0))
                        items_value += price
                    except (ValueError, TypeError):
                        continue
                
            order = OrderModel(
                id=item.get("id", ""),
                created_at=item.get("created_at", ""),
                items=items_list,
                items_value=items_value
            )
            orders.append(order)
        
        if not orders:
            return "0.00"
            
        average_value = sum(order.items_value for order in orders) / len(orders)
        return f"{average_value:,.2f}"