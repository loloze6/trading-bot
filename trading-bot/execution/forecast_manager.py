import math
import time
from typing import Any, Dict, List, Optional, Union, Tuple
import datetime
from performance.metrics import EnhancedPerformanceTracker, CompletedTrade
from data.data_manager import Candle
from strategies.registry import normalise_sizing_block, sizing_realised_vol
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

    NO DRIFT THRESHOLD LIVES HERE. This class holds no threshold and no
    per-bar state (D-176: `__init__` takes one optional `sizing` block; without
    it, nothing changes). The caller
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

    def __init__(self, sizing: Optional[Dict[str, Any]] = None):
        """
        sizing (D-176): a strategy_config.json strategies.sizing block, or None
        (the default -- key absent). None keeps this class exactly as before:
        forecast_to_allocation is forecast / 10 and nothing else. A block is
        validated here (normalise_sizing_block: loud ValueError when malformed)
        and turns on vol targeting in the allocation step.
        """
        self.sizing = normalise_sizing_block(sizing) if sizing is not None else None
        # Realised vol of the last sized allocation (None before one, without a
        # block, or when the closes could not give one). Read by the caller for
        # the bars.csv sizing columns; never read back here.
        self.last_realised_vol: Optional[float] = None

    def signal_allocation(self, forecast: float) -> float:
        """The unsized allocation, forecast / 10 -- the signal on the
        allocation scale (D-176: what the min_allocation_change band judges
        when a sizing block is present)."""
        return forecast / FORECAST_FOR_100_INVESTMENT

    def forecast_to_allocation(self, forecast: float, closes=None) -> float:
        """
        Convert forecast (-20 to +20) to target allocation (-200% to +200%).
        
        Args:
            forecast: Forecast value between min_forecast and max_forecast
            closes: (D-176, sizing block only) the strategy's close history up
                to and including the current bar; ignored without a block.
            
        Returns:
            Target allocation between -1.0 and 1.0 (without a sizing block)
        """
        
        # Linear mapping from forecast range to allocation range
        allocation = forecast / FORECAST_FOR_100_INVESTMENT

        if self.sizing is None:
            return allocation

        # D-176: allocation = forecast * target_annual_vol / realised / 10 --
        # the vol_target op's own arithmetic and order (registry._vol_target),
        # then this method's division by 10 -- clipped to +/-max_allocation.
        if closes is None:
            raise ValueError("ForecastManager: a sizing block needs the close history (closes=...)")
        self.last_realised_vol = None
        if not math.isfinite(allocation):
            return allocation  # NaN/inf forecast: left for the caller's CUL-274 hold
        realised = sizing_realised_vol(closes, self.sizing)
        self.last_realised_vol = realised
        if realised is None:
            return 0.0  # where the op would raise on its data: flat (see sizing_realised_vol)
        sized = forecast * self.sizing["target_annual_vol"] / realised / FORECAST_FOR_100_INVESTMENT
        if not math.isfinite(sized):
            return 0.0
        cap = float(self.sizing["max_allocation"])
        return float(min(max(sized, -cap), cap))
    
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
    



