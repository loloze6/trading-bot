from binance.client import Client
from config.settings import API_KEY, API_SECRET, USE_TESTNET
from typing import Dict, List, Optional, Union, Tuple, Any
import logging
import csv
import os
from datetime import datetime
import pandas as pd

logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere

"""
Portfolio Information Module
============================
Manages portfolio balances and conversions for live and simulated trading.

Classes:
    - PortfolioInfo: Live portfolio info from Binance API
    - MockPortfolioInfo: Simulated portfolio for backtesting
"""

class PortfolioInfo:
    """
    Live portfolio manager using Binance API.
    
    Features:
        - Retrieves real-time balances
        - Converts portfolio values to any currency
        - Handles multi-step conversions via BTC/ETH bridges
    """
    def __init__(self, initial_balance={'USDT': {'free': 1000, 'locked': 0}}, commission_rate=0.001):
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)


        self.commission_rate = commission_rate
        server_time = self.client.get_server_time()
        timestamp = server_time['serverTime']
        self.balance = self.get_account_balance()      
        logger.info(f"💼 Portfolio initialized │ Testnet: {USE_TESTNET} │ Server: {timestamp}")

    def get_portfolio_converted(self, symbol): #Value of the entire portfolio converted in symbol
        try:
        # Retrieve the balances of all coins in the user’s Binance account
            account_balances = self.client.get_account()['balances']

            # Get the current price of all tickers from the Binance API
            ticker_info = self.client.get_all_tickers()

            # Create a dictionary of tickers and their corresponding prices
            ticker_prices = {ticker['symbol']: float(ticker['price']) for ticker in ticker_info}

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
        
    def update_local_balance(self, symbol, price, quantity, trade_type):
        """
        Update balance after a trade.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            price: Trade execution price
            quantity: Trade quantity
            trade_type: Type of trade (LONG, SHORT, CLOSE, REDUCE_LONG, REDUCE_SHORT)
        """
        base_asset = symbol.replace('USDT', '')
        if symbol not in self.balance:
            self.balance[symbol] = {'free': 0, 'locked': 0}

        cost = price * quantity
        quantity_reduced_commission = quantity * (1 - self.commission_rate)
        cost_reduced_commission = cost * (1 - self.commission_rate)

        logger.debug(f"      💱 Balance Update │ {trade_type} │ {symbol}")


        if trade_type == 'LONG':
            if self.balance['USDT']['free'] >= cost:
                self.balance['USDT']['free'] -= cost
                self.balance[symbol]['free'] += quantity_reduced_commission
                logger.info(f"      ✓ Balance │ USDT: -{cost:.2f} │ {base_asset}: +{quantity_reduced_commission:.6f}")
            else:
                logger.error(f"      ✗ Insufficient USDT │ Have: ${self.balance['USDT']['free']:.2f} │ Need: ${cost:.2f}")

        elif trade_type == 'SHORT':
            if self.balance[symbol]['free'] >= quantity:
                self.balance['USDT']['free'] += cost_reduced_commission
                self.balance[symbol]['free'] -= quantity
                logger.info(f"      ✓ Balance │ {base_asset}: -{quantity:.6f} │ USDT: +${cost_reduced_commission:.2f}")
            else:
                logger.error(f"      ✗ Insufficient {base_asset} │ Have: {self.balance[base_asset]['free']:.6f} │ Need: {quantity:.6f}")

        elif trade_type == 'CLOSE':
            if self.balance[symbol]['free'] >= quantity:
                self.balance['USDT']['free'] += cost_reduced_commission
                self.balance[symbol]['free'] -= quantity
                logger.info(f"      ✓ Balance │ {base_asset}: -{quantity:.6f} │ USDT: +${cost_reduced_commission:.2f}")
            else:
                logger.error(f"      ✗ Insufficient {base_asset} to close │ Have: {self.balance[base_asset]['free']:.6f}")

        elif trade_type == 'REDUCE_LONG':
            # Partial sell of long position
            if self.balance[base_asset]['free'] >= quantity:
                self.balance[base_asset]['free'] -= quantity
                self.balance['USDT']['free'] += cost_reduced_commission
                logger.info(f"      ✓ Balance │ {base_asset}: -{quantity:.6f} │ USDT: +${cost_reduced_commission:.2f}")
            else:
                logger.error(f"      ✗ Insufficient {base_asset} │ Have: {self.balance[base_asset]['free']:.6f}")
        
        elif trade_type == 'REDUCE_SHORT':
            # Partial buy to cover short
            if self.balance['USDT']['free'] >= cost:
                self.balance['USDT']['free'] -= cost
                self.balance[base_asset]['free'] += quantity_reduced_commission
                logger.info(f"      ✓ Balance │ USDT: -${cost:.2f} │ {base_asset}: +{quantity_reduced_commission:.6f}")
            else:
                logger.error(f"      ✗ Insufficient USDT │ Have: ${self.balance['USDT']['free']:.2f}")


    def get_account_balance(self) -> Dict[str, float]:
        """Get account balances."""
        try:
            info = self.client.get_account()
            balances = {}
            
            for asset in info['balances']:
                free_bal = float(asset['free'])
                locked_bal = float(asset['locked'])

                if free_bal > 0 or locked_bal > 0:
                    balances[asset['asset']] = {
                        'free': free_bal,
                        'locked': locked_bal
                    }
                        # Log summary
            total_assets = len(balances)
            usdt_free = balances.get('USDT', {}).get('free', 0)
            logger.info(f"💰 Balance fetched │ Assets: {total_assets} │ USDT (free): ${usdt_free:.2f}")
            
            for asset, bal in balances.items():
                if bal['locked'] > 0:
                    logger.warning(f"   ⚠ {asset} locked: {bal['locked']:.6f}")
            
            return balances
        
        except Exception as e:
            logger.error(f"❌ Error fetching account balance: {e}")
            return {}

    def update_portfolio(self):
        """NOT IMPLEMENTED IN LIVE"""
        logger.error("NOT IMPLEMENTED IN LIVE")

        
class MockPortfolioInfo:
    """
    Mock portfolio for backtesting.
    
    Simulates balance changes from trades without API calls.
    Tracks borrowed assets for margin trading simulation.
    """
    def __init__(self, initial_balance={'USDT': {'free': 1000, 'locked': 0}}, commission_rate=0.001):
        self.balance = initial_balance
        self.commission_rate = commission_rate
        usdt_balance = initial_balance.get('USDT', {}).get('free', 0)
        logger.info(f"🧪 Mock Portfolio initialized │ USDT: ${usdt_balance:.2f} │ Commission: {commission_rate*100:.2f}%")


    def get_account_balance(self) -> Dict[str, float]:
        """Get account balances."""
        try:
            # Calculate summary
            usdt_free = self.balance.get('USDT', {}).get('free', 0)
            usdt_locked = self.balance.get('USDT', {}).get('locked', 0)
            
            # Count assets
            assets_with_balance = sum(1 for asset, bal in self.balance.items() 
                                     if bal.get('free', 0) > 0 or bal.get('locked', 0) > 0)
            
            logger.debug(f"💰 Mock Balance │ Assets: {assets_with_balance} │ USDT: ${usdt_free:.2f} (free) ${usdt_locked:.2f} (locked)")
            
            return self.balance
            
        except Exception as e:
            logger.error(f"❌ Error fetching mock balance: {e}")
            return {}

    def update_local_balance(self, symbol, price, quantity, trade_type): #Improvment To be done to see where the commission is deducted (cost / quantity) SHORT / LONG SELL BUY
        """
        Update simulated balance after a trade.
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            price: Trade execution price
            quantity: Trade quantity (positive)
            trade_type: Type of trade (LONG, SHORT, CLOSE, REDUCE_LONG, REDUCE_SHORT)
        """

        base_asset = symbol.replace('USDT', '')
        if symbol not in self.balance:
            self.balance[symbol] = {'free': 0, 'locked': 0}
        
        cost = price * quantity
        commission = self.commission_rate

        logger.info(f"      💱 Mock Update │ {trade_type} │ {symbol} │ {quantity:.6f} @ ${price:.2f}")


        if trade_type == 'LONG':
            # Buy asset with USDT (or margin)
            if self.balance['USDT']['free'] >= cost:
                # Normal buy
                self.balance['USDT']['free'] -= cost
                received_qty = quantity * (1 - commission)
                self.balance[symbol]['free'] += received_qty
                logger.debug(f"      ✓ Bought {quantity:.6f} {base_asset} │ Received: {received_qty:.6f} │ Paid: ${cost:.2f}")
            
            else: 
                # Margin buy (borrow USDT)
                borrowed = cost - self.balance['USDT']['free']
                logger.info(f"      📊 Margin buy │ Borrowed: ${borrowed:.2f} USDT")
                self.balance['USDT']['locked'] += borrowed
                self.balance['USDT']['free'] = 0
                received_qty = quantity * (1 - commission)
                self.balance[symbol]['free'] += received_qty
                logger.info(f"      ✓ Bought {quantity:.6f} {base_asset} (margin) │ Received: {received_qty:.6f}")

        elif trade_type == 'REDUCE_LONG': 
            # Sell part of long position
            if self.balance[symbol]['free'] >= quantity:
                self.balance[symbol]['free'] -= quantity
                usdt_received = cost * (1 - commission)
                
                # Repay borrowed USDT first if any
                if self.balance['USDT']['locked'] > 0:
                    repay = min(usdt_received, self.balance['USDT']['locked'])
                    self.balance['USDT']['locked'] -= repay
                    usdt_received -= repay
                    logger.info(f"      💸 Repaid ${repay:.2f} borrowed USDT │ Remaining borrow: ${self.balance['USDT']['locked']:.2f}")

                self.balance['USDT']['free'] += usdt_received
                logger.info(f"      ✓ Sold {quantity:.6f} {base_asset} │ Received: ${usdt_received:.2f}")
            else:
                logger.error(f"      ✗ Insufficient {base_asset} │ Have: {self.balance[base_asset]['free']:.6f}")

        elif trade_type == 'SHORT':  
            # Synthetic borrow asset, sell for USDT
            self.balance[symbol]['locked'] += quantity  # Owe the asset
            usdt_received = cost * (1 - commission)
            self.balance['USDT']['free'] += usdt_received
            logger.debug(f"      ✓ Shorted {quantity:.6f} {base_asset} │ Borrowed & sold │ Received: ${usdt_received:.2f}")

        elif trade_type == 'REDUCE_SHORT':
            # Buy back to cover short
            abs_quantity = abs(quantity)
            repay = min(quantity, self.balance[symbol]['locked'])
            cost_to_buy = price * repay / (1 - commission)
            
            if self.balance['USDT']['free'] >= cost_to_buy and self.balance[symbol]['locked'] > 0:
                self.balance['USDT']['free'] -= cost_to_buy
                self.balance[symbol]['locked'] -= repay
                logger.debug(f"      ✓ Reduced SHORT │ Covered {repay:.6f} {base_asset} │ Paid: ${cost_to_buy:.2f}")
            else:
                logger.error(f"      ✗ Cannot reduce SHORT │ USDT: ${self.balance['USDT']['free']:.2f} │ Locked: {self.balance[base_asset]['locked']:.6f}")

        elif trade_type == 'CLOSE':
            # Close position (works for both LONG and SHORT)
            if quantity > 0 and self.balance[symbol]['free'] >= quantity:
                # Close LONG by selling asset
                self.balance[symbol]['free'] -= quantity
                usdt_received = price * quantity * (1 - commission)
                
                # Repay borrowed first
                if self.balance['USDT']['locked'] > 0:
                    repay = min(usdt_received, self.balance['USDT']['locked'])
                    self.balance['USDT']['locked'] -= repay
                    usdt_received -= repay
                    logger.debug(f"      💸 Repaid ${repay:.2f} borrowed USDT")

                self.balance['USDT']['free'] += usdt_received
                logger.debug(f"      ✓ Closed LONG │ Sold {quantity:.6f} {base_asset} │ Received: ${usdt_received:.2f}")

            elif quantity < 0 and self.balance[symbol]['locked'] >= quantity:
                # Close SHORT by buying asset
                abs_quantity = abs(quantity)
                repay = min(abs_quantity, self.balance[symbol]['locked'])
                cost_to_buy = price * abs_quantity / (1 - commission)
                
                if self.balance['USDT']['free'] >= cost_to_buy and self.balance[symbol]['locked'] > 0:
                    self.balance['USDT']['free'] -= cost_to_buy
                    self.balance[symbol]['locked'] -= repay
                    logger.debug(f"      ✓ Closed SHORT │ Covered {repay:.6f} {base_asset} │ Paid: ${cost_to_buy:.2f}")

                else:
                    logger.error(f"      ✗ Insufficient USDT to close SHORT")

            else:
                logger.warning(f"      ⚠ Close issue │ No position to close")

        if self.balance['USDT']['locked'] > 0 or self.balance[symbol]['locked'] > 0:
            logger.info(f"      📊 Open borrows │ USDT: ${self.balance['USDT']['locked']:.2f} │ {symbol}: {self.balance[symbol]['locked']:.6f}")

    def get_portfolio_converted(self, symbol): #Value of the entire portfolio converted in symbol
        """Value of the entire portfolio converted in symbol."""
        logger.warning("⚠ get_portfolio_converted NOT IMPLEMENTED in mock mode")
        return 0
    
    def update_portfolio(self, symbol =None, targetPortfolio=None, data=None):
        """Trigger necessary orders to update portfolio."""
        logger.warning("⚠ update_portfolio NOT IMPLEMENTED in mock mode")

    def calculate_target_portfolio(self, symbol =None, signal=None, data=None):
        """Calculate target portfolio based on signal."""
        logger.warning("⚠ calculate_target_portfolio NOT IMPLEMENTED in mock mode")


class PortfolioStateTracker: 
    """
    Tracks portfolio state over time and exports to CSV.
    Records: Date, Forecast, Total Portfolio Value, USDT owned, BTC borrowed, BTC owned, USDT borrowed
    """
    
    def __init__(self, output_dir: str = "backtest_results"):
        self.output_dir = output_dir
        self.states = []
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

    
    def record_state(self,
                     timestamp: datetime,
                     forecast: float,
                     needs_rebalance: bool,
                     total_portfolio_value: float,
                     balances: Dict[str, Dict[str, float]],
                     allocation: float = None,
                     regime: str = None,
                     price: float = None):
        """
        Record portfolio state at a specific time.
        
        Args:
            timestamp: Current time
            forecast: Strategy forecast (-20 to +20)
            total_portfolio_value: Total portfolio value in USD
            balances: Balance dictionary from portfolio_info
            borrows: Borrowed amounts {asset: quantity}
            allocation: Current allocation (-1 to +1)
            regime: Market regime
            price: Current BTC price
        """
        # Extract USDT
        usdt_balance = balances.get('USDT', {})
        usdt_owned = float(usdt_balance.get('free', 0.0))
        usdt_borrowed = float(usdt_balance.get('locked', 0.0))  # Borrowed USDT
        
        # Extract BTC (key is 'BTCUSDT')
        btc_balance = balances.get('BTCUSDT', balances.get('BTC', {}))
        btc_owned = float(btc_balance.get('free', 0.0))
        btc_borrowed = float(btc_balance.get('locked', 0.0))  # Borrowed BTC or BTC in position
        
            
        state = {
            'timestamp': timestamp,
            'date': timestamp.strftime('%Y-%m-%d %H:%M:%S') if hasattr(timestamp, 'strftime') else str(timestamp),
            'forecast': forecast,
            'allocation': allocation if allocation is not None else None,
            'needs_rebalance': needs_rebalance,
            'regime': regime,
            'btc_price': price if price is not None else None,
            'total_portfolio_value': total_portfolio_value,
            'usdt_owned': usdt_owned,
            'btc_owned': btc_owned,
            'usdt_borrowed': usdt_borrowed,
            'btc_borrowed': btc_borrowed,
            'net_usdt': (usdt_owned - usdt_borrowed),
            'net_btc': (btc_owned - btc_borrowed),
        }
        
        self.states.append(state)
        
        # Debug log every 100 records
        if len(self.states) % 100 == 0:
            logger.debug(f"📊 Portfolio states recorded: {len(self.states)}")
    
    def save_to_csv(self, filename: str = None):
        """Save portfolio states to CSV file."""
        logger.debug(f"💾 Attempting to save portfolio history... ({len(self.states)} records)")

        if not self.states:
            logger.error("No portfolio states to save")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"portfolio_history_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        logger.debug(f"   Saving to: {filepath}")

        fieldnames = [
            'date',
            'forecast',
            'allocation',
            'needs_rebalance',
            'regime',
            'btc_price',
            'total_portfolio_value',
            'usdt_owned',
            'btc_owned',
            'usdt_borrowed',
            'btc_borrowed',
            'net_usdt',
            'net_btc'
        ]
        
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for state in self.states:
                # Write only the fields we want in CSV (exclude 'timestamp' object)
                row = {k: state[k] for k in fieldnames}
                writer.writerow(row)
        
        logger.info(f"✅ Portfolio history saved: {filepath} ({len(self.states)} records)")
        return filepath
    
    def get_dataframe(self) -> pd.DataFrame:
        """Return portfolio states as DataFrame."""
        if not self.states:
            return pd.DataFrame()
        
        return pd.DataFrame(self.states)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics of portfolio evolution."""
        if not self.states:
            return {}
        
        df = self.get_dataframe()
        
        return {
            'initial_value': df['total_portfolio_value'].iloc[0],
            'final_value': df['total_portfolio_value'].iloc[-1],
            'total_return': ((df['total_portfolio_value'].iloc[-1] / df['total_portfolio_value'].iloc[0]) - 1) * 100,
            'max_value': df['total_portfolio_value'].max(),
            'min_value': df['total_portfolio_value'].min(),
            'max_drawdown': ((df['total_portfolio_value'].min() / df['total_portfolio_value'].max()) - 1) * 100,
            'avg_forecast': df['forecast'].mean(),
            'max_btc_borrowed': df['btc_borrowed'].max(),
            'max_usdt_borrowed': df['usdt_borrowed'].max(),
            'num_records': len(self.states)
        }
