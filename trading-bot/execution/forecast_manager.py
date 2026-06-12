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
        3. Compare with current allocation
        4. Trigger rebalance if change > threshold
    """
    
    def __init__(self):  # 5% threshold
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
    



