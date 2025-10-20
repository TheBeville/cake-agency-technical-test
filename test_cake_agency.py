import unittest
from unittest.mock import patch, Mock
from order_model import OrderModel
from order_service import OrderService
import main

class TestOrderModel(unittest.TestCase):
    """Test cases for OrderModel class."""
    
    def test_order_model_initialization(self):
        """Test OrderModel object creation."""

        items = [{"name": "Cake", "price": "25.00"}]
        order = OrderModel(
            id="123",
            created_at="2025-10-20T10:00:00Z",
            items=items,
            items_value=25.00
        )
        
        self.assertEqual(order.id, "123")
        self.assertEqual(order.created_at, "2025-10-20T10:00:00Z")
        self.assertEqual(order.items, items)
        self.assertEqual(order.items_value, 25.00)
    
    def test_order_model_repr(self):
        """Test OrderModel string representation."""

        items = [{"name": "Cake", "price": "25.00"}]
        order = OrderModel(id="123", created_at="2025-10-20T10:00:00Z", items=items, items_value=25.00)
        
        expected = "OrderModel(id='123', items_value=25.0, items_count=1)"
        self.assertEqual(repr(order), expected)

class TestOrderService(unittest.TestCase):
    """Test cases for OrderService class."""
    
    def setUp(self):
        """Set up test data."""

        self.valid_data = {
            "orders": [
                {
                    "id": "1",
                    "created_at": "2025-10-20T10:00:00Z",
                    "items": [
                        {"name": "Chocolate Cake", "price": "25.50"},
                        {"name": "Vanilla Cake", "price": "22.00"}
                    ]
                },
                {
                    "id": "2",
                    "created_at": "2025-10-20T11:00:00Z",
                    "items": [
                        {"name": "Red Velvet Cake", "price": "30.00"}
                    ]
                }
            ]
        }
    
    def test_parse_orders_valid_data(self):
        """Test parsing valid order data."""

        result = OrderService.parse_orders(self.valid_data)
        # Average: (25.50 + 22.00 + 30.00) / 2 = 38.75
        self.assertEqual(result, "38.75")
    
    def test_parse_orders_empty_orders(self):
        """Test parsing data with no orders."""

        data = {"orders": []}
        result = OrderService.parse_orders(data)
        self.assertEqual(result, "0.00")
    
    def test_parse_orders_invalid_data_format(self):
        """Test parsing invalid data format."""

        with self.assertRaises(ValueError):
            OrderService.parse_orders("invalid")
        
        with self.assertRaises(ValueError):
            OrderService.parse_orders({"no_orders_key": []})
    
    def test_parse_orders_with_invalid_items(self):
        """Test parsing orders with invalid item data."""

        data = {
            "orders": [
                {
                    "id": "1",
                    "created_at": "2025-10-20T10:00:00Z",
                    "items": [
                        {"name": "Valid Cake", "price": "25.00"},
                        {"name": "Invalid Cake", "price": "invalid_price"},
                        "invalid_item"
                    ]
                }
            ]
        }
        result = OrderService.parse_orders(data)
        self.assertEqual(result, "25.00")  # Only the valid price (25.00) should be counted

class TestMain(unittest.TestCase):
    """Test cases for main module functions."""
    
    @patch('main.requests.get')
    def test_call_api_success(self, mock_get):
        """Test successful API call."""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = main.call_api()
        
        self.assertEqual(result, mock_response)
        mock_get.assert_called_once_with("https://fauxdata.codelayer.io/api/orders")
    
    @patch('main.requests.get')
    def test_call_api_failure(self, mock_get):
        """Test API call failure."""

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            main.call_api()
    
    @patch('main.OrderService.parse_orders')
    def test_handle_response_success(self, mock_parse_orders):
        """Test successful response handling."""

        mock_parse_orders.return_value = "25.50"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"orders": []}
        
        result = main.handle_response(mock_response)
        
        self.assertEqual(result, "25.50")
        mock_parse_orders.assert_called_once()
    
    def test_handle_response_server_error(self):
        """Test handling server error response."""

        mock_response = Mock()
        mock_response.status_code = 500
        
        result = main.handle_response(mock_response)
        
        self.assertIsNone(result)
    
    def test_handle_response_unhandled_status(self):
        """Test handling unhandled status codes."""

        mock_response = Mock()
        mock_response.status_code = 404
        
        result = main.handle_response(mock_response)
        
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main(verbosity=2)