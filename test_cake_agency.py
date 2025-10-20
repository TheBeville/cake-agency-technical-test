import unittest
from unittest.mock import patch, Mock
from models.order_model import OrderModel
from models.item_model import ItemModel
from order_service import OrderService
from utils.order_values import calculate_average_order_value
import main
import requests

class TestItemModel(unittest.TestCase):
    """Tests for ItemModel"""
    
    def test_item_model_from_json(self):
        """ItemModel creation from JSON data"""
        data = {
            "name": "Vanilla Cake", 
            "price": "30.00", 
            "sku": "VAN001",
        }
        item = ItemModel.from_json(data)
        
        self.assertEqual(item.name, "Vanilla Cake")
        self.assertEqual(item.price, 30.00)
        self.assertEqual(item.sku, "VAN001")

class TestOrderModel(unittest.TestCase):
    """Tests for OrderModel"""
    
    def test_order_model_from_json(self):
        """OrderModel creation from JSON data"""
        data = {
            "id": "123",
            "created_at": "2025-10-20T10:00:00Z",
            "items": [
                {"name": "Cake", "price": "25.00", "sku": "CAKE001"},
                {"name": "Cookie", "price": "5.50", "sku": "COOK001"}
            ],
        }
        order = OrderModel.from_json(data)
        
        self.assertEqual(order.id, "123")
        self.assertEqual(len(order.items), 2)
        self.assertEqual(order.items[0].name, "Cake")
        self.assertEqual(order.items[1].price, 5.50)
        self.assertEqual(order.calculate_total_order_value(), 30.50)

class TestOrderService(unittest.TestCase):
    """Tests for OrderService"""
    
    def test_get_orders_success(self):
        """Order-fetching and model creation from API"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "orders": [
                {
                    "id": "1",
                    "created_at": "2025-10-20T10:00:00Z",
                    "items": [{"name": "Cake", "price": "25.00", "sku": "CAKE001"}]
                },
                {
                    "id": "2", 
                    "created_at": "2025-10-20T11:00:00Z",
                    "items": [{"name": "Cookie", "price": "5.50", "sku": "COOK001"}]
                }
            ]
        }
        
        with patch('order_service.requests.get', return_value=mock_response):
            orders = OrderService.get_orders()
        
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0].id, "1")
        self.assertEqual(orders[1].id, "2")
        self.assertEqual(len(orders[0].items), 1)

class TestOrderValues(unittest.TestCase):
    """Tests for order values utility function"""
    
    def test_calculate_average_order_value(self):
        """Calculating average order value with multiple orders"""
        orders = [
            OrderModel("1", "2025-10-20T10:00:00Z", [
                ItemModel("Cake", 30.00, "CAKE001")
            ]),
            OrderModel("2", "2025-10-20T11:00:00Z", [
                ItemModel("Cookie", 10.00, "COOK001")
            ])
        ]
        
        average = calculate_average_order_value(orders)
        self.assertEqual(average, 20.00)
    
    def test_calculate_average_order_value_empty_list(self):
        """Calculating average with an empty list of orders"""
        average = calculate_average_order_value([])
        self.assertEqual(average, 0.0)

class TestMain(unittest.TestCase):
    """Tests for main()"""

    @patch('main.OrderService.get_orders')
    @patch('main.calculate_average_order_value')
    def test_main_success(self, mock_calculate_average, mock_get_orders):
        """Running main()"""
        mock_get_orders.return_value = [Mock()]
        mock_calculate_average.return_value = 25.50
        
        with patch('builtins.print') as mock_print:
            main.main()
        
        mock_print.assert_called_once_with("The average value of the orders is: 25.50")
    
    @patch('main.OrderService.get_orders')
    def test_main_api_failure(self, mock_get_orders):
        """Testing main() with API failure"""
        mock_get_orders.side_effect = requests.RequestException("API Error")
        
        with patch('builtins.print') as mock_print:
            main.main()
        
        mock_print.assert_called_once_with("API request failed: API Error")

if __name__ == '__main__':
    unittest.main(verbosity=2)