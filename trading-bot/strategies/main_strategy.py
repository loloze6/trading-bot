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

    def update(self, new_bar: pd.DataFrame):
        try:
            self.data_buffer.add_data(new_bar.iloc[-1].to_dict())
            window = self.data_buffer.get_df()
            self.regime_engine.update(window)
            self.strategy_engine.update(window)
        except Exception as e:
            logger.error(f"Error updating strategy: {e}")

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

