from binance.client import Client
from config.settings import API_KEY, API_SECRET, USE_TESTNET
from time import time, sleep
import logging
from typing import Dict, List, Optional, Union, Tuple
import datetime
from performance.metrics import EnhancedPerformanceTracker, CompletedTrade
from enum import Enum


logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere

class PositionType(Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    CLOSE = "CLOSE"

"""
Execution Handler Module
========================
Manages order execution for both live trading (Binance API) and backtesting (mock).

Classes:
    - PositionType: Enum for position types (LONG/SHORT/CLOSE)
    - ExecutionHandler: Live trading execution with Binance margin API
    - MockExecutionHandler: Simulated execution for backtesting
"""

class ExecutionHandler:

    """
    Live execution handler for real trading with Binance margin account.
    
    Features:
        - Opens long positions (borrows USDT to buy assets)
        - Opens short positions (borrows assets to sell)
        - Closes positions and repays loans automatically
        - Handles quantity/price rounding per exchange rules
    """
    def __init__(self, test_mode: bool = False, performance_tracker: Optional['EnhancedPerformanceTracker'] = None):
        self.client = Client(API_KEY, API_SECRET, testnet=USE_TESTNET)
        self.test_mode = test_mode
        self.performance_tracker = performance_tracker
        self.positions = {}  # Symbol -> Position details
   
        # Enable margin account if not already enabled
        try:
            self.client.enable_margin_account()
            logger.info(f"🔗 Execution Handler │ {'Testnet' if USE_TESTNET else 'Live'} │ Margin: Enabled")

            # client.create_isolated_margin_account(base='BTC', quote='USDT')
            # client.transfer_spot_to_margin(asset='USDC', amount='10')
            # client.transfer_spot_to_isolated_margin(asset='USDC',symbol='BTCUSDC', amount='10')
        except Exception as e:
            logger.info(f"🔗 Execution Handler │ Margin status: {e}")

    def open_long_position(self, symbol: str, quantity: float, 
                          stop_loss: Optional[float] = None, 
                          take_profit: Optional[float] = None, data = None,
                          signal: Optional[Dict] = None,
                          total_portfolio_value: Optional[float] = None) -> Dict:
        """Open a long position using margin trading (borrows USDT to buy the asset)."""

        try:
            current_price = data['close']
        except Exception as e:
            logger.error(f"❌ Cannot retrieve price: {e}")
            return {'status': 'ERROR', 'message': str(e)}
        
        try:          
            # Round quantity to appropriate precision
            quantity = self._round_quantity(symbol, quantity)
            required_usdt = quantity * current_price

            logger.debug(f"🟢 OPEN LONG │ {symbol} │ {quantity:.6f} @ ${current_price:.2f} │ Cost: ${required_usdt:.2f}")
                       
            # Borrow USDT for the trade
            borrow_result = self.client.create_margin_loan(
                asset='USDT',
                amount=required_usdt
            )
            logger.debug(f"   💰 Borrowed USDT: {borrow_result.get('tranId', 'N/A')}")
            
            # Buy the asset with borrowed USDT
            order = self.client.create_margin_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )

            order_id = order.get('orderId', 'N/A')
            executed_qty = float(order.get('executedQty', quantity))
            logger.info(f"   ✓ Order filled │ ID: {order_id} │ Qty: {executed_qty:.6f}")
            
            # Store position info
            self.positions[symbol] = {
                'type': PositionType.LONG,
                'entry_price': current_price,
                'quantity': quantity,
                'borrowed_amount': required_usdt,
                'borrowed_asset': 'USDT',
                'entry_time': datetime.datetime.now(),
                'stop_loss': stop_loss,
                'take_profit': take_profit
            }
            
            # Record with performance tracker
            if self.performance_tracker:
                self.performance_tracker.record_trade(
                    symbol, current_price, quantity,
                    signal=signal, total_portfolio_value=total_portfolio_value
                    )
            return order
            
        except Exception as e:
            logger.error(f"❌ LONG open failed │ {symbol}: {e}")
            return {'status': 'ERROR', 'message': str(e)}

    def open_short_position(self, symbol: str, quantity: float,
                           stop_loss: Optional[float] = None,
                           take_profit: Optional[float] = None, data = None,
                           signal: Optional[Dict] = None,
                           total_portfolio_value: Optional[float] = None) -> Dict:
        """Open a short position using margin trading (borrows asset and sells it)."""
        try:
            current_price = data['close']
        except Exception as e:
            logger.error(f"❌ Cannot retrieve price: {e}")
            return {'status': 'ERROR', 'message': str(e)}
        
        try:
            quantity = self._round_quantity(symbol, quantity)

            # Extract base asset from symbol (e.g., BTC from BTCUSDT)
            base_asset = symbol.replace('USDT', '').replace('BUSD', '').replace('BTC', '')
            if symbol.endswith('BTC'):
                base_asset = symbol.replace('BTC', '')
            elif symbol.endswith('USDT'):
                base_asset = symbol.replace('USDT', '')

            position_value = quantity * current_price
            logger.debug(f"🔴 OPEN SHORT │ {symbol} │ {quantity:.6f} @ ${current_price:.2f} │ Value: ${position_value:.2f}")

            # Borrow the base asset
            borrow_result = self.client.create_margin_loan(
                asset=base_asset,
                amount=-quantity
            )
            logger.debug(f"   💰 Borrowed {base_asset}: {borrow_result.get('tranId', 'N/A')}")
            
            # Sell the borrowed asset
            order = self.client.create_margin_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=self._round_quantity(symbol, quantity)
            )

            order_id = order.get('orderId', 'N/A')
            executed_qty = float(order.get('executedQty', quantity))
            logger.info(f"   ✓ Order filled │ ID: {order_id} │ Qty: {executed_qty:.6f}")
            
            # Store position info
            self.positions[symbol] = {
                'type': PositionType.SHORT,
                'entry_price': current_price,
                'quantity': quantity,
                'borrowed_amount': -quantity,
                'borrowed_asset': base_asset,
                'entry_time': datetime.datetime.now(),
                'stop_loss': stop_loss,
                'take_profit': take_profit
            }
            
            # Record with performance tracker
            if self.performance_tracker:
                self.performance_tracker.record_trade(
                    symbol, current_price, -quantity,
                    signal=signal, total_portfolio_value=total_portfolio_value
                )
            
            return order
            
        except Exception as e:
            logger.error(f"❌ SHORT open failed │ {symbol}: {e}")
            return {'status': 'ERROR', 'message': str(e)}

    def close_position(self, symbol: str, data=None, signal: Optional[Dict] = None,
                      total_portfolio_value: Optional[float] = None) -> Dict:
        """Close an existing position and repay the loan."""
        
        if symbol not in self.positions:
            logger.error(f"❌ No position found for {symbol}")
            return {'status': 'ERROR', 'message': f'No position for {symbol}'}

        try:
            current_price = data['close']
        except Exception as e:
            logger.error(f"❌ Cannot retrieve price: {e}")
            return {'status': 'ERROR', 'message': str(e)}
        
        try:
            position = self.positions[symbol]
            position_type = position['type']
            quantity = position['quantity']
            entry_price = position['entry_price']

            # Calculate P&L
            if position_type == PositionType.LONG:
                pnl_pct = ((current_price / entry_price) - 1) * 100
            else:
                pnl_pct = ((entry_price / current_price) - 1) * 100
            
            pnl_symbol = "📈" if pnl_pct > 0 else "📉"
            logger.debug(f"⚪ CLOSE {position_type.value} │ {symbol} │ {quantity:.6f} @ ${current_price:.2f} │ {pnl_symbol} P&L: {pnl_pct:+.2f}%")
            

            if position_type == PositionType.LONG:
                # Sell the asset to close long position
                order = self.client.create_margin_order(
                    symbol=symbol,
                    side=Client.SIDE_SELL,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=quantity
                )
                
                # Repay the USDT loan
                repay_result = self.client.repay_margin_loan(
                    asset='USDT',
                    amount=position['borrowed_amount']
                )
                logger.info(f"   💸 Repaid USDT: {repay_result.get('tranId', 'N/A')}")
                
            else:  # SHORT position
                # Buy back the asset to close short position
                order = self.client.create_margin_order(
                    symbol=symbol,
                    side=Client.SIDE_BUY,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=position['quantity']
                )
                
                # Repay the borrowed asset
                repay_result = self.client.repay_margin_loan(
                    asset=position['borrowed_asset'],
                    amount=position['borrowed_amount']
                )
                logger.info(f"   💸 Repaid {position['borrowed_asset']}: {repay_result.get('tranId', 'N/A')}")

            order_id = order.get('orderId', 'N/A')
            logger.info(f"   ✓ Position closed │ ID: {order_id}")

            # Record exit with performance tracker
            if self.performance_tracker:
                self.performance_tracker.record_trade(
                    symbol, current_price, -quantity,
                    signal=signal, total_portfolio_value=total_portfolio_value
                )

            # Remove position
            del self.positions[symbol]
            
            return order
            
        except Exception as e:
            logger.error(f"❌ CLOSE failed │ {symbol}: {e}")
            return {'status': 'ERROR', 'message': str(e)}


    # def place_stop_loss(self, symbol: str, side: str, quantity: float, stop_price: float) -> Dict:
    #     """Place a stop loss order."""
    #     try:
    #         logger.info(f"Placing {side} stop loss for {quantity} {symbol} at {stop_price}")
            
    #         quantity = self._round_quantity(symbol, quantity)
    #         stop_price = self._round_price(symbol, stop_price)
            
    #         order = self.client.create_margin_order(
    #             symbol=symbol,
    #             side=side,
    #             type='STOP_LOSS_LIMIT',
    #             timeInForce='GTC',
    #             quantity=quantity,
    #             price=stop_price * 0.99 if side == 'CLOSE' else stop_price * 1.01,
    #             stopPrice=stop_price
    #         )
            
    #         logger.info(f"Stop loss placed: {order}")
    #         return order
            
    #     except Exception as e:
    #         logger.error(f"Error placing stop loss: {e}")
    #         return {'status': 'ERROR', 'message': str(e)}

    # def place_take_profit(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
    #     """Place a take profit order."""
    #     try:
    #         logger.info(f"Placing {side} take profit for {quantity} {symbol} at {price}")
            
    #         quantity = self._round_quantity(symbol, quantity)
    #         price = self._round_price(symbol, price)
            
    #         order = self.client.create_margin_order(
    #             symbol=symbol,
    #             side=side,
    #             type='LIMIT',
    #             timeInForce='GTC',
    #             quantity=quantity,
    #             price=price
    #         )
            
    #         logger.info(f"Take profit placed: {order}")
    #         return order
            
    #     except Exception as e:
    #         logger.error(f"Error placing take profit: {e}")
    #         return {'status': 'ERROR', 'message': str(e)}

    def get_margin_account_info(self) -> Dict:
        """Get margin account information."""
        try:
            info = self.client.get_margin_account()
            total_asset_btc = float(info.get('totalAssetOfBtc', 0))
            total_liability_btc = float(info.get('totalLiabilityOfBtc', 0))
            total_net_btc = float(info.get('totalNetAssetOfBtc', 0))
            
            logger.info(f"📊 Margin Account │ Assets: {total_asset_btc:.6f} BTC │ Liabilities: {total_liability_btc:.6f} BTC │ Net: {total_net_btc:.6f} BTC")
            return info
        except Exception as e:
            logger.error(f"❌ Failed to get margin info: {e}")
            return {}

    def get_current_positions(self) -> Dict:
        """Get all current positions."""
        if self.positions:
            logger.info(f"📋 Current positions: {len(self.positions)} open")
            for symbol, pos in self.positions.items():
                logger.info(f"   {symbol}: {pos['type'].value} {pos['quantity']:.6f} @ ${pos['entry_price']:.2f}")
        return self.positions.copy()

    # Function to sell all assets to a specified target currency
    def sell_all_assets_to_target(self, target_currency):
        """Sell all assets to a specified target currency."""
        try:
            balances = self.client.get_account()['balances']
            sold_count = 0

            for balance in balances:
                asset = balance['asset']
                free = float(balance['free'])
                
                if asset != target_currency and free > 0:
                    symbol = f"{asset}{target_currency}"
                    try:
                        price = float(self.client.get_symbol_ticker(symbol=symbol)['price'])
                        value = free * price
                        logger.info(f"💱 Selling {free:.6f} {asset} → {target_currency} │ Value: ${value:.2f}")

                        # Place a market sell order
                        self.close_position(symbol=symbol, quantity=free, side='CLOSE')
                        sold_count += 1
                        sleep(1)  # Rate limit protection

                    except Exception as e:
                        logger.error(f"❌ Error selling {asset}: {e}")        

            logger.info(f"✓ Sold {sold_count} assets to {target_currency}")

        except Exception as e:
            logger.error(f"❌ Sell all assets failed: {e}")
            
    def _round_quantity(self, symbol: str, quantity: float) -> float:
        """Round quantity to the appropriate precision for the symbol."""
        # In a real implementation, this would fetch symbol info from the exchange
        # For now, we'll use a simple approach
        return round(quantity, 5)
    
    def _round_price(self, symbol: str, price: float) -> float:
        """Round price to the appropriate precision for the symbol."""
        # In a real implementation, this would fetch symbol info from the exchange
        return round(price, 2)




# # >>>

#     def place_order(self, side: str, symbol: str, quantity: float, data = None) -> Dict:
#         """
#         Place a market order.
        
#         Args:
#             symbol: Trading pair symbol (e.g., 'BTCUSDT')
#             side: 'BUY' or 'SELL'
#             quantity: Quantity to buy/sell
            
#         Returns:
#             Order information
#         """
#         # Get the latest price from the historical data
#         try:
#             logger.debug(f"data {data['close']}")
#             price = data['close']
#         except Exception as e:
#             raise RuntimeError(f"Cannot retrieve latest price: {e}")
        
#         try:
#             logger.info(f"Placing {side} market order for {quantity} {symbol}")

#             # Round quantity to appropriate precision
#             quantity = self._round_quantity(symbol, quantity)

#             order = self.client.create_order(
#                 symbol=symbol,
#                 side=side.upper(),
#                 type=Client.ORDER_TYPE_MARKET,
#                 quantity=quantity
#             )
#             logger.info(f"Order placed: {order}")

#             if self.performance_tracker:
#                 if side.upper() == 'BUY':
#                     # trade_id = self.performance_tracker.record_entry(symbol, price, quantity)
#                     trade_id = self.performance_tracker.record_trade(symbol, price, quantity)

#                 elif side.upper() == 'CLOSE':
#                     # self.performance_tracker.record_exit(symbol, price)
#                     self.performance_tracker.record_trade(symbol, price, -quantity)

#             return order
#         except Exception as e:
#             raise RuntimeError(f"Order failed: {e}")
    
#     def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict:
#         """
#         Place a limit order.
        
#         Args:
#             symbol: Trading pair symbol (e.g., 'BTCUSDT')
#             side: 'BUY' or 'SELL'
#             quantity: Quantity to buy/sell
#             price: Limit price
            
#         Returns:
#             Order information
#         """
#         try:
#             logger.info(f"Placing {side} limit order for {quantity} {symbol} at {price}")
            
#             # Round values to appropriate precision
#             quantity = self._round_quantity(symbol, quantity)
#             price = self._round_price(symbol, price)
            
#             if self.test_mode:
#                 # Test order
#                 logger.info(f"Test limit order placed: {side} {quantity} {symbol} at {price}")
#                 return {'status': 'TEST_ORDER', 'symbol': symbol, 'quantity': quantity, 'price': price}
#             else:
#                 # Real order
#                 order = self.client.create_order(
#                     symbol=symbol,
#                     side=side,
#                     type='LIMIT',
#                     timeInForce='GTC',  # Good Till Cancelled
#                     quantity=quantity,
#                     price=price
#                 )
#                 logger.info(f"Order placed: {order}")
#                 return order
                
#         except Exception as e:
#             logger.error(f"Error placing limit order: {e}")
#             return {'status': 'ERROR', 'message': str(e)}
    
#     def place_stop_loss(self, symbol: str, side: str, quantity: float, stop_price: float) -> Dict:
#         """
#         Place a stop loss order.
        
#         Args:
#             symbol: Trading pair symbol (e.g., 'BTCUSDT')
#             side: 'BUY' or 'SELL' (opposite of the main position)
#             quantity: Quantity to buy/sell
#             stop_price: Stop price
            
#         Returns:
#             Order information
#         """
#         try:
#             logger.info(f"Placing {side} stop loss for {quantity} {symbol} at {stop_price}")
            
#             # Round values to appropriate precision
#             quantity = self._round_quantity(symbol, quantity)
#             stop_price = self._round_price(symbol, stop_price)
            
#             if self.test_mode:
#                 # Test order
#                 logger.info(f"Test stop loss placed: {side} {quantity} {symbol} at {stop_price}")
#                 return {'status': 'TEST_ORDER', 'symbol': symbol, 'quantity': quantity, 'stop_price': stop_price}
#             else:
#                 # Real order
#                 order = self.client.create_order(
#                     symbol=symbol,
#                     side=side,
#                     type='STOP_LOSS_LIMIT',
#                     timeInForce='GTC',
#                     quantity=quantity,
#                     price=stop_price * 0.99 if side == 'SELL' else stop_price * 1.01,  # Small buffer to be reviewed
#                     stopPrice=stop_price
#                 )
#                 logger.info(f"Stop loss placed: {order}")
#                 return order
                
#         except Exception as e:
#             logger.error(f"Error placing stop loss: {e}")
#             return {'status': 'ERROR', 'message': str(e)}
 
class MockExecutionHandler:
    """
    Mock execution handler for backtesting without real API calls.
    
    Simulates order execution and tracks positions locally.
    Works with MockPortfolioInfo to simulate balance changes.
    """
    
    def __init__(self, test_mode: bool = False, performance_tracker: Optional['PerformanceTracker'] = None, 
                 portfolio_info: Optional['MockPortfolioInfo'] = None):
        """Initialize the mock execution handler."""
        self.performance_tracker = performance_tracker
        self.portfolio_info = portfolio_info
        self.positions = {}  # Symbol -> Position details
        self.trade_history = []
        logger.info(f"🧪 Mock Execution Handler initialized │ Tracker: {'Yes' if performance_tracker else 'No'}")

    
    def open_long_position(self, symbol: str, quantity: float, data=None,
                          stop_loss: Optional[float] = None, 
                          take_profit: Optional[float] = None, signal: Optional[Dict] = None,
                          total_portfolio_value: Optional[float] = None) -> Dict:
        """Simulate opening a long position."""
        try:
            # Extract last price from DataFrame or scalar value
            price = data['close'].iloc[-1] if hasattr(data['close'], 'iloc') else data['close']  # Get the last price in the data
            data_time = data['timestamp'].iloc[-1] if hasattr(data['timestamp'], 'iloc') else data['timestamp']  # Get the last timestamp in the data
        except Exception as e:
            logger.error(f"❌ Cannot retrieve price: {e}")
            return {'status': 'ERROR', 'message': str(e)}

        cost = quantity * price
        logger.info(f"🟢 MOCK LONG │ {symbol} │ {quantity:.6f} @ ${price:.2f} │ Cost: ${cost:.2f}")
        
        # Store position details for tracking
        self.positions[symbol] = {
            'type': PositionType.LONG,
            'entry_price': price,
            'quantity': quantity,
            'entry_time': data_time,
            # 'stop_loss': stop_loss,
            # 'take_profit': take_profit
        }
        
        # Record trade in performance tracker if available
        if self.performance_tracker:
            self.performance_tracker.record_trade(
                symbol, price, quantity, data_time, signal, total_portfolio_value
                )

        self.trade_history.append({
            'time': data_time, 'symbol': symbol, 'type': 'LONG', 
            'quantity': quantity, 'price': price
        })

        return {'status': 'FILLED', 'price': price, 'symbol': symbol, 'quantity': quantity}
    
    def open_short_position(self, symbol: str, quantity: float, data=None,
                           stop_loss: Optional[float] = None,
                           take_profit: Optional[float] = None, signal: Optional[Dict] = None,
                           total_portfolio_value: Optional[float] = None) -> Dict:
        """Simulate opening a short position."""
        try:
            price = data['close'].iloc[-1] if hasattr(data['close'], 'iloc') else data['close']  # Get the last price in the data
            data_time = data['timestamp'].iloc[-1] if hasattr(data['timestamp'], 'iloc') else data['timestamp']  # Get the last timestamp in the data
        except Exception as e:
            logger.error(f"❌ Cannot retrieve price: {e}")
            return {'status': 'ERROR', 'message': str(e)}

        value = quantity * price
        logger.info(f"🔴 MOCK SHORT │ {symbol} │ {quantity:.6f} @ ${price:.2f} │ Value: ${value:.2f}")
        
        self.positions[symbol] = {
            'type': PositionType.SHORT,
            'entry_price': price,
            'quantity': quantity,
            'entry_time': data_time,
            # 'stop_loss': stop_loss,
            # 'take_profit': take_profit
        }
        
        if self.performance_tracker:
            self.performance_tracker.record_trade(
                symbol, price, quantity, data_time, signal, total_portfolio_value
            )

        self.trade_history.append({
            'time': data_time, 'symbol': symbol, 'type': 'SHORT', 
            'quantity': quantity, 'price': price
        })
        
        return {'status': 'FILLED', 'price': price, 'symbol': symbol, 'quantity': quantity}
    
    def close_position(self, symbol: str, data=None, signal: Optional[Dict] = None,total_portfolio_value: Optional[float] = None) -> Dict:
        """Simulate closing a position."""
        
        if symbol not in self.positions:
            logger.error(f"❌ No mock position found for {symbol}")
            return {'status': 'ERROR', 'message': f'No position for {symbol}'}
        try:
            # Get current position from portfolio
   
            positions = self.portfolio_info.get_account_balance()
            base_asset = symbol.replace('USDT', '')

            position_qty = positions.get(base_asset, {}).get('free', 0) - positions.get(base_asset, {}).get('locked', 0)
            price = data['close'].iloc[-1] if hasattr(data['close'], 'iloc') else data['close']
            data_time = data['timestamp'].iloc[-1]

            position = positions.get(symbol, None).get('free', None) - positions.get(symbol, None).get('locked', None)

        except Exception as e:
            logger.error(f"❌ Cannot retrieve close data: {e}")
            return {'status': 'ERROR', 'message': str(e)}

        # Calculate P&L
        stored_position = self.positions[symbol]
        entry_price = stored_position['entry_price']
        
        if stored_position['type'] == PositionType.LONG:
            pnl_pct = ((price / entry_price) - 1) * 100
        else:
            pnl_pct = ((entry_price / price) - 1) * 100
        
        pnl_symbol = "📈" if pnl_pct > 0 else "📉"
        logger.info(f"⚪ MOCK CLOSE │ {symbol} │ {abs(position):.6f} @ ${price:.2f} │ {pnl_symbol} P&L: {pnl_pct:+.2f}%")

        if self.performance_tracker:
            logger.debug(f"   Recording: price={price}, qty={-position}, time={data_time}, portfolio=${total_portfolio_value}")
            self.performance_tracker.record_trade(symbol, price, quantity=-position, timestamp=data_time, signal=signal, total_portfolio_value=total_portfolio_value)

        self.trade_history.append({
            'time': data_time, 'symbol': symbol, 'type': 'CLOSE', 
            'quantity': position, 'price': price, 'pnl_pct': pnl_pct
        })
        
        del self.positions[symbol]
        return {'status': 'FILLED', 'quantity': position, 'price': price}
    
    
    def place_stop_loss(self, symbol: str, side: str, quantity: float, stop_price: float):
        """Place a mock stop loss order."""
        logger.debug(f"🛑 MOCK STOP LOSS │ {symbol} │ {side} {quantity:.6f} @ ${stop_price:.2f}")
        
        return {
            'symbol': symbol,
            'side': side,
            'quantity': quantity,
            'stop_price': stop_price,
            'status': 'NEW'
        }
    
    def get_current_positions(self) -> Dict:
        """Get all current mock positions."""
        if self.positions:
            logger.debug(f"📋 Mock positions: {len(self.positions)} open")
            for symbol, pos in self.positions.items():
                logger.debug(f"   {symbol}: {pos.get('type', 'UNKNOWN')} {pos['quantity']:.6f} @ ${pos['entry_price']:.2f}")
        return self.positions.copy()
    
    def get_current_data(self, symbol: str) -> float:
        """Get the current price for a symbol (placeholder)."""
        logger.debug(f"⚠ get_current_data not implemented for mock handler")
        return 0.0
