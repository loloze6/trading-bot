import json
import os
import time
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime

from performance.metrics import CompletedTrade, EnhancedPerformanceTracker
import pandas as pd
from core.trading_bot import TradingBot
from data.fetchers import CcxtFetcher
from data.fetchers import FundingRateFetcher, FearGreedFetcher
from data.feed_registry import FEED_WINDOW_SECONDS
from data.data_manager import Candle
from execution.portfolio_info import flatten_dict_columns
from reporting.run_artifact import (
    new_run_dir, write_manifest, write_bars_csv, write_trades_json,
    write_metrics_json, write_forecast_distribution,
    build_core, build_per_regime, build_forecast_bins, build_dynamic, build_regime_validity,
    build_bar_equity,
    _get_git_sha,
)
"""
Backtesting Engine
=================
Engine for backtesting trading strategies against historical data.
"""


class FeedRequirementError(RuntimeError):
    """Raised by BacktestEngine.load_data when a strategy's required aux feed
    (AdvancedStrategy.required_feeds) is absent from extra_feeds at registration
    time (before any data fetch)."""


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
                 human_reports: bool = False,
                 warmup_cutoff_timestamp=None,
                 bar_equity: bool = False,
                 exchange: str = "binance",
                 drop_feeds: list[str] | None = None,
                 ):
        if symbols is None: symbols = ["BTCUSDT"]
        # 2026-07-07: bars with timestamp < warmup_cutoff_timestamp still update the
        # strategy (see TradingBot._process_symbol_candle_completion) but never trade
        # or touch portfolio state -- used to silently warm up indicator history from
        # data fetched before the real scoring window (see launcher.run_backtest's
        # warmup_prefetch). Default None preserves exact prior behavior: every bar
        # trades, as before this parameter existed.
        self.warmup_cutoff_timestamp = warmup_cutoff_timestamp
        # 2026-07-31: off-by-default bar-level equity metrics (fix/metrics-bar-equity).
        # When True, _end_of_backtest adds a "bar_equity" block to metrics.json computed
        # from the full per-bar portfolio_states series instead of core's trade-exit
        # curve -- see performance/bar_equity.py and reporting/run_artifact.py::
        # build_bar_equity. Default False: build_bar_equity is never called, so
        # write_metrics_json never receives the key and metrics.json is byte-identical
        # to before this parameter existed (see tests/test_bar_equity_bit_identical.py).
        self.bar_equity = bar_equity
        # 2026-08-06: CCXT exchange id this backtest's price cache comes from
        # (fix/kraken-cache-engine-reachability). "binance" is the value
        # fetch_historical_data already applied when no exchange was passed, so
        # an engine built without it reads the same unqualified BTCUSDT_1h.csv
        # as before; "kraken" reaches the exchange-qualified kraken_*_1h.csv
        # caches (see CcxtFetcher.cache_key).
        self.exchange = exchange
        # 2026-08-11: campaign-tooling feed-drop provenance
        # (fix/feed-dependency-safety, Step 2). This engine never filters
        # FEED_REGISTRY itself -- core/launcher.py::run_backtest does that before
        # calling load_data -- self.drop_feeds is stored purely so
        # _end_of_backtest can attach a "feeds" provenance block (registered/
        # dropped/required) to the run's manifest.json. Default None: no block
        # is added, manifest.json stays byte-identical to before this parameter
        # existed.
        self.drop_feeds = drop_feeds
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
        self.human_reports = human_reports
        self.historical_data = {}
        self.data_loaded = {}

        # Trading data
        self.open_trades: Dict[str, CompletedTrade] = {}
        self.closed_trades: List[CompletedTrade] = []
        self.equity_curve: List[Dict[str, Any]] = []
        self._last_run_dir = None

        logger.debug("Backtest bot initialized")


    def load_data(self, start_date='2025-01-01',end_date='2025-01-10', extra_feeds=None):
        self.logger.debug("BT - Loading data...")

        if not self.historical_data:
            self.logger.debug("BT - Fetch historical data...")
            self.historical_data[self.symbols[0]] = self.data_manager.fetch_historical_data(self.symbols[0], start_date, end_date, exchange=self.exchange)

            data_folder = os.path.dirname(os.path.abspath(__file__))
            project_folder = os.path.dirname(data_folder)
            data_storage_dir = os.path.join(project_folder, "local_data")

            # V1 -- registration completeness. No strategy (self.strategy is None)
            # means no requirements: BacktestEngine.__init__ defaults strategy=None,
            # and several tests drive load_data on a strategy-less engine (e.g.
            # tests/test_aux_feed_venue.py, tests/test_exchange_selection.py) -- this
            # exemption is their regression coverage, not defensive bloat.
            required_feeds = self.strategy.required_feeds if self.strategy is not None else {}
            missing = set(required_feeds) - set((extra_feeds or {}).keys())
            if missing:
                details = "; ".join(
                    f"'{feed}' (required by: {', '.join(required_feeds[feed])})"
                    for feed in sorted(missing)
                )
                raise FeedRequirementError(
                    f"Strategy requires aux feed(s) not present in extra_feeds: {details}. "
                    "Was the feed dropped via drop_feeds? Reserved feeds need explicit "
                    "RESERVED_FEED_REGISTRY opt-in."
                )

            # Register before initialize() so the pre-merge picks it up.
            # window_seconds is looked up by name, not defaulted — a feed
            # missing from FEED_WINDOW_SECONDS is a KeyError here, not a
            # merge that silently trusts an undeclared window.
            for feed_name, factory in (extra_feeds or {}).items():
                self.data_manager.register_feed(
                    name           = feed_name,
                    fetcher        = factory(self.symbols, start_date, end_date, data_dir = data_storage_dir, exchange = self.exchange),
                    window_seconds = FEED_WINDOW_SECONDS[feed_name],
                    agg            = 'last',
                    required       = feed_name in required_feeds,
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
            symbols=self.symbols,
            warmup_cutoff_timestamp=self.warmup_cutoff_timestamp,
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

        # E-012: the replay loop feeds the last fetched row but leaves its
        # candle open (has_more_data goes False before that row ever closes).
        # Flush each symbol's final still-open candle through the normal
        # completion path so every fetched bar is processed, same as any
        # other bar. Backtest-only -- flush_final_candle raises in live mode.
        for symbol in self.symbols:
            self.data_manager.flush_final_candle(symbol)

        return self._end_of_backtest(bot)

    def _end_of_backtest(self, bot):

        self.logger.info("")
        self.logger.info("="*70)
        self.logger.info("🏁 BACKTEST ENDING - Closing all open positions")
        self.logger.info("="*70)
        bot.stop()

        # === REGIME ANALYSIS ===
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
        flat_state_df = None
        if tracker and tracker.states:
            state_df = tracker.get_tracker_full_record()

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

            # Build the flattened state DataFrame for the run artifact
            flat_state_df = flatten_dict_columns(state_df.copy())
            flat_state_df = flat_state_df.map(lambda x: x.item() if hasattr(x, 'item') else x)
        else:
            self.logger.warning("⚠ Could not find portfolio states! Make sure tracker.record_state() is running.")

        # === BUILD RUN ARTIFACT DIR ===
        # Read config from the path the strategy actually loaded (may be a candidate config).
        _config_path = getattr(self.strategy, '_config_path', None)
        if _config_path is None:
            _strategies_dir = os.path.dirname(os.path.abspath(__file__))
            _project_dir = os.path.dirname(_strategies_dir)
            _config_path = os.path.join(_project_dir, 'strategy_config.json')
        with open(_config_path) as _f:
            _strategy_config = json.load(_f)

        results_root = (
            tracker.output_dir if tracker else os.path.join(_project_dir, "results")
        )
        run_dir = new_run_dir(results_root, _strategy_config,
                              runs_dir=getattr(tracker, "runs_dir", None))
        self._last_run_dir = run_dir
        self.logger.info(f"Run artifact dir: {run_dir}")

        # Write manifest
        raw_price_df = self.extract_historical_price_data()
        # fix/feed-dependency-safety, Step 2: non-None self.drop_feeds (including
        # an explicit []) records the "feeds" provenance block; None (the
        # default) passes feeds=None below, which write_manifest omits entirely --
        # manifest.json is byte-identical to before this parameter existed.
        feeds = None
        if self.drop_feeds is not None:
            aux_feeds = self.data_manager._aux_feeds if self.data_manager is not None else {}
            feeds = {
                "registered": sorted(aux_feeds.keys()),
                "dropped": sorted(self.drop_feeds),
                "required": sorted(self.strategy.required_feeds) if self.strategy is not None else [],
            }
        write_manifest(
            run_dir=run_dir,
            config=_strategy_config,
            data_df=raw_price_df if raw_price_df is not None else pd.DataFrame(
                columns=["timestamp", "open", "high", "low", "close", "volume"]
            ),
            symbols=self.symbols,
            timeframe=f"{self.data_manager.interval_seconds}s",
            git_sha=_get_git_sha(),
            lookback=self.strategy.strategy_engine.lookback,
            warmup=self.strategy.strategy_engine._warmup,
            feeds=feeds,
        )

        # Write trades JSON
        write_trades_json(run_dir, self.performance_tracker.completed_trades)

        # === EXCEL (always written, unchanged logic) ===
        self.performance_tracker.export_trades_to_excel(str(run_dir / "tradesxl.xlsx"))

        # Calculate metrics (pass price_data only when human_reports requested)
        metrics = self.performance_tracker.get_performance_metrics(
            price_data=price_data if self.human_reports else None
        )
        self.performance_tracker.export_metrics_to_excel(str(run_dir / "tradesxl.xlsx"), metrics)
        self.performance_tracker.log_performance_metrics(metrics)

        # Write metrics JSON
        completed_trades = self.performance_tracker.completed_trades
        core_metrics      = build_core(metrics, completed_trades, flat_state_df)
        per_regime        = build_per_regime(flat_state_df, completed_trades) if flat_state_df is not None else {}
        forecast_bins     = build_forecast_bins(completed_trades)
        dynamic           = build_dynamic(flat_state_df) if flat_state_df is not None else {}
        regime_validity   = build_regime_validity(flat_state_df) if flat_state_df is not None else {}
        bar_equity_metrics = (
            build_bar_equity(flat_state_df)
            if self.bar_equity and flat_state_df is not None else None
        )
        write_metrics_json(
            run_dir, core_metrics, per_regime, forecast_bins, dynamic, regime_validity,
            bar_equity=bar_equity_metrics,
        )

        # Write bars CSV and forecast distribution
        if flat_state_df is not None:
            write_bars_csv(run_dir, flat_state_df)
            write_forecast_distribution(run_dir, flat_state_df)

        # Write tracker CSV into run dir
        if tracker and tracker.states:
            tracker.output_dir = str(run_dir)
            tracker.to_csv()

        # === HUMAN REPORTS (optional) ===
        if self.human_reports:
            from performance.forecast_analyzer import ForecastAnalyzer
            ForecastAnalyzer(output_path=str(run_dir / "forecast_analysis.xlsx")).analyze(
                self.performance_tracker.completed_trades
            )

        # === INTEGRITY CHECK ===
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

