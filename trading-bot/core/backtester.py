import time
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime
from performance.metrics import CompletedTrade, EnhancedPerformanceTracker
import pandas as pd
from core.trading_bot import TradingBot
from data.fetchers import CcxtFetcher
from data.fetchers import FundingRateFetcher, FearGreedFetcher
from data.data_manager import Candle
import os
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
                 symbols: List[str] = None,
                 initial_capital: float = 10000.0,
                 commission_rate: float = 0.001,
                 ):
        if symbols is None: symbols = ["BTCUSDT"]
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
        self.open_trades: Dict[str, CompletedTrade] = {}
        self.closed_trades: List[CompletedTrade] = []
        self.equity_curve: List[Dict[str, Any]] = []

        logger.debug("Backtest bot initialized")


    def load_data(self, start_date='2025-01-01',end_date='2025-01-10', extra_feeds=None):
        self.logger.debug("BT - Loading data...")

        if not self.historical_data:
            self.logger.debug("BT - Fetch historical data...")
            self.historical_data[self.symbols[0]] = self.data_manager.fetch_historical_data(self.symbols[0], start_date, end_date)

            data_folder = os.path.dirname(os.path.abspath(__file__))
            project_folder = os.path.dirname(data_folder)
            data_storage_dir = os.path.join(project_folder, "local_data")

            # Register before initialize() so the pre-merge picks it up
            for feed_name, factory in (extra_feeds or {}).items():
                self.data_manager.register_feed(
                    name    = feed_name,
                    fetcher = factory(self.symbols, start_date, end_date, data_dir = data_storage_dir),
                    agg     = 'last',
                )
            self.logger.debug(f"Registered feeds before initialize: {list(self.data_manager._aux_feeds.keys())}")

        else: 
            self.logger.debug("BT - Data was already loaded...")

        # Load data manager with historical data and initialize indexes
        if self.historical_data:
            self.logger.debug("BT - Initialize DataManager...")
            self.data_manager.historical_data = self.historical_data
            self.data_manager.initialize()
        else: 
            self.logger.error("BT - Cannot load data manager with historical data")

    # ------------------------------------------------------------------
    # Simulation loop
    # ------------------------------------------------------------------

    def simulate_on_loaded_data(self):
        self.logger.debug("BT - Starting backtest...")
        
        """Run the backtest."""
        if not self.data_manager.historical_data:
            self.logger.error("BT - No data in DataManager cannot run backtest.")
            return
        
        self.logger.debug("Initiate Trading bot...")
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

        # Wire the candle callback now that bot exists
        self.data_manager.candle_builder.candle_completion_callback = (
            bot._process_symbol_candle_completion
        )

        # Process each time step
        # self.logger.debug("Process each time step...")
        BT_finished = False
        while not BT_finished:       
            all_symbols_finished = True

            for symbol in self.symbols:
                if not self.data_manager.has_more_data(symbol):
                    continue
                all_symbols_finished = False

                completed_candle = self.data_manager.process_next_tick(symbol)

                if not self.data_manager.advance(symbol):
                    continue

            if all_symbols_finished:
                BT_finished = True

        return self._end_of_backtest(bot)

    def _end_of_backtest(self, bot):

        self.logger.info("")
        self.logger.info("="*70)
        self.logger.info("🏁 BACKTEST ENDING - Closing all open positions")
        self.logger.info("="*70)
        bot.stop()
        

        # === REGIME ANALYZIS ===
        self.logger.debug(f"\n{'='*80}")
        self.logger.debug("TRADE REGIME AGREEMENT ANALYSIS")
        self.logger.debug(f"{'='*80}")


        # Extract base price data and resample to the candle interval used during backtest
        price_data = self.extract_historical_price_data()
        if price_data is not None and self.data_manager.interval_seconds > 60:
            freq = f"{self.data_manager.interval_seconds}s"
            price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])
            price_data = (
                price_data.set_index('timestamp')
                .resample(freq, closed='left', label='left')
                .agg({
                    'open':   'first',
                    'high':   'max',
                    'low':    'min',
                    'close':  'last',
                    'volume': 'sum',
                    **{c: 'last' for c in price_data.columns
                       if c not in ('timestamp', 'open', 'high', 'low', 'close', 'volume')}
                })
                .dropna(subset=['close'])
                .reset_index()
            )
            self.logger.debug(f"✓ Price data resampled to {self.data_manager.interval_seconds}s candles: {len(price_data)} bars")

        # === MERGE TICK-BY-TICK STATE INTO PRICE DATA ===
        tracker = getattr(self, 'portfolio_state_tracker', None)
        if tracker and tracker.states:  # Check if states list has data
            state_df = tracker.get_tracker_full_record()
            tracker.to_csv()  # Export states to CSV for debugging

            state_df['timestamp'] = pd.to_datetime(state_df['timestamp'])
            price_data['timestamp'] = pd.to_datetime(price_data['timestamp'])
            
            # Rename total_portfolio_value to portfolio_value so the chart recognizes it
            if 'total_portfolio_value' in state_df.columns:
                state_df['portfolio_value'] = state_df['total_portfolio_value']
                
            # Select columns to merge
            cols_to_merge = ['timestamp']
            if 'forecast' in state_df.columns: 
                cols_to_merge.append('forecast')
            else: 
                print('forecast not in column')
            if 'portfolio_value' in state_df.columns: 
                cols_to_merge.append('portfolio_value')
            else: 
                print('portfolio_value not in column')
            if 'regime' in state_df.columns: 
                cols_to_merge.append('regime')
            else: 
                print('regime not in column')

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
                
            self.logger.debug(f"✓ State merged successfully. Columns available: {price_data.columns.tolist()}")
        else:
            self.logger.warning("⚠ Could not find portfolio states! Make sure tracker.record_state() is running.")

        self.performance_tracker.export_trades_to_excel('results/tradesxl.xlsx')
        
        # Calculate metrics and plot the chart (which now contains 'forecast' and 'portfolio_value')
        metrics = self.performance_tracker.get_performance_metrics(price_data=price_data)
        self.performance_tracker.export_metrics_to_excel('results/tradesxl.xlsx', metrics)
        self.performance_tracker.log_performance_metrics(metrics)


        # Integrity assertion: every record_trade call must correspond to an executed order.
        orders_placed = self.execution_handler.executed_orders_counter
        trades_recorded = self.performance_tracker.execution_counter
        if orders_placed != trades_recorded:
            self.logger.error(
                f"INTEGRITY VIOLATION: executed_orders={orders_placed} != record_trade_calls={trades_recorded}"
            )
        zero_qty = [t for t in self.performance_tracker.completed_trades if abs(t.matched_quantity) < 1e-9]
        if zero_qty:
            self.logger.error(
                f"INTEGRITY VIOLATION: {len(zero_qty)} CompletedTrade(s) with matched_quantity≈0"
            )
        if orders_placed == trades_recorded and not zero_qty:
            self.logger.debug(
                f"✓ INTEGRITY OK: executed_orders={orders_placed}, record_trade_calls={trades_recorded}, zero_qty_trades=0"
            )

        self.logger.debug("="*70)
        self.logger.debug("✓ Backtest completed!")
        self.logger.debug("="*70)
        self.logger.debug("")

        return metrics

    def extract_historical_price_data(self) -> Optional[pd.DataFrame]:
        """Return a copy of the raw (base-resolution) price DataFrame."""
        if not self.historical_data or not self.symbols:
            return None
        symbol = self.symbols[0]
        df = self.historical_data.get(symbol)
        if df is None or not isinstance(df, pd.DataFrame) or df.empty:
            return None
        price_data = df.copy()
        price_data["timestamp"] = pd.to_datetime(price_data["timestamp"])
        return price_data

