from binance.client import Client
from config.settings import API_KEY, API_SECRET, USE_TESTNET
from typing import Dict, List, Optional, Union, Tuple
import logging

logger = logging.getLogger(__name__)  # Use the logger set up elsewhere


class PortfolioInfo:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)

        server_time = self.client.get_server_time()
        timestamp = server_time['serverTime']

    def get_portfolio(self, symbol): #Value of the entire portfolio
        try:
        # Retrieve the balances of all coins in the user’s Binance account
            account_balances = self.client.get_account()['balances']
            # print('account_balances ', account_balances)
            # Get the current price of all tickers from the Binance API
            ticker_info = self.client.get_all_tickers()

            # Create a dictionary of tickers and their corresponding prices
            ticker_prices = {ticker['symbol']: float(ticker['price']) for ticker in ticker_info}
            # print('ticker_prices ', ticker_prices)

            # Calculate the USDT value of each coin in the user’s account
            coin_values = []

            for coin_balance in account_balances:
                # Get the coin symbol and the free and locked balance of each coin
                coin_symbol = coin_balance['asset']
                unlocked_balance = float(coin_balance['free'])
                locked_balance = float(coin_balance['locked'])

                # If the coin is USDT and the total balance is greater than 1, add it to the list of coins with their USDT values
                if coin_symbol == symbol and unlocked_balance + locked_balance > 1:
                    coin_values.append((symbol, (unlocked_balance + locked_balance)))
                # Otherwise, check if the coin has a USDT trading pair or a BTC trading pair
                elif unlocked_balance + locked_balance > 0.0:
                # Check if the coin has a USDT trading pair
                    if (any(coin_symbol + symbol in i for i in ticker_prices)):
                        # If it does, calculate its USDT value and add it to the list of coins with their USDT values
                        ticker_symbol = coin_symbol + symbol
                        ticker_price = ticker_prices.get(ticker_symbol)
                        coin_usdt_value = (unlocked_balance + locked_balance) * ticker_price
                        if coin_usdt_value > 1:
                            coin_values.append((coin_symbol, coin_usdt_value))
                    # If the coin does not have a USDT trading pair, check if it has a BTC trading pair
                    elif (any(coin_symbol + 'BTC' in i for i in ticker_prices)):
                        # If it does, calculate its USDT value and add it to the list of coins with their USDT values
                        ticker_symbol = coin_symbol + 'BTC'
                        ticker_price = ticker_prices.get(ticker_symbol)
                        coin_usdt_value = (unlocked_balance + locked_balance) * ticker_price * ticker_prices.get(str('BTC'+symbol))
                        if coin_usdt_value > 1:
                            coin_values.append((coin_symbol, coin_usdt_value))

            # Sort the list of coins and their USDT values by USDT value in descending order
            coin_values.sort(key=lambda x: x[1], reverse=True)

            return coin_values
        
        except Exception as e:
            raise RuntimeError(f"Could not retrieve Portfolio Info: {e}")
        

    def get_account_balance(self) -> Dict[str, float]:
        """Get account balances."""
        try:
            info = self.client.get_account()
            balances = {}
            for asset in info['balances']:
                if float(asset['free']) > 0 or float(asset['locked']) > 0:
                    balances[asset['asset']] = {
                        'free': float(asset['free']),
                        'locked': float(asset['locked'])
                    }
            return balances
        except Exception as e:
            logger.error(f"Error fetching account balance: {e}")
            return {}