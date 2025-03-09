# from data import stocks
# import requests
# import pytest

# BASE_URL = "http://localhost:5001"

# STOCK2_ID = None

# def test_post_stocks():
#     # Prepare the stock data for the POST requests
#     stock_data = [
#         stocks["stock1"],
#         stocks["stock2"],
#         stocks["stock3"]
#     ]

#     # List to hold the response IDs
#     response_ids = []

#     for stock in stock_data:
#         # Send POST request to /stock endpoint
#         response = requests.post(f"{BASE_URL}/stocks", json=stock)
        
#         # Check if the status code is 201
#         assert response.status_code == 201, f"Expected status code 201 but got {response.status_code} for {stock['name']}"
        
#         # Extract the ID from the response
#         response_json = response.json()
#         response_ids.append(response_json.get("id"))  # Assuming the response contains an "id" field

#     # Check that all IDs are unique
#     assert len(response_ids) == len(set(response_ids)), "Response IDs are not unique"

# def get_all_stocks_id():
#     # Execute a GET request for all stocks
#     response = requests.get(f"{BASE_URL}/stocks")  # Adjust the URL as necessary
#     response_json = response.json()
    
#     # Extract the IDs from the response
#     stock_ids = [stock["_id"] for stock in response_json]  # Assuming each stock has an "_id" field
#     return stock_ids

# def test_get_stock_by_id():
#     stock_ids = get_all_stocks_id()  # Get all stock IDs
#     stock_id = stock_ids[0]  # Assuming you want to test the first stock ID

#     # Execute a GET request for the specific stock ID
#     response = requests.get(f"{BASE_URL}/stocks/{stock_id}")  # Adjust the URL as necessary
#     response_json = response.json()
    
#     # Check if the symbol field equals "NVDA"
#     assert response_json["symbol"] == "NVDA", f"Expected symbol 'NVDA' but got {response_json['symbol']}"
#     # Check if the status code is 200
#     assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

# def test_get_all_stocks():
#     # Execute a GET request for all stocks
#     response = requests.get(f"{BASE_URL}/stocks")  # Adjust the URL as necessary
#     response_json = response.json()
    
#     # Check if the returned JSON object has 3 embedded JSON objects (stocks)
#     assert len(response_json) == 3, f"Expected 3 stocks but got {len(response_json)}"
#     # Check if the status code is 200
#     assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"

# def test_get_stock_value():
#     stock_ids = get_all_stocks_id()  # Get all stock IDs
#     stock_values = []

#     # Execute GET requests for stock values
#     for i, stock_id in enumerate(stock_ids):
#         response = requests.get(f"{BASE_URL}/stock-value/{stock_id}")  # Adjust the URL as necessary
#         response_json = response.json()
        
#         # Check if the status code is 200
#         assert response.status_code == 200, f"Expected status code 200 but got {response.status_code} for stock ID {stock_id}"
        
#         # Store the stock value
#         stock_values.append(response_json["stock value"])

#         # Check if the symbol field matches
#         expected_symbols = ["NVDA", "AAPL", "GOOG"]
#         assert response_json["symbol"] == expected_symbols[i], f"Expected symbol '{expected_symbols[i]}' but got '{response_json['symbol']}'"

#     return stock_values  # Return the list of stock values

# def test_get_portfolio_value():
#     # Execute a GET request for portfolio value
#     response = requests.get(f"{BASE_URL}/portfolio-value")  # Adjust the URL as necessary
#     response_json = response.json()
    
#     # Check if the status code is 200
#     assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
#     # Get the portfolio value
#     pv = response_json["portfolio value"]
    
#     # Get stock values from the previous test
#     stock_values = test_get_stock_value()  # Call the previous test to get stock values
#     sv_total = sum(stock_values)  # Calculate the total stock value

#     # Check the portfolio value condition
#     assert pv * 0.97 <= sv_total <= pv * 1.03, f"Portfolio value condition failed: {pv * 0.97} <= {sv_total} <= {pv * 1.03}"

# def test_post_stock7_missing_symbol():
#     stock = stocks["stock7"]
#     response = requests.post(f"{BASE_URL}/stocks", json=stock)
#     assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}"

# def test_delete_stock2():
#     global STOCK2_ID
#     stock_ids = get_all_stocks_id()  # Get all stock IDs
#     stock2_id = stock_ids[1]  # Assuming stock2 is the second stock
#     STOCK2_ID = stock2_id
#     response = requests.delete(f"{BASE_URL}/stocks/{stock2_id}")
#     assert response.status_code == 204, f"Expected status code 204 but got {response.status_code}"

# def test_get_stock2_after_deletion():
#     global STOCK2_ID
#     response = requests.get(f"{BASE_URL}/stocks/{STOCK2_ID}")
#     assert response.status_code == 404, f"Expected status code 404 but got {response.status_code}"

# def test_post_stock8_incorrect_date_format():
#     stock = stocks["stock8"]
#     response = requests.post(f"{BASE_URL}/stocks", json=stock)
#     assert response.status_code == 400, f"Expected status code 400 but got {response.status_code}"

# # Main function to run tests in order
# if __name__ == "__main__":
#     test_post_stocks()
#     test_get_stock_by_id()
#     test_get_all_stocks()
#     test_get_stock_value()
#     test_get_portfolio_value()
#     test_post_stock7_missing_symbol()
#     test_delete_stock2()
#     test_get_stock2_after_deletion()
#     test_post_stock8_incorrect_date_format()


# Tester code

import requests
import pytest

BASE_URL = "http://localhost:5001" 

# Stock data
stock1 = { "name": "NVIDIA Corporation", "symbol": "NVDA", "purchase price": 134.66, "purchase date": "18-06-2024", "shares": 7 }
stock2 = { "name": "Apple Inc.", "symbol": "AAPL", "purchase price": 183.63, "purchase date": "22-02-2024", "shares": 19 }
stock3 = { "name": "Alphabet Inc.", "symbol": "GOOG", "purchase price": 140.12, "purchase date": "24-10-2024", "shares": 14 }

def test_post_stocks():
    response1 = requests.post(f"{BASE_URL}/stocks", json=stock1)
    response2 = requests.post(f"{BASE_URL}/stocks", json=stock2)
    response3 = requests.post(f"{BASE_URL}/stocks", json=stock3)
    
    assert response1.status_code == 201
    assert response2.status_code == 201
    assert response3.status_code == 201

    # Ensure unique IDs
    data1 = response1.json()
    data2 = response2.json()
    data3 = response3.json()
    assert data1['id'] != data2['id']
    assert data1['id'] != data3['id']
    assert data2['id'] != data3['id']

def test_get_stocks():
    response = requests.get(f"{BASE_URL}/stocks")
    assert response.status_code == 200
    stocks = response.json()
    assert len(stocks) == 3 
    
def test_get_portfolio_value():
    response = requests.get(f"{BASE_URL}/portfolio-value")
    assert response.status_code == 200
    portfolio_value = response.json()
    assert portfolio_value['portfolio value'] > 0  # Portfolio value should be greater than 0

def test_post_stocks_invalid_data():
    stock_invalid = { "name": "Amazon", "purchase price": 100.50, "purchase date": "15-03-2025", "shares": 50 }
    response = requests.post(f"{BASE_URL}/stocks", json=stock_invalid)
    assert response.status_code == 400
