from data import stocks
import requests

# Define the base URL for your API
BASE_URL = "http://localhost:5001"  # Adjust this URL based on your setup

def get_stocks_id():

    response_ids = []



def test_post_stocks():
    # Prepare the stock data for the POST requests
    stock_data = [
        stocks["stock1"],
        stocks["stock2"],
        stocks["stock3"]
    ]

    # List to hold the response IDs
    response_ids = []

    for stock in stock_data:
        # Send POST request to /stock endpoint
        response = requests.post(f"{BASE_URL}/stock", json=stock)
        
        # Check if the status code is 201
        assert response.status_code == 201, f"Expected status code 201 but got {response.status_code} for {stock['name']}"
        
        # Extract the ID from the response
        response_json = response.json()
        response_ids.append(response_json.get("id"))  # Assuming the response contains an "id" field

    # Check that all IDs are unique
    assert len(response_ids) == len(set(response_ids)), "Response IDs are not unique"

def get_all_stocks_id():
    # Execute a GET request for all stocks
    response = requests.get(f"{BASE_URL}/stocks")  # Adjust the URL as necessary
    response_json = response.json()
    
    # Extract the IDs from the response
    stock_ids = [stock["_id"] for stock in response_json]  # Assuming each stock has an "_id" field
    return stock_ids

def test_get_stock_by_id():
    stock_ids = get_all_stocks_id()  # Get all stock IDs
    stock_id = stock_ids[0]  # Assuming you want to test the first stock ID

    # Execute a GET request for the specific stock ID
    response = requests.get(f"{BASE_URL}/stocks/{stock_id}")  # Adjust the URL as necessary
    response_json = response.json()
    
    # Check if the symbol field equals "NVDA"
    assert response_json["symbol"] == "NVDA", f"Expected symbol 'NVDA' but got {response_json['symbol']}"
    # Check if the status code is 200
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

def test_get_all_stocks():
    # Execute a GET request for all stocks
    response = requests.get(f"{BASE_URL}/stocks")  # Adjust the URL as necessary
    response_json = response.json()
    
    # Check if the returned JSON object has 3 embedded JSON objects (stocks)
    assert len(response_json) == 3, f"Expected 3 stocks but got {len(response_json)}"
    # Check if the status code is 200
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

def test_get_stock_value():
    stock_ids = get_all_stocks_id()  # Get all stock IDs
    stock_values = []

    # Execute GET requests for stock values
    for i, stock_id in enumerate(stock_ids):
        response = requests.get(f"{BASE_URL}/stock-value/{stock_id}")  # Adjust the URL as necessary
        response_json = response.json()
        
        # Check if the status code is 200
        assert response.status_code == 200, f"Expected status code 200 but got {response.status_code} for stock ID {stock_id}"
        
        # Store the stock value
        stock_values.append(response_json["stock value"])

        # Check if the symbol field matches
        expected_symbols = ["NVDA", "AAPL", "GOOG"]
        assert response_json["symbol"] == expected_symbols[i], f"Expected symbol '{expected_symbols[i]}' but got '{response_json['symbol']}'"

    return stock_values  # Return the list of stock values

def test_get_portfolio_value():
    # Execute a GET request for portfolio value
    response = requests.get(f"{BASE_URL}/portfolio-value")  # Adjust the URL as necessary
    response_json = response.json()
    
    # Check if the status code is 200
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
    # Get the portfolio value
    pv = response_json["portfolio value"]
    
    # Get stock values from the previous test
    stock_values = test_get_stock_value()  # Call the previous test to get stock values
    sv_total = sum(stock_values)  # Calculate the total stock value

    # Check the portfolio value condition
    assert pv * 0.97 <= sv_total <= pv * 1.03, f"Portfolio value condition failed: {pv * 0.97} <= {sv_total} <= {pv * 1.03}"

# Add more tests as needed

