import requests
from typing import Optional
from order_service import OrderService

def call_api() -> requests.Response:
    """Fetch orders data from the API."""
    response = requests.get("https://fauxdata.codelayer.io/api/orders")
    response.raise_for_status()
    return response

def handle_response(response: requests.Response) -> Optional[str]:
    """Process API response and calculate average order value."""
    try:
        if 200 <= response.status_code < 300:
            data = response.json()
            average_value = OrderService.parse_orders(data)
            print(f"The average value of the orders is: {average_value}")
            return average_value
        elif response.status_code == 500:
            print("Error occurred: 500 Server error")
            return None
        else:
            print(f"Unhandled status code: {response.status_code}")
            return None
    except (ValueError, KeyError) as e:
        print(f"Error parsing response data: {e}")
        return None

def main() -> None:
    """Main entry point."""
    try:
        response = call_api()
        handle_response(response)
    except requests.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()