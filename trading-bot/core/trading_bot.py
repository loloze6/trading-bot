"""
Trading Bot Core Module
Handles live trading operations including signal processing, position management,
and portfolio rebalancing based on forecast allocations.
"""

import time
import datetime
import logging
from typing import Any, Dict, List, Optional, Tuple
from performance.metrics import EnhancedPerformanceTracker, CompletedTrade
from data.data_manager import Candle


class TradingBot:
    """
    Core trading bot that manages live trading operations.
    
    Handles candle processing, signal generation, risk management,
    and position execution for multiple trading symbols.
    """

    def __init__(
        self,
        data_manager=None,
        strategy=None,
        execution_handler=None,
        logger: Optional[logging.Logger] = None,
        portfolio_info=None,
        portfolio_state_tracker=None,
        forecast_manager=None,
        risk_manager=None,
        performance_tracker: Optional[EnhancedPerformanceTracker] = None,
        price_fetch_interval: int = 60,
        candle_interval_seconds: int = 180,
        test_mode: bool = True,
        symbols: List[str] = None
    ):
        """
        Initialize the trading bot.

        Args:
            data_manager: Manager for price data and candles
            strategy: Trading strategy instance
            execution_handler: Handler for order execution
            logger: Logger instance for bot operations
            portfolio_info: Portfolio information manager
            forecast_manager: Manager for forecast-based allocations
            risk_manager: Risk management instance
            performance_tracker: Performance tracking instance
            price_fetch_interval: Interval for fetching price data (seconds)
            candle_interval_seconds: Candle formation interval (seconds)
            test_mode: Whether running in test mode
            symbols: List of trading symbols
        """
        # Core components
        self.data_manager = data_manager
        self.strategy = strategy
        self.execution_handler = execution_handler
        self.logger = logger or logging.getLogger(__name__)
        self.portfolio_info = portfolio_info
        self.portfolio_state_tracker = portfolio_state_tracker
        self.forecast_manager = forecast_manager
        self.risk_manager = risk_manager
        self.performance_tracker = performance_tracker
        
        # Configuration
        self.price_fetch_interval = price_fetch_interval
        self.candle_interval_seconds = candle_interval_seconds
        self.test_mode = test_mode
        self.symbols = symbols or ['BTCUSDT']
        
        # Trading state
        self.open_trades: Dict[str, CompletedTrade] = {}
        self.closed_trades: List[CompletedTrade] = []
        self.equity_curve: List[Dict[str, Any]] = []
        self.positions: Dict[str, Dict] = {}
        
        # Data access
        self.candle_builder = data_manager.candle_builder if data_manager else None
        
        # Threading control
        self.running = False
        self.threads: List = []
        
        self.logger.info(f"🤖 Trading bot initialized │ Mode: {'TEST' if test_mode else 'LIVE'} │ Symbols: {self.symbols}")

    def run(self) -> None:
        """
        Start the trading bot main loop.
        
        Initiates price fetching thread and begins candle processing.
        Handles graceful shutdown on keyboard interrupt or errors.
        """
        self.logger.info(f"{'='*70}")
        self.logger.info(f"🚀 STARTING TRADING BOT")
        self.logger.info(f"{'='*70}")
        self.logger.info(f"│ Candle Interval: {self.candle_interval_seconds}s")
        self.logger.info(f"│ Price Check: Every {self.price_fetch_interval}s")
        self.logger.info(f"└{'─'*68}")


        self.running = True
        self.data_manager.running = True
        
        try:
            # Start price fetching in separate thread
            price_thread = self.data_manager.initiate_start_thread()
            if price_thread:
                self.threads.append(price_thread)
                self.logger.info("✓ Price fetching thread started")
            
            # Start main candle processing loop (blocking)
            self.logger.info("✓ Entering main candle processing loop...\n")
            self.data_manager._main_candle_processing_loop()
            
        except KeyboardInterrupt:
            self.logger.info("\n⚠ Bot stopped by user (Ctrl+C)")
        except Exception as e:
            self.logger.error(f"❌ Fatal error in main loop: {e}", exc_info=True)
        finally:
            self.stop()

    def _process_symbol_candle_completion(
        self, 
        symbol: str, 
        completed_candle: Candle
    ) -> None:
        """
        Process candle completion for a specific symbol.
        
        Called automatically when a candle is completed. Generates signals,
        updates target allocations, and executes rebalancing if needed.

        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            completed_candle: The completed candle object
        """
        try:
            # Get historical candle data for strategy
            data = self.candle_builder.get_candle_history(symbol)
            
            if data.empty:
                self.logger.warning(f"⚠ No candle data available for {symbol}")
                return
            
            # Update strategy and generate signals
            self.strategy.update(data)
            signal = self.strategy.generate_signals()
            
            forecast = signal.get('forecast', 0.0)
            confidence = signal.get('confidence', 0.0)
            regime = signal.get('regime', 'N/A')
            debug_info = signal.get('debug_info', {})
            forecast_regime = debug_info.get('score_regime', None)

            candle_time = data['timestamp'].iloc[-1]
            
            # Single line candle log
            self.logger.info(f"🕯 CANDLE │ {symbol} │ {candle_time} │ Close: ${completed_candle.close:.2f} ")

            # Get target allocation from forecast
            target_allocation = self.forecast_manager.forecast_to_allocation(forecast)

            # === CALCULATE ACTUAL MARKET ALLOCATION ===
            balances = self.portfolio_info.get_account_balance()
            total_value = self._calculate_total_portfolio_value(balances, completed_candle.close)
            

            self.logger.info(f"   💼 Portfolio: ${total_value:.2f}")
            self.logger.info(f"   🧠 Forecast: {forecast:+.4f} │ Regime: {regime} (score: {forecast_regime})")

            # Calculate actual position value for
            # For BTCUSDT: (free + locked) * current_price
            btc_balance = balances.get('BTCUSDT', balances.get('BTC', {}))
            btc_quantity = btc_balance.get('free', 0.0) - btc_balance.get('locked', 0.0)
            position_value = btc_quantity * completed_candle.close            
            actual_allocation = position_value / total_value if total_value > 0 else 0.0
            self.logger.debug(f"   Position Value: ${position_value:.2f} │ Actual Allocation: {actual_allocation:+.4f} │ Target Allocation: {target_allocation:+.4f}")

            # Check if rebalance needed compared to threshold
            needs_rebalance, allocation_change = self.forecast_manager.needs_rebalance(
                symbol, target_allocation, actual_allocation
            )
            
            if needs_rebalance:
                self.logger.info(
                    f"   🔄 REBALANCE │ Actual: {actual_allocation} → Target: {target_allocation} "
                )

                # Risk management approval
                if self.risk_manager and not self.risk_manager.approve_allocation_change(
                    symbol, allocation_change, data
                ):
                    self.logger.warning(f"   ✗ REJECTED by risk manager")
                    return
                
                # Execute portfolio rebalancing
                self.logger.info(f"   ✓ APPROVED - Executing...")
                self._execute_portfolio_rebalance( 
                    symbol=symbol,
                    target_allocation=target_allocation,
                    actual_allocation=actual_allocation,  
                    current_price=completed_candle.close,
                    data=data,
                    signal=signal
                )
                # self.logger.info(f"   ✓ COMPLETE │ New Target reached: {target_allocation:+.4f}")

                # self.forecast_manager.set_target_allocation(symbol, target_allocation)

            else:
                self.logger.info(f"   X🔄X No rebalance needed │ Actual allocation: {actual_allocation:+.4f} | Δ: {allocation_change:+.4f}")
                               
            
            # === RECORD PORTFOLIO STATE === --> This is to store at a bar level and visualize it in a graph.
            if hasattr(self, 'portfolio_state_tracker'):
                tracker = getattr(self, 'portfolio_state_tracker', None)
                
                # Get current balances
                current_balances = self.portfolio_info.get_account_balance()
                
                # Calculate total portfolio value
                end_of_bar_value = self._calculate_total_portfolio_value(current_balances, completed_candle.close)
                
                # # Get current allocation
                # current_allocation = self.forecast_manager.get_current_allocation(symbol)
                current_allocation = self.forecast_manager.get_target_allocation(symbol)

                # 3. Calculate the true post-trade allocation
                btc_balance = current_balances.get(symbol.replace('USDT', ''), {}) 
                btc_qty = btc_balance.get('free', 0.0) + btc_balance.get('locked', 0.0)
                actual_alloc = (btc_qty * completed_candle.close) / end_of_bar_value if end_of_bar_value > 0 else 0.0

                # Record state - To be cleaned up and standardized later
                tracker.record_state(
                    timestamp=candle_time,
                    forecast=forecast,
                    needs_rebalance=needs_rebalance,
                    total_portfolio_value=end_of_bar_value,
                    balances=current_balances,
                    allocation=current_allocation,
                    regime=regime,
                    price=completed_candle.close
                )
            else: 
                self.logger.warning(f"   ⚠ No portfolio state tracker available, skipping state recording")

        except Exception as e:
            self.logger.error(
                f"❌ Error processing candle for {symbol}: {e}", 
                exc_info=True
            )

    def _execute_portfolio_rebalance(
        self,
        symbol: str,
        target_allocation: float,
        actual_allocation: float,  # ✅ Receive as parameter
        current_price: float,
        data: Dict,
        signal: Optional[Dict] = None
    ) -> None:
        """
        Execute portfolio rebalancing to reach target allocation.

        Args:
            symbol: Trading symbol
            target_allocation: Target allocation (-1.0 to 1.0)
            actual_allocation: Current actual market-value allocation
            current_price: Current asset price
            data: Market data dictionary
            signal: Optional signal dictionary with metadata
        """
        try:
            # # Get current allocation and calculate change
            # current_allocation = self.forecast_manager.get_current_allocation(symbol) 
            # allocation_change = target_allocation - current_allocation
            
            allocation_change = target_allocation - actual_allocation

            # Get portfolio balances and value
            balances = self.portfolio_info.get_account_balance()
            self.logger.debug(f"   Balances: {balances}")
            
            quote_currency = self._extract_quote_currency(symbol)
            if quote_currency not in balances:
                self.logger.error(f"   ✗ Quote currency {quote_currency} not found")
                return
                
            # Calculate total portfolio value
            total_portfolio_value = self._calculate_total_portfolio_value(
                balances, current_price
            )
        
            # Calculate target position value and quantity
            target_position_value = total_portfolio_value * abs(target_allocation)
            quantity = target_position_value / current_price
            
            self.logger.info(f"   💼 Portfolio: ${total_portfolio_value:.2f} │ Target Position: ${target_position_value:.2f} ({quantity:.6f} units)")

            
            # Determine action based on allocation change direction
            if allocation_change > 0:
                self._handle_allocation_increase(
                    symbol, actual_allocation, target_allocation,
                    allocation_change, quantity, current_price,
                    data, signal, total_portfolio_value
                )
            elif allocation_change < 0:
                self._handle_allocation_decrease(
                    symbol, actual_allocation, target_allocation,
                    allocation_change, quantity, current_price,
                    data, signal, total_portfolio_value
                )
            
            # Update stored target allocation after successful execution
            self.forecast_manager.set_target_allocation(symbol, target_allocation)
            # self.logger.info(f"   ✓ COMPLETE │ New Allocation: {target_allocation:+.4f}\n")
            
        except Exception as e:
            self.logger.error(f"   ❌ Rebalance error for {symbol}: {e}", exc_info=True)

    def _handle_allocation_increase(
        self,
        symbol: str,
        current_allocation: float,
        target_allocation: float,
        allocation_change: float,
        quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict],
        total_portfolio_value: float
    ) -> None:
        """
        Handle increasing allocation (more long or less short).

        Args:
            symbol: Trading symbol
            current_allocation: Current allocation value
            target_allocation: Target allocation value
            allocation_change: Change in allocation
            quantity: Target position quantity
            current_price: Current price
            data: Market data
            signal: Signal dictionary
            total_portfolio_value: Total portfolio value
        """
        if current_allocation <= 0 and target_allocation >= 0:
            # Transition from short/neutral to long/neutral
            self.logger.info(f"   📈 TRANSITION │ Short/Neutral → Long/Neutral │ {quantity:.6f} @ ${current_price:.2f}")
            
            self._execute_position_transition(
                symbol, current_allocation, target_allocation,
                quantity, current_price, data, signal, total_portfolio_value
            )
        elif current_allocation >= 0:
            # Increase existing long position
            additional_qty = abs(allocation_change) * total_portfolio_value / current_price
            self.logger.info(f"   📈 ADD LONG │ +{additional_qty:.6f} @ ${current_price:.2f}")
            
            self._increase_long_position(
                symbol, additional_qty, current_price, 
                data, signal, total_portfolio_value
            )
        else:
            # Reduce existing short position
            additional_qty = abs(allocation_change) * total_portfolio_value / current_price
            self.logger.info(f"   📈 REDUCE SHORT │ -{additional_qty:.6f} @ ${current_price:.2f}")

            self._reduce_short_position(
                symbol, additional_qty, current_price, 
                data, signal, total_portfolio_value
            )

    def _handle_allocation_decrease(
        self,
        symbol: str,
        current_allocation: float,
        target_allocation: float,
        allocation_change: float,
        quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict],
        total_portfolio_value: float
    ) -> None:
        """
        Handle decreasing allocation (less long or more short).

        Args:
            symbol: Trading symbol
            current_allocation: Current allocation value
            target_allocation: Target allocation value
            allocation_change: Change in allocation
            quantity: Target position quantity
            current_price: Current price
            data: Market data
            signal: Signal dictionary
            total_portfolio_value: Total portfolio value
        """
        if current_allocation >= 0 and target_allocation <= 0:
            # Transition from long/neutral to short/neutral
            self.logger.info(f"   📉 TRANSITION │ Long/Neutral → Short/Neutral │ {quantity:.6f} @ ${current_price:.2f}")

            self._execute_position_transition(
                symbol, current_allocation, target_allocation,
                quantity, current_price, data, signal, total_portfolio_value
            )
        elif current_allocation <= 0:
            # Increase existing short position
            additional_qty = abs(allocation_change) * total_portfolio_value / current_price
            self.logger.info(f"   📉 ADD SHORT │ +{additional_qty:.6f} @ ${current_price:.2f}")
            
            self._increase_short_position(
                symbol, additional_qty, current_price, 
                data, signal, total_portfolio_value
            )
        else:
            # Reduce existing long position
            additional_qty = abs(allocation_change) * total_portfolio_value / current_price
            self.logger.info(f"   📉 REDUCE LONG │ -{additional_qty:.6f} @ ${current_price:.2f}")

            self._reduce_long_position(
                symbol, additional_qty, current_price, 
                data, signal, total_portfolio_value
            )

    def _execute_position_transition(
        self,
        symbol: str,
        current_allocation: float,
        target_allocation: float,
        quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict] = None,
        total_portfolio_value: Optional[float] = None
    ) -> None:
        """
        Execute transition between position types (long/short/neutral).

        Args:
            symbol: Trading symbol
            current_allocation: Current allocation
            target_allocation: Target allocation
            quantity: Position quantity
            current_price: Current price
            data: Market data
            signal: Signal dictionary
            total_portfolio_value: Total portfolio value
        """
        try:
            # Close existing position if significant
            if abs(current_allocation) > 0.00000001:                
                close_order = self.execution_handler.close_position(
                    symbol=symbol, 
                    data=data, 
                    signal=signal, 
                    total_portfolio_value=total_portfolio_value
                )
                if close_order.get('status') == 'ERROR':
                    self.logger.error(f"      ✗ Failed to close existing position")
                    return
                
                # Update local balance after close
                current_quantity = close_order['quantity']
                self.logger.info(f"      ✓ Closed {current_quantity:.6f} @ ${current_price:.2f}")

                self.portfolio_info.update_local_balance(
                    symbol=symbol,
                    price=current_price,
                    quantity=current_quantity,
                    trade_type='CLOSE'
                )

            elif abs(current_allocation) != 0:
                self.logger.warning(f"      ⚠ Current allocation was too small to close: {current_allocation}")

            # Open new position based on target allocation
            if target_allocation > 0.00000001:
                # Open long position
                self._open_long_position(
                    symbol, quantity, current_price, 
                    data, signal, total_portfolio_value
                )
            elif target_allocation < -0.00000001:
                # Open short position
                self._open_short_position(
                    symbol, quantity, current_price, 
                    data, signal, total_portfolio_value
                )
            elif abs(target_allocation) != 0:
                self.logger.warning(f"      ⚠ Target allocation was too small to open: {target_allocation}")
                
        except Exception as e:
            self.logger.error(f"      ❌ Transition error: {e}", exc_info=True)

    def _open_long_position(
        self,
        symbol: str,
        quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict] = None,
        total_portfolio_value: Optional[float] = None
    ) -> None:
        """Open a new long position."""
        try:
            order = self.execution_handler.open_long_position(
                symbol=symbol,
                quantity=quantity,
                data=data,
                signal=signal,
                total_portfolio_value=total_portfolio_value
            )
            
            if order.get('status') != 'ERROR':
                self.portfolio_info.update_local_balance(
                    symbol=symbol,
                    price=current_price,
                    quantity=quantity,
                    trade_type='LONG'
                )
                self.logger.info(f"      ✓ Opened LONG {quantity:.6f} @ ${current_price:.2f} │ Cost: ${quantity * current_price:.2f}")
            else:
                self.logger.error(f"      ✗ Failed to open LONG position")
                
        except Exception as e:
            self.logger.error(f"      ❌ Error opening LONG: {e}", exc_info=True)


    def _open_short_position(
        self,
        symbol: str,
        quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict] = None,
        total_portfolio_value: Optional[float] = None
    ) -> None:
        """Open a new short position."""
        try:
            order = self.execution_handler.open_short_position(
                symbol=symbol,
                quantity=-quantity,
                data=data,
                signal=signal,
                total_portfolio_value=total_portfolio_value
            )
            
            if order.get('status') != 'ERROR':
                self.portfolio_info.update_local_balance(
                    symbol=symbol,
                    price=current_price,
                    quantity=quantity,
                    trade_type='SHORT'
                )
                self.logger.info(f"      ✓ Opened SHORT {quantity:.6f} @ ${current_price:.2f} │ Value: ${quantity * current_price:.2f}")
            else:
                self.logger.error(f"      ✗ Failed to open SHORT position")
                
        except Exception as e:
            self.logger.error(f"      ❌ Error opening SHORT: {e}", exc_info=True)


    def _increase_long_position(
        self,
        symbol: str,
        additional_quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict] = None,
        total_portfolio_value: Optional[float] = None
    ) -> None:
        """Increase existing long position."""
        try:
            order = self.execution_handler.open_long_position(
                symbol=symbol,
                quantity=additional_quantity,
                data=data,
                signal=signal,
                total_portfolio_value=total_portfolio_value
            )
            
            if order.get('status') != 'ERROR':
                self.portfolio_info.update_local_balance(
                    symbol=symbol,
                    price=current_price,
                    quantity=additional_quantity,
                    trade_type='LONG'
                )
                self.logger.info(f"      ✓ Added +{additional_quantity:.6f} to LONG")
            else:
                self.logger.error(f"      ✗ Failed to increase LONG")
                
        except Exception as e:
            self.logger.error(f"      ❌ Error increasing LONG: {e}", exc_info=True)


    def _reduce_short_position(
        self,
        symbol: str,
        additional_quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict] = None,
        total_portfolio_value: Optional[float] = None
    ) -> None:
        """Reduce existing short position (buy to cover)."""
        try:
            order = self.execution_handler.open_long_position(
                symbol=symbol,
                quantity=additional_quantity,
                data=data,
                signal=signal,
                total_portfolio_value=total_portfolio_value
            )
            
            if order.get('status') != 'ERROR':
                self.portfolio_info.update_local_balance(
                    symbol=symbol,
                    price=current_price,
                    quantity=additional_quantity,
                    trade_type='REDUCE_SHORT'
                )
                self.logger.info(f"      ✓ Reduced SHORT by {additional_quantity:.6f}")
            else:
                self.logger.error(f"      ✗ Failed to reduce SHORT")
                
        except Exception as e:
            self.logger.error(f"      ❌ Error reducing SHORT: {e}", exc_info=True)


    def _increase_short_position(
        self,
        symbol: str,
        additional_quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict] = None,
        total_portfolio_value: Optional[float] = None
    ) -> None:
        """Increase existing short position."""
        try:
            order = self.execution_handler.open_short_position(
                symbol=symbol,
                quantity=-additional_quantity,
                data=data,
                signal=signal,
                total_portfolio_value=total_portfolio_value
            )
            
            if order.get('status') != 'ERROR':
                self.portfolio_info.update_local_balance(
                    symbol=symbol,
                    price=current_price,
                    quantity=additional_quantity,
                    trade_type='SHORT'
                )
                self.logger.info(f"      ✓ Added +{additional_quantity:.6f} to SHORT")
            else:
                self.logger.error(f"      ✗ Failed to increase SHORT")
                
        except Exception as e:
            self.logger.error(f"      ❌ Error increasing SHORT: {e}", exc_info=True)


    def _reduce_long_position(
        self,
        symbol: str,
        additional_quantity: float,
        current_price: float,
        data: Dict,
        signal: Optional[Dict] = None,
        total_portfolio_value: Optional[float] = None
    ) -> None:
        """Reduce existing long position (sell)."""
        try:
            order = self.execution_handler.open_short_position(
                symbol=symbol,
                quantity=-additional_quantity,
                data=data,
                signal=signal,
                total_portfolio_value=total_portfolio_value
            )

            if order.get('status') != 'ERROR':
                self.portfolio_info.update_local_balance(
                    symbol=symbol,
                    price=current_price,
                    quantity=additional_quantity,
                    trade_type='REDUCE_LONG'
                )
                self.logger.info(f"      ✓ Reduced LONG by {additional_quantity:.6f}")
            else:
                self.logger.error(f"      ✗ Failed to reduce LONG")
                
        except Exception as e:
            self.logger.error(f"      ❌ Error reducing LONG: {e}", exc_info=True)

    def _extract_quote_currency(self, symbol: str) -> str:
        """
        Extract quote currency from trading symbol.

        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')

        Returns:
            Quote currency string (e.g., 'USDT')
        """
        quote_currencies = ['USDT', 'BUSD', 'BTC', 'ETH', 'BNB']
        
        for currency in quote_currencies:
            if symbol.endswith(currency):
                return currency
        
        # Default fallback
        self.logger.warning(f"Could not extract quote currency from {symbol}, using USDT")
        return 'USDT'

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

        self.logger.debug(f"║ ┌─ PORTFOLIO VALUATION ─")
        
        # Add quote currency balance
        if quote_currency in balances:
            quote_balance = balances[quote_currency].get('free', 0.0)
            total_value += quote_balance
            self.logger.debug(f"║ │ {quote_currency} (free): ${quote_balance}")
            borrowed_balance = balances[quote_currency].get('locked', 0.0)
            total_value -= borrowed_balance
            self.logger.debug(f"║ │ {quote_currency} (locked): ${borrowed_balance}")
        
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
                self.logger.debug(
                    f"║ │ {symbol} (free): {free_balance} × ${current_price} = ${asset_value}"
                )
            
            # Subtract value of locked assets (short positions/liabilities)
            if locked_balance != 0:
                liability_value = locked_balance * current_price
                total_value -= liability_value
                self.logger.debug(
                    f"║ │ {symbol} (locked): {locked_balance} × ${current_price} = -${liability_value}"
                )
        
        self.logger.debug(f"║ └─ TOTAL: ${total_value} {quote_currency}")
        return total_value

    def get_portfolio_status(self) -> Dict:
        """
        Get current portfolio status snapshot.

        Returns:
            Dictionary with current and target allocations
        """
        return {
            'current_allocations': self.forecast_manager.current_allocations.copy(),
            'target_allocations': self.forecast_manager.target_allocations.copy(),
            'symbols': self.symbols,
            'running': self.running,
            'test_mode': self.test_mode
        }

    def stop(self) -> None:
        """
        Stop the trading bot gracefully.
        
        Stops data manager, joins threads, and logs shutdown.
        """
        self.logger.info(f"\n{'='*70}")
        self.logger.info(f"🛑 INITIATING BOT SHUTDOWN")
        self.logger.info(f"{'='*70}")

        self.running = False
        
        if hasattr(self.data_manager, 'running'):
            self.data_manager.running = False
        
        # Wait for threads to finish with timeout
        for i, thread in enumerate(self.threads):
            if thread.is_alive():
                self.logger.info(f"│ Waiting for thread {i+1}/{len(self.threads)}...")
                thread.join(timeout=5)
                if thread.is_alive():
                    self.logger.warning(f"│ ⚠ Thread {i+1} timeout")
                else:
                    self.logger.info(f"│ ✓ Thread {i+1} stopped")
        
        self.logger.info(f"└{'─'*68}")
        self.logger.info(f"✓ Trading bot stopped successfully")
        self.logger.info(f"{'='*70}\n")
