"""A live run on Kraken Futures: completed candles in, the backtest's own decision, the books recorded.

Business: a live decision must be the decision the backtest would make on the same candles. So the strategy, its
config, the per-bar decision (TradingBot) and the local book (the backtest's simulated portfolio and fills) are the
backtest's, unchanged. Only the candles' source (Kraken Futures, polled) and the records differ.

One folder per run, trading-bot/live_runs/<name>/:
    live_config.json      the run's settings (written at the first start)
    strategy_config.json  a copy of the strategy config, so a later edit of the original changes nothing here
    summary.md            short status, rewritten after every bar
    run.log               the run's log (appended by every start)
    session_NN/           one per start: candles.csv (every completed candle fed, warm-up included),
                          local_book.csv (the backtest's per-bar record), real_book.csv (decision time, the real
                          account's value and position), local_trades.json, session.json (start value, cut-off)
Stopping (Ctrl+C) closes the local book's position, as at the end of a backtest (operator 2026-11-17).

Why this can't leak: only candles whose whole period has passed are fed (live/kraken.py); a bar is decided once
all of its period has passed (DataManager.ingest_completed_rows); warm-up bars only prime the strategy.
"""
from __future__ import annotations

import datetime
import json
import logging
import shutil
import time
from pathlib import Path

import pandas as pd

from config.cost_model import resolve_cost_model
from config.settings import ConfigManager
from core.launcher import DEFAULT_GAP_POLICY, build_risk_and_forecast_managers
from core.trading_bot import TradingBot
from data.data_manager import DataManager
from execution.execution_handler import MockExecutionHandler
from execution.portfolio_info import MockPortfolioInfo, PortfolioStateTracker
from live import kraken
from performance.metrics import EnhancedPerformanceTracker
from strategies.main_strategy import AdvancedStrategy
from utils.logger import setup_logger

BOT = Path(__file__).resolve().parents[1]
LIVE_RUNS = BOT / "live_runs"
# The step-4 backtest's venue (Kraken, perpetual): its fee and slippage price the local book.
VENUE = ("kraken", "futures")
DEFAULTS = {"symbol": None, "interval_seconds": 86400, "fetch_interval_seconds": 3600, "poll_seconds": 60,
            "orders": "off", "target": "real", "test_host": None, "start_value": None, "log_level": "INFO"}
logger = logging.getLogger("trading_bot")


def prepare_run(name: str, strategy: str | None = None, symbol: str | None = None, root: Path = LIVE_RUNS):
    """The run folder: created at the first start, read back at a restart (refused if the arguments differ)."""
    run_dir = Path(root) / name
    if not run_dir.exists():
        if not strategy or not symbol:
            raise SystemExit(f"new run '{name}': give --strategy and --symbol")
        kraken.ccxt_symbol(symbol)  # refuses a name that is not <COIN>USD
        run_dir.mkdir(parents=True)
        shutil.copyfile(strategy, run_dir / "strategy_config.json")
        cfg = dict(DEFAULTS, symbol=symbol, strategy_source=str(Path(strategy).resolve()))
        (run_dir / "live_config.json").write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")
        return run_dir, cfg
    cfg = dict(DEFAULTS, **json.loads((run_dir / "live_config.json").read_text(encoding="utf-8")))
    if strategy and Path(strategy).read_bytes() != (run_dir / "strategy_config.json").read_bytes():
        raise SystemExit(f"run '{name}' already exists with another strategy config; use a new --run name")
    if symbol and symbol != cfg["symbol"]:
        raise SystemExit(f"run '{name}' already exists for {cfg['symbol']}, not {symbol}; use a new --run name")
    return run_dir, cfg


def build_book(strategy_path, symbol, interval, fetch_interval, start_value, out_dir, mode):
    """The strategy and the local book, exactly as run_backtest builds them for the step-4 backtest: the same
    classes, costs, risk controls and gap rule. Used by a live session (mode 'live') and by its replay proof
    (mode 'backtest')."""
    strategy = AdvancedStrategy(config_path=str(strategy_path), candle_interval_seconds=interval,
                                ignore_max_bars=None)
    risk_manager, forecast_manager, risk_gate = build_risk_and_forecast_managers(
        ConfigManager("config.json"), strategy.min_allocation_change_override, strategy.sizing)
    fee_bps, _ = resolve_cost_model(*VENUE)
    commission_rate = fee_bps / 10000
    performance_tracker = EnhancedPerformanceTracker(commission_rate, initial_capital=start_value,
                                                     log_file=str(Path(out_dir) / "local_trades.json"))
    portfolio_info = MockPortfolioInfo(initial_balance={"USDT": {"free": start_value, "locked": 0}},
                                       commission_rate=commission_rate)
    return dict(
        strategy=strategy,
        data_manager=DataManager(symbols=[symbol], interval_seconds=interval, mode=mode,
                                 fetch_interval_seconds=fetch_interval),
        execution_handler=MockExecutionHandler(performance_tracker=performance_tracker,
                                               portfolio_info=portfolio_info, exchange=VENUE[0],
                                               market_type=VENUE[1]),
        portfolio_info=portfolio_info,
        portfolio_state_tracker=PortfolioStateTracker(output_dir=str(out_dir)),
        forecast_manager=forecast_manager, risk_manager=risk_manager, performance_tracker=performance_tracker,
        risk_gate=risk_gate, gap_detection=True, gap_policy=dict(DEFAULT_GAP_POLICY),
    )


class LiveSession:
    """One start of a live run. exchange, clock, sleep and account are passed in so a test can replay recorded
    candles on a simulated clock; live, they are Kraken, the wall clock and the real account."""

    def __init__(self, run_dir, cfg, exchange, clock=kraken.utc_now, sleep=time.sleep, account=None):
        self.run_dir, self.cfg, self.ex = Path(run_dir), cfg, exchange
        self.clock, self.sleep, self.account = clock, sleep, account
        if cfg["orders"] != "off":
            raise SystemExit("orders 'on' is not built yet (step 4): set \"orders\": \"off\"")
        self.symbol, self.interval = cfg["symbol"], int(cfg["interval_seconds"])
        self.fetch_interval = int(cfg["fetch_interval_seconds"])
        n = 1 + len(list(self.run_dir.glob("session_*")))
        self.session_dir = self.run_dir / f"session_{n:02d}"
        self.session_dir.mkdir()

        start_value = cfg["start_value"]
        snapshot = self._account_snapshot()
        if start_value is None:
            if snapshot is None:
                raise SystemExit("the local book starts at the real account's value: set the Kraken key "
                                 "(see the plan) or put \"start_value\" in live_config.json")
            start_value = snapshot["value"]
        start_value = float(start_value)

        self.parts = build_book(self.run_dir / "strategy_config.json", self.symbol, self.interval,
                                self.fetch_interval, start_value, self.session_dir, mode="live")
        self.strategy = self.parts["strategy"]
        if self.strategy.required_feeds:
            raise SystemExit(f"the strategy needs aux feeds {sorted(self.strategy.required_feeds)}; "
                             "live runs do not support aux feeds yet")
        self.data_manager = self.parts["data_manager"]

        now = pd.Timestamp(self.clock())
        # The bar forming at the start is the first one traded; every bar before it only primes the strategy
        # (the backtest's warm-up cut-off), over the backtest's warm-up length: 2 x required_bars.
        self.cutoff = now.floor(f"{self.interval}s")
        self.warmup_bars = 2 * self.strategy.required_bars
        self.warmup_start = self.cutoff - datetime.timedelta(seconds=self.warmup_bars * self.interval)
        self.bot = TradingBot(
            data_manager=self.data_manager, logger=logger, price_fetch_interval=int(cfg["poll_seconds"]),
            candle_interval_seconds=self.interval, test_mode=True, symbols=[self.symbol],
            warmup_cutoff_timestamp=self.cutoff,
            **{k: v for k, v in self.parts.items() if k != "data_manager"},
        )
        self.data_manager.candle_builder.candle_completion_callback = self._on_bar
        self.start_value, self.started = start_value, now
        self.live_bars, self.last_bar, self.stopped = 0, None, False
        (self.session_dir / "session.json").write_text(json.dumps({
            "started_utc": str(now), "start_value": start_value, "cutoff": str(self.cutoff),
            "warmup_bars": self.warmup_bars, "warmup_start": str(self.warmup_start),
            "required_bars": self.strategy.required_bars, "venue_costs": list(VENUE),
            "start_account": snapshot, "target": cfg["target"]}, indent=2) + "\n", encoding="utf-8")
        logger.info(f"LIVE session {n:02d} | {self.symbol} | bar {self.interval}s from {self.fetch_interval}s "
                    f"candles | warm-up {self.warmup_bars} bars | first traded bar {self.cutoff} | "
                    f"local book starts at {start_value:.2f}")

    # ---- records -------------------------------------------------------------------------------------------
    def _account_snapshot(self):
        if self.account is None:
            return None
        try:
            return self.account()
        except Exception as e:  # the record says it failed; the decision does not depend on it
            logger.error(f"real account read failed: {e}")
            return {"value": float("nan"), "position": float("nan")}

    def _on_bar(self, symbol, candle):
        self.bot._process_symbol_candle_completion(symbol, candle)
        if pd.Timestamp(candle.start_time) < self.cutoff:
            return
        self.live_bars += 1
        self.last_bar = candle.start_time
        tracker = self.parts["portfolio_state_tracker"]
        tracker.to_csv("local_book.csv")
        state = tracker.states[-1] if tracker.states else {}
        real = self._account_snapshot() or {}
        row = {"timestamp": candle.start_time, "decided_utc": pd.Timestamp(self.clock()), "close": candle.close,
               "forecast": state.get("forecast"), "local_value": state.get("postRebalance_total_value"),
               "real_value": real.get("value"), "real_position": real.get("position")}
        path = self.session_dir / "real_book.csv"
        pd.DataFrame([row]).to_csv(path, mode="a", header=not path.exists(), index=False,
                                   date_format="%Y-%m-%d %H:%M:%S")
        logger.info(f"BAR {candle.start_time} | close {candle.close} | forecast {row['forecast']} | "
                    f"local book {row['local_value']} | real account {row['real_value']}")
        self._write_summary(row)

    def _write_summary(self, row=None):
        lines = [f"# Live run {self.run_dir.name}", "",
                 f"- Coin: {self.symbol}; bars of {self.interval} s built from {self.fetch_interval} s candles",
                 f"- Strategy: {self.cfg.get('strategy_source')}",
                 f"- Orders: {self.cfg['orders']}; target: {self.cfg['target']}",
                 f"- Session: {self.session_dir.name}, started {self.started} (UTC); "
                 f"warm-up {self.warmup_bars} bars; first traded bar {self.cutoff}",
                 f"- Local book start value: {self.start_value:.2f}",
                 f"- Live bars decided: {self.live_bars}; last bar: {self.last_bar}"]
        if row:
            lines.append(f"- Last bar: close {row['close']}, forecast {row['forecast']}, "
                         f"local book {row['local_value']}, real account {row['real_value']}")
        if self.stopped:
            lines.append("- Stopped: the local book's position was closed")
        (self.run_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---- the loop ------------------------------------------------------------------------------------------
    def poll_once(self):
        """Fetch the candles completed since the last one fed, record them, feed them (bars decide inside)."""
        now = pd.Timestamp(self.clock())
        last = self.data_manager._last_fed.get(self.symbol)
        since = self.warmup_start if last is None else last + datetime.timedelta(seconds=self.fetch_interval)
        rows = kraken.fetch_completed_candles(self.ex, self.symbol, self.fetch_interval, since, now)
        if rows.empty:
            return 0
        path = self.session_dir / "candles.csv"
        rows.to_csv(path, mode="a", header=not path.exists(), index=False, date_format="%Y-%m-%d %H:%M:%S")
        return self.data_manager.ingest_completed_rows(self.symbol, rows)

    def warm_up(self):
        self.poll_once()
        # Readiness is checked on a throwaway copy fed the same warm-up bars, as run_backtest's warm-up check
        # does: is_ready() on the live strategy itself moves its state (the regime's bar count).
        probe = AdvancedStrategy(config_path=str(self.run_dir / "strategy_config.json"),
                                 candle_interval_seconds=self.interval, ignore_max_bars=None)
        bars = self.data_manager.candle_builder.get_candle_history(self.symbol, count=10**9)
        for i in range(len(bars)):
            probe.update(bars.iloc[i:i + 1])
        if not probe.is_ready():
            raise SystemExit(f"strategy not ready after the warm-up ({self.warmup_bars} bars from "
                             f"{self.warmup_start}); Kraken's history may be too short for this strategy")
        logger.info(f"warm-up done: strategy ready at {self.cutoff}")
        self._write_summary()

    def run(self, max_polls=None):
        self.warm_up()
        polls = 0
        try:
            while max_polls is None or polls < max_polls:
                self.sleep(int(self.cfg["poll_seconds"]))
                try:
                    self.poll_once()
                except Exception as e:  # a failed fetch is retried at the next poll
                    logger.error(f"poll failed: {e}")
                polls += 1
        except KeyboardInterrupt:
            logger.info("stop requested")
        finally:
            self.stop()

    def stop(self):
        self.bot.stop()   # closes the local book's position at the last decided bar, as a backtest's end does
        self.parts["portfolio_state_tracker"].to_csv("local_book.csv")
        self.stopped = True
        self._write_summary()


def start(name, strategy=None, symbol=None):
    run_dir, cfg = prepare_run(name, strategy, symbol)
    setup_logger("trading_bot", str(run_dir / "run.log"), getattr(logging, cfg["log_level"]), console=True,
                 mode="a")
    ex = kraken.make_exchange(cfg["target"], cfg["test_host"])
    account = (lambda: kraken.account_snapshot(ex, cfg["symbol"])) if kraken.keys_present() else None
    LiveSession(run_dir, cfg, ex, account=account).run()


def check(symbol="BTCUSD"):
    """Read-only: Kraken Futures reachable, the instrument, the last complete candles, the account if a key is set."""
    ex = kraken.make_exchange("real")
    print(f"instrument: {symbol} -> {kraken.instrument_id(ex, symbol)}")
    now = kraken.utc_now()
    rows = kraken.fetch_completed_candles(ex, symbol, 3600, now - pd.Timedelta(hours=4), now)
    print(f"now (UTC): {now}\nlast complete hourly candles:\n{rows.to_string(index=False)}")
    print(f"key found: {'yes' if kraken.keys_present() else 'no'}")
    if kraken.keys_present():
        snap = kraken.account_snapshot(ex, symbol)
        print(f"account value (USD): {snap['value']:.2f}; position {symbol}: {snap['position']}")
