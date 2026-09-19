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
from risk.portfolio_risk_gate import PortfolioRiskGate, validate_portfolio_controls
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
    fetch_interval: Optional[int] = None   # backtest OHLCV fetch resolution (CUL-250); None = interval


@dataclass
class MockStack:
    data_manager: DataManager
    performance_tracker: EnhancedPerformanceTracker
    portfolio_info: MockPortfolioInfo
    execution_handler: MockExecutionHandler
    risk_manager: RiskManager
    forecast_manager: ForecastManager
    portfolio_state_tracker: Optional[PortfolioStateTracker]
    risk_gate: Optional[PortfolioRiskGate]


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


def _validated_exchange(exchange: str, logger: logging.Logger) -> str:
    """
    Validate a CCXT exchange id, exiting loudly if it is not one -- the single
    choke point every venue string passes through before being used to route
    a fetch (fix/exchange-plumbing-campaign-aux, Ticket 13). Extracted from
    Launcher._read_trading_params so run_backtest's explicit `exchange`
    argument gets the identical fail-loud parity as the config-read path
    instead of a typo silently reaching CcxtFetcher, which logs, leaves its
    client None, and surfaces as an empty DataFrame and "No data" far from the
    real cause.

    This is also the designed slot where a future Venue/ExchangeSpec object
    (deferred epic, see the plan's governance section) would land with a
    one-site change -- the only place a venue string is interpreted into a
    routing decision.
    """
    if exchange not in ccxt.exchanges:
        logger.error(
            f"Unknown trading.exchange '{exchange}': not a ccxt exchange id. "
            f"Omit the key to use the default 'binance'."
        )
        sys.exit(1)
    return exchange


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

    def _build_risk_and_forecast_managers(self, min_allocation_change_override: Optional[float] = None):
        controls_cfg = self.config.get('risk_management', 'controls', {})
        # E-055: a strategy's strategy_config.json may set strategies
        # .min_allocation_change to override RiskManager's min_allocation_change
        # threshold for its own runs. None (the default -- key absent) leaves
        # controls_cfg untouched, byte-identical to before this override existed.
        # Only the min_allocation_change sub-dict is replaced; max_allocation_change
        # and any other configured control pass through unchanged.
        if min_allocation_change_override is not None:
            controls_cfg = {
                **controls_cfg,
                "min_allocation_change": {"threshold": min_allocation_change_override},
            }
        risk_manager = RiskManager(controls_cfg=controls_cfg)
        forecast_manager = ForecastManager(
        )
        # fix/risk-layer, PR-1: build the portfolio risk gate from config.json's
        # risk_management.portfolio_controls when non-empty, else None. Absent block
        # (the committed config) -> None -> no gate is threaded anywhere and every
        # output is byte-identical. ConfigManager.validate has already vetted the
        # block by the time this runs (launcher.py init path), so PortfolioRiskGate's
        # own ctor validation is defense in depth here.
        portfolio_controls = self.config.get('risk_management', 'portfolio_controls', {})
        risk_gate = PortfolioRiskGate(portfolio_controls) if portfolio_controls else None
        return risk_manager, forecast_manager, risk_gate

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
        exchange = _validated_exchange(
            self.config.get('trading', 'exchange', 'binance'), self.logger
        )
        # Optional key (CUL-250). Absent/None means "fetch at trading.interval
        # directly" -- byte-identical to every config written before this key
        # existed. When set, backtest OHLCV is fetched/cached at THIS
        # resolution instead, and CandleBuilder aggregates it up to
        # trading.interval during replay (e.g. fetch_interval_seconds="1h"
        # with interval="4h" backtests a 4h strategy off an hourly cache).
        # Live mode never reads this value -- DataManager only honours it in
        # fetch_historical_data(), the backtest-only OHLCV loader.
        raw_fetch_interval = self.config.get('trading', 'fetch_interval_seconds', None)
        fetch_interval = (
            parse_interval_seconds(raw_fetch_interval) if raw_fetch_interval is not None else None
        )
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
            fetch_interval=fetch_interval,
        )

    def _build_mock_stack(
        self,
        params: TradingParams,
        initial_balance: int = DEFAULT_INITIAL_BALANCE,
        with_state_tracker: bool = True,
        trades_log_file: Optional[str] = None,
        min_allocation_change_override: Optional[float] = None,
    ) -> MockStack:
        risk_manager, forecast_manager, risk_gate = self._build_risk_and_forecast_managers(
            min_allocation_change_override=min_allocation_change_override
        )

        # Backtest DataManager — no thread, no Binance client
        data_manager = DataManager(
            symbols=params.symbols,
            interval_seconds=params.interval,
            mode="backtest",
            fetch_interval_seconds=params.fetch_interval,
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
            risk_gate=risk_gate,
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
        risk_manager, forecast_manager, risk_gate = self._build_risk_and_forecast_managers(
            min_allocation_change_override=strategy.min_allocation_change_override
        )

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
            risk_gate=risk_gate,
        )

        # Wire candle callback now that bot exists
        data_manager.candle_builder.candle_completion_callback = (
            bot._process_symbol_candle_completion
        )
        self.logger.debug("Bot initialized successfully. Starting main loop...")
        self.logger.debug("=" * 80)

        # ORDERING CONSTRAINT (CUL-25): the line above sets
        # candle_builder.candle_completion_callback for the first time in this
        # method. The commented-out warmup TODO below is only safe BECAUSE it
        # sits after that assignment. If a future implementation of this TODO
        # feeds historical rows through candle_builder before the callback is
        # wired -- e.g. by moving this block earlier, or by warming up before
        # TradingBot/the callback wiring exist -- any candle completed during
        # warmup calls a None callback, which raises TypeError. Whether that
        # surfaces loudly depends entirely on what (if anything) catches it
        # upstream; this method has no test coverage (run_bot() is the
        # forbidden live-trading entry point, never exercised in CI), so
        # nothing here would catch a silent regression. Keep any warmup
        # implementation strictly after the callback assignment above.
        # TODO: load historical warmup data before going live
        # self._load_historical_warmup(bot, lookback_days=90)

        try:
            bot.run()
        except KeyboardInterrupt:
            self.logger.debug("Bot stopped by user (Ctrl+C)")
        except Exception as e:
            self.logger.error(f"Bot crashed with error: {e}", exc_info=True)
            sys.exit(1)


    def simulate(self, feed_local_storage: bool = True):
        """Run backtest simulation.

        feed_local_storage: default True preserves the historical aux-feed
            write-through-on-read behaviour (bit-identical — main.py's
            Launcher().simulate() passes nothing). False threads a pure read
            into every aux-feed factory so a gapped read cannot mutate a tracked
            cache (CUL-161).
        """
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

        stack = self._build_mock_stack(
            params, initial_balance,
            min_allocation_change_override=strategy.min_allocation_change_override,
        )

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
            risk_gate=stack.risk_gate,
        )

        try:
            self.logger.debug("Loading historical data...")
            
            bot.load_data(
                start_date   = start_date,
                end_date     = end_date,
                extra_feeds  = FEED_REGISTRY,
                feed_local_storage = feed_local_storage,
            )

            # A total fetch failure is not a zero-return backtest. Without this,
            # an empty fetch runs the loop over nothing, produces all-zero
            # metrics and an artifact whose data hash is the hash of nothing,
            # and exits 0 — a failed run that is indistinguishable from a real
            # one that simply made no money. Raise so the except-block below
            # turns it into a non-zero exit.
            loaded = bot.historical_data.get(params.symbols[0])
            if loaded is None or len(loaded) == 0:
                raise RuntimeError(
                    f"No historical data for {params.symbols[0]} over "
                    f"{start_date:%Y-%m-%d}..{end_date:%Y-%m-%d} "
                    f"(exchange={params.exchange}). The fetch returned nothing, so "
                    f"there is nothing to simulate. Refusing to emit a zero-metric "
                    f"run that would look like a completed backtest."
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

        stack = self._build_mock_stack(
            params, initial_balance,
            min_allocation_change_override=strategy.min_allocation_change_override,
        )

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
            risk_gate=stack.risk_gate,
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
                 bar_equity: bool = False, exchange: str | None = None,
                 drop_feeds: list[str] | None = None,
                 model_funding: bool = False,
                 risk_controls: dict | None = None,
                 feed_local_storage: bool = True,
                 fetch_interval_seconds: int | None = None,
                 gap_detection: bool = False,
                 gap_policy: dict | None = None):
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
    exchange: CCXT exchange id selecting which venue's price (and, for feeds that
        have adopted exchange_id, aux data) cache this backtest reads -- see
        CcxtFetcher.cache_key() and FundingRateFetcher.cache_key(). Defaults to
        None, which resolves to config.json's trading.exchange (absent -> "binance"),
        exactly the same None-means-prior-behavior contract as commission_rate above
        -- a caller that omits this must produce bit-identical results to before this
        parameter existed. Never mutates config.json. An explicit value (e.g.
        "kraken") is validated the same way simulate() validates trading.exchange
        (_validated_exchange) and exits loudly on an unknown id -- a typo must not be
        indistinguishable from missing history. See tests/test_exchange_selection.py.
    drop_feeds: names of FEED_REGISTRY entries to exclude from this backtest's aux-feed
        registry (fix/feed-dependency-safety, Step 2 -- campaign tooling's escape
        hatch for the venue guard's own documented remedy, "...or drop '{name}' from
        extra_feeds", data_manager.py:807-808). Defaults to None, which passes the
        SAME FEED_REGISTRY object through to engine.load_data unchanged -- bit-
        identical to before this parameter existed. A non-None value (including an
        explicit empty list) is validated against FEED_REGISTRY's keys -- an unknown
        name raises ValueError, same fail-loud rationale as _validated_exchange above
        -- and a filtered copy is passed instead; the global FEED_REGISTRY is never
        mutated. Dropping a feed the loaded strategy actually requires raises
        FeedRequirementError at BacktestEngine.load_data's V1 registration guard,
        before any data fetch (see core/backtester.py). Threaded into BacktestEngine
        so a non-None value also adds a "feeds" provenance block (registered/dropped/
        required feed names) to the run's manifest.json; a None value adds no such
        key, so a default run's manifest.json is unchanged. See
        tests/test_feed_dependencies.py.
    model_funding: when True, accrues off-by-default perpetual-funding cash flow on the
        held position each bar (design 2026-07-24 §5) -- builds the daily-summed funding
        COST series (data/feed_registry.py::build_daily_funding_series) and threads it
        through BacktestEngine into TradingBot's per-bar hook (execution/portfolio_info.py
        ::apply_funding). REQUIRES daily bars: pass interval_seconds=86400, else
        BacktestEngine raises ValueError naming the reason (the daily-summed series would
        multiple-charge each intraday bar and charge not-yet-settled funding -- look-
        ahead). Fails loud when the flag is on but no {symbol}_funding_8h.csv daily series
        exists, rather than silently reporting a fee-only run as funding-costed. Default
        False preserves the exact prior behavior: funding_daily is never built and the
        hook at trading_bot.py:205 is never entered -- byte-identical to before this
        parameter existed. See tests/test_model_funding_bit_identical.py.
    risk_controls: full-replacement override for this backtest's
        risk_management.portfolio_controls (fix/risk-layer, PR-1). Defaults to None,
        which means "use config.json's portfolio_controls exactly as live would" --
        with the committed config that block is absent, so no gate is built and output
        is byte-identical to before this parameter existed. A dict IS the complete
        portfolio_controls for this run (no merge): {} explicitly means no controls
        (gate off); {"absolute_allocation_cap": {"cap": 1.0}} clamps the target
        allocation. Validated by validate_portfolio_controls (fail-loud ValueError on
        bad shapes/ranges/unknown keys), the same rule set ConfigManager.validate
        applies to config.json. When a gate is active the effective block is folded
        into run identity (dir hash + manifest config_sha256) so the run is
        distinguishable from a no-controls one, and a "risk_controls" block is added to
        metrics.json. Does NOT touch RiskManager's band controls. See
        risk/portfolio_risk_gate.py and tests/test_risk_layer_bit_identical.py.
    feed_local_storage: controls whether the aux-feed read may write-through to
        the on-disk cache. Defaults to True -- the historical write-through-on-read
        behaviour, bit-identical to before this parameter existed (forwarded to
        engine.load_data unchanged). False threads localStorage=False into every
        aux-feed factory, so a gapped aux-feed read reaches the (still-allowed)
        remote but cannot MUTATE a tracked cache -- the same opt-out CUL-26 added
        for OHLCV (fetch_historical_data), extended to the feed path (CUL-161).
        See tests/test_aux_feed_localstorage_flag.py.
    fetch_interval_seconds: backtest OHLCV fetch resolution override (CUL-250).
        Defaults to None, which resolves to config.json's trading.fetch_interval_seconds
        (itself absent by default) -- same None-means-prior-behavior contract as
        interval_seconds/commission_rate/exchange above. When set (directly or via
        config), historical OHLCV is fetched/cached at THIS resolution instead of
        `interval`, and CandleBuilder aggregates the finer rows up to `interval`
        during replay -- e.g. fetch_interval_seconds=3600 with interval_seconds=14400
        backtests a 4h strategy off an hourly cache. Must be <= interval and divide
        it evenly (DataManager raises otherwise). See
        tests/test_data_manager_fetch_interval.py.
    gap_detection: when True, adds an off-by-default "data_quality" block to
        metrics.json (CUL-261 / E-039). On every candle completion (the same
        callback live trading uses), compares the candle's timestamp against the
        previous one FOR THAT SYMBOL against `interval` -- a mismatch means a real
        gap in the data (not merely "no trade happened"), and is recorded with its
        timestamps and actual/expected step. This is the first place in the whole
        pipeline that surfaces gap detection as structured, countable data rather
        than a console warning -- prescreen_signal.py's own gap-aware statistics
        (the #50/CUL-15 family) were the only prior instance, and only reached the
        prescreen kill path, never a real backtest. Default False: the check is
        never called, self.gap_events stays empty and unread, metrics.json is
        byte-identical to before this parameter existed. See
        tests/test_gap_detection_bit_identical.py.
    gap_policy: further, independent opt-in on top of gap_detection (raises if
        set without it) -- CUL-271, replaces the earlier single-bar
        suppress_allocation_after_gap. `{"ignore_max_bars": int,
        "large_min_bars": int, "on_large_gap": "flatten"}`. Classifies each
        detected gap by how many bars were actually missed: "ignore" (<=
        ignore_max_bars) does nothing special; "middle" keeps any existing
        position but blocks a NEW entry until enough real post-gap bars have
        accumulated to flush the contaminated indicator window; "large" (>=
        large_min_bars, default the strategy's own required_bars) forces an
        immediate flatten AND resets the strategy's accumulated history (a real
        segment split), after which the engine's own pre-existing readiness gate
        naturally withholds new entries until re-warmed. None (default):
        byte-identical, same contract as gap_detection above. See
        core/trading_bot.py's constructor docstring for why a per-indicator
        variant was investigated and rejected (Step 1/2 of the design spec).
    """
    from data.feed_registry import FEED_REGISTRY

    if drop_feeds is None:
        effective_feed_registry = FEED_REGISTRY
    else:
        unknown = sorted(set(drop_feeds) - set(FEED_REGISTRY.keys()))
        if unknown:
            raise ValueError(
                f"Unknown feed name(s) in drop_feeds: {unknown}. "
                f"Valid feed names: {sorted(FEED_REGISTRY.keys())}."
            )
        effective_feed_registry = {
            name: factory for name, factory in FEED_REGISTRY.items()
            if name not in drop_feeds
        }

    launcher = Launcher()
    if interval_seconds is not None:
        interval = interval_seconds
    else:
        interval = parse_interval_seconds(launcher.config.get('trading', 'interval', 3600))
    resolved_commission_rate = (
        commission_rate if commission_rate is not None else DEFAULT_COMMISSION_RATE
    )
    resolved_exchange = _validated_exchange(
        exchange if exchange is not None
        else launcher.config.get('trading', 'exchange', 'binance'),
        launcher.logger,
    )
    if fetch_interval_seconds is not None:
        resolved_fetch_interval = fetch_interval_seconds
    else:
        _raw_fetch_interval = launcher.config.get('trading', 'fetch_interval_seconds', None)
        resolved_fetch_interval = (
            parse_interval_seconds(_raw_fetch_interval) if _raw_fetch_interval is not None else None
        )
    params = TradingParams(
        symbols=[symbol],
        interval=interval,
        check_interval=launcher.config.get('trading', 'check_interval_seconds', 3600),
        test_mode=True,
        commission_rate=resolved_commission_rate,
        exchange=resolved_exchange,
        fetch_interval=resolved_fetch_interval,
    )

    # CUL-273b: wires RollingBuffer's dormant reindex-to-NaN-grid mechanism
    # (built in CUL-273, previously accepted by AdvancedStrategy's constructor
    # but never supplied by any real call site). `interval` above is already
    # the resolved candle interval in seconds for THIS backtest, computed
    # before this line specifically so it's available here. ignore_max_bars
    # comes from gap_policy when the caller supplies one; both stay None
    # (reindex off, byte-identical to before this wiring existed) when
    # gap_policy is absent -- matches RollingBuffer's own "both required, or
    # neither" contract.
    _reindex_ignore_max_bars = (gap_policy or {}).get("ignore_max_bars") if gap_detection else None
    strategy = AdvancedStrategy(
        config_path=config_path,
        candle_interval_seconds=interval,
        ignore_max_bars=_reindex_ignore_max_bars,
    )
    stack = launcher._build_mock_stack(
        params, DEFAULT_INITIAL_BALANCE, trades_log_file=trades_log_file,
        min_allocation_change_override=strategy.min_allocation_change_override,
    )
    # fix/risk-layer, PR-1: risk_controls is a FULL-REPLACEMENT override of the
    # config.json-derived gate in the stack. None -> keep the config-derived gate
    # (absent block -> None -> byte-identical). A dict IS the run's complete
    # portfolio_controls, validated fail-loud here (the override path bypasses
    # ConfigManager.validate); {} means no controls (gate off).
    if risk_controls is not None:
        _risk_errors = validate_portfolio_controls(risk_controls)
        if _risk_errors:
            raise ValueError(
                "Invalid risk_controls override: " + "; ".join(_risk_errors)
            )
        risk_gate = PortfolioRiskGate(risk_controls) if risk_controls else None
    else:
        risk_gate = stack.risk_gate
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
        exchange=params.exchange,
        drop_feeds=drop_feeds,
        model_funding=model_funding,
        risk_gate=risk_gate,
        gap_detection=gap_detection,
        gap_policy=gap_policy,
    )

    engine.load_data(start_date=fetch_start, end_date=end, extra_feeds=effective_feed_registry,
                     feed_local_storage=feed_local_storage)

    # Same guard as Launcher.simulate(), and needed MORE here: this is the entry
    # point the campaign runner uses, so an empty fetch would write an all-zero
    # metrics.json that the research pipeline then reads as a real, if
    # unprofitable, result. Placed before the warmup probe below, which would
    # otherwise die on a bare KeyError: 'timestamp' against the empty frame and
    # blame the strategy for what is actually a missing-data failure.
    _loaded = engine.historical_data.get(symbol)
    if _loaded is None or len(_loaded) == 0:
        raise RuntimeError(
            f"No historical data for {symbol} over {start}..{end} "
            f"(exchange={resolved_exchange}). The fetch returned nothing, so there "
            f"is nothing to backtest. Refusing to emit a zero-metric run that would "
            f"be indistinguishable from a strategy that simply never traded."
        )

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