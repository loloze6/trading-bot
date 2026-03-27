from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import numpy as np
import pandas as pd
import logging
from strategies.strategy_base import CompositeStrategy, SubStrategyComponent, RollingDataBuffer, MainStrategy, ComponentOutput
from strategies.regime_detector import RegimeDetector, MarketRegime, RegimeDetector2
import os

logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere

class RegimeToStrategyMapping():
    """Mapping of market regimes to sub-strategies."""
    @staticmethod 
    def get_mapping():
        return {
            MarketRegime.TRENDING: WeightedComponentStrategy(
                ma_weight=0,
                momentum_weight=1.0
            ),
            MarketRegime.UNKNOWN: None,
        }

class AdvancedStrategy(MainStrategy):
    """Multi-regime adaptive trading strategy."""
    
    def __init__(self):
        

        self.regime_detector = RegimeDetector2(
            # lookback=100,        # 100-bar window for metrics
            # memory_window=500    # 500-bar historical comparison
        )
        
        self.strategies = RegimeToStrategyMapping.get_mapping()

        # Calculate required buffer size
        strategy_requirements = [
            strategy.get_required_periods() 
            for strategy in self.strategies.values() 
            if strategy is not None
        ]
        regime_requirement = self.regime_detector.get_required_bars()
        
        self.required_bars = max(
            max(strategy_requirements) if strategy_requirements else 0,
            regime_requirement
        )
        
        # Set the data rolling buffer size
        self.data_buffer = RollingDataBuffer(self.required_bars + 100)  # Add margin

        # max_buffer = max(
        #     [strategy.get_required_periods() for strategy in self.strategies.values()]
        #     )  
        # self.price_buffer = RollingDataBuffer(max_buffer)
        # self.volume_buffer = RollingDataBuffer(max_buffer)
        
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
        if self.data_buffer.get_size() < self.required_bars:
            logger.debug(
                f"⏳ Warming up: {self.data_buffer.get_size()}/{self.required_bars} bars"
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
            # self.price_buffer.add(data['close'].iloc[-1])
            # self.volume_buffer.add(data['volume'].iloc[-1])
            
            # Convert row to dict
            bar_dict = new_bar.iloc[-1].to_dict()
            self.data_buffer.add(bar_dict)

            logger.debug(f"✅ Buffer updated: {self.data_buffer.get_size()} bars")
        except Exception as e:
            logger.error(f"Error updating buffers: {e}")
        
        # Get rolling window
        window = self.data_buffer.get_dataframe()
        
        #Update regime detector using data_buffer
        try: 
            self.regime_detector.update_regime_metrics(window)
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
        self.current_regime  = self.regime_detector.classify_regime()

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
                logger.info(f"   ⛔ NO STRATEGY for {self.current_regime.value}")
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
                'bars_in_regime': self.regime_detector.bars_in_current_regime
            }
            
            return (forecast, None, self.current_regime, 0.0, debug_info)
        
        # STRATEGY - Check if active strategy is ready 
        # Note: Should be always ready due to is_ready check in MainStrategy(ABC)
        if not primary_strategy.is_ready():
            logger.error(
                f"⚠️  Unexpected ! Active strategy {primary_strategy.name} not ready "
                f"(needs {primary_strategy.get_required_periods()} bars)"
            )
            
            forecast = 0.0
            forecast_delta = forecast - self.last_forecast
            self.last_forecast = forecast

            debug_info = {
                'regime': self.current_regime.value,
                'status': 'strategy_not_ready',
                'strategy_name': primary_strategy.name
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

class WeightedComponentStrategy(CompositeStrategy):
    """
    Mean reversion strategy with momentum confirmation.
    Combines MA divergence + momentum confirmation via weighted ensemble.
    """
    
    def __init__(self,
                 ma_weight: float = 1,
                 momentum_weight: float = 0): #Weight array as class input with weight retrieval (get) , with array weight normalization to 1, 
        
        components = [
            MADivergenceComponent(
                name="MA Divergence 20/50 div 0.3% Scale 8.0",
                weight=ma_weight,
                parameters={'fast_period': 20, 'slow_period': 50, 'min_divergence': 0.3, 'scaling_factor': 8.0}
            ),
            MomentumConfirmationComponent(
                name="MomentumConfirmation 3/10",
                weight=momentum_weight,
                parameters={'short_period': 3, 'long_period': 10}
            )
        ]
        
        super().__init__(components, name="WeightedComponentStrategy")


# >>>>>>>>>>> Component implementations <<<<<<<<<<<


# ============================================================================
# COMPONENT 1: MA DIVERGENCE 
# ============================================================================


class MADivergenceComponent(SubStrategyComponent):
    """
    Detects when price is stretched from moving average.
    Generates mean reversion signal (inverted).
    """
    
    def __init__(self,
                 name: str = "MADivergence",
                 weight: float = 0.7,
                 parameters: Optional[Dict[str, Any]] = {},
                 ):
        super().__init__(name, weight, parameters)

        self.fast_period = parameters.get('fast_period', 20)
        self.slow_period = parameters.get('slow_period', 50)
        self.min_divergence = parameters.get('min_divergence', 0.3)
        self.scaling_factor = parameters.get('scaling_factor', 8.0)

        self.fast_ma = None
        self.slow_ma = None
        self.divergence_pct = None

        logger.info(f"   ├─ {name}: MA {self.fast_period}/{self.slow_period}, "
                   f"min_div={self.min_divergence}%, scale={self.scaling_factor}")

    def update(self, data: pd.DataFrame):
        """Calculate MA divergence."""
        self.data = data
        
        if len(data) >= self.slow_period:
            close_prices = data['close'].values
            self.fast_ma = np.mean(close_prices[-self.fast_period:])
            self.slow_ma = np.mean(close_prices[-self.slow_period:])
            
            if self.slow_ma != 0:
                self.divergence_pct = ((self.fast_ma / self.slow_ma) - 1) * 100
            else:
                self.divergence_pct = 0.0
    
    def is_ready(self) -> bool:
        """Check if enough data."""
        if self.data is None:
            return False
        return len(self.data) >= self.slow_period
    
    def generate_forecast(self) -> ComponentOutput:
        """
        Generate mean reversion forecast based on MA divergence.
        INVERTED: Large positive divergence → SHORT signal
        """
        
        if not self.is_ready() or self.divergence_pct is None:
            return 0.0, {'error': 'not_ready'}
        
        # Apply minimum threshold
        if abs(self.divergence_pct) < self.min_divergence:
            forecast = 0.0
        else:
            # INVERTED signal for mean reversion
            raw_forecast = -self.divergence_pct * self.scaling_factor
            
            # Apply dampening for weak signals
            if abs(raw_forecast) < 5:
                raw_forecast *= 0.5
            
            forecast = np.clip(raw_forecast, -20, 20)

        confidence = 20

        debug_info = {
            'fast_ma': float(self.fast_ma),
            'slow_ma': float(self.slow_ma),
            'divergence_pct': float(self.divergence_pct),
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
        return self.slow_period


# ============================================================================
# COMPONENT 2: MOMENTUM CONFIRMATION
# ============================================================================

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



# ============================================================================
# COMPONENT 3: BUY AND HOLD STRATE
# ============================================================================

class BuyAndHoldStrategy(SubStrategyComponent):
    """
    Simple buy-and-hold strategy.
    """
    
    def __init__(self,
                 weight: float = 1.0,
                 name: str = "BuyAndHold", 
                 parameters: Optional[Dict[str, Any]] = {},):
        super().__init__(name, weight, parameters=parameters)
        logger.info(f"   ├─ {name}: Buying and holding")

    def update(self, data: pd.DataFrame):
        """No update needed for buy-and-hold."""
        pass

    def is_ready(self) -> bool:
        """Check if enough data."""
        return True  # Always ready
    
    def generate_forecast(self) -> Tuple[float, Dict[str, Any]]:
        """
        Generate buy-and-hold forecast.
        """
        
        if not self.is_ready():
            return 0.0, {'error': 'not_ready'}
        
        # Buy
        forecast = 20.0  # Strong LONG signal
        confidence = None
        debug_info = {}
        
        return ComponentOutput(
            forecast=float(forecast),
            confidence=confidence,
            componentName=self.name,
            parameters=self.parameters,
            weight=self.weight,
            debug_info=debug_info
        )    
    def get_required_periods(self) -> int:
        return 0


# ============================================================================
# SubStrat - Template of Strategy
# ============================================================================

class PlaceHolderStrategy(SubStrategyComponent):
    """
    Strategy with forecast at 20
    """
    
    def __init__(self, name: str = "placeholder_strategy"):
        super().__init__(name)
        self.n=0

    def update(self, data: pd.DataFrame):
        self.n+=1
        return 

    def is_ready(self):
        return self.n > 10

    def generate_forecast(self) -> Tuple[float, float, Dict[str, Any]]:
        """Generate forecast based on MA crossover strength."""
        
        forecast = 20
        confidence = 0
        
        debug = {
            'forecast': 20
        }

        return forecast, confidence, debug

    def get_required_periods(self) -> int:
        """For now static, can be dynamically calculated from indicators used"""
        return 10     