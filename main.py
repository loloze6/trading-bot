import logging
#Test
from binance.client import Client
from binance.enums import *
import time
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Set up logging
logging.basicConfig(filename="bot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

client = Client(API_KEY, API_SECRET, testnet=True)  # Use testnet for safety

# Function to place a test order (simulated buy/sell)
def place_order(order_type):
    logging.info(f"{order_type} Order Simulated!")
    print(f"{order_type} Order Simulated!")

# Function to fetch and log market prices
def fetch_price(symbol="BTCUSDT"):
    price = client.get_symbol_ticker(symbol=symbol)
    logging.info(f"Price for {symbol}: {price['price']}")
    print(f"Price for {symbol}: {price['price']}")
    return price

# Main trading loop
def main():
    while True:
        try:
            # Simulate a trading action
            fetch_price()
            place_order("BUY")
            time.sleep(10)  # Wait for 10 seconds before repeating

        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
