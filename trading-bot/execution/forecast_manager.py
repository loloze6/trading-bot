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

Maps forecast values (-20 to +20) to allocation percentages (-100% to +100%).
Triggers rebalancing when allocation drift exceeds threshold.
"""

class ForecastManager:
    """
    Manages continuous portfolio rebalancing based on forecasts.
    
    Workflow:
        1. Strategy generates forecast (e.g., +15 = bullish)
        2. Convert to allocation (e.g., +75% long)
        3. Compare with current allocation
        4. Trigger rebalance if change > threshold
    """
    
    def __init__(self, 
                 max_forecast: float = 20.0,
                 min_forecast: float = -20.0,
                 max_allocation: float = 1.0,  # 100%
                 min_allocation: float = -1.0,  # -100%
                 rebalance_threshold: float = 0.05):  # 5% threshold
        
        self.max_forecast = max_forecast
        self.min_forecast = min_forecast
        self.max_allocation = max_allocation
        self.min_allocation = min_allocation
        self.rebalance_threshold = rebalance_threshold
        
        # Current positions: symbol -> allocation (-1.0 to 1.0)
        self.current_allocations: Dict[str, float] = {}
        # Target positions: symbol -> allocation (-1.0 to 1.0)
        self.target_allocations: Dict[str, float] = {}
        
        logger.info(f"📊 Forecast Manager initialized │ "
                   f"Forecast range: [{min_forecast}, {max_forecast}] │ "
                   f"Allocation range: [{min_allocation:+.0%}, {max_allocation:+.0%}] │ "
                   f"Rebalance threshold: {rebalance_threshold:.1%}")

    def get_target_allocation(self, symbol: str) -> float:
        """Get the intended target allocation (static)."""
        return self.target_allocations.get(symbol, 0.0)

    def set_target_allocation(self, symbol: str, allocation: float):
        """Set the target allocation after a rebalance."""
        self.target_allocations[symbol] = allocation
        logger.debug(f"      📝 Target allocation set: {symbol} = {allocation}")

    
    def calculate_actual_allocation(self, symbol: str, position_value: float, 
                                     total_portfolio_value: float) -> float:
        """
        Calculate the ACTUAL market-value allocation.
        
        Args:
            position_value: Current market value of position (qty * current_price)
            total_portfolio_value: Total portfolio value
            
        Returns:
            Actual allocation (-1 to +1)
        """
        if total_portfolio_value == 0:
            return 0.0
        
        actual_allocation = position_value / total_portfolio_value
        return actual_allocation

    def forecast_to_allocation(self, forecast: float) -> float:
        """
        Convert forecast (-20 to +20) to target allocation (-100% to +100%).
        
        Args:
            forecast: Forecast value between min_forecast and max_forecast
            
        Returns:
            Target allocation between -1.0 and 1.0
        """
        # Store original forecast for logging
        original_forecast = forecast


        # Clamp forecast to valid range
        forecast = max(self.min_forecast, min(self.max_forecast, forecast))
        if forecast != original_forecast:
            logger.warning(f"⚠ Forecast clamped │ {original_forecast} → {forecast}")
        
        # Linear mapping from forecast range to allocation range
        allocation = ((forecast - self.min_forecast) / 
                     (self.max_forecast - self.min_forecast) * 
                     (self.max_allocation - self.min_allocation) + 
                     self.min_allocation)
        
        # LOG ONLY / Log mapping with visual indicator
        direction = "🟢 LONG" if allocation > 0 else "🔴 SHORT" if allocation < 0 else "⚪ NEUTRAL"
        logger.debug(f"   🔄 Forecast→Allocation │ {forecast} → {allocation:+.1%} │ {direction}")
        
        return allocation

    def needs_rebalance(self, symbol: str, new_target: float, current_actual: float) -> Tuple[bool, float]:
        """
        Check if rebalance is needed.
        
        CRITICAL: Compare new target with ACTUAL market allocation, not old target!
        
        Args:
            new_target: New target allocation from forecast
            current_actual: Current ACTUAL market-value allocation
            
        Returns:
            (needs_rebalance, allocation_change)
        """
        # Calculate change from actual market position, not target!
        allocation_change = new_target - current_actual
        
        needs_rebalance = abs(allocation_change) >= self.rebalance_threshold

        if needs_rebalance:
            self.set_current_allocation(symbol, current_actual)  # Update current allocation for logging
        
        return needs_rebalance, allocation_change

    def calculate_rebalance_needed(self, symbol: str, target_allocation: float) -> Tuple[bool, float]:
        """
        Check if rebalancing is needed for a symbol.
        
        Args:
            symbol: Trading symbol
            target_allocation: Target allocation (-1.0 to 1.0)
            
        Returns:
            Tuple of (needs_rebalance, allocation_change)
        """
        current_allocation = self.current_allocations.get(symbol, 0.0)
        allocation_change = target_allocation - current_allocation
        
        needs_rebalance = abs(allocation_change) >= self.rebalance_threshold

        # Log decision with visual indicators
        if needs_rebalance:
            change_pct = allocation_change * 100
            direction = "📈" if allocation_change > 0 else "📉"
            logger.debug(f"   ✓ Rebalance needed │ {symbol} │ {direction} Δ: {change_pct:+.1f}% │ "
                        f"Current: {current_allocation:+.1%} → Target: {target_allocation:+.1%}")
        else:
            logger.debug(f"   ✗ No rebalance │ {symbol} │ Δ: {allocation_change:+.1%} < {self.rebalance_threshold:.1%} threshold")

        return needs_rebalance, allocation_change
    
    def update_target_allocation(self, symbol: str, forecast: float):
        """Update target allocation based on new forecast."""
        
        if forecast is not None:
            target_allocation = self.forecast_to_allocation(forecast)
        else: 
            target_allocation = self.current_allocations.get(symbol, 0.0)
            logger.debug(f"   ⚠ No forecast for {symbol}, maintaining current allocation: {target_allocation:+.1%}")

        # Track previous target for comparison
        previous_target = self.target_allocations.get(symbol, None)
        self.target_allocations[symbol] = target_allocation
            
        # LOG ONLY / Only log if there's a meaningful change or in debug mode
        if previous_target is not None and abs(target_allocation - previous_target) > 0.001:
            change = target_allocation - previous_target
            change_symbol = "↗" if change > 0 else "↘"
            logger.debug(f"   🎯 Target updated │ {symbol} │ {previous_target:+.1%} {change_symbol} {target_allocation:+.1%} │ "
                        f"Forecast: {forecast if forecast else 'N/A'}")
        elif previous_target is None:
            logger.debug(f"   🎯 Target set │ {symbol} │ {target_allocation:+.1%} │ Forecast: {forecast if forecast else 'N/A'}")
            
    def get_current_allocation(self, symbol: str) -> float:
        """Get current allocation for a symbol."""
        allocation = self.current_allocations.get(symbol, 0.0)
        logger.debug(f"   📍 Current allocation │ {symbol}: {allocation:+.1%}")
        return allocation
    
    def set_current_allocation(self, symbol: str, allocation: float):
        """Set current allocation after successful trade execution."""
        previous_allocation = self.current_allocations.get(symbol, None)
        self.current_allocations[symbol] = allocation

        # # LONG ONLY / Log with visual indicators
        # direction = "🟢" if allocation > 0 else "🔴" if allocation < 0 else "⚪"
        
        # if previous_allocation is not None and previous_allocation != allocation:
        #     change = allocation - previous_allocation
        #     change_pct = change
        #     arrow = "↗" if change > 0 else "↘"
        #     logger.info(f"   {direction} Allocation updated │ {symbol} │ {previous_allocation} {arrow} {allocation} │ Δ: {change_pct:+.1f}%")
        # else:
        #     logger.info(f"   {direction} Allocation set │ {symbol}: {allocation}")


    def get_allocation_summary(self) -> Dict[str, Dict[str, float]]:
        """
        Get summary of all current and target allocations.
        
        Returns:
            Dictionary with allocation details for each symbol
        """
        summary = {}
        
        all_symbols = set(list(self.current_allocations.keys()) + list(self.target_allocations.keys()))
        
        for symbol in all_symbols:
            current = self.current_allocations.get(symbol, 0.0)
            target = self.target_allocations.get(symbol, 0.0)
            drift = target - current
            
            summary[symbol] = {
                'current': current,
                'target': target,
                'drift': drift,
                'needs_rebalance': abs(drift) >= self.rebalance_threshold
            }
        
        # Log summary table
        if summary:
            logger.info(f"📊 Allocation Summary │ {len(summary)} symbol(s)")
            for symbol, data in summary.items():
                status = "🔄" if data['needs_rebalance'] else "✓"
                logger.info(f"   {status} {symbol} │ Current: {data['current']:+.1%} │ "
                           f"Target: {data['target']:+.1%} │ Drift: {data['drift']:+.1%}")
        
        return summary
    
    def reset_allocations(self, symbol: Optional[str] = None):
        """
        Reset allocations to neutral (0.0).
        
        Args:
            symbol: If provided, reset only this symbol. Otherwise reset all.
        """
        if symbol:
            if symbol in self.current_allocations:
                logger.info(f"♻️ Reset allocation │ {symbol} │ {self.current_allocations[symbol]:+.1%} → 0.0%")
                self.current_allocations[symbol] = 0.0
                self.target_allocations[symbol] = 0.0
        else:
            num_symbols = len(self.current_allocations)
            logger.info(f"♻️ Reset all allocations │ {num_symbols} symbol(s) → 0.0%")
            self.current_allocations.clear()
            self.target_allocations.clear()
    
    def get_position_type(self, symbol: str) -> str:
        """
        Get human-readable position type based on current allocation.
        
        Returns:
            Position type: 'LONG', 'SHORT', or 'NEUTRAL'
        """
        allocation = self.current_allocations.get(symbol, 0.0)
        
        if allocation > 0.01:
            return "LONG"
        elif allocation < -0.01:
            return "SHORT"
        else:
            return "NEUTRAL"