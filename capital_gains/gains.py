from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import requests
import logging

logging.basicConfig(level=logging.DEBUG)
# Load environment variables from .env file outside the app folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

# Flask App Initialization
app = Flask(__name__)

STOCKS1_API_URL = 'http://stocks1:8000/stocks'
STOCKS1_PORTFOLIO = 'stocks1'

# Configuration
NINJA_API_KEY = "0WmrbDjfZIsC3HyQ57AAVw==XrgmjX1A3aNZsahJ"

# Utility functions
def get_stock_price(symbol):
    symbol = symbol.strip('"').strip("'")  
    """Retrieve the current price of a stock using the Ninja API."""
    url = f"https://api.api-ninjas.com/v1/stockprice?ticker={symbol}"
    headers = {"X-Api-Key": NINJA_API_KEY}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        logging.debug(f"fetched stock value for {symbol}")
        return data.get('price', None)
    else:
        raise Exception(f"API response code {response.status_code}")

@app.route('/capital-gains', methods=['GET'])
def capital_gains():
    try:
        portfolio_filter = request.args.get('portfolio')
        numsharesgt_filter = request.args.get('numsharesgt', type=int)
        numshareslt_filter = request.args.get('numshareslt', type=int)
        total_capital_gains = 0
        # Log query params
        app.logger.debug(f"Received query params: portfolio={portfolio_filter}, numsharesgt={numsharesgt_filter}, numshareslt={numshareslt_filter}")
        # Determine which stock portfolio to fetch
        if portfolio_filter == STOCKS1_PORTFOLIO:
            stocks_url = STOCKS1_API_URL
        else:
            stocks_url = None

        # Get stocks from the relevant portfolio, or both if no portfolio filter
        if stocks_url:
            logging.debug(f"fetching stocks from {stocks_url}")
            stocks_response = requests.get(stocks_url)
            stocks = stocks_response.json() if stocks_response.status_code == 200 else []
        else:
            logging.debug(f"fetching stocks from both portfolios")
            stocks1_response = requests.get(STOCKS1_API_URL)
            stocks = stocks1_response.json()

        # Filter stocks based on number of shares if necessary
        if numsharesgt_filter:
            logging.debug(f"got stocks greather than {numsharesgt_filter}")
            stocks = [stock for stock in stocks if stock["shares"] > numsharesgt_filter]
        if numshareslt_filter:
            logging.debug(f"got stocks less than {numshareslt_filter}")
            stocks = [stock for stock in stocks if stock["shares"] < numshareslt_filter]

        # Calculate capital gains for the selected stocks
        for stock in stocks:
            purchase_price = stock["purchase price"]
            shares = stock["shares"]
            symbol = stock["symbol"]
            stock_value = get_stock_price(symbol)
            capital_gain = stock_value - purchase_price
            logging.debug(f"capital gain for {symbol}: {capital_gain}")
            total_capital_gains += (capital_gain*shares)

        return jsonify({"total_capital_gains": round(total_capital_gains, 2)}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching stocks data: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


