from typing import List, Dict, Any
from models.item_model import ItemModel

class OrderModel:
    """Model of an order with its items and total order value"""

    def __init__(self, id: str, created_at: str, items: List[ItemModel], items_value: float = 0):
        self.id = id
        self.created_at = created_at # Unused but kept for completeness
        self.items = items
        self.items_value = items_value
    
    def __repr__(self) -> str:
        return f"OrderModel(id='{self.id}', items_value={self.items_value}, items_count={len(self.items)})"
    
    @staticmethod
    def from_json(data: Dict[str, Any]) -> "OrderModel":
        return OrderModel(
            id = data.get("id"),
            created_at = data.get("created_at"),
            items = [ItemModel.from_json(item) for item in data.get("items", [])],
        )
    
    def calculate_total_order_value(self) -> float:
        """Calculate the total value of all items in the order"""
        return sum(item.price for item in self.items)