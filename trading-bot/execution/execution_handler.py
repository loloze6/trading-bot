from binance.client import Client
from config.settings import API_KEY, API_SECRET, USE_TESTNET
from time import time, sleep
import logging
from typing import Dict, List, Optional, Union, Tuple



logger = logging.getLogger(__name__)  # Use the logger set up elsewhere

class ExecutionHandler:
    def __init__(self, test_mode: bool = False):
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)
        # self.trading_pair = TRADING_PAIR
        # self.trade_amount = TRADE_AMOUNT
        self.test_mode = test_mode


    def place_order(self, side: str, symbol: str, quantity: float):
        """
        Place a market order.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Quantity to buy/sell
            
        Returns:
            Order information
        """

        try:
            logger.info(f"Placing {side} market order for {quantity} {symbol}")

            # Round quantity to appropriate precision
            quantity = self._round_quantity(symbol, quantity)

            order = self.client.create_order(
                symbol=symbol,
                side=side.upper(),
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logger.info(f"Order placed: {order}")

            return order
        except Exception as e:
            raise RuntimeError(f"Order failed: {e}")
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
        """
        Place a limit order.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL'
            quantity: Quantity to buy/sell
            price: Limit price
            
        Returns:
            Order information
        """
        try:
            logger.info(f"Placing {side} limit order for {quantity} {symbol} at {price}")
            
            # Round values to appropriate precision
            quantity = self._round_quantity(symbol, quantity)
            price = self._round_price(symbol, price)
            
            if self.test_mode:
                # Test order
                logger.info(f"Test limit order placed: {side} {quantity} {symbol} at {price}")
                return {'status': 'TEST_ORDER', 'symbol': symbol, 'quantity': quantity, 'price': price}
            else:
                # Real order
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type='LIMIT',
                    timeInForce='GTC',  # Good Till Cancelled
                    quantity=quantity,
                    price=price
                )
                logger.info(f"Order placed: {order}")
                return order
                
        except Exception as e:
            logger.error(f"Error placing limit order: {e}")
            return {'status': 'ERROR', 'message': str(e)}
    
    def place_stop_loss(self, symbol: str, side: str, quantity: float, stop_price: float) -> Dict:
        """
        Place a stop loss order.
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
            side: 'BUY' or 'SELL' (opposite of the main position)
            quantity: Quantity to buy/sell
            stop_price: Stop price
            
        Returns:
            Order information
        """
        try:
            logger.info(f"Placing {side} stop loss for {quantity} {symbol} at {stop_price}")
            
            # Round values to appropriate precision
            quantity = self._round_quantity(symbol, quantity)
            stop_price = self._round_price(symbol, stop_price)
            
            if self.test_mode:
                # Test order
                logger.info(f"Test stop loss placed: {side} {quantity} {symbol} at {stop_price}")
                return {'status': 'TEST_ORDER', 'symbol': symbol, 'quantity': quantity, 'stop_price': stop_price}
            else:
                # Real order
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type='STOP_LOSS_LIMIT',
                    timeInForce='GTC',
                    quantity=quantity,
                    price=stop_price * 0.99 if side == 'SELL' else stop_price * 1.01,  # Small buffer
                    stopPrice=stop_price
                )
                logger.info(f"Stop loss placed: {order}")
                return order
                
        except Exception as e:
            logger.error(f"Error placing stop loss: {e}")
            return {'status': 'ERROR', 'message': str(e)}

    # Function to sell all assets to a specified target currency
    def sell_all_assets_to_target(self, target_currency):
        try:
            balances = self.client.get_account()['balances']
            for balance in balances:
                asset = balance['asset']
                free = float(balance['free'])
                if asset != target_currency and free > 0:
                    # Define the trading pair (e.g., BTCUSDT if target_currency is USDT)
                    symbol = f"{asset}{target_currency}"
                    try:
                        price = float(self.client.get_symbol_ticker(symbol=symbol)['price'])
                        quantity = free
                        # Place a market sell order
                        self.place_order(
                            symbol=symbol,
                            quantity=quantity,
                            side='SELL'
                        )
                        print(f"Sold {quantity} {asset} for {target_currency}")
                        time.sleep(1)  # Pause to avoid rate limits

                    except Exception as e:
                        raise RuntimeError(f"Error selling {asset} to {target_currency}: {e}")
        
        except Exception as e:
            raise RuntimeError(f"Sell all assets failed: {e}")

    def _round_quantity(self, symbol: str, quantity: float) -> float:
        """Round quantity to the appropriate precision for the symbol."""
        # In a real implementation, this would fetch symbol info from the exchange
        # For now, we'll use a simple approach
        return round(quantity, 5)
    
    def _round_price(self, symbol: str, price: float) -> float:
        """Round price to the appropriate precision for the symbol."""
        # In a real implementation, this would fetch symbol info from the exchange
        return round(price, 2)