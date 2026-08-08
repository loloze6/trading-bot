"""
Launcher: wires all trading-bot components and dispatches run modes.
"""

from __future__ import annotations

import datetime
import logging
import os
import sys
from dataclasses import dataclass
from typing import Optional, Tuple

import ccxt

from config.settings import ConfigManager
from core.backtester import BacktestEngine
from core.trading_bot import TradingBot
from data.feed_registry import FEED_REGISTRY
from data.data_manager import DataManager, HistoricalDataFetcher
from execution.execution_handler import ExecutionHandler, MockExecutionHandler
from execution.forecast_manager import ForecastManager
from execution.portfolio_info import MockPortfolioInfo, PortfolioInfo, PortfolioStateTracker, OtherPortfolioOperations
from performance.metrics import EnhancedPerformanceTracker, DEFAULT_COMMISSION_RATE
from risk.risk_manager import RiskManager
from strategies.main_strategy import AdvancedStrategy
from utils.logger import setup_logger

DEFAULT_INITIAL_BALANCE: int = 1000    # USDT
# DEFAULT_COMMISSION_RATE now lives in performance.metrics (single source of truth,
# see that module for why) and is imported above rather than redefined here.


@dataclass
class TradingParams:
    symbols: list
    interval: int         # candle interval, seconds
    check_interval: int   # price-fetch interval, seconds
    test_mode: bool
    commission_rate: float = DEFAULT_COMMISSION_RATE
    exchange: str = "binance"


@dataclass
class MockStack:
    data_manager: DataManager
    performance_tracker: EnhancedPerformanceTracker
    portfolio_info: MockPortfolioInfo
    execution_handler: MockExecutionHandler
    risk_manager: RiskManager
    forecast_manager: ForecastManager
    portfolio_state_tracker: Optional[PortfolioStateTracker]


def initialize_config_and_logger() -> Tuple[Optional[ConfigManager], Optional[logging.Logger]]:
    try:
        config = ConfigManager('config.json')
        if not config.validate():
            print("ERROR: Configuration validation failed. Please check config.json")
            return None, None
        log_file_path = config.get('logging', 'file_path', 'logs/bot.log')
        core_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(core_dir) 
        log_path = os.path.join(project_root, log_file_path)

        log_level = config.get_log_level()
        logger = setup_logger('trading_bot', log_path, log_level)
        return config, logger
    except Exception as e:
        print(f"FATAL: Failed to initialize configuration: {e}")
        return None, None


def parse_interval_seconds(value, default: int = 900) -> int:
    """Convert interval to seconds. Accepts int or string like '15m', '1h', '4h'."""
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        multipliers = {'m': 60, 'h': 3600, 'd': 86400, 's': 1}
        try:
            num = int(''.join(filter(str.isdigit, value)))
            unit = ''.join(filter(str.isalpha, value)).lower()
            return num * multipliers.get(unit, 60)
        except (ValueError, KeyError):
            pass
    return default


def parse_date_safe(
    date_str: str,
    logger: logging.Logger,
    default_days_back: int = 30,
) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        logger.error(f"Invalid date format '{date_str}': {e}")
        default_date = datetime.datetime.now() - datetime.timedelta(days=default_days_back)
        logger.warning(f"Using default date: {default_date.strftime('%Y-%m-%d')}")
        return default_date

class Launcher:
    def __init__(self):
        config, logger = initialize_config_and_logger()
        if not config or not logger:
            sys.exit(1)
        self.config = config
        self.logger = logger

    def _build_risk_and_forecast_managers(self):
        # risk_manager = RiskManager(
        #     max_position_size=self.config.get('risk_management').get('max_abs_allocation_change', 2.0),
        #     rebalance_threshold=self.config.get('risk_management').get('rebalance_threshold', 0.2)
        # )
        risk_manager = RiskManager(
            controls_cfg=self.config.get('risk_management', 'controls', {})
        )
        forecast_manager = ForecastManager(
        )
        return risk_manager, forecast_manager

    def _read_trading_params(
        self,
        interval_default: int = 180,
        check_interval_default: int = 60,
    ) -> TradingParams:
        # Optional key. It names the venue whose PRICE CACHE the backtest engine
        # resolves (see CcxtFetcher.cache_key), not the venue orders would be
        # sent to: run_bot reaches this validation, but the live DataManager it
        # builds never reads the value.
        # Absent means 'binance', which is what every config
        # written before it existed implies. A bogus id would otherwise reach
        # CcxtFetcher, which logs, leaves its client None, and surfaces a whole
        # run later as an empty DataFrame and "No data" -- a typo must not be
        # indistinguishable from missing history.
        exchange = self.config.get('trading', 'exchange', 'binance')
        if exchange not in ccxt.exchanges:
            self.logger.error(
                f"Unknown trading.exchange '{exchange}': not a ccxt exchange id. "
                f"Omit the key to use the default 'binance'."
            )
            sys.exit(1)
        return TradingParams(
            symbols=self.config.get('trading', 'symbols', ['BTCUSDT']),
            interval=parse_interval_seconds(
                self.config.get('trading', 'interval', interval_default)
            ),
            check_interval=self.config.get(
                'trading', 'check_interval_seconds', check_interval_default
            ),
            test_mode=self.config.get('trading', 'test_mode', True),
            exchange=exchange,
        )

    def _build_mock_stack(
        self,
        params: TradingParams,
        initial_balance: int = DEFAULT_INITIAL_BALANCE,
        with_state_tracker: bool = True,
        trades_log_file: Optional[str] = None,
    ) -> MockStack:
        risk_manager, forecast_manager = self._build_risk_and_forecast_managers()

        # Backtest DataManager — no thread, no Binance client
        data_manager = DataManager(
            symbols=params.symbols,
            interval_seconds=params.interval,
            mode="backtest",
        )
        # trades_log_file defaults to None, which lets EnhancedPerformanceTracker
        # keep its own default (the flat results/trades.json path) -- bit-identical
        # to prior behaviour. A caller that opts in (e.g. a backtest that must not
        # write into the shared results dir) passes an explicit path instead.
        tracker_log_kwargs = {} if trades_log_file is None else {'log_file': trades_log_file}
        if trades_log_file is not None:
            log_dir = os.path.dirname(trades_log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
        performance_tracker = EnhancedPerformanceTracker(
            params.commission_rate, initial_capital=initial_balance,
            **tracker_log_kwargs,
        )
        portfolio_info = MockPortfolioInfo(
            initial_balance={'USDT': {'free': initial_balance, 'locked': 0}},
            commission_rate=params.commission_rate,
        )

        core_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(core_dir) 
        results_path = os.path.join(project_root, "results")

        portfolio_state_tracker = (
            PortfolioStateTracker(output_dir=results_path) if with_state_tracker else None
        )
        execution_handler = MockExecutionHandler(
            performance_tracker=performance_tracker,
            portfolio_info=portfolio_info,
        )
        return MockStack(
            data_manager=data_manager,
            performance_tracker=performance_tracker,
            portfolio_info=portfolio_info,
            execution_handler=execution_handler,
            risk_manager=risk_manager,
            forecast_manager=forecast_manager,
            portfolio_state_tracker=portfolio_state_tracker,
        )

    def run_bot(self):
        """Run live trading bot."""
        self.logger.debug("Starting live trading bot...")
        self.logger.debug("-" * 80)

        params = self._read_trading_params(interval_default=120, check_interval_default=10)

        self.logger.debug(f"Mode: {'TEST' if params.test_mode else 'LIVE'}")
        self.logger.debug(f"Symbols: {', '.join(params.symbols)}")
        self.logger.debug(f"Candle interval: {params.interval}s, Check interval: {params.check_interval}s")

        strategy = AdvancedStrategy()
        risk_manager, forecast_manager = self._build_risk_and_forecast_managers()

        # Live DataManager — owns REST thread and CandleBuilder internally
        data_manager = DataManager(
            symbols=params.symbols,
            interval_seconds=params.interval,
            mode="live",
            price_fetch_interval=params.check_interval,
        )

        performance_tracker = EnhancedPerformanceTracker(DEFAULT_COMMISSION_RATE)
        execution_handler = ExecutionHandler(performance_tracker)
        portfolio_info = PortfolioInfo()

        bot = TradingBot(
            data_manager=data_manager,
            strategy=strategy,
            execution_handler=execution_handler,
            logger=self.logger,
            portfolio_info=portfolio_info,
            forecast_manager=forecast_manager,
            risk_manager=risk_manager,
            price_fetch_interval=params.check_interval,
            candle_interval_seconds=params.interval,
            test_mode=params.test_mode,
            symbols=params.symbols,
        )

        # Wire candle callback now that bot exists
        data_manager.candle_builder.candle_completion_callback = (
            bot._process_symbol_candle_completion
        )
        self.logger.debug("Bot initialized successfully. Starting main loop...")
        self.logger.debug("=" * 80)

        # TODO: load historical warmup data before going live
        # self._load_historical_warmup(bot, lookback_days=90)

        try:
            bot.run()
        except KeyboardInterrupt:
            self.logger.debug("Bot stopped by user (Ctrl+C)")
        except Exception as e:
            self.logger.error(f"Bot crashed with error: {e}", exc_info=True)
            sys.exit(1)


    def simulate(self):
        """Run backtest simulation."""
        self.logger.debug("Starting backtest simulation...")
        self.logger.debug("-" * 80)

        params = self._read_trading_params()
        initial_balance = DEFAULT_INITIAL_BALANCE
        start_date = parse_date_safe('2024-04-01', self.logger, default_days_back=60)
        end_date = parse_date_safe('2024-05-30', self.logger, default_days_back=0)

        self.logger.debug(f"Backtest period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        self.logger.debug(f"Initial balance: {initial_balance} USDT")
        self.logger.debug(f"Symbols: {', '.join(params.symbols)}")

        strategy = AdvancedStrategy()
        self.logger.debug(f"Using strategy: {strategy.__class__.__name__}")

        stack = self._build_mock_stack(params, initial_balance)

        bot = BacktestEngine(
            data_manager=stack.data_manager,
            strategy=strategy,
            execution_handler=stack.execution_handler,
            logger=self.logger,
            portfolio_info=stack.portfolio_info,
            portfolio_state_tracker=stack.portfolio_state_tracker,
            forecast_manager=stack.forecast_manager,
            risk_manager=stack.risk_manager,
            performance_tracker=stack.performance_tracker,
            price_fetch_interval=params.check_interval,
            candle_interval_seconds=params.interval,
            test_mode=params.test_mode,
            symbols=params.symbols,
            initial_capital=initial_balance,
            exchange=params.exchange,
        )

        try:
            self.logger.debug("Loading historical data...")
            
            bot.load_data(
                start_date   = start_date,
                end_date     = end_date,
                extra_feeds  = FEED_REGISTRY,   
            )            
            self.logger.debug("Running simulation...")
            self.logger.debug("=" * 80)
            bot.simulate_on_loaded_data()
            
            self.logger.debug("=" * 80)
            self.logger.debug("BACKTEST COMPLETED")
            self.logger.debug("=" * 80)
            report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backtest_report.html')
            self.logger.debug(f"Performance report saved to: {report_path}")
        
        except Exception as e:
            self.logger.error(f"Backtest failed: {e}", exc_info=True)
            sys.exit(1)

    def analyze_past_data(self):
        """Analyze historical data and plot regime chart."""
        self.logger.debug("Starting past data analysis...")
        self.logger.debug("-" * 80)

        params = self._read_trading_params()
        initial_balance = DEFAULT_INITIAL_BALANCE
        start_date = parse_date_safe('2024-06-01', self.logger, default_days_back=60)
        end_date = parse_date_safe('2024-12-01', self.logger, default_days_back=0)

        self.logger.debug(f"Analysis period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        self.logger.debug(f"Initial balance: {initial_balance} USDT")
        self.logger.debug(f"Symbols: {', '.join(params.symbols)}")

        strategy = AdvancedStrategy()
        self.logger.debug(f"Using strategy: {strategy.__class__.__name__}")

        stack = self._build_mock_stack(params, initial_balance)

        bot = BacktestEngine(
            data_manager=stack.data_manager,
            strategy=strategy,
            execution_handler=stack.execution_handler,
            logger=self.logger,
            portfolio_info=stack.portfolio_info,
            portfolio_state_tracker=stack.portfolio_state_tracker,
            forecast_manager=stack.forecast_manager,
            risk_manager=stack.risk_manager,
            performance_tracker=stack.performance_tracker,
            price_fetch_interval=params.check_interval,
            candle_interval_seconds=params.interval,
            test_mode=params.test_mode,
            symbols=params.symbols,
            initial_capital=initial_balance,
            exchange=params.exchange,
        )

        try:
            bot.load_data(start_date=start_date, end_date=end_date)
            price_data = bot.extract_historical_price_data()
            full_regimes, price_index = bot.performance_tracker.classify_full_history(price_data)
            bot.performance_tracker.plot_regime_chart(full_regimes, price_data)
        except Exception as e:
            self.logger.error(f"Past data analysis failed: {e}", exc_info=True)
            sys.exit(1)

    def visualize_data(self):
        """Fetch and validate historical data continuity."""
        self.logger.debug("Starting data visualization...")
        self.logger.debug("-" * 80)

        start_date = '2025-04-01'
        # Last day before the sealed holdout (strategy-research/config/
        # campaign_data_policy.yaml). tests/test_no_sealed_date_literals.py
        # fails if this ever falls inside the seal.
        end_date = '2025-12-31'
        symbols = ['BTCUSDT']

        self.logger.debug(f"Fetching data for: {', '.join(symbols)}")
        self.logger.debug(f"Period: {start_date} to {end_date}")

        try:
            fetcher = HistoricalDataFetcher(
                start_date, end_date, symbols,
                candle_interval_seconds=60,
                exchange='binance',
                localStorage=True,
            )
            data = fetcher.get_data()

            for symbol in symbols:
                if symbol in data and not data[symbol].empty:
                    is_continuous, gaps = fetcher.validate_data_continuity(symbol)
                    self.logger.debug(f"\n{symbol} DATA SUMMARY")
                    self.logger.debug("-" * 40)
                    self.logger.debug(f"  Records: {len(data[symbol]):,}")
                    self.logger.debug(f"  Date range: {data[symbol]['timestamp'].min()} to {data[symbol]['timestamp'].max()}")
                    self.logger.debug(f"  Continuous: {'Yes' if is_continuous else 'No'}")
                    if not is_continuous:
                        self.logger.warning(f"  Found {len(gaps)} gap(s) in data")
                        for i, (gap_start, gap_end) in enumerate(gaps[:5]):
                            duration = (gap_end - gap_start).total_seconds() / 60
                            self.logger.warning(f"    Gap {i+1}: {gap_start} to {gap_end} ({duration:.0f} minutes)")
                        if len(gaps) > 5:
                            self.logger.warning(f"    ... and {len(gaps) - 5} more gap(s)")
                else:
                    self.logger.error(f"No data available for {symbol}")
        except Exception as e:
            self.logger.error(f"Data visualization failed: {e}", exc_info=True)
            sys.exit(1)

    def optimize_strategy(self):
        """Run strategy optimization using backtesting with parameter grid search."""
        self.logger.debug("Starting strategy optimization...")
        self.logger.debug("=" * 80)

        params = self._read_trading_params()
        initial_balance = DEFAULT_INITIAL_BALANCE
        start_date = parse_date_safe('2025-01-01', self.logger, default_days_back=60)
        end_date = parse_date_safe('2025-03-01', self.logger, default_days_back=0)

        self.logger.debug(f"Optimization period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        self.logger.debug(f"Symbols: {', '.join(params.symbols)}")

        stack = self._build_mock_stack(params, initial_balance, with_state_tracker=False)

        short_window_range = [20, 50, 100]
        long_window_range = [100, 200, 300]
        total_combinations = sum(1 for s in short_window_range for l in long_window_range if s < l)
        self.logger.debug(f"Testing {total_combinations} parameter combinations")
        self.logger.debug("-" * 80)

        best_sharpe = -float('inf')
        best_params = {}
        test_count = 0

        try:
            for short_window in short_window_range:
                for long_window in long_window_range:
                    if short_window >= long_window:
                        continue

                    test_count += 1
                    self.logger.debug(f"Test {test_count}/{total_combinations}: short={short_window}, long={long_window}")

                    strategy = AdvancedStrategy()
                    bot = BacktestEngine(
                        data_manager=stack.data_manager,
                        strategy=strategy,
                        execution_handler=stack.execution_handler,
                        logger=self.logger,
                        portfolio_info=stack.portfolio_info,
                        forecast_manager=stack.forecast_manager,
                        risk_manager=stack.risk_manager,
                        performance_tracker=stack.performance_tracker,
                        price_fetch_interval=params.check_interval,
                        candle_interval_seconds=params.interval,
                        test_mode=params.test_mode,
                        symbols=params.symbols,
                        initial_capital=initial_balance,
                        exchange=params.exchange,
                    )

                    bot.load_data(start_date=start_date, end_date=end_date)
                    metrics = bot.simulate_on_loaded_data()

                    current_sharpe = metrics.get('sharpe_ratio', -float('inf'))
                    self.logger.debug(f"  Result: Sharpe={current_sharpe:.4f}")

                    if current_sharpe > best_sharpe:
                        best_sharpe = current_sharpe
                        best_params = {'short_window': short_window, 'long_window': long_window}
                        self.logger.debug(f"  NEW BEST: {best_params} with Sharpe={best_sharpe:.4f}")

            self.logger.debug("=" * 80)
            self.logger.debug("OPTIMIZATION COMPLETED")
            self.logger.debug("=" * 80)
            self.logger.debug(f"Best parameters: {best_params}")
            self.logger.debug(f"Best Sharpe ratio: {best_sharpe:.4f}")
            self.logger.debug(f"Total tests run: {test_count}")
        except Exception as e:
            self.logger.error(f"Optimization failed: {e}", exc_info=True)
            sys.exit(1)

    def get_portfolio_converted(self):
        """Print portfolio holdings converted to USDT."""
        coin_values = OtherPortfolioOperations().get_portfolio_converted('USDT')
        print(coin_values)

    def get_value_portfolio(self):
        """Print total portfolio value in USDT."""
        coin_values = OtherPortfolioOperations().get_portfolio_converted('USDT')
        grand_usdt_total = sum(map(lambda coin_usdt_value: coin_usdt_value[1], coin_values))
        print(f"Total portfolio value: {grand_usdt_total:.2f} USDT")


# ---------------------------------------------------------------------------
# Standalone callable used by run_protocol.py
# ---------------------------------------------------------------------------

def run_backtest(config_path: str, symbol: str, start: str, end: str, results_root: str,
                 runs_root: str = None, interval_seconds: int = None,
                 warmup_prefetch: bool = False, holdout_start: str = None,
                 commission_rate: float = None, trades_log_file: str = None,
                 bar_equity: bool = False):
    """Wire and run a single-symbol backtest; return the run_dir Path.

    runs_root: if set, individual run folders are created directly inside this
               directory (no /runs/ subdirectory), e.g. runs/run_xxx/results/.
    interval_seconds: candle interval override for this backtest only (e.g. 86400
        for daily bars). Defaults to None, which preserves the exact prior
        behavior of reading the live bot's global config.json interval — a
        protocol that doesn't pass this must produce bit-identical results to
        before this parameter existed. Never mutates config.json itself, so a
        daily-bar research run can never affect the live trading interval.
    warmup_prefetch: when True, fetches 2 * strategy.required_bars of EXTRA
        history before `start` and feeds it through the strategy silently (no
        trading, see BacktestEngine.warmup_cutoff_timestamp) so indicators are
        already warmed up by `start` itself, instead of degrading the first
        ~required_bars of every window. 2x is a proven-sufficient upper bound:
        strategy_engine.is_ready() needs the per-component history deque to
        reach length strategy_engine._warmup AFTER the component itself becomes
        ready at required_bars, and _warmup <= required_bars always (it's
        min(config_warmup, min_buf) where min_buf <= required_bars) -- so the
        exact bar of first readiness (required_bars + _warmup - 2) is always
        < 2*required_bars. This ~2x-required_bars warmup applies to every
        strategy config, including 1h production ones -- not something specific
        to daily bars, so this flag is not restricted to any one timeframe.
        Verified empirically against the P4_ts_trend SmaTrendLongOnlyComponent
        shakedown (required_bars=101: naive assumption would use 101 bars, but
        is_ready() actually first returns True at bar 201).
        Default False preserves the exact prior behavior (fetch exactly
        [start, end), every bar trades) -- bit-identical, see
        tests/test_warmup_prefetch_bit_identical.py.
    holdout_start: when warmup_prefetch is True and this is set (a "YYYY-MM-DD"
        string), asserts the computed prefetch fetch_start never reaches at or
        past holdout_start -- the backward-extended warmup buffer must never
        pull holdout data into a training window. No-op unless both
        warmup_prefetch=True and holdout_start are set.
    commission_rate: per-trade commission rate override (e.g. Kraken's taker rate) for
        this backtest only. Defaults to None, which resolves to DEFAULT_COMMISSION_RATE
        exactly as before this parameter existed -- a protocol that doesn't pass this
        must produce bit-identical results to prior behavior (same pattern as
        interval_seconds above). Never mutates config.json or the module-level default,
        so a Kraken-calibrated research run can never affect the live trading rate.
    trades_log_file: path for the performance tracker's interim trades.json dump.
        Defaults to None, which resolves to EnhancedPerformanceTracker's own
        default (the flat, shared results/trades.json) exactly as before this
        parameter existed -- bit-identical prior behaviour, same additive/opt-in
        pattern as commission_rate above. A caller that must not touch the shared
        results dir (notably the test suite, which passes a tmp_path) opts in with
        an explicit path; production callers that omit it are unaffected.
    bar_equity: when True, adds an off-by-default "bar_equity" block to metrics.json
        computed from the full per-bar portfolio_states series (postRebalance_total_value,
        the value AFTER each bar's rebalance -- what actually carries into the next bar)
        instead of core's trade-exit equity curve. core.sharpe/max_drawdown_pct sample
        only 24 points (one per completed trade, reference window) and fill every
        non-trading calendar day with a synthetic 0.0 return; this instead resamples the
        real bar series to daily closes and excludes the ~120 NOT_READY warmup bars, which
        otherwise dilute volatility with flat bars the strategy never acted on. See
        performance/bar_equity.py and reporting/run_artifact.py::build_bar_equity for the
        full convention (turnover from executed allocation deltas, not the raw
        allocation_change field, which also counts rejected rebalance attempts; Sharpe/
        Sortino annualized sqrt(365), matching core's own convention in form only -- the
        two are not expected to numerically agree, they measure different things).
        Default False preserves the exact prior behavior: build_bar_equity is never
        called, so write_metrics_json never receives a bar_equity argument and the key is
        never inserted into the payload dict -- metrics.json is byte-identical to before
        this parameter existed, by construction, not merely by matching values. See
        tests/test_bar_equity_bit_identical.py.
    """
    from data.feed_registry import FEED_REGISTRY

    launcher = Launcher()
    if interval_seconds is not None:
        interval = interval_seconds
    else:
        interval = parse_interval_seconds(launcher.config.get('trading', 'interval', 3600))
    resolved_commission_rate = (
        commission_rate if commission_rate is not None else DEFAULT_COMMISSION_RATE
    )
    params = TradingParams(
        symbols=[symbol],
        interval=interval,
        check_interval=launcher.config.get('trading', 'check_interval_seconds', 3600),
        test_mode=True,
        commission_rate=resolved_commission_rate,
    )

    strategy = AdvancedStrategy(config_path=config_path)
    stack = launcher._build_mock_stack(
        params, DEFAULT_INITIAL_BALANCE, trades_log_file=trades_log_file
    )
    stack.portfolio_state_tracker.output_dir = results_root
    if runs_root is not None:
        stack.portfolio_state_tracker.runs_dir = runs_root

    warmup_cutoff_timestamp = None
    fetch_start = start
    if warmup_prefetch:
        prefetch_bars = 2 * strategy.required_bars
        fetch_start_dt = datetime.datetime.strptime(start, "%Y-%m-%d") - datetime.timedelta(
            seconds=prefetch_bars * interval
        )
        fetch_start = fetch_start_dt.strftime("%Y-%m-%d")
        warmup_cutoff_timestamp = datetime.datetime.strptime(start, "%Y-%m-%d")

        if holdout_start is not None:
            holdout_start_dt = datetime.datetime.strptime(holdout_start, "%Y-%m-%d")
            assert fetch_start_dt < holdout_start_dt, (
                f"warmup_prefetch: computed fetch_start={fetch_start} is at or past "
                f"holdout_start={holdout_start} -- the backward-extended warmup buffer "
                f"would pull holdout data into a training window. Investigate before "
                f"proceeding (likely a window scheduled too close to the holdout boundary)."
            )

    engine = BacktestEngine(
        data_manager=stack.data_manager,
        strategy=strategy,
        execution_handler=stack.execution_handler,
        logger=launcher.logger,
        portfolio_info=stack.portfolio_info,
        portfolio_state_tracker=stack.portfolio_state_tracker,
        forecast_manager=stack.forecast_manager,
        risk_manager=stack.risk_manager,
        performance_tracker=stack.performance_tracker,
        price_fetch_interval=params.check_interval,
        candle_interval_seconds=params.interval,
        test_mode=params.test_mode,
        symbols=params.symbols,
        initial_capital=DEFAULT_INITIAL_BALANCE,
        warmup_cutoff_timestamp=warmup_cutoff_timestamp,
        bar_equity=bar_equity,
    )

    engine.load_data(start_date=fetch_start, end_date=end, extra_feeds=FEED_REGISTRY)

    if warmup_prefetch:
        # Verify the prefetch actually suffices -- fail loudly rather than silently
        # score a not-yet-ready strategy. Uses a throwaway probe instance (NOT the
        # real `strategy` object, which must stay untouched until the engine's own
        # bar-by-bar loop feeds it -- double-feeding would corrupt its RollingBuffer).
        probe = AdvancedStrategy(config_path=config_path)
        prefetch_df = engine.historical_data[symbol]
        prefetch_only = prefetch_df[prefetch_df['timestamp'] < warmup_cutoff_timestamp]
        for i in range(len(prefetch_only)):
            probe.update(prefetch_only.iloc[i:i + 1])
        assert probe.is_ready(), (
            f"warmup_prefetch: strategy not ready after {len(prefetch_only)} prefetch bars "
            f"({fetch_start} to {start}) -- required_bars={strategy.required_bars}. "
            f"2x-required_bars was insufficient for this config; investigate before proceeding."
        )

    engine.simulate_on_loaded_data()
    return engine._last_run_dir