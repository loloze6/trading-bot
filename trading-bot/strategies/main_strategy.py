from strategies.simple_strategy import (
WeightedComponentRegimeDetector,
RegimeToStrategyMapping,
MainStrategy,
MarketRegime,
RollingBuffer
)

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import logging
import numpy as np
from collections import deque
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere


class AdvancedStrategy(MainStrategy):
    """Strategy --> Multi-regime adaptive trading strategy."""
    
    def __init__(self):
        

        self.regime_detector = WeightedComponentRegimeDetector()
        self.strategies = RegimeToStrategyMapping.get_mapping()

        # Calculate required buffer size
        strategy_requirements = [
            strategy.get_required_periods() 
            for strategy in self.strategies.values() 
            if strategy is not None
        ]
        regime_requirement = self.regime_detector.get_required_periods()
        
        self.required_bars = max(
            max(strategy_requirements) if strategy_requirements else 0,
            regime_requirement, 
            std_dev_period := 24  # For stddev indicator
        )
        
        # Set the data rolling buffer size

        self.data_buffer = RollingBuffer(self.required_bars + 100)  # Add margin
        self.data_buffer.register_indicator('stddev_24', lambda df: df['close'].rolling(std_dev_period).std())
        
        # State tracking
        self.current_regime = MarketRegime.UNKNOWN
        self.regime_confidence = 0.0
        self.last_forecast = 0.0


        logger.info(f"✅ Strategy initialized")
        logger.info(f"   Required bars: {self.required_bars}")
        logger.info(f"   Buffer size: {self.data_buffer.max_size}")

    def is_ready(self) -> bool:
        """
        Check if strategy has enough data to trade.
        
        Returns:
            True if all components are ready
        """
        # Check buffer size
        if self.data_buffer.size < self.required_bars:
            logger.debug(
                f"⏳ Warming up: {self.data_buffer.size}/{self.required_bars} bars"
            )
            return False
        
        # Check regime detector
        if not self.regime_detector.is_ready():
            logger.debug("⏳ Regime detector not ready")
            return False
        
        # Check active strategy for current regime
        if self.current_regime != MarketRegime.UNKNOWN:
            active_strategy = self.strategies.get(self.current_regime)
            if active_strategy is not None and not active_strategy.is_ready():
                logger.debug(f"⏳ Active strategy {active_strategy.name} not ready")
                return False
        
        return True

    def update(self, new_bar: pd.DataFrame):
        """Update data rolling buffers with new data and regime metrics. Need to update also each strategy individually ?"""
        
        #Update data_buffer
        try:           
            # Convert row to dict
            bar_dict = new_bar.iloc[-1].to_dict()
            self.data_buffer.add_data(bar_dict)

            logger.debug(f"Standard Dev: {self.data_buffer['stddev_24']}")
            logger.debug(f"✅ Buffer updated: {self.data_buffer.size} bars")
        except Exception as e:
            logger.error(f"Error updating buffers: {e}")
        
        # Get rolling window for updates
        window = self.data_buffer.get_df()
        #Update regime detector using data_buffer
        try: 
            self.regime_detector.update(window)
            logger.debug(f"✅ Updated regime metrics")
        except Exception as e:
            logger.error(f"Error updating regime: {e}")

        # Update all sub-strategies using data_buffer
        try: 
            for regime, strategy in self.strategies.items():
                if strategy is not None:
                    strategy.update(window)
                    logger.debug(f"✅ Updated strategy: {strategy.name}")
        except Exception as e:
            logger.error(f"Error updating strategies: {e}")
    
    def generate_forecast(self) -> Tuple[float, Any, MarketRegime, float, Dict[str, Any]]:
        """Generate trading signals using regime-adaptive approach."""

        # REGIME - Detect current regime
        previous_regime = self.current_regime
        self.current_regime, debug_regime  = self.regime_detector.classify_regime()
        # REGIME - Log regime transition
        if self.current_regime != previous_regime and previous_regime != MarketRegime.UNKNOWN:
            logger.info("=" * 80)
            logger.info("🎯 STRATEGY REGIME TRANSITION")
            logger.info(f"   Previous: {previous_regime.value}")
            logger.info(f"   New:      {self.current_regime.value}")
            
            primary_strategy = self.strategies[self.current_regime]
            if primary_strategy is not None:
                logger.info(f"   ✅ Activating: {primary_strategy.name}")
            else:
                logger.info(f"   ⛔ NO STRATEGY for regime")
            logger.info("=" * 80)

        # STRATEGY - Get primary strategy for this regime
        primary_strategy = self.strategies.get(self.current_regime, None)
        
        # STRATEGY - Manage primary_strategy when None
        if primary_strategy is None:
            if self.current_regime not in self.strategies: # Handle not existing regimes
                logger.warning(
                    f"⚠️  Regime {self.current_regime.value} not mapped to any strategy. "
                    f"Available mappings: {list(self.strategies.keys())}"
                )

            logger.debug(
                f"⛔ No trading in {self.current_regime.value} "
                f"(bar {self.regime_detector.bars_in_current_regime})"
            )

            forecast = 0.0
            forecast_delta = forecast - self.last_forecast
            self.last_forecast = forecast

            debug_info = {
                'regime': self.current_regime.value,
                'reason': 'Strategy_is_None_for_regime',
                'bars_in_regime': self.regime_detector.bars_in_current_regime,
                'score_regime': debug_regime.get('forecast_regime', None)
            }
            
            return (forecast, None, self.current_regime, 0.0, debug_info)
        

        
        # STRATEGY - Get forecast of selected strategy
        forecast, confidence, debug = primary_strategy.generate_forecast()
        self.regime_confidence = confidence
        forecast_delta = forecast - self.last_forecast
        self.last_forecast = forecast

        debug_info = {
            'forecast_delta': forecast_delta,
            'status': 'active_trading',
            'strategy_name': primary_strategy.name,
            'score_regime': debug_regime.get('forecast_regime', None)
        }

        # Can be included later - Performance-based strategy weighting with get_performance_score
        
        # Can be included later - Ensemble with secondary strategies for robustness ; retrieving forecast and confidencce from primary_result
          
        # Can be included later - If primary strategy is underperforming, blend with others
                # Can be included later - Weighted blend
                # Can be included later - Combine primary and secondary

        # Can be included later - Apply confidence and risk filters
                # Can be included later - Reduce position size for low confidence
            
        # Update state

        # Prepare debug info

        return (forecast, primary_strategy, self.current_regime, self.regime_confidence, debug_info)
