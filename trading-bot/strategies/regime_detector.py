from enum import Enum
from dataclasses import dataclass
import numpy as np
import pandas as pd
import logging
# from strategies.strategy_base import ComponentOutput
# # from strategies.strategy_base import SubStrategyComponent
# # from strategies.strategy_base import CompositeStrategy
# from strategies.simple_strategy import MomentumStrategy

logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere


class MarketRegime(Enum):
    """Market regime classifications"""
    TRENDING = "trending"                   # Strong directional trend
    UNKNOWN = "unknown"                       # Not enough data

@dataclass
class RegimeMetrics:
    """Market regime metrics calculated from rolling window with
    trend_strength -> Rolling return over lookback
    lookback_bars -> Window size used
    current_price -> For reference
    """
    trend_strength: float       # Rolling return over lookback
    
    # Meta
    lookback_bars: int         # Window size used
    current_price: float       # For reference

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import logging
import numpy as np
from collections import deque
from dataclasses import dataclass
from enum import Enum

@dataclass
class ComponentOutput:
    """Output from any component - standardized format."""
    forecast: float  # -20 to +20
    confidence: float  # 0 to 1 (how confident are we?)
    componentName: str  # Active strategy
    parameters: Dict[str, Any]  # Parameters used
    weight: float  # Weight of the component in ensemble
    debug_info: Dict[str, Any]  # For logging and analysis


class SubStrategyComponent(ABC):
    """
    Base class for sub-strategy components.
    Each component generates a forecast independently.
    """
    
    def __init__(self, name: str, weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        self.name = name
        self.weight = weight
        self.parameters = parameters if parameters is not None else {}
        self.data = None

        self.active = True
        self.performance_window = 50
        self.recent_performance = []

    @abstractmethod
    def is_ready(self) -> bool:
        """Check if component has enough data."""
        pass

    @abstractmethod
    def update(self, data: pd.DataFrame):
        """Update component with new data."""
        pass
    
    @abstractmethod
    def generate_forecast(self) -> ComponentOutput:
        """
        Generate forecast for this component.
        
        Returns:
            forecast: -20 to +20
            debug: Dictionary with calculation details
        """
        pass
    
    
    @abstractmethod
    def get_required_periods(self) -> int:
        """Minimum data periods required."""
        pass

class CompositeStrategy2(SubStrategyComponent):
    """
    Composite strategy that combines multiple sub-strategy components.
    Loop on components to 
    - initialize
    - update
    - check readiness
    - generate weighted forecast
    """
    
    def __init__(self, 
                 components: List[SubStrategyComponent],
                 name: str = "CompositeStrategy"):
        super().__init__(name)
        
        self.components = components
        self.data = None
        
        # Normalize weights        
        logger.info(f"✅ Strategy initialized with {len(components)} components")
        total_weight = sum(c.weight for c in components)            
        for comp in components:
            comp.weight = comp.weight / total_weight
            logger.info(f"   • {comp.name}: weight={comp.weight:.2f}")

    def update(self, data: pd.DataFrame):
        """Update all components with new data."""
        pass


    def update_regime_metrics(self, data: pd.DataFrame):
        """Update all components with new data."""
        self.data = data
        
        for component in self.components:
            component.update(data)
    
    def is_ready(self) -> bool:
        """Check if all components are ready."""
        if self.data is None:
            return False
        
        return all(comp.is_ready() for comp in self.components)
    
    def generate_forecast(self) -> Tuple[float, float, Dict[str, Any]]:
        """
        Generate weighted ensemble forecast.
        
        Returns:
            forecast: Combined forecast from all components
            confidence: 0 for now
            debug: Details from all components
        """
        
        if not self.is_ready():
            return 0.0, 0.0, {'error': 'not_ready'}
        
        # Collect forecasts from all components
        component_forecasts = []
        debug_info = {'components': {}}
        
        for component in self.components:
            ComponentOutput = component.generate_forecast()
            component_forecasts.append({
                'name': ComponentOutput.componentName,
                'forecast': ComponentOutput.forecast,
                'weight': ComponentOutput.weight,
                'weighted_contribution': ComponentOutput.forecast * ComponentOutput.weight,
                'confidence': ComponentOutput.confidence,
                'parameters': ComponentOutput.parameters,
            })

            debug_info['components'][component.name] = ComponentOutput.debug_info
        
        # Calculate weighted ensemble
        final_forecast = sum(c['weighted_contribution'] for c in component_forecasts)
        
        # Clip to range
        final_forecast = np.clip(final_forecast, -20, 20)
        
        # Add ensemble info to debug
        debug_info['ensemble'] = component_forecasts
        debug_info['final_forecast'] = final_forecast
        
        # Log ensemble
        logger.debug(f"   🎯 Strategy ensemble:")
        for c in component_forecasts:
            logger.debug(f"      {c['name']}: {c['forecast']:+.2f} × {c['weight']:.2f} = {c['weighted_contribution']:+.2f}")
        logger.debug(f"      Final: {final_forecast:+.2f}")
        
        return float(final_forecast), 0.0, debug_info
    
    def get_required_periods(self) -> int:
        """Return maximum periods required by any component."""
        return max(comp.get_required_periods() for comp in self.components)

class MomentumConfirmationComponent(SubStrategyComponent):
    """
    Confirms that momentum is reversing (not just price stretched).
    Compares very recent momentum vs recent momentum.
    
    Theory: If price stretched AND momentum turning → reversion starting
    """
    
    def __init__(self,
                 weight: float = 0.3,
                 name: str = "MomentumConfirmation", 
                 parameters: Optional[Dict[str, Any]] = {},):
        super().__init__(name, weight, parameters)
        
        self.parameters = parameters
        
        self.short_period = self.parameters.get('short_period', 3)
        self.long_period = self.parameters.get('long_period', 10)
        
        self.short_momentum = None
        self.long_momentum = None
        
        logger.info(f"   ├─ {name}: Comparing {self.short_period}-bar vs {self.long_period}-bar momentum")
    
    def update(self, data: pd.DataFrame):
        """Calculate momentum over different timeframes."""
        self.data = data
        
        if len(data) >= self.long_period:
            prices = data['close'].values
            
            # Short-term momentum (last 3 bars)
            recent_avg = np.mean(prices[-self.short_period:])
            base_price = prices[-(self.short_period + 1)]
            self.short_momentum = (recent_avg / base_price - 1) * 100
            
            # Longer-term momentum (last 10 bars)
            longer_avg = np.mean(prices[-self.long_period:])
            base_longer = prices[-(self.long_period + 1)]
            self.long_momentum = (longer_avg / base_longer - 1) * 100
    
    def is_ready(self) -> bool:
        """Check if enough data."""
        if self.data is None:
            return False
        return len(self.data) >= self.long_period + 1
    
    def generate_forecast(self) -> Tuple[float, Dict[str, Any]]:
        """
        Generate momentum-based confirmation signal.
        
        Logic:
        - If short-term momentum OPPOSING long-term → reversion likely → STRONG signal
        - If momentum neutral → MODERATE signal
        - If momentum aligned with trend → NO signal (wait for confirmation)
        """
        
        if not self.is_ready():
            return 0.0, {'error': 'not_ready'}
        
        # Detect momentum reversal
        momentum_divergence = self.short_momentum - self.long_momentum
        
        # Generate confirmation signal
        # Negative momentum_divergence = momentum weakening = reversal starting
        # We want to AMPLIFY the base signal when this happens
        
        if abs(momentum_divergence) < 0.1:
            # Neutral momentum - no clear signal
            forecast = 0.0
            confirmation_state = 'NEUTRAL'
        elif momentum_divergence < 0:
            # Momentum weakening - confirms reversal DOWN
            # Generate NEGATIVE forecast (SHORT)
            forecast = momentum_divergence * 2  # Scale up
            forecast = np.clip(forecast, -20, 0)
            confirmation_state = 'REVERSAL_DOWN'
        else:
            # Momentum strengthening - confirms reversal UP
            # Generate POSITIVE forecast (LONG)
            forecast = momentum_divergence * 2
            forecast = np.clip(forecast, 0, 20)
            confirmation_state = 'REVERSAL_UP'
        
        confidence = 20

        debug_info = {
            'momentum_divergence': float(momentum_divergence),
            'confirmation_state': confirmation_state
        }

        return ComponentOutput(
            forecast=float(forecast),
            confidence=confidence,
            componentName=self.name,
            parameters=self.parameters,
            weight=self.weight,
            debug_info=debug_info
        )

    def get_required_periods(self) -> int:
        return self.long_period + 1

class RegimeDetector(CompositeStrategy2):
    """
    Detects market regimes using RELATIVE comparisons.
    NO fixed thresholds - compares current to recent historical behavior.
    """
    def __init__(self, 
                #  lookback: int = 100, memory_window: int = 500
                 ):
        """
        Args:
            lookback: Window for calculating current metrics (default: 100 bars)
            memory_window: Historical window for comparison (default: 500 bars)
        """
        ma_weight = 0
        momentum_weight = 1
        components = [
            MomentumConfirmationComponent(
                name="MomentumConfirmation 3/10",
                weight=momentum_weight,
                parameters={'short_period': 3, 'long_period': 10}
            )
        ]
        super().__init__(components, name="WeightedComponentStrategy")

        # self.lookback = lookback
        # self.memory_window = memory_window #Storage limit for historical comparison
        # self.metrics = None
        # self.historical_metrics = []  # Store past metric values

        # For Logging - Track regime state
        self.current_regime = MarketRegime.UNKNOWN
        self.previous_regime = MarketRegime.UNKNOWN
        self.regime_change_count = 0
        self.bars_in_current_regime = 0

        # # Track data availability
        # self.bars_received = 0

        logger.info(f"🔧 RegimeDetector initialized")

    def get_required_bars(self) -> int:
        """Return minimum bars needed for operation."""
        return max(100, 50)  # Need 50 for historical percentiles
    
    def classify_regime(self) -> MarketRegime:
        """
        Classify regime using RELATIVE thresholds.
        Compares current metrics to historical percentiles.
        NO FIXED VALUES - adapts to market behavior.
        """
        if not self.is_ready():
            logger.info("⚠️  Cannot classify regime: detector not ready")
            return MarketRegime.UNKNOWN
        



        # Store previous regime
        self.previous_regime = self.current_regime

        # ====================================
        # REGIME CLASSIFICATION RULES
        # ====================================

        # Get score 
        forecast_regime, confidence_regime, debug_info = self.generate_forecast()
        
     

        # ====================================
        # CLASSIFICATION
        # ====================================
        
        # Favorable: Score >= 4 out of 5
        if forecast_regime <= 0:
            self.current_regime = MarketRegime.TRENDING
        
        # Everything else is unknown
        else:
            self.current_regime = MarketRegime.UNKNOWN
        
        # ====================================
        # TRACKING & LOGGING
        # ====================================
        
        # Increment bars in regime
        if self.current_regime == self.previous_regime:
            self.bars_in_current_regime += 1
        else:
            # REGIME CHANGE DETECTED
            self.bars_in_current_regime = 1
            self.regime_change_count += 1
            
            logger.info("=" * 80)
            logger.info(f"🔄 REGIME CHANGE #{self.regime_change_count}")
            logger.info(f"   Previous: {self.previous_regime.value}")
            logger.info(f"   New:      {self.current_regime.value}")
            logger.info(f"   Score:    {forecast_regime}")
            logger.info("-" * 80)
            # logger.info("   Criteria breakdown:")
            # for detail in debug_info.get('components', {}).values():
            #     logger.info(f"     {detail}")
            # logger.info("-" * 80)
            # logger.info(f"   Current Metrics:")
            # logger.info(f"     Trend:       {current_trend:+.2f}%")
            # logger.info("=" * 80)
        
        # Log periodic status (every 50 bars when no change)
        if self.bars_in_current_regime % 50 == 0:
            logger.info(
                f"📊 Regime Status: {self.current_regime.value} "
                f"(for {self.bars_in_current_regime} bars, score: {forecast_regime})"
            )
        
        return self.current_regime


# class RegimeDetector:
#     """
#     Detects market regimes using RELATIVE comparisons.
#     NO fixed thresholds - compares current to recent historical behavior.
#     """
#     def __init__(self, lookback: int = 100, memory_window: int = 500):
#         """
#         Args:
#             lookback: Window for calculating current metrics (default: 100 bars)
#             memory_window: Historical window for comparison (default: 500 bars)
#         """
#         self.lookback = lookback
#         self.memory_window = memory_window #Storage limit for historical comparison
#         self.metrics = None
#         self.historical_metrics = []  # Store past metric values

#         # For Logging - Track regime state
#         self.current_regime = MarketRegime.UNKNOWN
#         self.previous_regime = MarketRegime.UNKNOWN
#         self.regime_change_count = 0
#         self.bars_in_current_regime = 0

#         # Track data availability
#         self.bars_received = 0

#         logger.info(f"🔧 RegimeDetector initialized: lookback={lookback}, memory={memory_window}")

#     def is_ready(self) -> bool:
#         """
#         Check if regime detector has enough data.
        
#         Returns:
#             True if sufficient data for regime classification
#         """
#         # Need at least lookback bars for metrics
#         # AND at least 50 historical metrics for percentile calculations
#         has_data = self.bars_received >= self.lookback
#         has_history = len(self.historical_metrics) >= 50
        
#         if not has_data:
#             logger.debug(f"⏳ RegimeDetector warming up: {self.bars_received}/{self.lookback} bars")
#             return False
        
#         if not has_history:
#             logger.debug(f"⏳ RegimeDetector building history: {len(self.historical_metrics)}/50 metrics")
#             return False
        
#         return True

#     def get_required_bars(self) -> int:
#         """Return minimum bars needed for operation."""
#         return max(self.lookback, 50)  # Need 50 for historical percentiles

#     def update_regime_metrics(self, data: pd.DataFrame) -> RegimeMetrics:
#         """
#         Calculate current market regime metrics.
#         """
#         self.bars_received = len(data)

#         if len(data) < self.lookback:
#             # Not enough data
#             self.metrics = RegimeMetrics(0, #Trend strength
#                                          0, #Lookback bars
#                                          data['close'].iloc[-1] if len(data) > 0 else 0 #Current price
#                                          )
#             logger.info(f"⚠️  Insufficient data for metrics: {len(data)}/{self.lookback} bars")
#             return self.metrics

        
#         # Get current window
#         close_prices = data['close'].tail(self.lookback).values
#         current_price = close_prices[-1]
        
#         # ====================================
#         # 1. TREND STRENGTH (rolling return)
#         # ====================================
#         trend_strength = ((close_prices[-1] - close_prices[0]) / close_prices[0]) * 100
        
        
#         # Create metrics object
#         self.metrics = RegimeMetrics(
#             trend_strength=trend_strength,
#             lookback_bars=self.lookback,
#             current_price=current_price
#         )
        
#         # Store for historical comparison (keep last N)
#         self.historical_metrics.append({
#             'trend': trend_strength
#         })
        
#         if len(self.historical_metrics) > self.memory_window:
#             self.historical_metrics.pop(0)
        
#         return self.metrics

    
#     def classify_regime(self) -> MarketRegime:
#         """
#         Classify regime using RELATIVE thresholds.
#         Compares current metrics to historical percentiles.
#         NO FIXED VALUES - adapts to market behavior.
#         """
#         if not self.is_ready():
#             logger.info("⚠️  Cannot classify regime: detector not ready")
#             return MarketRegime.UNKNOWN
        

#         # Store previous regime
#         self.previous_regime = self.current_regime

#         # Extract historical distributions
#         hist_trends = [m['trend'] for m in self.historical_metrics]

#         # Calculate percentiles
#         trend_p50 = np.percentile(hist_trends, 50)
#         trend_p75 = np.percentile(hist_trends, 75)
#         trend_p25 = np.percentile(hist_trends, 25)
        

#         # ====================================
#         # REGIME CLASSIFICATION RULES
#         # ====================================
        
#         current_trend = self.metrics.trend_strength
        
#         # Score each condition (0-5 scale)
#         score = 0
#         max_score = 5
#         score_details = []

#         # 1. Is trend weak? (between 25th-75th percentile)
#         if trend_p25 <= current_trend <= trend_p75:
#             score += 1  # Weak trend = good for mean reversion
#             score_details.append(f"✓ Weak trend ({current_trend:+.2f}% in [{trend_p25:+.1f}, {trend_p75:+.1f}])")
#         else:
#             score_details.append(f"✗ Strong trend ({current_trend:+.2f}% outside [{trend_p25:+.1f}, {trend_p75:+.1f}])")
        
        
#         # ====================================
#         # CLASSIFICATION
#         # ====================================
        
#         # Favorable: Score >= 4 out of 5
#         if score <= 4:
#             self.current_regime = MarketRegime.TRENDING
        
#         # Everything else is unknown
#         else:
#             self.current_regime = MarketRegime.UNKNOWN
        
#         # ====================================
#         # TRACKING & LOGGING
#         # ====================================
        
#         # Increment bars in regime
#         if self.current_regime == self.previous_regime:
#             self.bars_in_current_regime += 1
#         else:
#             # REGIME CHANGE DETECTED
#             self.bars_in_current_regime = 1
#             self.regime_change_count += 1
            
#             logger.info("=" * 80)
#             logger.info(f"🔄 REGIME CHANGE #{self.regime_change_count}")
#             logger.info(f"   Previous: {self.previous_regime.value}")
#             logger.info(f"   New:      {self.current_regime.value}")
#             logger.info(f"   Score:    {score}/{max_score}")
#             logger.info("-" * 80)
#             logger.info("   Criteria breakdown:")
#             for detail in score_details:
#                 logger.info(f"     {detail}")
#             logger.info("-" * 80)
#             logger.info(f"   Current Metrics:")
#             logger.info(f"     Trend:       {current_trend:+.2f}%")
#             logger.info("=" * 80)
        
#         # Log periodic status (every 50 bars when no change)
#         if self.bars_in_current_regime % 50 == 0:
#             logger.info(
#                 f"📊 Regime Status: {self.current_regime.value} "
#                 f"(for {self.bars_in_current_regime} bars, score: {score}/{max_score})"
#             )
        
#         return self.current_regime

