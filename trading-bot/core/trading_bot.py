"""
Trading Bot Core Module
Handles live trading operations including signal processing, position management,
and portfolio rebalancing based on forecast allocations.
"""

import time
import datetime
import logging
import math
from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
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
        symbols: List[str] = None,
        warmup_cutoff_timestamp=None,
        model_funding: bool = False,
        funding_daily=None,
        risk_gate=None,
        gap_detection: bool = False,
        gap_policy: Optional[Dict[str, Any]] = None,
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
        # 2026-07-07: see BacktestEngine.warmup_cutoff_timestamp docstring. Default
        # None preserves exact prior behavior (every candle always trades).
        self.warmup_cutoff_timestamp = warmup_cutoff_timestamp
        self.risk_manager = risk_manager
        self.performance_tracker = performance_tracker
        
        # Configuration
        self.price_fetch_interval = price_fetch_interval
        self.candle_interval_seconds = candle_interval_seconds
        self.test_mode = test_mode
        self.symbols = symbols or ['BTCUSDT']
        
        # 2026-08-30: the engine loads and trades symbols[0] only and marks every
        # asset at that one symbol's close, so len(symbols) > 1 runs silently
        # corrupted economics with no error. Refuse it loudly. Unconditional by
        # design: a capable multi-symbol path is a separate orchestrator, not this
        # class behind a flag.
        if len(self.symbols) > 1:
            raise ValueError(
                f"multi-symbol trading is not supported: TradingBot received "
                f"{len(self.symbols)} symbols {self.symbols}; the engine trades only "
                f"symbols[0] and would silently corrupt portfolio valuation. Pass a "
                f"single symbol."
            )

        # 2026-07-24: off-by-default perpetual-funding accrual (design 2026-07-24 §5).
        # When model_funding is False (default) the funding hook in
        # _process_symbol_candle_completion is never entered, so behavior is
        # byte-identical to before this mechanism existed. Turning it on additionally
        # requires funding_daily to be populated (a per-symbol daily funding COST
        # series, distinct from the forward-filled signal feed; see
        # data/feed_registry.py::build_daily_funding_series). Both are threaded in from
        # run_backtest(model_funding=True) -> BacktestEngine's daily-bar guard -> these
        # params; no production config sets the flag, and default False leaves behavior
        # byte-identical.
        self.model_funding = model_funding
        self.funding_daily = funding_daily

        # 2026-08-29: off-by-default portfolio risk gate (fix/risk-layer, PR-1). When
        # None (default) the per-bar hook below is never entered and no state is
        # recorded, so behavior is byte-identical to before this mechanism existed.
        # When set (built from config.json's risk_management.portfolio_controls, or a
        # run_backtest risk_controls override) it clamps the target allocation to the
        # configured absolute cap. See risk/portfolio_risk_gate.py.
        self.risk_gate = risk_gate

        # CUL-261 / E-039: off-by-default gap detection at candle completion. When
        # True, every candle completion (live and backtest alike -- this is the
        # shared callback for both) compares this candle's timestamp against the
        # previous completed candle FOR THIS SYMBOL against candle_interval_seconds,
        # the same expected step CandleBuilder aggregates to. A mismatch is recorded
        # in self.gap_events; the caller (BacktestEngine._end_of_backtest) surfaces
        # it into metrics.json's "data_quality" block. Default False: _check_and_
        # record_gap is never called, self.gap_events stays empty and unread, and no
        # key is added anywhere -- byte-identical to before this parameter existed.
        #
        # CUL-271: gap_policy REPLACES the single-bar suppress_allocation_after_gap
        # this ticket shipped with. Investigated first (Step 1 of the design spec):
        # every strategy component already exposes get_required_periods()/is_ready()
        # (strategies/strategy_components.py), but the LIVE engines actually wired
        # into AdvancedStrategy -- ConfigDrivenRegimeEngine/ConfigDrivenStrategyEngine
        # -- collapse readiness to ONE SHARED warmup value per engine
        # (`all(len(h) >= self._warmup ...)`), not a true per-indicator check;
        # CompositeStrategy's per-indicator all(is_ready_with_standardization())
        # pattern in strategy_base.py is never instantiated anywhere in the live
        # path (grepped: zero call sites outside its own definition). Genuine
        # per-indicator validity would mean restructuring both engines' warmup
        # semantics for every caller, not a targeted gap-response diff, and the
        # plumbing alone touches 5 files (trading_bot/backtester/launcher/
        # main_strategy + one engine), over the spec's <=3-file ceiling. Per the
        # spec's own mechanical rule, that routes to the fixed-tier fallback below,
        # not the per-indicator variant -- this is not a judgment call, it is what
        # Step 1's findings dictate under Step 2's rule.
        #
        # gap_policy shape: {"ignore_max_bars": int, "large_min_bars": int,
        # "on_large_gap": "flatten"}. None (default) disables all tiers --
        # byte-identical to before this parameter existed. Requires
        # gap_detection=True (there is nothing to classify a tier from otherwise).
        #
        # Tiers, classified by how many bars were actually missed
        # (round(actual_delta / expected_step) - 1):
        #   ignore  (missed <= ignore_max_bars): no special handling. The engine
        #     only ever sees REAL bars (there is no synthetic-candle mechanism in
        #     CandleBuilder to forward-fill into) -- for a gap this short, trading
        #     resumes on the next real bar exactly as it does today.
        #   middle  (ignore_max_bars < missed < large_min_bars): existing position
        #     is KEPT, but a NEW entry (previous_allocation == 0 and target != 0)
        #     is blocked until bars_since_gap >= the strategy's own required_bars
        #     -- long enough for the contaminated indicator window to fully flush
        #     with real post-gap data. No history reset: rolling windows still
        #     span the gap (this repo's own prescreen gap policy already tried and
        #     rejected full segment-and-re-warm -- it destroyed 91% of a real
        #     sample -- so only NEW risk is withheld, not existing exposure).
        #   large   (missed >= large_min_bars): immediate forced flatten (same
        #     direct-execute bypass pattern PR-2's risk_gate kill-switch uses),
        #     plus AdvancedStrategy.reset_history() (a real segment split -- the
        #     shared data buffer and both engines' component history are cleared).
        #     The forced flatten holds until a full warmup (required_bars) of
        #     real bars has passed since the gap, then the tier clears and the
        #     strategy trades again (CUL-359; it used to never clear).
        #   Recovery (CUL-359): both middle and large clear once
        #     bars_since_gap >= required_bars, checked before the bar's own
        #     update (so the tier clears on the (required_bars+1)-th real bar
        #     after the gap -- one bar conservative, pinned by tests). An
        #     ignore-tier gap during an active tier counts as one real bar and
        #     does not cancel it; a middle gap during a large re-warm keeps
        #     'large' (recorded as the event's active_tier).
        if gap_policy is not None and not gap_detection:
            raise ValueError(
                "gap_policy requires gap_detection=True -- there is nothing to "
                "classify a tier from without gap detection enabled. Pass "
                "gap_detection=True or omit gap_policy."
            )
        self.gap_detection = gap_detection
        self.gap_policy = gap_policy
        self._last_candle_time: Dict[str, Any] = {}
        self.gap_events: List[Dict[str, Any]] = []
        # CUL-274: bars whose forecast was NaN (held, see below), per symbol,
        # plus the first few as samples. Empty on every run without one.
        self.nan_forecast_bars: Dict[str, int] = {}
        self.nan_forecast_samples: List[Dict[str, Any]] = []
        self._bars_since_gap: Dict[str, int] = {}
        self._active_gap_tier: Dict[str, str] = {}

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

    def _funding_rate_for_bar(self, symbol, data_time):
        """
        Daily funding rate to accrue for `symbol` on the bar dated `data_time`.

        Looks the bar's calendar day up in self.funding_daily (a per-symbol dict of
        normalized-day-Timestamp → summed funding rate; see
        data/feed_registry.py::build_daily_funding_series). Returns None when there is
        no series for the symbol or no settlement dated to that day — the caller then
        applies no funding. Only the bar's own day is read, so a settlement dated after
        this bar can never be charged to it (no look-ahead).
        """
        series = self.funding_daily.get(symbol) if self.funding_daily else None
        if not series:
            return None
        day = pd.Timestamp(data_time).normalize()
        val = series.get(day)
        return None if val is None else float(val)

    def _check_and_record_gap(self, symbol: str, data_time) -> bool:
        """
        CUL-261 / E-039: off-by-default gap detection (see self.gap_detection).

        Compares `data_time` (this candle's timestamp) against the previous
        completed candle's timestamp FOR THIS SYMBOL, against candle_interval_seconds
        -- the same expected step CandleBuilder aggregates every bar to, so a real
        data gap (a delistings-style hole, an exchange outage, a fetch that
        returned fewer rows than the window implies) shows up here as a delta that
        isn't exactly one step. The very first candle seen for a symbol has nothing
        to compare against and is never flagged.

        Only ever looks backward at the immediately preceding candle -- no
        look-ahead. Returns True the bars a gap was just detected on, so the caller
        can optionally suppress that one bar's allocation change without touching
        any indicator state.
        """
        ts = pd.Timestamp(data_time)
        # datetime.timedelta: pd.Timedelta(seconds=int) emits numpy's generic-unit
        # DeprecationWarning on every bar while gap detection is on. Same value.
        expected_step = datetime.timedelta(seconds=self.candle_interval_seconds)
        previous = self._last_candle_time.get(symbol)
        self._last_candle_time[symbol] = ts
        if previous is None:
            return False
        delta = ts - previous
        if delta == expected_step:
            return False
        self.gap_events.append({
            "symbol": symbol,
            "timestamp": str(ts),
            "previous_timestamp": str(previous),
            "expected_step_seconds": self.candle_interval_seconds,
            "actual_delta_seconds": delta.total_seconds(),
        })
        return True

    @staticmethod
    def _gap_bars_missing(actual_delta_seconds: float, expected_step_seconds: int) -> int:
        """CUL-271: number of whole bars missing from a detected gap (0 would
        mean no gap; this is only ever called when a gap was already detected,
        so the real minimum is 1). round(), not int(), so a delta that's a hair
        off an exact multiple of the step (float accumulation) doesn't undercount."""
        return max(round(actual_delta_seconds / expected_step_seconds) - 1, 1)

    def _classify_gap_tier(self, bars_missing: int) -> str:
        """CUL-271: which gap_policy tier a just-detected gap falls into.
        Only called when self.gap_policy is not None."""
        ignore_max = self.gap_policy.get("ignore_max_bars", 2)
        large_min = self.gap_policy.get("large_min_bars", self.strategy.required_bars)
        if bars_missing <= ignore_max:
            return "ignore"
        if bars_missing >= large_min:
            return "large"
        return "middle"

    def _process_symbol_candle_completion(
        self,
        symbol: str,
        completed_candle: Optional[Candle] = None,
    ) -> None:
        """
        Process candle completion for a specific symbol.

        Called automatically when a candle is completed. Generates signals,
        updates target allocations, and executes rebalancing if needed.

        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            completed_candle: The completed candle object, passed by
                CandleBuilder's callback contract. Signals are derived from
                get_data_history(), so this argument is currently unused.
        """
        try:
            # Retrieve stored data around OHLCV and AUX data  
            data = self.data_manager.get_data_history(symbol, count=1)

            if data.empty:
                self.logger.warning(f"⚠ No data available for {symbol}")
                return
            close = data['close'].iloc[-1]
            data_time = data['timestamp'].iloc[-1]

            # CUL-261 / E-039: off-by-default gap detection, checked BEFORE the
            # warmup-cutoff return below so a gap during warmup is recorded too --
            # gap_detection default False -> never called, byte-identical.
            gap_detected_this_bar = (
                self._check_and_record_gap(symbol, data_time) if self.gap_detection else False
            )

            # CUL-271: gap_policy tier classification, on top of CUL-261's
            # detection. gap_policy None (default) -> this whole block is
            # skipped, byte-identical to before gap_policy existed.
            if self.gap_policy is not None:
                tier = None
                if gap_detected_this_bar:
                    bars_missing = self._gap_bars_missing(
                        self.gap_events[-1]["actual_delta_seconds"], self.candle_interval_seconds
                    )
                    tier = self._classify_gap_tier(bars_missing)
                    # CUL-359: the tier and bar count are recorded on the event, so
                    # data_quality shows what each gap did, not only that it happened.
                    self.gap_events[-1]["bars_missing"] = bars_missing
                    self.gap_events[-1]["tier"] = tier
                if tier is not None and tier != "ignore":
                    # A middle or large gap (re)starts the recovery window. The more
                    # severe tier wins: a middle gap during a large gap's re-warm
                    # keeps 'large' (CUL-359).
                    active = self._active_gap_tier.get(symbol)
                    if active == "large" and tier == "middle":
                        tier = "large"
                    self.gap_events[-1]["active_tier"] = tier
                    self._active_gap_tier[symbol] = tier
                    self._bars_since_gap[symbol] = 0
                    self.logger.info(
                        f"⛔ GAP TIER '{tier}' │ {symbol} │ {bars_missing} bar(s) missing"
                    )
                    if self.gap_events[-1].get("tier") == "large":
                        # Segment split now, before this bar's own data is
                        # added below -- it becomes bar #1 of the fresh
                        # segment, not blended with pre-gap history.
                        self.strategy.reset_history()
                elif symbol in self._active_gap_tier:
                    # A normal bar, or an ignore-tier gap (no special handling: it
                    # must NOT cancel an active tier -- CUL-359), counts one real
                    # bar towards the recovery window. After a full warmup of real
                    # bars both tiers clear: the middle tier's contaminated window
                    # has flushed, and the large tier's re-warm is over. Before
                    # CUL-359 the large tier was never cleared, so gap_forced_flat
                    # kept the symbol flat for the rest of the run.
                    self._bars_since_gap[symbol] = self._bars_since_gap.get(symbol, 0) + 1
                    if self._bars_since_gap[symbol] >= self.strategy.required_bars:
                        del self._active_gap_tier[symbol]

            # 2026-07-07: warmup-only prefetch bars (see BacktestEngine.warmup_cutoff_timestamp)
            # update the strategy's internal history so indicators are primed by the
            # real scoring window's start, but must never trade or touch portfolio
            # state. Default None preserves exact prior behavior: every bar trades.
            if self.warmup_cutoff_timestamp is not None and data_time < self.warmup_cutoff_timestamp:
                self.strategy.update(data)
                return

            self.logger.debug(f"🕯 CANDLE │ {symbol} │ {data_time} │ Close: ${close:.2f} ")

            # Retrieve portfolio information
            balances = self.portfolio_info.get_account_balance()

            # 2026-07-24 (design §5): off-by-default funding accrual. Charge funding on
            # the position HELD INTO this bar — i.e. on `balances` as they stand BEFORE
            # this bar's rebalance below — using `close` as the mark and the funding
            # settled during this bar (settlements dated to this bar's day). Placed here
            # so the accrual flows into the mark-to-market at the next line and into the
            # recorded bar-level total_portfolio_value series. Flag off (default) or no
            # feed → skipped entirely, preserving byte-identical prior behavior.
            if self.model_funding and self.funding_daily is not None:
                f_bar = self._funding_rate_for_bar(symbol, data_time)
                if f_bar is not None:
                    self.portfolio_info.apply_funding(symbol, close, f_bar)

            total_portfolio_value = self.portfolio_info._calculate_total_portfolio_value(balances, close)
            self.logger.debug(f"   💼 Portfolio: ${total_portfolio_value:.2f}")

            # 2026-08-29 (fix/risk-layer, PR-2): fold this bar's decision-time equity
            # into the stateful controls (drawdown peak, Paris-day loss anchor) BEFORE
            # the forecast is mapped, so a trip forces the target flat below. Gate None
            # (default) or cap-only -> no state tracked, output byte-identical. Reads
            # only this bar's close-derived equity -> no look-ahead.
            if self.risk_gate is not None:
                self.risk_gate.observe(data_time, total_portfolio_value)

            previous_allocation = self.portfolio_info._calculate_actual_allocation(close, balances, total_portfolio_value, symbol)

            # Update strategy with data history and generate signals
            self.strategy.update(data)
            signal = self.strategy.generate_signals()

            # Get target allocation from forecast
            
            target_allocation = self.forecast_manager.forecast_to_allocation(signal.forecast)

            # CUL-274: a NaN forecast (a component that could not measure --
            # CUL-273 propagate_invalid, a 0/0, a feed not started yet) must
            # never reach an order: abs(NaN) != 0.0 is True and every risk
            # comparison against NaN is False, so it used to pass straight to
            # execution. Policy (operator 2026-10-01): HOLD -- the strategy's
            # own target is the current position, so the strategy makes no new
            # decision on this bar. The risk controls and gap tiers below still
            # apply, exactly as on any held bar: a latched kill switch or a large
            # gap forces flat, and a cap clamp can still trim a position that
            # drifted above the cap. Counted, sampled and surfaced in
            # metrics.json ("nan_forecast"); 'NaN -> forced flat' with a context
            # label on the trade waits for E-029 (CUL-358). Also catches +/-inf
            # (the production engine clips to +/-20, so only a custom strategy
            # could produce one). Warmup-cutoff bars return earlier and are not
            # counted. A run without a non-finite forecast is byte-identical.
            nan_forecast_bar = not math.isfinite(target_allocation)
            if nan_forecast_bar:
                self.nan_forecast_bars[symbol] = self.nan_forecast_bars.get(symbol, 0) + 1
                if len(self.nan_forecast_samples) < 20:
                    self.nan_forecast_samples.append({"symbol": symbol, "timestamp": str(data_time)})
                self.logger.warning(
                    f"⚠ NaN FORECAST │ {symbol} │ {data_time} │ holding the current "
                    f"allocation {previous_allocation:+.4f} (no strategy trade; risk "
                    f"controls and gap tiers still apply)"
                )
                target_allocation = previous_allocation

            # 2026-08-29 (fix/risk-layer): off-by-default portfolio risk gate.
            # Gate None (default) -> risk_extras stays {} and record_state below adds
            # no columns, so output is byte-identical. Gate set -> the target is
            # clamped to the configured cap (PR-1), or forced to 0.0 while the gate is
            # latched flat by max_drawdown_kill / daily_loss_limit (PR-2); the raw/
            # clamped/killed/halted telemetry is recorded.
            risk_extras = {}
            if self.risk_gate is not None:
                target_allocation, risk_extras = self.risk_gate.apply(target_allocation)
                if nan_forecast_bar:
                    # the strategy asked for nothing measurable: record that, not
                    # the held allocation, as the raw (pre-gate) target
                    risk_extras["risk_target_raw"] = float("nan")

            # CUL-271: "large" tier forces flat, composed with the risk gate the
            # same way risk_gate.apply() itself forces flat when latched -- both
            # act on target_allocation BEFORE allocation_change is derived from
            # it, so whichever fires, the delta is computed consistently. gap_
            # policy None (default) or no active "large" tier for this symbol ->
            # gap_forced_flat False, byte-identical to before this existed.
            gap_forced_flat = self._active_gap_tier.get(symbol) == "large"
            if gap_forced_flat:
                target_allocation = 0.0

            allocation_change = self.forecast_manager.calculate_allocation_change(target_allocation, previous_allocation)

            # CUL-271: "middle" tier keeps an existing position but blocks a NEW
            # entry (flat -> nonzero) until the recovery window elapses (cleared
            # in the gap-classification block above once bars_since_gap reaches
            # the strategy's own required_bars). Reducing or closing an existing
            # position is NOT blocked -- only OPENING new exposure on indicator
            # state that may still span the gap. gap_policy None (default) or no
            # active "middle" tier -> this is never reached, byte-identical.
            if self._active_gap_tier.get(symbol) == "middle" and previous_allocation == 0.0 and allocation_change != 0.0:
                self.logger.info(
                    f"⛔ GAP MIDDLE-TIER │ {symbol} │ new entry blocked (target {target_allocation:+.4f})"
                )
                allocation_change = 0.0

            #Init variables
            approved_rebalance = None
            debug_approve_allocation_change = {}
            success_execute_portfolio_rebalance = None
            debug_execute_portfolio_rebalance = {}
            
            # PR-2: when the gate is latched flat (killed / daily-halted, whether it
            # tripped this bar or earlier) the forced close is routed DIRECTLY through
            # _execute_portfolio_rebalance, bypassing approve_allocation_change exactly
            # as _close_all_positions_at_end does -- otherwise the min-Δ band rejects a
            # residual position smaller than 0.2 and the kill never flattens (Phase-A
            # trap Q1). Keying off the latch (not "tripped this bar") means a failed
            # flatten retries next bar through the same bypass. Gate None -> False ->
            # the existing per-trade flow below is byte-identical.
            # CUL-271: gap_forced_flat (computed above, before allocation_change)
            # reuses this exact same bypass -- a large-gap flatten has the same
            # min-Δ-band problem a risk-gate flatten does.
            risk_forced_flat = gap_forced_flat or (
                self.risk_gate is not None and (self.risk_gate.killed or self.risk_gate.daily_halted)
            )

            if risk_forced_flat:
                if abs(allocation_change) != 0.0:
                    self.logger.debug(
                        f"   🛑 {'GAP' if gap_forced_flat else 'RISK'} FLATTEN │ Actual: {previous_allocation} → 0.0"
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
                        self.logger.debug("   ✓ RISK FLATTEN executed successfully")
                    else:
                        self.logger.error(f"   ✗ RISK FLATTEN execution failed. Debug info: {debug_execute_portfolio_rebalance}")

            elif abs(allocation_change) != 0.0:
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
            postRebalance_current_allocation = self.portfolio_info._calculate_actual_allocation(close, postRebalance_balances, postRebalance_total_portfolio_value, symbol) if success_execute_portfolio_rebalance else previous_allocation
            
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
                    succcess_execute_portfolio_rebalance = success_execute_portfolio_rebalance if (approved_rebalance or risk_forced_flat) else None,
                    debug_execute_portfolio_rebalance = debug_execute_portfolio_rebalance if (approved_rebalance or risk_forced_flat) else {},
                    postRebalance_balances=postRebalance_balances,
                    postRebalance_total_value=postRebalance_total_portfolio_value,
                    postRebalance_current_allocation=postRebalance_current_allocation,
                    **risk_extras,
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
                actual_allocation = self.portfolio_info._calculate_actual_allocation(close, balances, total_value, symbol)

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
                    # None is what the per-bar path records when no rebalance was attempted
                    # (initialised :226, forced at :275 whenever approved_rebalance is falsy).
                    # No call is made here either, so match that convention.
                    success_execute_portfolio_rebalance, debug_execute_portfolio_rebalance = None, {}

                # Retrieve portfolio information after rebalance 
                postRebalance_balances = self.portfolio_info.get_account_balance() if success_execute_portfolio_rebalance else balances
                postRebalance_total_portfolio_value = self.portfolio_info._calculate_total_portfolio_value(postRebalance_balances, close) if success_execute_portfolio_rebalance else total_value
                if success_execute_portfolio_rebalance : self.logger.debug(f"   💼 Portfolio after rebalance: ${postRebalance_total_portfolio_value:.2f}")
                postRebalance_current_allocation = self.portfolio_info._calculate_actual_allocation(close, postRebalance_balances, postRebalance_total_portfolio_value, symbol) if success_execute_portfolio_rebalance else actual_allocation
                
                # === RECORD PORTFOLIO STATE === --> This is to store at a bar level and visualize it in a graph.
                if hasattr(self, 'portfolio_state_tracker'):
                    tracker = getattr(self, 'portfolio_state_tracker', None)
                    # `data` here is the SAME final bar the per-bar loop already
                    # recorded (get_data_history defaults to count=1), so a plain
                    # append would give portfolio_states.csv two rows for one
                    # instant -- pre-close and post-close. replace_if_same_bar folds
                    # the post-close numbers onto that existing row instead, keeping
                    # the file one-row-per-bar. It fires only when the last recorded
                    # timestamp actually matches, so the paths that record nothing
                    # for this bar (warmup-gated, or the per-bar body raised) still
                    # append normally. Single-symbol only: rows carry no symbol, so
                    # with several replaying symbols the previous row could belong to
                    # another one -- that case keeps today's behaviour untouched.
                    tracker.record_state(
                        data = data,
                        replace_if_same_bar=len(self.symbols) == 1,
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
