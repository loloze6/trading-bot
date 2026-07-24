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

class OtherPortfolioOperations:
    """
    Live portfolio manager using Binance API.
    
    Features:
        - Retrieves real-time balances
        - Converts portfolio values to any currency
        - Handles multi-step conversions via BTC/ETH bridges
    """
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)  
        logger.debug(f"💼 Portfolio connection initialized │ Testnet: {USE_TESTNET} │ Server: {self.client.get_server_time()['serverTime']}")

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
 
class CommonPortfolioDef:
    def __init__(self, commission_rate=0.001):
        self.commission_rate = commission_rate
        
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
        if symbol not in self.local_balance:
            self.local_balance[symbol] = {'free': 0, 'locked': 0}
        
        cost = price * quantity
        commission = self.commission_rate

        logger.debug(f"      💱 Mock Update │ {trade_type} │ {symbol} │ {quantity:.6f} @ ${price:.2f}")


        if trade_type == 'LONG':
            # Buy asset with USDT (or margin)
            if self.local_balance['USDT']['free'] >= cost:
                # Normal buy
                self.local_balance['USDT']['free'] -= cost
                received_qty = quantity * (1 - commission)
                self.local_balance[symbol]['free'] += received_qty
                # logger.debug(f"      ✓ Bought {quantity:.6f} {base_asset} │ Received: {received_qty:.6f} │ Paid: ${cost:.2f}")
            
            else: 
                # Margin buy (borrow USDT)
                borrowed = cost - self.local_balance['USDT']['free']
                logger.debug(f"      📊 Margin buy │ Borrowed: ${borrowed:.2f} USDT")
                self.local_balance['USDT']['locked'] += borrowed
                self.local_balance['USDT']['free'] = 0
                received_qty = quantity * (1 - commission)
                self.local_balance[symbol]['free'] += received_qty
                logger.debug(f"      ✓ Bought {quantity:.6f} {base_asset} (margin) │ Received: {received_qty:.6f}")

        elif trade_type == 'REDUCE_LONG': 
            # Sell part of long position
            if self.local_balance[symbol]['free'] >= quantity:
                self.local_balance[symbol]['free'] -= quantity
                usdt_received = cost * (1 - commission)
                
                # Repay borrowed USDT first if any
                if self.local_balance['USDT']['locked'] > 0:
                    repay = min(usdt_received, self.local_balance['USDT']['locked'])
                    self.local_balance['USDT']['locked'] -= repay
                    usdt_received -= repay
                    logger.debug(f"      💸 Repaid ${repay:.2f} borrowed USDT │ Remaining borrow: ${self.local_balance['USDT']['locked']:.2f}")

                self.local_balance['USDT']['free'] += usdt_received
                logger.debug(f"      ✓ Sold {quantity:.6f} {base_asset} │ Received: ${usdt_received:.2f}")
            else:
                logger.error(f"      ✗ Insufficient {base_asset} │ Have: {self.local_balance[base_asset]['free']:.6f}")

        elif trade_type == 'SHORT':  
            # Synthetic borrow asset, sell for USDT
            self.local_balance[symbol]['locked'] += quantity  # Owe the asset
            usdt_received = cost * (1 - commission)
            self.local_balance['USDT']['free'] += usdt_received
            # logger.debug(f"      ✓ Shorted {quantity:.6f} {base_asset} │ Borrowed & sold │ Received: ${usdt_received:.2f}")

        elif trade_type == 'REDUCE_SHORT':
            # Buy back to cover short
            abs_quantity = abs(quantity)
            repay = min(quantity, self.local_balance[symbol]['locked'])
            cost_to_buy = price * repay / (1 - commission)
            
            if self.local_balance['USDT']['free'] >= cost_to_buy and self.local_balance[symbol]['locked'] > 0:
                self.local_balance['USDT']['free'] -= cost_to_buy
                self.local_balance[symbol]['locked'] -= repay
                # logger.debug(f"      ✓ Reduced SHORT │ Covered {repay:.6f} {base_asset} │ Paid: ${cost_to_buy:.2f}")
            else:
                logger.error(f"      ✗ Cannot reduce SHORT │ USDT: ${self.local_balance['USDT']['free']:.2f} │ Locked: {self.local_balance[base_asset]['locked']:.6f}")

        elif trade_type == 'CLOSE':
            # Close position (works for both LONG and SHORT)
            if quantity > 0 and self.local_balance[symbol]['free'] >= quantity:
                # Close LONG by selling asset
                self.local_balance[symbol]['free'] -= quantity
                usdt_received = price * quantity * (1 - commission)
                
                # Repay borrowed first
                if self.local_balance['USDT']['locked'] > 0:
                    repay = min(usdt_received, self.local_balance['USDT']['locked'])
                    self.local_balance['USDT']['locked'] -= repay
                    usdt_received -= repay
                    # logger.debug(f"      💸 Repaid ${repay:.2f} borrowed USDT")

                self.local_balance['USDT']['free'] += usdt_received
                # logger.debug(f"      ✓ Closed LONG │ Sold {quantity:.6f} {base_asset} │ Received: ${usdt_received:.2f}")

            elif quantity < 0 and self.local_balance[symbol]['locked'] >= quantity:
                # Close SHORT by buying asset
                abs_quantity = abs(quantity)
                repay = min(abs_quantity, self.local_balance[symbol]['locked'])
                cost_to_buy = price * abs_quantity / (1 - commission)
                
                if self.local_balance['USDT']['free'] >= cost_to_buy and self.local_balance[symbol]['locked'] > 0:
                    self.local_balance['USDT']['free'] -= cost_to_buy
                    self.local_balance[symbol]['locked'] -= repay
                    # logger.debug(f"      ✓ Closed SHORT │ Covered {repay:.6f} {base_asset} │ Paid: ${cost_to_buy:.2f}")

                else:
                    logger.error(f"      ✗ Insufficient USDT to close SHORT")

            else:
                logger.warning(f"      ⚠ Close issue │ No position to close")

        if self.local_balance['USDT']['locked'] > 0 or self.local_balance[symbol]['locked'] > 0:
            logger.debug(f"      📊 Open borrows │ USDT: ${self.local_balance['USDT']['locked']:.2f} │ {symbol}: {self.local_balance[symbol]['locked']:.6f}")

    def apply_funding(self, symbol, mark_price, f_bar):
        """
        Accrue perpetual-funding cash flow on the currently-held position (design
        2026-07-24 §5(a)). Sibling to update_local_balance, but off the trade path:
        funding accrues every bar a position is open, independent of any trade, and
        never interacts with commission.

            funding_cash_flow = - position_sign * N * f_bar
                N            = |position_qty| * mark_price
                position_sign = +1 for a LONG (free asset), -1 for a SHORT (locked asset)

        Positive funding + LONG  → cash_flow < 0 (long pays).
        Positive funding + SHORT → cash_flow > 0 (short receives).
        Negative funding flips both. Matches the Binance convention (positive rate ⇒
        longs pay shorts, funding_rate_fetcher.py:9-10).

        Pure USDT.free balance mutation. Flat position → zero. Returns the applied
        cash flow (for logging/tests).

        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            mark_price: Mark price used for notional (the bar close at the hook site)
            f_bar: Funding rate accrued over the bar (daily-summed; see
                   data/feed_registry.py::build_daily_funding_series)
        """
        if f_bar is None or symbol not in self.local_balance:
            return 0.0

        free = self.local_balance[symbol].get('free', 0.0)
        locked = self.local_balance[symbol].get('locked', 0.0)
        position_qty = free - locked  # long (free asset) > 0; short (locked asset) < 0

        if position_qty == 0:
            return 0.0

        position_sign = 1.0 if position_qty > 0 else -1.0
        notional = abs(position_qty) * mark_price
        funding_cash_flow = -position_sign * notional * f_bar

        if 'USDT' not in self.local_balance:
            self.local_balance['USDT'] = {'free': 0.0, 'locked': 0.0}
        self.local_balance['USDT']['free'] += funding_cash_flow

        logger.debug(
            f"      💰 Funding │ {symbol} │ f_bar={f_bar:+.6f} │ N=${notional:.2f} │ "
            f"cash_flow=${funding_cash_flow:+.4f}"
        )
        return funding_cash_flow

    def _calculate_total_portfolio_value(
        self,
        balances: Dict,
        current_price: float
    ) -> float:
        """
        Calculate total portfolio value in quote currency.

        Args:
            balances: Dictionary of balances by currency
            current_price: Current price for conversion

        Returns:
            Total portfolio value in quote currency
        """
        quote_currency = 'USDT'
        total_value = 0.0

        # self.logger.debug (f"║ ┌─ PORTFOLIO VALUATION ─")
        
        # Add quote currency balance
        if quote_currency in balances:
            quote_balance = balances[quote_currency].get('free', 0.0)
            total_value += quote_balance
            # self.logger.debug (f"║ │ {quote_currency} (free): ${quote_balance}")
            borrowed_balance = balances[quote_currency].get('locked', 0.0)
            total_value -= borrowed_balance
            # self.logger.debug (f"║ │ {quote_currency} (locked): ${borrowed_balance}")
        
        # Add/subtract other asset balances converted to quote currency
        for symbol, balance_info in balances.items():
            if symbol == quote_currency:
                continue
            
            free_balance = balance_info.get('free', 0.0)
            locked_balance = balance_info.get('locked', 0.0)
            
            if current_price is None:
                self.logger.warning(f"║ │ ⚠ No price for {symbol}, skipped")
                continue
            
            # Add value of free assets (long positions)
            if free_balance != 0:
                asset_value = free_balance * current_price
                total_value += asset_value
                # # self.logger.debug (
                #     f"║ │ {symbol} (free): {free_balance} × ${current_price} = ${asset_value}"
                # )
            
            # Subtract value of locked assets (short positions/liabilities)
            if locked_balance != 0:
                liability_value = locked_balance * current_price
                total_value -= liability_value
                # # self.logger.debug (
                #     f"║ │ {symbol} (locked): {locked_balance} × ${current_price} = -${liability_value}"
                # )
        
        # self.logger.debug (f"║ └─ TOTAL: ${total_value} {quote_currency}")
        return total_value

    def _calculate_actual_allocation(self, close, balances, total_value, symbol) -> float:
            # # Calculate actual position value for
            # # For BTCUSDT: (free + locked) * current_price
            # btc_balance = balances.get('BTCUSDT', balances.get('BTC', {}))
            # btc_quantity = btc_balance.get('free', 0.0) - btc_balance.get('locked', 0.0)
            # position_value = btc_quantity * close
            # logger.debug(f"btc_balance: {btc_balance} │btc_quantity {btc_quantity}│ position_value: ${position_value:.2f}")       
            # actual_allocation = position_value / total_value if total_value > 0 else 0.0
            # return actual_allocation
        quote_currency = 'USDT'
        base_asset = symbol.replace(quote_currency, '')  # or use a proper symbol->base-asset mapping if one exists
        asset_balance = balances.get(symbol, balances.get(base_asset, {}))
        quantity = asset_balance.get('free', 0.0) - asset_balance.get('locked', 0.0)
        position_value = quantity * close
        actual_allocation = position_value / total_value if total_value > 0 else 0.0
        return actual_allocation

    def get_account_balance(self) -> Dict[str, float]:
        return self.local_balance   

class PortfolioInfo(CommonPortfolioDef):
    """
    Live portfolio manager using Binance API.
    
    Features:
        - Retrieves real-time balances
        - Converts portfolio values to any currency
        - Handles multi-step conversions via BTC/ETH bridges
    """
    def __init__(self, initial_balance={'USDT': {'free': 1000, 'locked': 0}}, commission_rate=0.001):
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)
        self.local_balance = initial_balance
        super().__init__(commission_rate)
        logger.debug(f"💼 Portfolio initialized │ Testnet: {USE_TESTNET} │ Server: {self.client.get_server_time()['serverTime']}")

    def get_local_account_balance(self) -> Dict[str, float]:
        """Get the current local balance (for backtesting)."""
        return self.local_balance

    def get_account_balance(self) -> Dict[str, float]:  # Real override needed
        try:
            info = self.client.get_account()
            balances = {
                asset['asset']: {'free': float(asset['free']), 'locked': float(asset['locked'])}
                for asset in info['balances']
                if float(asset['free']) > 0 or float(asset['locked']) > 0
            }
            logger.debug(f"💰 Balance fetched │ Assets: {len(balances)} │ USDT free: ${balances.get('USDT', {}).get('free', 0):.2f}")
            return balances
        except Exception as e:
            logger.error(f"❌ Error fetching balance: {e}")
            return {}
       
class MockPortfolioInfo(CommonPortfolioDef):
    """
    Mock portfolio for backtesting.
    
    Simulates balance changes from trades without API calls.
    Tracks borrowed assets for margin trading simulation.
    """
    def __init__(self, initial_balance={'USDT': {'free': 1000, 'locked': 0}}, commission_rate=0.001):
        self.local_balance = initial_balance
        logger.debug(f"🧪 Mock Portfolio initialized │ Balance: {self.local_balance} │ Commission: {commission_rate*100:.2f}%")
        super().__init__(commission_rate)
    
def flatten_dict_columns(df):
    """Recursively expand dict-valued columns into dot-separated scalar columns."""
    changed = True
    while changed:
        changed = False
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, dict) and len(x) > 0).any():
                df = df.drop(columns=[col]).join(
                    df[col].apply(lambda x: pd.Series(x) if isinstance(x, dict) else pd.Series(dtype=object))
                        .add_prefix(f"{col}.")
                )
                changed = True
    return df


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

        
    def record_state(self, data: pd.DataFrame, signal=None, **extras):
        last_row = data.iloc[-1].to_dict()

        signal_info = {}
        if signal:
            if hasattr(signal, '__dataclass_fields__'):
                signal_info = {k: getattr(signal, k) for k in signal.__dataclass_fields__}
            elif hasattr(signal, '__dict__'):
                signal_info = signal.__dict__

        state = {
            **last_row,
            **signal_info,
            **extras
        }
        self.states.append(state)
        
    
    def to_csv(self, filename: str = "portfolio_states.csv") -> str:
        if not self.states:
            return None

        df = self.get_tracker_full_record()

        df = flatten_dict_columns(df)

        # Clean numpy types
        df = df.map(lambda x: x.item() if hasattr(x, 'item') else x)

        path = os.path.join(self.output_dir, filename)
        df.to_csv(path, index=False)
        logger.info(f"📊 Portfolio states exported to CSV │ Records: {len(self.states)} │ Path: {path}")
        return path

    def get_tracker_full_record(self) -> pd.DataFrame:
        """Return portfolio states as DataFrame."""
        if not self.states:
            return pd.DataFrame()
        
        return pd.DataFrame(self.states)
    
    def get_tracker_summary(self) -> Dict[str, Any]:
        """Get summary statistics of portfolio evolution."""
        if not self.states:
            return {}
        
        df = self.get_tracker_full_record()
        
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
