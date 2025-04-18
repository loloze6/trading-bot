import time
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv
import os
import logging
from collections import deque

prices = deque(maxlen=3)  # pour une moyenne mobile simple


# Configurer le logging
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Charger les clés API depuis .env
load_dotenv()

USE_TESTNET = os.getenv("USE_TESTNET", "True").lower() == "true"

# Initialiser le client Binance
if USE_TESTNET:
    API_KEY = os.getenv("BINANCE_API_KEY_TEST")
    API_SECRET = os.getenv("BINANCE_API_SECRET_TEST")
    client = Client(API_KEY, API_SECRET)
    client.API_URL = 'https://testnet.binance.vision/api'

else:
    API_KEY = os.getenv("BINANCE_API_KEY")
    API_SECRET = os.getenv("BINANCE_API_SECRET")
    client = Client(API_KEY, API_SECRET)
    client.API_URL = 'https://testnet.binance.vision/api'


SYMBOL = "BTCUSDT"
INTERVAL = 1 * 60  # 15 minutes en secondes

# Critère d'achat simple : si le prix baisse d'au moins 0.5% depuis le dernier
last_price = None

def get_price(symbol):
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def place_test_order(symbol):
    logging.info("🔄 PLACING TEST BUY ORDER")
    order = client.create_test_order(
        symbol=symbol,
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=0.001  # À ajuster selon ton solde
    )
    logging.info("✅ ORDER SIMULATED")

def place_test_sell_order(symbol):
    print("🔄 PLACING TEST SELL ORDER")
    order = client.create_test_order(
        symbol=symbol,
        side=SIDE_SELL,
        type=ORDER_TYPE_MARKET,
        quantity=0.001  # Ajuste selon ton solde
    )
    print("✅ SELL ORDER SIMULATED")
    logging.info("SELL order simulated")


def trading_loop():
    global last_price
    logging.info("📈 Starting trading bot...")

    while True:
        try:
            price = get_price(SYMBOL)
            logging.info(f"Current price of {SYMBOL}: {price} USD")

            prices.append(price)
            if len(prices) == 3:
                average_price = sum(prices) / 3
                logging.info(f"📊 Moyenne mobile 3 dernières : {average_price:.2f}")


                if price > average_price * 1.01:
                    logging.info("🚀 Prix dépasse la moyenne → SELL")
                    place_test_sell_order(SYMBOL)
                elif price < average_price * 0.99:
                    logging.info("💸 Prix sous la moyenne → BUY")
                    place_test_order(SYMBOL)

            last_price = price
        except Exception as e:
            logging.info(f"⚠️ Error: {e}")

        logging.info(f"⏳ Waiting {INTERVAL / 60:.0f} minutes...\n")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    trading_loop()