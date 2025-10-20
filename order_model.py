from typing import List, Dict, Any

class OrderModel:
    """Model representing an order with its items and total order value."""
    
    def __init__(self, id: str, created_at: str, items: List[Dict[str, Any]], items_value: float = 0):
        self.id = id
        self.created_at = created_at # Unused but kept for completeness
        self.items = items
        self.items_value = items_value
    
    def __repr__(self) -> str:
        return f"OrderModel(id='{self.id}', items_value={self.items_value}, items_count={len(self.items)})"