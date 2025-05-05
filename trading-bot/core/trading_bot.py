import time
from typing import Dict, List, Optional, Union, Tuple
from datetime import datetime

class TradingBot:
    def __init__(self, data_manager =None, strategy=None, execution_handler=None, logger=None, portfolio_info=None, risk_manager=None, fetch_interval: int=60, interval: str = '5m', test_mode: bool = True, symbols: List[str] = ['BTCUSDT']):
        self.data_manager = data_manager 
        self.strategy = strategy 
        self.execution_handler = execution_handler
        self.logger = logger
        self.portfolio_info = portfolio_info
        self.risk_manager = risk_manager
        self.fetch_interval = fetch_interval
        self.interval = interval
        
        # Initialize Binance client
        self.symbols = symbols
        self.test_mode = test_mode

        logger.info("Trading bot initialized")

    def run(self):
        """
        Start the trading bot.
        
        Args:
            interval: Data timeframe (e.g., '1h', '15m')
            check_interval_seconds: How often to check for new signals (in seconds)
        """

        self.logger.info(f"Starting trading bot with {self.interval} interval")
        self.running = True

        try:
            while self.running:
                for symbol in self.symbols:
                    self._process_symbol(symbol, self.interval)

                # # Step 2: Decide what to do
                # action = self.strategy.decide(current_price, self.previous_price)
                # self.logger.info(f"Price: {current_price:.2f}, Action: {action}")

                # # Step 3: Risk Management (optional)
                # if self.risk_manager:
                #     if not self.risk_manager.approve_trade(action, current_price):
                #         self.logger.warning("Trade rejected by risk manager.")
                #         action = 'hold'

                # # Step 4: Execute trade if needed
                # if action in ['buy', 'sell']:
                #     self.execution_handler.place_order(action)

                # # Step 5: Update previous price
                # self.previous_price = current_price

                # Wait before next fetch
                time.sleep(self.fetch_interval)

        except KeyboardInterrupt:
            self.logger.info("Trading bot stopped by user")
            self.stop()

        except Exception as e:
            self.logger.error(f"Error occurred: {e}")
            self.stop()

    def stop(self):
        """Stop the trading bot."""
        self.logger.info("Stopping trading bot")
        self.running = False

    def _process_symbol(self, symbol: str, interval: str):
        """Process a single symbol."""
        try:
            # Fetch market data
            # current_price = self.data_manager.fetch_latest_price()

            data = self.data_manager.get_historical_klines(symbol, interval)
            if data.empty:
                self.logger.warning(f"No data available for {symbol}")
                return
            
            # Generate trading signals
            # action = self.strategy.decide(current_price, self.previous_price)
            
            signal = self.strategy.generate_signals(data)
            current_price = data['close']
            
            self.logger.info(f"Signal for {symbol}: {signal['action']} ({signal['reason']})")

            # Step 3: Risk Management of new trade
            if self.risk_manager:
                if not self.risk_manager.approve_trade(signal['action'], current_price):
                    self.logger.warning("Trade rejected by risk manager.")
                else:
                    # Execute trades based on signals
                    if signal['action'] == 'BUY' and symbol not in self.positions:
                        self._execute_buy(symbol, current_price)
                    elif signal['action'] == 'SELL' and symbol in self.positions:
                        self._execute_sell(symbol, current_price)

                # # Step 4: Execute trade if needed
                # if action in ['buy', 'sell']:
                #     self.execution_handler.place_order(action)

                # # Step 5: Update previous price
                # self.previous_price = current_price
             
        except Exception as e:
            self.logger.error(f"Error processing {symbol}: {e}", exc_info=True)

        
    def _execute_buy(self, symbol: str, price: float):
        """Execute a buy order."""
        try:
            
            """First calculate position size for buy order."""
            # Get available balance
            balances = self.data_fetcher.get_account_balance()
            quote_currency = symbol[len(symbol)-4:]  # Assumes 4-letter quote currency like USDT
            
            # Skip if we don't have the quote currency
            if quote_currency not in balances:
                self.logger.warning(f"No {quote_currency} balance available")
                return
            
            available_balance = balances[quote_currency]['free']
            
            # Calculate position size
            quantity = self.risk_manager.calculate_position_size(
                available_balance, price)

            """Second place main buy order."""
            order = self.execution_handler.place_order(
                symbol, 'BUY', quantity)

            """Third place risk limitation order."""         
            if order['status'] != 'ERROR':
                # Calculate stop loss
                stop_loss = self.risk_manager.calculate_stop_loss(price, 'LONG')
                
                # Place stop loss order 
                # if not self.test_mode: #(only in live mode)
                stop_order = self.execution_handler.place_stop_loss(
                    symbol, 'SELL', quantity, stop_loss)
                
                """Finally record position"""
                # Record position
                self.positions[symbol] = {
                    'entry_price': price,
                    'quantity': quantity,
                    'stop_loss': stop_loss,
                    'entry_time': datetime.now()
                }
                self.logger.info(f"Opened position for {symbol}: {quantity} at {price}")
            
        except Exception as e:
            self.logger.error(f"Error executing buy for {symbol}: {e}")
    
        
    def _execute_sell(self, symbol: str, price: float):
        """Execute a sell order."""
        try:
            
            """First fecth existing position of buy order."""
            # Get position details
            position = self.positions[symbol]

            """Second open main sell order"""
            # Place sell order
            order = self.execution_handler.place_order(
                symbol, 'SELL', position['quantity'])
            
            """Then calculate perforamnce of order"""
            
            if order['status'] != 'ERROR':
                # Calculate profit/loss
                profit = (price - position['entry_price']) * position['quantity']
                profit_pct = ((price / position['entry_price']) - 1) * 100
                
                self.logger.info(f"Closed position for {symbol}: {position['quantity']} at {price}")
                self.logger.info(f"Profit: {profit:.2f} ({profit_pct:.2f}%)")
                
                """Finally remove position of order"""
                # Remove from positions
                del self.positions[symbol]
            
        except Exception as e:
            self.logger.error(f"Error executing sell for {symbol}: {e}")
