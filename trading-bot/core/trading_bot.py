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
        
        self.logger.debug(f"🤖 Trading bot initialized │ Mode: {'TEST' if test_mode else 'LIVE'} │ Symbols: {self.symbols}")

    def run(self) -> None:
        """
        Start the trading bot main loop on live mode.
        
        Initiates price fetching thread and begins candle processing.
        Handles graceful shutdown on keyboard interrupt or errors.
        """
        self.logger.debug(f"{'='*70}")
        self.logger.debug(f"🚀 STARTING TRADING BOT LIVE")
        self.logger.debug(f"{'='*70}")
        self.logger.debug(f"│ Candle Interval: {self.candle_interval_seconds}s")
        self.logger.debug(f"│ Price Check: Every {self.price_fetch_interval}s")
        self.logger.debug(f"└{'─'*68}")


        self.running = True
        self.data_manager.running = True
        
        try:
            # Start price fetching in separate thread
            price_thread = self.data_manager.initiate_start_thread()
            if price_thread:
                self.threads.append(price_thread)
                self.logger.debug("✓ Price fetching thread started")
            
            # Start main candle processing loop (blocking)
            self.logger.debug("✓ Entering main candle processing loop...\n")
            self.data_manager.live_main_candle_processing_loop()
            
        except KeyboardInterrupt:
            self.logger.debug("\n⚠ Bot stopped by user (Ctrl+C)")
        except Exception as e:
            self.logger.error(f"❌ Fatal error in main loop: {e}", exc_info=True)
        finally:
            self.stop()

    def _process_symbol_candle_completion(
        self, 
        symbol: str
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
            # Retrieve stored data around OHLCV and AUX data  
            data = self.data_manager.get_data_history(symbol, count=1)

            if data.empty:
                self.logger.warning(f"⚠ No data available for {symbol}")
                return
            close = data['close'].iloc[-1]
            data_time = data['timestamp'].iloc[-1]
            self.logger.debug(f"🕯 CANDLE │ {symbol} │ {data_time} │ Close: ${close:.2f} ")

            # Retrieve portfolio information
            balances = self.portfolio_info.get_account_balance()
            total_portfolio_value = self.portfolio_info._calculate_total_portfolio_value(balances, close)
            self.logger.debug(f"   💼 Portfolio: ${total_portfolio_value:.2f}")
            previous_allocation = self.portfolio_info._calculate_actual_allocation(close, balances, total_portfolio_value)

            # Update strategy with data history and generate signals
            self.strategy.update(data)
            signal = self.strategy.generate_signals()
            self.logger.debug(f"   🧠 Forecast: {signal.forecast:+.4f} │ Confidence: {signal.confidence:+.4f} │ Regime: {signal.regime} (score: {signal.debug_info.get('score_regime', None)})")

            # Get target allocation from forecast
            target_allocation = self.forecast_manager.forecast_to_allocation(signal.forecast)
            allocation_change = self.forecast_manager.calculate_allocation_change(target_allocation, previous_allocation)
            
            #Init variables
            approved_rebalance = None
            debug_approve_allocation_change = {}
            success_execute_portfolio_rebalance = None
            debug_execute_portfolio_rebalance = {}
            
            if abs(allocation_change) != 0.0:
                # Check if rebalance is ok from risk management perspective
                approved_rebalance, debug_approve_allocation_change = self.risk_manager.approve_allocation_change(symbol, allocation_change, data)

                if approved_rebalance:
                    self.logger.debug(
                        f"   🔄 EXECUTING REBALANCE │ Actual: {previous_allocation} → Target: {target_allocation} "
                    )

                    success_execute_portfolio_rebalance , debug_execute_portfolio_rebalance = self.execution_handler._execute_portfolio_rebalance( 
                        symbol=symbol,
                        target_allocation=target_allocation,
                        actual_allocation=previous_allocation,  
                        allocation_change=allocation_change,
                        balances=balances,
                        total_portfolio_value=total_portfolio_value,
                        data=data,
                        signal=signal
                    )

                    if success_execute_portfolio_rebalance: 
                        self.logger.debug("   ✓ REBALANCE executed successfully")
                    else: 
                        self.logger.error(f"   ✗ REBALANCE execution failed. Debug info: {debug_execute_portfolio_rebalance}")

                else:
                    self.logger.debug(f"   X🔄X No rebalance performed (rejected) │ Actual allocation: {previous_allocation:+.4f} | Δ (rejected): {allocation_change:+.4f}")
                
            # Retrieve portfolio information after rebalance 
            postRebalance_balances = self.portfolio_info.get_account_balance() if success_execute_portfolio_rebalance else balances
            postRebalance_total_portfolio_value = self.portfolio_info._calculate_total_portfolio_value(postRebalance_balances, close) if success_execute_portfolio_rebalance else total_portfolio_value
            if success_execute_portfolio_rebalance : self.logger.debug(f"   💼 Portfolio after rebalance: ${postRebalance_total_portfolio_value:.2f}")
            postRebalance_current_allocation = self.portfolio_info._calculate_actual_allocation(close, postRebalance_balances, postRebalance_total_portfolio_value) if success_execute_portfolio_rebalance else previous_allocation
            
            # === RECORD PORTFOLIO STATE === --> This is to store at a bar level and visualize it in a graph.
            if hasattr(self, 'portfolio_state_tracker'):
                tracker = getattr(self, 'portfolio_state_tracker', None)
                tracker.record_state(
                    data = data,
                    balances=balances,
                    total_portfolio_value=total_portfolio_value,
                    previous_allocation = previous_allocation,
                    signal=signal,
                    allocation_change = allocation_change,
                    approved_rebalance=approved_rebalance if abs(allocation_change) != 0.0 else None,
                    debug_approve_allocation_change=debug_approve_allocation_change if abs(allocation_change) != 0.0 else {},
                    succcess_execute_portfolio_rebalance = success_execute_portfolio_rebalance if approved_rebalance else None,
                    debug_execute_portfolio_rebalance = debug_execute_portfolio_rebalance if approved_rebalance else {},
                    postRebalance_balances=postRebalance_balances,
                    postRebalance_total_value=postRebalance_total_portfolio_value,
                    postRebalance_current_allocation=postRebalance_current_allocation
                )
            
            else: 
                self.logger.warning(f"   ⚠ No portfolio state tracker available, skipping state recording")

        except Exception as e:
            self.logger.error(
                f"❌ Error processing candle for {symbol}: {e}", 
                exc_info=True
            )


    def stop(self) -> None:
        """
        Stop the trading bot gracefully in Live Mode.
        
        Stops data manager, joins threads, and logs shutdown.
        """
        self.logger.debug(f"\n{'='*70}")
        self.logger.debug(f"🛑 INITIATING BOT SHUTDOWN")
        self.logger.debug(f"{'='*70}")

        self.running = False
        
        if hasattr(self.data_manager, 'running'):
            self.data_manager.running = False
        
        # Complete threads of Live data
        for i, thread in enumerate(self.threads):
            if thread.is_alive():
                self.logger.debug(f"│ Waiting for thread {i+1}/{len(self.threads)}...")
                thread.join(timeout=5)
                if thread.is_alive():
                    self.logger.warning(f"│ ⚠ Thread {i+1} timeout")
                else:
                    self.logger.debug(f"│ ✓ Thread {i+1} stopped")
        
        # Closting all positions
        self._close_all_positions_at_end()

        self.logger.debug(f"└{'─'*68}")
        self.logger.debug(f"✓ Trading bot stopped successfully")
        self.logger.debug(f"{'='*70}\n")

    def _close_all_positions_at_end(self):
        """Force-close any positions still open at end of backtest."""
        
        #Checking if any open position
        open_positions = self.performance_tracker.get_open_positions()
        if not open_positions:
            self.logger.debug("   No open positions to close")
            return
        self.logger.debug(f"   Closing {len(open_positions)} open position(s)...")

        for symbol, position_info in open_positions.items():
            try:
                # Use the shared candle history from DataManager
                data = self.data_manager.get_data_history(symbol)
                if data.empty:
                    self.logger.warning(f"   ⚠ No price data for {symbol}, cannot close")
                    continue
                close = data['close'].iloc[-1]

                balances = self.portfolio_info.get_account_balance()
                total_value = self.portfolio_info._calculate_total_portfolio_value(balances, close)
                actual_allocation = self.portfolio_info._calculate_actual_allocation(close, balances, total_value)

                target_allocation = 0.0  # Force flat
                allocation_change = self.forecast_manager.calculate_allocation_change(target_allocation, actual_allocation)
                if abs(allocation_change) != 0.0:             
                    self.logger.debug(f"   🔚 Force closing {symbol} │ {actual_allocation:+.4f} → 0.0 @ ${close:.2f}")

                    success_execute_portfolio_rebalance, debug_execute_portfolio_rebalance = self.execution_handler._execute_portfolio_rebalance(
                        symbol=symbol,
                        target_allocation=target_allocation,
                        actual_allocation=actual_allocation,
                        allocation_change=allocation_change,
                        balances=balances,
                        total_portfolio_value=total_value,
                        data=data,
                        signal={}
                    )

                    if success_execute_portfolio_rebalance: 
                        self.logger.debug(f"   ✓ {symbol} closed successfully")
                    else: 
                        self.logger.error(f"   ✗ {symbol} close failed: {debug_execute_portfolio_rebalance}")
                else:
                    self.logger.warning(f"   {symbol} foreact was already at 0, but position opened")

                # Retrieve portfolio information after rebalance 
                postRebalance_balances = self.portfolio_info.get_account_balance() if success_execute_portfolio_rebalance else balances
                postRebalance_total_portfolio_value = self.portfolio_info._calculate_total_portfolio_value(postRebalance_balances, close) if success_execute_portfolio_rebalance else total_value
                if success_execute_portfolio_rebalance : self.logger.debug(f"   💼 Portfolio after rebalance: ${postRebalance_total_portfolio_value:.2f}")
                postRebalance_current_allocation = self.portfolio_info._calculate_actual_allocation(close, postRebalance_balances, postRebalance_total_portfolio_value) if success_execute_portfolio_rebalance else previous_allocation
                
                # === RECORD PORTFOLIO STATE === --> This is to store at a bar level and visualize it in a graph.
                if hasattr(self, 'portfolio_state_tracker'):
                    tracker = getattr(self, 'portfolio_state_tracker', None)
                    tracker.record_state(
                        data = data,
                        balances=balances,
                        total_portfolio_value=total_value,
                        previous_allocation = actual_allocation,
                        signal={},
                        allocation_change = allocation_change,
                        approved_rebalance=None,
                        debug_approve_allocation_change= {},
                        succcess_execute_portfolio_rebalance = success_execute_portfolio_rebalance ,
                        debug_execute_portfolio_rebalance = debug_execute_portfolio_rebalance ,
                        postRebalance_balances=postRebalance_balances,
                        postRebalance_total_value=postRebalance_total_portfolio_value,
                        postRebalance_current_allocation=postRebalance_current_allocation
                    )
                
                else: 
                    self.logger.warning(f"   ⚠ No portfolio state tracker available, skipping state recording")


            except Exception as e:
                self.logger.error(f"   ❌ Error closing {symbol}: {e}", exc_info=True)
