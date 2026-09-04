from strategies.regime_engine import ConfigDrivenRegimeEngine
from strategies.strategy_engine import ConfigDrivenStrategyEngine
from strategies.strategy_base import MainStrategy, MarketRegime, RollingBuffer
from tools.validate_config import validate as _validate_config
from typing import Any, Dict, Optional, Tuple
import json
import os
import pandas as pd
import logging

logger = logging.getLogger("trading_bot")


class AdvancedStrategy(MainStrategy):
    """Multi-regime adaptive trading strategy driven by strategy_config.json."""

    def __init__(self, config_path: Optional[str] = None,
                 candle_interval_seconds: Optional[int] = None,
                 ignore_max_bars: Optional[int] = None):
        """
        candle_interval_seconds/ignore_max_bars: CUL-273 -- both None (default,
        every existing call site) leaves data_buffer's timestamp-reindex off,
        byte-identical to before this ticket. Supplying both enables it (see
        RollingBuffer._reindex_to_expected_grid). NOT YET wired through
        core/launcher.py's AdvancedStrategy(...) call sites or gap_policy --
        that is real-path wiring, a separate, larger, not-yet-done change;
        this constructor accepting the parameters is the tested mechanism
        those call sites would need to actually pass them through.
        """
        if config_path is None:
            strategies_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir    = os.path.dirname(strategies_dir)
            config_path    = os.path.join(project_dir, 'strategy_config.json')

        self._config_path = config_path

        with open(config_path) as f:
            config = json.load(f)

        errors = _validate_config(config)
        if errors:
            for e in errors:
                logger.error(e)
            raise ValueError("invalid strategy_config")

        self.config = config

        self.regime_engine   = ConfigDrivenRegimeEngine(config["regime_detector"])
        self.strategy_engine = ConfigDrivenStrategyEngine(config["strategies"])

        std_dev_period = 24
        self.required_bars = max(
            self.regime_engine.get_required_periods(),
            self.strategy_engine.get_required_periods(),
            std_dev_period,
        )
        # CUL-273: required_bars is the single source of truth for how many
        # real bars this strategy needs before it trusts itself. Before this,
        # strategy_engine derived its own internal per-regime readiness
        # threshold (_warmup) independently, from its own local config --
        # measured on this fork's real strategy_config.json, the two had
        # already drifted (51 vs required_bars=120, the architecture doc's
        # own documented "~120 bars"). Reconciled here rather than leaving
        # strategy_engine's constructor guess in place.
        self.strategy_engine.set_warmup(self.required_bars)

        self.data_buffer = RollingBuffer(
            self.required_bars + 100,
            candle_interval_seconds=candle_interval_seconds,
            ignore_max_bars=ignore_max_bars,
        )
        self.data_buffer.register_calculated_column(
            'stddev_24', lambda df: df['close'].rolling(std_dev_period).std()
        )

        self.last_forecast = 0.0
        # F7: memoized regime_engine.classify() result for the bar currently being
        # evaluated. classify() has per-call side effects (veto-bar streak counters,
        # bars_in_current_regime/regime_change_count via _tick()) so it may run at
        # most once per bar. Invalidated in update(); populated lazily by whichever
        # of is_ready()/generate_forecast() runs first each bar (see _classify_once).
        self._regime_classification = None

        # F5b (P1a shakedown, 2026-07-04): update() previously swallowed any component
        # exception with a bare log line and no other trace. A component-level bug
        # (e.g. FundingRateMeanReversionComponent's threshold=0 divide-by-zero, F5a)
        # could therefore silently zero out an entire prescreen window and be
        # indistinguishable from a genuine "no signal" result (see run_044, 2026-07-04).
        # These counters make that distinguishable without changing update()'s
        # fail-open behavior (a bad component still must not crash the whole strategy).
        self.component_error_count = 0
        self.component_error_samples = []  # capped list; see _MAX_ERROR_SAMPLES
        self._update_call_count = 0

        logger.debug(f"✅ AdvancedStrategy initialized (required_bars={self.required_bars})")

    def reset_history(self) -> None:
        """CUL-271: large-gap segment split. Clears the shared data buffer and
        both engines' component history so the strategy re-warms from scratch
        on real post-gap bars, rather than treat a position held across a real
        market hole as informed by pre-gap history. Called by the trading
        engine when its gap_policy classifies a gap as "large"; never called
        when gap_policy is unset (byte-identical to before this method existed)."""
        self.data_buffer.clear()
        self.regime_engine.reset_history()
        self.strategy_engine.reset_history()
        self._regime_classification = None

    def _classify_once(self) -> Tuple[MarketRegime, Dict[str, Any]]:
        """regime_engine.classify() for the CURRENT bar, memoized so is_ready() and
        generate_forecast() agree on the same classification within one bar instead
        of running it twice (which would double-count classify()'s side effects:
        veto-bar streaks, bars_in_current_regime, regime_change_count)."""
        if self._regime_classification is None:
            self._regime_classification = self.regime_engine.classify()
        return self._regime_classification

    def is_ready(self) -> bool:
        if self.data_buffer.size < self.required_bars:
            logger.debug(f"NOT READY: buffer {self.data_buffer.size} / {self.required_bars}")
            return False
        if not self.regime_engine.is_ready():
            logger.debug(f"NOT READY: regime engine")
            return False
        # F7 fix: classify THIS bar before checking strategy-engine readiness, instead
        # of reading current_regime from before classify() has run (which was always
        # last bar's regime, or the UNKNOWN class-init default on the very first
        # ready-candidate bar -- vacuously "ready" for any regime with no components
        # registered under that key, letting the first forecast fire from under-warmed
        # per-regime history). See tests/test_ungated_config_pattern.py.
        regime, _ = self._classify_once()
        if not self.strategy_engine.is_ready(regime):
            logger.debug(f"NOT READY: strategy engine for {regime}")
            return False
        return True

    @property
    def required_feeds(self) -> dict[str, tuple[str, ...]]:
        """Feed name -> sorted tuple of consuming component names, merged across
        both engines. Configuration = intent: a component declared under any
        regime requires its feeds even if that regime never activates this run.
        Drives the V1 registration guard in core/backtester.py::load_data."""
        by_feed: dict[str, set] = {}
        for engine in (self.regime_engine, self.strategy_engine):
            for feed, names in engine.required_feeds().items():
                by_feed.setdefault(feed, set()).update(names)
        return {feed: tuple(sorted(names)) for feed, names in by_feed.items()}

    _MAX_ERROR_SAMPLES = 5

    def update(self, new_bar: pd.DataFrame):
        self._update_call_count += 1
        self._regime_classification = None  # new bar: last bar's classify() memo is stale
        stage = "buffer"
        try:
            self.data_buffer.add_data(new_bar.iloc[-1].to_dict())
            window = self.data_buffer.get_df()
            stage = "regime_engine"
            self.regime_engine.update(window)
            stage = "strategy_engine"
            self.strategy_engine.update(window)
        except Exception as e:
            # F5b: count and classify instead of a bare log line (see __init__ note).
            self.component_error_count += 1
            if len(self.component_error_samples) < self._MAX_ERROR_SAMPLES:
                self.component_error_samples.append({
                    "bar_index": self._update_call_count,
                    "stage": stage,
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                })
            logger.error(f"Error updating strategy (stage={stage}, bar={self._update_call_count}): {e}")

    def generate_forecast(self) -> Tuple[float, Any, MarketRegime, float, Dict[str, Any]]:
        regime, debug_regime = self._classify_once()

        forecast, debug_components = self.strategy_engine.forecast(regime)
        forecast_delta = forecast - self.last_forecast
        self.last_forecast = forecast

        debug_info = {
            'regime':        regime.value,
            'forecast_delta': forecast_delta,
            'regime_scores': debug_regime.get('scores', {}),
            'regime_margin': debug_regime.get('margin'),
            'bars_in_regime': self.regime_engine.bars_in_current_regime,
            'components': debug_components,
        }

        return forecast, None, regime, 0.0, debug_info

