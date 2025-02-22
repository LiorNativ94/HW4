from flask import Flask, jsonify, request
from dotenv import load_dotenv
from datetime import datetime
import os
import requests
import pymongo
from bson.objectid import ObjectId

# Load environment variables from .env file outside the app folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

#MongoDB connection Setup
client = pymongo.MongoClient("mongodb://mongo:27017/")
db = client["myDB"]
stocks_collection = db["stocks"]

# Flask App Initialization
app = Flask(__name__)

# Configuration
NINJA_API_KEY = os.getenv('NINJA_API_KEY')

# Utility functions
def get_stock_price(symbol):
    symbol = symbol.strip('"').strip("'")  
    """Retrieve the current price of a stock using the Ninja API."""
    url = f"https://api.api-ninjas.com/v1/stockprice?ticker={symbol}"
    headers = {"X-Api-Key": NINJA_API_KEY}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('price', None)
    else:
        raise Exception(f"API response code {response.status_code}")

# Routes
@app.route('/stocks', methods=['POST'])
def add_stock():
    """Add a new stock to the portfolio."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Expected json media type"}), 415

    # Validate required fields
    required_fields = {'symbol':str, 'purchase price': float, 'shares': int}

    for field, field_type in required_fields.items():
        if field not in data:
            return jsonify({"error:"f"missing required field: {field}"}), 415
        if not isinstance(data[field], field_type):
            return jsonify({"error:":f"field {field} must be of type {field_type.__name__}"}), 415

    #Validate stock symbol
    symbol = data['symbol'].upper()
    # Check for duplicate symbol
    if stocks_collection.find_one({"symbol": symbol}):
        return jsonify({"error": "Stock symbol already exists"}), 400


    # Insert stock into MongoDB
    stock = {
        "name": data.get("name", "NA"),
        "symbol": symbol,
        "purchase price": round(data["purchase price"], 2),
        "purchase date": data.get("purchase date", "NA"),
        "shares": data["shares"]
    }
    result = stocks_collection.insert_one(stock)
    return jsonify({"id": str(result.inserted_id)}), 201


@app.route('/stocks', methods=['GET'])
def get_stocks():
    """Get all stocks in the portfolio."""
    try:
        stocks = list(stocks_collection.find())
        for stock in stocks:
            stock["_id"] = str(stock["_id"])
        return jsonify(stocks), 200
    except Exception as e:
        return jsonify({"server error": str(e)}), 500

@app.route('/stocks/<string:stock_id>', methods=['GET'])
def get_stock(stock_id):
    """Retrieve a stock by its ID."""
    try:
        stock = stocks_collection.find_one({"_id": ObjectId(stock_id)})
        if not stock:
            return jsonify({"error": "Not found"}), 404
        stock["_id"] = str(stock["_id"])
        return jsonify(stock), 200
    except RuntimeError as e:
        return jsonify({"server error": str(e)}), 500

@app.route('/stocks/<string:stock_id>', methods=['PUT'])
def update_stock(stock_id):
    """Update an existing stock."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Malformed data"}), 400
    try:
        stock = stocks_collection.find_one({"_id": ObjectId(stock_id)})
        if not stock:
            return jsonify({"error": "Not found"}), 404
        if 'id' not in data:
            return jsonify({"error":"missing required field: id"}), 415
        if stock_id != data['id']:
            return jsonify({"error":"not allowed to change id"}), 400
         # Validate required fields and their field type
        required_fields = {'id':str,'name':str,'symbol':str, 'purchase price': float,'purchase date':str, 'shares': int}
        for field, field_type in required_fields.items():
            if field not in data:
                return jsonify({"error:"f"missing required field: {field}"}), 415
            if not isinstance(data[field], field_type):
                return jsonify({"error:":f"field {field} must be of type {field_type.__name__}"}), 415
        
        # Update stock
        updated_data = {
            "name": data["name"],
            "symbol": data["symbol"].upper(),
            "purchase price": round(data["purchase price"], 2),
            "purchase date": data["purchase date"],
            "shares": data["shares"]
        }
        stocks_collection.update_one({"_id": ObjectId(stock_id)}, {"$set": updated_data})
        return jsonify({"id": stock_id}), 200
        
    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@app.route('/stocks/<string:stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    """Delete a stock from the portfolio."""
    try:
        result = stocks_collection.delete_one({"_id": ObjectId(stock_id)})
        if result.deleted_count == 0:
            return jsonify({"error": "Not found"}), 404
        return '', 204
    except RuntimeError as e:
        return jsonify({"server error": str(e)}), 500


@app.route('/stock-value/<string:stock_id>', methods=['GET'])
def get_stock_value(stock_id):
    """Retrieve the current value of a stock."""
    try:
        stock = stocks_collection.find_one({"_id": ObjectId(stock_id)})
        if not stock:
            return jsonify({"error": "Not found"}), 404
        
        # Fetch current stock price using it's symbol
        ticker_price = get_stock_price(stock["symbol"])
        stock_value = round(ticker_price * stock["shares"], 2)
        return jsonify({
            "symbol": stock["symbol"],
            "ticker": round(ticker_price, 2),
            "stock value": stock_value
        }), 200
    except Exception as e:
        return jsonify({"server error": str(e)}), 500


@app.route('/portfolio-value', methods=['GET'])
def get_portfolio_value():
    """Calculate the total value of the portfolio."""
    try:
        total_value = 0
        stocks = list(stocks_collection)
        for stock in stocks:
            ticker_price = get_stock_price(stock["symbol"])
            total_value += ticker_price * stock["shares"]
        
        return jsonify({
            "date": datetime.now().strftime("%d-%m-%Y"),
            "portfolio value": round(total_value, 2)
        }), 200
    except Exception as e:
        return jsonify({"server error": str(e)}), 500

@app.route('/kill', methods =['GET'])
def kill_container():
    os._exit(1)
