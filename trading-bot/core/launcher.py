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

from config.settings import ConfigManager
from core.backtester import BacktestEngine
from core.trading_bot import TradingBot
from data.feed_registry import FEED_REGISTRY
from data.data_manager import DataManager, HistoricalDataFetcher
from execution.execution_handler import ExecutionHandler, MockExecutionHandler
from execution.forecast_manager import ForecastManager
from execution.portfolio_info import MockPortfolioInfo, PortfolioInfo, PortfolioStateTracker, OtherPortfolioOperations
from performance.metrics import EnhancedPerformanceTracker
from risk.risk_manager import RiskManager
from strategies.main_strategy import AdvancedStrategy
from utils.logger import setup_logger

DEFAULT_INITIAL_BALANCE: int = 1000    # USDT
DEFAULT_COMMISSION_RATE: float = 0.001  # 0.1 %


@dataclass
class TradingParams:
    symbols: list
    interval: int         # candle interval, seconds
    check_interval: int   # price-fetch interval, seconds
    test_mode: bool
    commission_rate: float = DEFAULT_COMMISSION_RATE


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
        return TradingParams(
            symbols=self.config.get('trading', 'symbols', ['BTCUSDT']),
            interval=parse_interval_seconds(
                self.config.get('trading', 'interval', interval_default)
            ),
            check_interval=self.config.get(
                'trading', 'check_interval_seconds', check_interval_default
            ),
            test_mode=self.config.get('trading', 'test_mode', True),
        )

    def _build_mock_stack(
        self,
        params: TradingParams,
        initial_balance: int = DEFAULT_INITIAL_BALANCE,
        with_state_tracker: bool = True,
    ) -> MockStack:
        risk_manager, forecast_manager = self._build_risk_and_forecast_managers()
        
        # Backtest DataManager — no thread, no Binance client
        data_manager = DataManager(
            symbols=params.symbols,
            interval_seconds=params.interval,
            mode="backtest",
        )
        performance_tracker = EnhancedPerformanceTracker(
            params.commission_rate, initial_capital=initial_balance,
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
        end_date = '2026-04-23'
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
                    is_continuous, gaps = fetcher.validate_quality_data_continuity(symbol)
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

def run_backtest(config_path: str, symbol: str, start: str, end: str, results_root: str):
    """Wire and run a single-symbol backtest; return the run_dir Path."""
    from data.feed_registry import FEED_REGISTRY

    launcher = Launcher()
    interval = parse_interval_seconds(launcher.config.get('trading', 'interval', 3600))
    params = TradingParams(
        symbols=[symbol],
        interval=interval,
        check_interval=launcher.config.get('trading', 'check_interval_seconds', 3600),
        test_mode=True,
        commission_rate=DEFAULT_COMMISSION_RATE,
    )

    strategy = AdvancedStrategy()
    stack = launcher._build_mock_stack(params, DEFAULT_INITIAL_BALANCE)
    stack.portfolio_state_tracker.output_dir = results_root

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
    )

    engine.load_data(start_date=start, end_date=end, extra_feeds=FEED_REGISTRY)
    engine.simulate_on_loaded_data()
    return engine._last_run_dir