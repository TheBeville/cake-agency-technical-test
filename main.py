import requests
from order_service import OrderService
from utils.order_values import calculate_average_order_value

def main() -> None:
    try:
        orders = OrderService.get_orders()
        average_value = calculate_average_order_value(orders)
        print(f"The average value of the orders is: {average_value:,.2f}")
    except requests.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()