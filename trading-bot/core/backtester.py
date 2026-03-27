import time
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime
from performance.metrics import CompletedTrade, EnhancedPerformanceTracker
import pandas as pd
from data.data_manager import  HistoricalDataFetcher, Candle, MockCandleBuilder
from core.trading_bot import TradingBot

"""
Backtesting Engine
=================
Engine for backtesting trading strategies against historical data.
"""


class BacktestEngine:
    def __init__(self, 
                 data_manager =None, 
                 strategy=None, 
                 execution_handler=None, 
                 logger=None, 
                 portfolio_info=None,
                 portfolio_state_tracker=None,
                 forecast_manager=None,
                 risk_manager=None,
                 performance_tracker=None,
                 price_fetch_interval: int=60, 
                 candle_interval_seconds: int = 300, 
                 test_mode: bool = True, 
                 symbols: List[str] = ['BTCUSDT'],
                 initial_capital: float = 10000.0,
                 commission_rate: float = 0.001,
                 ):
        
        self.data_manager = data_manager 
        self.strategy = strategy 
        self.execution_handler = execution_handler
        self.logger = logger
        self.portfolio_info = portfolio_info
        self.portfolio_state_tracker = portfolio_state_tracker
        self.forecast_manager = forecast_manager
        self.risk_manager = risk_manager
        self.performance_tracker = performance_tracker
        self.price_fetch_interval = price_fetch_interval
        self.candle_interval_seconds = candle_interval_seconds
        
        # Initialize Binance client
        self.symbols = symbols
        self.test_mode = test_mode

        # Initialize BT data
        self.initial_capital = initial_capital
        self.commission_rate = commission_rate
        self.historical_data = {}
        self.data_loaded = {}

        # Trading data
        self.open_trades: Dict[str, Trade] = {}
        self.closed_trades: List[Trade] = []
        self.equity_curve: List[Dict[str, Any]] = []

        logger.info("Backtest bot initialized")
        self.logger.debug(f"self.symbols: {self.symbols}, type self.symbols {type(self.symbols)}")
        for symbol in self.symbols: 
            self.logger.debug(f"symbol: {symbol}, type self.symbols {type(symbol)}")

        # Mock candle builder for backtesting
        self.mock_candle_builder = MockCandleBuilder()
        self.data_manager.candle_builder = self.mock_candle_builder

    def fetch_historical_data(self, start_date, end_date, store_var: dict):

        """
    Fetch historical data and store it into a inputed dictionary
        """
        self.logger.debug(f"Fetch_historical_data is called")

        # formatted_symbols = [self.symbols[:-4] + '/' + self.symbols[-4:] for self.symbols in self.symbols]
        self.logger.info(f"Fetching historical data for {self.symbols} from {start_date} to {end_date}")
        
        # Create data fetcher
        fetcher = HistoricalDataFetcher(
            start_date, 
            end_date, 
            self.symbols, 
            candle_interval_seconds=self.price_fetch_interval, #1min per default?
            exchange='binance', 
            localStorage=True
            )

        # Get data
        try: 
            data = fetcher.get_data()
            # Log statistics for each symbol
            for symbol in self.symbols:         
                if symbol in data and not data[symbol].empty:
                    # Check data continuity
                    is_continuous, gaps = fetcher.validate_data_continuity(symbol)
                    self.logger.info(f"\n{symbol} data summary:")
                    self.logger.info(f"  Records: {len(data[symbol])}")
                    self.logger.info(f"  Date range: {data[symbol]['timestamp'].min()} to {data[symbol]['timestamp'].max()}")
                    self.logger.info(f"  Continuous data: {is_continuous}")

                    store_var[symbol] = data
                    self.data_loaded[symbol] = True

                else:     
                    self.logger.warning(f"BT - No data available for {symbol}")
                    
        except Exception as e:
            self.logger.error(f"Global Error fetching data: {e}",stack_info=True, exc_info=True)
            
        self.logger.info(f"fetch_historical_data completed : {len(store_var) > 0}")
        return len(store_var) > 0

    def load_data(self, start_date='2025-01-01',end_date='2025-01-10'):
        self.logger.info("BT - Loading data...")
        
        if not self.historical_data:
            self.logger.info("BT - Fetch historical data...")
            success = self.fetch_historical_data(start_date, end_date, store_var = self.historical_data) 
            if not success:
                self.logger.error("BT - Failed to fetch historical data. Aborting backtest.")        
        else: 
            self.logger.info("BT - Data was already loaded...")

        # Load data manager with historical data and initialize indexes
        if self.historical_data:
            self.logger.info("BT - Initialize DataManager...")
            self.data_manager.historical_data = self.historical_data
            self.data_manager.initialize()
        else: 
            self.logger.error("BT - Cannot load data manager with historical data")

    def simulate_on_loaded_data(self):
        self.logger.info("BT - Starting backtest...")
        
        """Run the backtest."""
        if not self.data_manager.historical_data:
            self.logger.error("BT - No data in DataManager cannot run backtest.")
            return
        
        # Initate trading bot with mock modules
        self.logger.info("Initiate Trading bot...")
        bot = TradingBot(
            data_manager=self.data_manager,
            strategy=self.strategy,
            execution_handler=self.execution_handler,
            logger=self.logger,
            portfolio_info= self.portfolio_info,
            portfolio_state_tracker= self.portfolio_state_tracker,
            forecast_manager = self.forecast_manager,
            risk_manager=self.risk_manager,
            performance_tracker= self.performance_tracker,
            price_fetch_interval= self.price_fetch_interval, 
            candle_interval_seconds=self.candle_interval_seconds,
            test_mode=True,
            symbols=self.symbols
        )

        # Make required adjustments for backtesting
        self.execution_handler.positions = {}  # Reset positions
        bot.positions = {}

        # Process each time step
        # self.logger.info("Process each time step...")
        finished = False
        while not finished:       

            all_symbols_finished = True
            for symbol in self.symbols:

                if not self.data_manager.has_more_data(symbol):
                    # Process final candle if exists
                    final_candle = self.data_manager.get_final_candle(symbol)
                    if final_candle and symbol in bot.positions:
                        self.logger.info(f"Final candle for {symbol}: SELL because end of backtest")
                        # Get current data for _execute_sell method
                        current_data = self.data_manager.historical_data[symbol][symbol]
                        self.execution_handler.get_current_data = lambda s, current_data=current_data: current_data
                        bot._execute_sell(symbol, current_data)
                    continue
                    
                all_symbols_finished = False

                # Process next tick and check if candle is completed
                completed_candle = self.data_manager.process_next_tick(symbol)
                 
                if completed_candle is not None:
                    self.logger.debug(f"Candle completed for {symbol} at {completed_candle.end_time}")

                    # Update mock candle builder with completed candle
                    self.mock_candle_builder.add_completed_candle(symbol, completed_candle)
                    
                    # Trigger candle completion callback
                    bot._process_symbol_candle_completion(symbol, completed_candle)
                    
                    # Check stop losses with current price
                    self._check_stop_losses(symbol, completed_candle.close)


                
                # Advance to the next candle
                if not self.data_manager.advance(symbol):
                    continue

            if all_symbols_finished:
                finished = True

        metrics = self._end_of_backtest(bot)

        return metrics
    

    def _end_of_backtest(self, bot):

        self.logger.info("")
        self.logger.info("="*70)
        self.logger.info("🏁 BACKTEST ENDING - Closing all open positions")
        self.logger.info("="*70)

        self._close_all_positions_at_end(bot)

        # # === SAVE PORTFOLIO HISTORY ===
        # if hasattr(self, 'portfolio_state_tracker'):
        #     filepath = self.portfolio_state_tracker.save_to_csv()
            
        #     # log summary
        #     summary = self.portfolio_state_tracker.get_summary()
        #     self.logger.info("="*70)
        #     self.logger.info("📊 PORTFOLIO SUMMARY")
        #     self.logger.info("="*70)
        #     self.logger.info(f"   Initial Value: ${summary['initial_value']:.2f}")
        #     self.logger.info(f"   Final Value: ${summary['final_value']:.2f}")
        #     self.logger.info(f"   Total Return: {summary['total_return']:.2f}%")
        #     self.logger.info(f"   Max Drawdown: {summary['max_drawdown']:.2f}%")
        #     self.logger.info(f"   Records: {summary['num_records']}")
        #     self.logger.info("="*70)


        # === REGIME ANALYZIS ===
        self.logger.info(f"\n{'='*80}")
        self.logger.info("TRADE REGIME AGREEMENT ANALYSIS")
        self.logger.info(f"{'='*80}")

        # # Get full price data for ground truth calculation
        # price_data = None
        # if self.historical_data and len(self.symbols) > 0:
        #     symbol = self.symbols[0]  # Primary symbol (BTCUSDT)
        #     if symbol in self.historical_data:
        #         data = self.historical_data[symbol]
        #         # Handle nested dict structure: historical_data['BTCUSDT']['BTCUSDT']
        #         df = data[symbol]
        #         if df is not None and isinstance(df, pd.DataFrame) and not df.empty:
        #             price_data = df.copy()
        #             if price_data is not None:
        #                 # Ensure timestamp is datetime
        #                 price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])
        #                 self.logger.debug(f"Using {len(price_data)} bars for ground truth calculation")

# Extract base price data
        price_data = self.extract_historical_price_data()
        
        # === NEW: MERGE TICK-BY-TICK STATE INTO PRICE DATA ===
# 2. Merge Tick-by-Tick State using your tracker's native get_dataframe()
        tracker = getattr(self, 'portfolio_state_tracker', None)
        
        if tracker and tracker.states:  # Check if states list has data
            state_df = tracker.get_dataframe()
            
            # Ensure datetime format for merging
            state_df['timestamp'] = pd.to_datetime(state_df['timestamp'])
            price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])
            
            # Rename total_portfolio_value to portfolio_value so the chart recognizes it
            if 'total_portfolio_value' in state_df.columns:
                state_df['portfolio_value'] = state_df['total_portfolio_value']
                
            # Select columns to merge
            cols_to_merge = ['timestamp']
            if 'forecast' in state_df.columns: cols_to_merge.append('forecast')
            if 'portfolio_value' in state_df.columns: cols_to_merge.append('portfolio_value')
            if 'regime' in state_df.columns: cols_to_merge.append('regime') # <-- NEW

            # Merge into price_data
            price_data = pd.merge(price_data, state_df[cols_to_merge], on='timestamp', how='left')
            
            # Rename and forward-fill so every bar has a calculated regime
            if 'regime' in price_data.columns:
                price_data.rename(columns={'regime': 'calc_regime'}, inplace=True)
                price_data['calc_regime'] = price_data['calc_regime'].ffill().fillna('UNKNOWN')

            # Forward-fill portfolio values and default empty forecasts to 0
            if 'portfolio_value' in price_data.columns:
                price_data['portfolio_value'] = price_data['portfolio_value'].ffill() 
            if 'forecast' in price_data.columns:
                price_data['forecast'] = price_data['forecast'].fillna(0.0)
                
            self.logger.info(f"✓ State merged successfully. Columns available: {price_data.columns.tolist()}")
        else:
            self.logger.warning("⚠ Could not find portfolio states! Make sure tracker.record_state() is running.")

        self.performance_tracker.export_trades_to_excel()
        
        # Calculate metrics and plot the chart (which now contains 'forecast' and 'portfolio_value')
        metrics = self.performance_tracker.get_performance_metrics(price_data=price_data)
        self.performance_tracker.export_metrics_to_excel('tradesxl.xlsx', metrics)

        # self.performance_tracker.calculate_trade_regime_agreement(
        #     price_data=price_data
        # )

        self.performance_tracker.log_performance_metrics(metrics)


        self.logger.info("="*70)
        self.logger.info("✓ Backtest completed!")
        self.logger.info("="*70)
        self.logger.info("")


        # # Generate HTML report
        # self.performance_tracker.generate_report('backtest_report.html')

        return metrics

    # def _create_candle_from_data(self, symbol: str, candle_data: pd.Series) -> Candle:
    #     """Convert DataFrame row to Candle object."""
    #     return Candle(
    #         symbol=symbol,
    #         open=candle_data['open'],
    #         high=candle_data['high'],
    #         low=candle_data['low'],
    #         close=candle_data['close'],
    #         volume=candle_data['volume'],
    #         start_time=candle_data['timestamp'],
    #         end_time=candle_data['timestamp'],  # For backtesting, start and end are the same
    #         tick_count=1
    #     )


    def extract_historical_price_data(self):
        # Get full price data for ground truth calculation
        price_data = None
        if self.historical_data and len(self.symbols) > 0:
            symbol = self.symbols[0]  # Primary symbol (BTCUSDT)
            if symbol in self.historical_data:
                data = self.historical_data[symbol]
                # Handle nested dict structure: historical_data['BTCUSDT']['BTCUSDT']
                df = data[symbol]
                if df is not None and isinstance(df, pd.DataFrame) and not df.empty:
                    price_data = df.copy()
                    if price_data is not None:
                        # Ensure timestamp is datetime
                        price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])
                        self.logger.debug(f"Using {len(price_data)} bars for ground truth calculation")
        return price_data

    def _close_all_positions_at_end(self, bot: TradingBot):
        """Close all open positions at the end of backtest."""
        
        # Get open positions from performance tracker
        open_positions = self.performance_tracker.get_open_positions()
        
        if not open_positions:
            self.logger.info("   No open positions to close")
            return
        
        self.logger.info(f"   Closing {len(open_positions)} open position(s)...")


        for symbol, position_info in open_positions.items():
            try:
                # Get the last available price for this symbol
                candle_history = self.mock_candle_builder.get_candle_history(symbol) 
                
                if candle_history.empty:
                    self.logger.warning(f"   ⚠ No price data for {symbol}, cannot close")
                    continue
                current_price = float(candle_history['close'].iloc[-1])

                signal = {}
                forecast = signal.get('forecast', 0.0)
                confidence = signal.get('confidence', 0.0)
                regime = signal.get('regime', 'N/A')
                debug_info = signal.get('debug_info', {})
                forecast_regime = debug_info.get('score_regime', None)

                # Get current allocation
                # current_allocation = self.forecast_manager.get_current_allocation(symbol)
                side = position_info['side']
                quantity = position_info['quantity']
                
                self.logger.info(f"   🔚 Force closing {side} position │ {symbol} │ "
                            f"{abs(quantity)} @ ${current_price}")

                # Get target allocation from forecast
                self.logger.info(f"Reached target_allocation")

                target_allocation = self.forecast_manager.forecast_to_allocation(forecast)

                # === CALCULATE ACTUAL MARKET ALLOCATION ===
                balances = self.portfolio_info.get_account_balance()
                total_value = bot._calculate_total_portfolio_value(balances, current_price)
                
                self.logger.info(f"   💼 Portfolio: ${total_value:.2f}")
                self.logger.info(f"   🧠 Forecast: {forecast:+.4f} │ Regime: {regime} (score: {forecast_regime})")
                
                # Calculate actual position value
                # For BTCUSDT: (free + locked) * current_price
                btc_balance = balances.get('BTCUSDT', balances.get('BTC', {}))
                btc_quantity = btc_balance.get('free', 0.0) - btc_balance.get('locked', 0.0)
                position_value = btc_quantity * current_price
                self.logger.info(f"   Position Value: ${position_value} │ Total Portfolio Value: ${total_value}")
                
                # Calculate actual allocation
                actual_allocation = position_value / total_value if total_value > 0 else 0.0
                self.logger.debug(f"   Actual Allocation: {actual_allocation} │ Target Allocation: {target_allocation}")

                # Check if rebalance needed (compare target with ACTUAL, not old target)
                needs_rebalance, allocation_change = self.forecast_manager.needs_rebalance(
                    symbol, target_allocation, actual_allocation
                )

                if needs_rebalance:
                    self.logger.info(f"Reached needs_rebalance")

                    self.logger.info(
                        f"   🔄 REBALANCE │ Actual: {actual_allocation} → Target: {target_allocation} "
                    )

                    # Risk management approval
                    if self.risk_manager and not self.risk_manager.approve_allocation_change(
                        symbol, allocation_change, candle_history
                    ):
                        self.logger.warning(f"   ✗ REJECTED by risk manager")
                        return
                    
                    # Execute portfolio rebalancing
                    self.logger.info(f"   ✓ APPROVED - Executing...")
                    bot._execute_portfolio_rebalance( 
                        symbol=symbol,  
                        target_allocation=target_allocation,
                        actual_allocation=actual_allocation,  
                        current_price=current_price,
                        data=candle_history,
                        signal=signal
                    )
                    # self.logger.info(f"   ✓ COMPLETE │ New Target reached: {target_allocation:+.4f}")

                    # self.forecast_manager.set_target_allocation(symbol, target_allocation)

                else:
                    self.logger.info(f"   X🔄X No rebalance needed │ Actual allocation: {actual_allocation} | Δ: {allocation_change}")
                    
                    
            except Exception as e:
                self.logger.error(f"   ❌ Error closing position for {symbol}: {e}", exc_info=True)

    def _check_stop_losses(self, symbol: str, price: float):
        """
        Check if stop losses have been triggered.
        
        Args:
            symbol: Trading pair symbol
            price: Current price
        """
        # Check if we have an open position with a stop loss
        if symbol in self.execution_handler.positions and 'stop_loss' in self.execution_handler.positions[symbol]:
            position = self.execution_handler.positions[symbol]
            stop_loss = position['stop_loss']
            
            self.logger.debug(f"Stop loss found for {symbol}")

            # Check if stop loss is triggered
            if price <= stop_loss:
                self.logger.info(f"Stop loss triggered for {symbol} at {price}")
                
                # Execute the stop loss
                self.execution_handler.place_order(
                    symbol=symbol,
                    side='CLOSE',
                    quantity=position['quantity'], 
                    price=price
                )
        else: self.logger.debug(f"No Stop loss found for {symbol}")
