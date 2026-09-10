import time
from typing import Any, Dict, List, Optional, Union, Tuple
import datetime
from performance.metrics import EnhancedPerformanceTracker, CompletedTrade
from data.data_manager import Candle
import logging

logger = logging.getLogger("trading_bot")

"""
Forecast Manager Module
=======================
Converts strategy forecasts to portfolio allocations and manages rebalancing.

Maps forecast values (-20 to +20) to allocation percentages (-200% to +200%).
Triggers rebalancing when allocation drift exceeds threshold.
"""

FORECAST_FOR_100_INVESTMENT = 10.0  # Forecast value that corresponds to 100% allocation

class ForecastManager:
    """
    Manages continuous portfolio rebalancing based on forecasts.
    
    Workflow:
        1. Strategy generates forecast (e.g., +15 = bullish)
        2. Convert to allocation (e.g., +75% long)
        3. Compute the delta against current allocation

    NO DRIFT THRESHOLD LIVES HERE. This class is stateless and holds no
    threshold -- `__init__` takes no arguments. The caller
    (`trading_bot.py:305`) proceeds to `risk_manager.approve_allocation_change`
    on `abs(allocation_change) != 0.0`, so ForecastManager itself never blocks
    a rebalance.

    CORRECTED (E-055, 2026-09-10): a prior revision of this docstring claimed
    "none lives anywhere else either" -- false. A change-based drift gate DOES
    exist, in `RiskManager._ctrl_min_allocation_change`
    (`risk/risk_manager.py`): it rejects any rebalance where
    `abs(allocation_change) < risk_management.controls.min_allocation_change
    .threshold` (`config.json`, default 0.2). This is not new -- it has been
    live since the `ac277917` repository restructure. Git archaeology on that
    commit (same diff hunk) shows the OLD `risk_management.rebalance_threshold`
    key and its `RiskManager(rebalance_threshold=...)` constructor call
    (both now deleted as dead) were replaced by this control in the same
    change -- i.e. this is that mechanism's successor, not an unrelated one.
    What IS new (E-055): a strategy's own `strategy_config.json` may set
    `strategies.min_allocation_change` to override the 0.2 default for that
    strategy's runs only (see `strategies/main_strategy.py` and
    `core/launcher.py::_build_risk_and_forecast_managers`); omitting the key
    preserves the exact prior global-0.2 behaviour byte-for-byte. See
    `strategy-research/engineering/improvements/known_divergences.md` (1).
    """

    def __init__(self):
        pass

    def forecast_to_allocation(self, forecast: float) -> float:
        """
        Convert forecast (-20 to +20) to target allocation (-200% to +200%).
        
        Args:
            forecast: Forecast value between min_forecast and max_forecast
            
        Returns:
            Target allocation between -1.0 and 1.0
        """
        
        # Linear mapping from forecast range to allocation range
        allocation = forecast / FORECAST_FOR_100_INVESTMENT
        
        return allocation
    
    def calculate_allocation_change(self, target_allocation: float, current_allocation: float) -> float:
        """
        Calculate the change in allocation needed to rebalance.
        
        Args:
            target_allocation: Desired target allocation from forecast
            current_allocation: Current ACTUAL market-value allocation
        Returns:
            Allocation change needed to rebalance
        """
        allocation_change = target_allocation - current_allocation
        return allocation_change
    



