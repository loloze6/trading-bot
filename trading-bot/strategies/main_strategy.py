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

    def __init__(self, config_path: Optional[str] = None):
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

        self.regime_engine   = ConfigDrivenRegimeEngine(config["regime_detector"])
        self.strategy_engine = ConfigDrivenStrategyEngine(config["strategies"])

        std_dev_period = 24
        self.required_bars = max(
            self.regime_engine.get_required_periods(),
            self.strategy_engine.get_required_periods(),
            std_dev_period,
        )

        self.data_buffer = RollingBuffer(self.required_bars + 100)
        self.data_buffer.register_calculated_column(
            'stddev_24', lambda df: df['close'].rolling(std_dev_period).std()
        )

        self.last_forecast = 0.0

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

    def is_ready(self) -> bool:
        if self.data_buffer.size < self.required_bars:
            logger.debug(f"NOT READY: buffer {self.data_buffer.size} / {self.required_bars}")
            return False
        if not self.regime_engine.is_ready():
            logger.debug(f"NOT READY: regime engine")
            return False
        # current_regime is from the previous bar (classify() hasn't run yet this bar).
        # Harmless in practice: regime transitions are rare and generate_forecast() is only
        # called when is_ready() returns True.
        if not self.strategy_engine.is_ready(self.regime_engine.current_regime):
            logger.debug(f"NOT READY: strategy engine for {self.regime_engine.current_regime}")
            return False
        return True

    _MAX_ERROR_SAMPLES = 5

    def update(self, new_bar: pd.DataFrame):
        self._update_call_count += 1
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
        regime, debug_regime = self.regime_engine.classify()

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

