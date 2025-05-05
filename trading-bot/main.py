#Below code v2
from core.trading_bot import TradingBot
from data.data_manager import DataManager
from execution.execution_handler import ExecutionHandler
from risk.risk_manager import RiskManager
from execution.portfolio_info import PortfolioInfo
from strategies.simple_strategy import SimpleMovingAverageStrategy
from utils.logger import setup_logger
from config.settings import ConfigManager
import argparse
import os

def main():

    config = ConfigManager('config.json')
    
    # Check and update some values
    # print(f"Test mode: {config.get('trading', 'test_mode')}")
    # config.set('trading', 'symbols', ['BTCUSDT'])
    # config.save_config()

    if not config.validate():
        return

    log_path = config.get('logging', 'file_path', 'logs/bot.log')
    log_level = config.get('logging', 'level', 'INFO')
    logger = setup_logger('trading_bot',log_path,log_level)

    # # Get API credentials
    # api_key = config.get('api', 'key') or os.environ.get('BINANCE_API_KEY', '')
    # api_secret = config.get('api', 'secret') or os.environ.get('BINANCE_API_SECRET', '')

    # Get trading parameters
    test_mode = config.get('trading', 'test_mode', True)
    symbols = config.get('trading', 'symbols', ['BTCUSDT'])
    interval = config.get('trading', 'interval', '5m')
    check_interval = config.get('trading', 'check_interval_seconds', 60)
    
    # Configure strategy
    strategy_params = config.get('strategy', 'params', {})
    strategy = SimpleMovingAverageStrategy(
        short_window=strategy_params.get('short_window', 50),
        long_window=strategy_params.get('long_window', 200)
    )
    
    # Configure risk management
    risk_params = config.get('risk_management')
    risk_manager = RiskManager(
        max_position_size=risk_params.get('max_position_size', 0.1),
        stop_loss_pct=risk_params.get('stop_loss_pct', 0.05)
    )

    data_manager = DataManager()
    execution_handler = ExecutionHandler()
    portfolio_info = PortfolioInfo()

    bot = TradingBot(
        data_manager=data_manager,
        strategy=strategy,
        execution_handler=execution_handler,
        logger=logger,
        portfolio_info =portfolio_info,
        risk_manager=risk_manager,
        fetch_interval=check_interval,
        interval=interval,
        test_mode=test_mode,
        symbols=symbols
    )
    # Overwrite the strategy and risk manager
    bot.strategy = strategy
    bot.risk_manager = risk_manager

    bot.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Execute functions from MakeMeRich.")
    parser.add_argument(
        "function",
        choices=["run_bot", "sell_all_assets_to_target", "get_portfolio", "get_value_portfolio"],
        help="Specify the function to run"
    )
    args = parser.parse_args()

    if args.function == "run_bot":
        main()

    if args.function == "sell_all_assets_to_target":
        ExecutionHandler().sell_all_assets_to_target('USDT')
    
    if args.function == "get_portfolio":
        coin_values = PortfolioInfo().get_portfolio('USDT')
        print(coin_values)
    
    if args.function == "get_value_portfolio":
        coin_values = PortfolioInfo().get_portfolio('USDT')
        grand_usdt_total = sum(map(lambda coin_usdt_value: coin_usdt_value[1], coin_values))
        print(grand_usdt_total)



# import time
# from binance.client import Client
# from binance.enums import *
# from binance.helpers import interval_to_milliseconds
# from dotenv import load_dotenv
# import os
# import logging
# from collections import deque
# import numpy as np
# import pandas as pd
# from scipy.stats import zscore


# # # # Charger les clés API depuis .env
# # # load_dotenv(override = True)

# # # USE_TESTNET = os.getenv("USE_TESTNET", "True").lower() == "true"
# # # # Initialiser le client Binance
# # # if USE_TESTNET:
# # #     API_KEY = os.getenv("BINANCE_API_KEY_TEST")
# # #     API_SECRET = os.getenv("BINANCE_API_SECRET_TEST")
# # #     client = Client(API_KEY, API_SECRET, testnet=True)
# # #     client.API_URL = 'https://testnet.binance.vision/api'
    
# # #     # # #Clear account to USDT
# # #     # account_balances = client.get_account()['balances']
# # #     # for coin_balance in account_balances:
# # #     #     # Get the coin symbol and the free and locked balance of each coin
# # #     #     coin_symbol = coin_balance['asset']
# # #     #     unlocked_balance = float(coin_balance['free'])
# # #     #     locked_balance = float(coin_balance['locked'])
# # #     #     place_sell_order(coin_symbol,unlocked_balance)

# # # else:
# # #     API_KEY = os.getenv("BINANCE_API_KEY")
# # #     API_SECRET = os.getenv("BINANCE_API_SECRET")
# # #     client = Client(API_KEY, API_SECRET)
# # #     client.API_URL = 'https://api.binance.com'


# # # # ---- Config ----
# # # SYMBOL = 'BTCUSDT'
# # # INTERVAL = '1m'
# # # INTERVAL_ms= interval_to_milliseconds(INTERVAL)

# # # INTERVAL = 1 * 60  # 1 minutes en secondes
# # TRADE_SIZE = 0.001  # BTC amount for simulation


# # # ---- Logging setup ----
# # logging.basicConfig(
# #     filename='log.txt',
# #     level=logging.INFO,
# #     format='%(asctime)s - %(levelname)s - %(message)s'
# # )

# # ---- State ----
# portfolio = {'usd': 1000.0, 'btc': 0.0}
# price_history = []
# regret_log = []

# # def fetch_latest_price(symbol):
# #     klines = client.get_klines(symbol=symbol, interval=INTERVAL, limit=2)
# #     close_price = float(klines[-1][4])
# #     return close_price

# # def simulate_trade(price, quantity, action):  # action: 'buy' or 'sell'
# #     global portfolio
# #     if action == 'buy' and portfolio['usd'] >= price * TRADE_SIZE:
# #         portfolio['btc'] += TRADE_SIZE
# #         portfolio['usd'] -= price * TRADE_SIZE
# #         place_buy_order(SYMBOL, quantity)

# #     elif action == 'sell' and portfolio['btc'] >= TRADE_SIZE:
# #         portfolio['btc'] -= TRADE_SIZE
# #         portfolio['usd'] += price * TRADE_SIZE
# #         place_sell_order(SYMBOL, quantity)

# def get_value_portfolio(): #Value of the entire portfolio

#     # Retrieve the balances of all coins in the user’s Binance account
#     account_balances = client.get_account()['balances']
#     # print('account_balances ', account_balances)
#     # Get the current price of all tickers from the Binance API
#     ticker_info = client.get_all_tickers()

#     # Create a dictionary of tickers and their corresponding prices
#     ticker_prices = {ticker['symbol']: float(ticker['price']) for ticker in ticker_info}
#     # print('ticker_prices ', ticker_prices)

#     # Calculate the USDT value of each coin in the user’s account
#     coin_values = []

#     for coin_balance in account_balances:
#         # Get the coin symbol and the free and locked balance of each coin
#         coin_symbol = coin_balance['asset']
#         unlocked_balance = float(coin_balance['free'])
#         locked_balance = float(coin_balance['locked'])

#         # If the coin is USDT and the total balance is greater than 1, add it to the list of coins with their USDT values
#         if coin_symbol == 'USDT' and unlocked_balance + locked_balance > 1:
#             coin_values.append(('USDT', (unlocked_balance + locked_balance)))
#         # Otherwise, check if the coin has a USDT trading pair or a BTC trading pair
#         elif unlocked_balance + locked_balance > 0.0:
#         # Check if the coin has a USDT trading pair
#             if (any(coin_symbol + 'USDT' in i for i in ticker_prices)):
#                 # If it does, calculate its USDT value and add it to the list of coins with their USDT values
#                 ticker_symbol = coin_symbol + 'USDT'
#                 ticker_price = ticker_prices.get(ticker_symbol)
#                 coin_usdt_value = (unlocked_balance + locked_balance) * ticker_price
#                 if coin_usdt_value > 1:
#                     coin_values.append((coin_symbol, coin_usdt_value))
#             # If the coin does not have a USDT trading pair, check if it has a BTC trading pair
#             elif (any(coin_symbol + 'BTC' in i for i in ticker_prices)):
#                 # If it does, calculate its USDT value and add it to the list of coins with their USDT values
#                 ticker_symbol = coin_symbol + 'BTC'
#                 ticker_price = ticker_prices.get(ticker_symbol)
#                 coin_usdt_value = (unlocked_balance + locked_balance) * ticker_price * ticker_prices.get('BTCUSDT')
#                 if coin_usdt_value > 1:
#                     coin_values.append((coin_symbol, coin_usdt_value))

#     # Sort the list of coins and their USDT values by USDT value in descending order
#     coin_values.sort(key=lambda x: x[1], reverse=True)
#     grand_usdt_total = sum(map(lambda coin_usdt_value: coin_usdt_value[1], coin_values))

#     return grand_usdt_total


# def regret(current_value, best_value_seen):
#     return max(0, best_value_seen - current_value)

# def place_buy_order(symbol, quantity):
#     logging.info("🔄 PLACING BUY ORDER")
#     order = client.create_order(
#         symbol=symbol,
#         side=SIDE_BUY,
#         type=ORDER_TYPE_MARKET,
#         quantity=quantity  # À ajuster selon ton solde
#     )
#     logging.info("✅ ORDER SENT")

# def place_sell_order(symbol, quantity):
#     logging.info("🔄 PLACING SELL ORDER")
#     order = client.create_order(
#         symbol=symbol,
#         side=SIDE_SELL,
#         type=ORDER_TYPE_MARKET,
#         quantity=quantity  # Ajuste selon ton solde
#     )
#     logging.info("✅ ORDER SENT")

# def compute_entropy(prices, bins=10, window=100): #GPT: Should we base it on simple returns or even log price?
#     if len(prices) < window:
#         return 0  # not enough data for meaningful histogram
#     hist, _ = np.histogram(prices[-window:], bins=bins, density=True)
#     hist = hist[hist > 0]  # filter out zero entries
#     entropy = -np.sum(hist * np.log(hist))
#     return entropy

# def select_action():
#     entropy = compute_entropy(price_history, bins=10, window=100)
#     logging.info(f"🔍 Entropy: {entropy:.4f}")

#     scores = {}
#     for action in action_stats:
#         regrets = action_stats[action]['regrets']
#         if regrets:
#             avg_regret = np.mean(regrets)
#             std_regret = np.std(regrets)
#             base_score = std_regret - avg_regret
#         else:
#             base_score = 1.0  # Encourage unexplored actions

#         # Entropy-based bias
#         if entropy < 1.0:
#             if action in ['buy', 'sell']:
#                 base_score += 0.5
#         else:
#             if action == 'hold':
#                 base_score += 0.5

#         scores[action] = base_score

#     # Normalize scores for numerical stability before softmax
#     score_values = np.array(list(scores.values()))
#     norm_scores = zscore(score_values) if len(score_values) > 1 else score_values
#     exps = np.exp(norm_scores)
#     probs = exps / np.sum(exps)

#     # Log probabilities
#     for a, p in zip(scores.keys(), probs):
#         logging.info(f"📊 Action '{a}' probability: {p:.4f}")

#     chosen = np.random.choice(list(scores.keys()), p=probs)
#     return chosen


# def main():

#     logging.info("📈 Starting trading bot...")
#     best_value = get_value_portfolio()
#     prev_action = None

#     while True:
#         try:
            
#             #Retrieve price
#             price = fetch_latest_price(SYMBOL)
#             price_history.append(price)
#             logging.info(f"Current price of {SYMBOL}: {price} USD")

#             # Action selector
#             action = select_action()
#             if action != 'hold':
#                 simulate_trade(price, TRADE_SIZE, action)
#             else:
#                 logging.info("⏳ HOLD POSITION")

#             value = get_value_portfolio()
#             best_value = max(best_value, value)
#             reg = regret(value, best_value)

#             # ✅ Assign regret to the previous action, not the current one
#             if prev_action:
#                 action_stats[prev_action]['regrets'].append(reg)


#             regret_log.append(reg)
#             prev_action = action  # Save for next cycle

#             logging.info(f"Price: {price:.2f} | Portfolio Value: {value:.2f} | Regret: {reg:.4f}")
            
#             logging.info(f"⏳ Waiting {INTERVAL_ms / 60000:.0f} minutes...\n")
#             time.sleep(INTERVAL_ms/1000)

#         except KeyboardInterrupt:
#             logging.info("⚠️ Stopped.")
#             logging.info(str(action_stats))
#             break

#         except Exception as e:
#             logging.info(f"⚠️ Error: {e}")
#             time.sleep(5)

# if __name__ == "__main__":

#     main()