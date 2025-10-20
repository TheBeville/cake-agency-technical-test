from typing import Any, Dict

class ItemModel:
    """Model of an item from the list of items in an order"""
    def __init__(self, name: str, price: float, sku: str ):
        self.name = name
        self.price = price
        self.sku = sku

    @staticmethod
    def from_json(data: Dict[str, Any]) -> "ItemModel":
        """Deserialises the json data into an ItemModel instance"""
        return ItemModel(
            name = data.get("name"),
            price = float(data.get("price")),
            sku = data.get("sku"),
        )