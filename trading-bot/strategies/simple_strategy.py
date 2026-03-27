from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import logging
import numpy as np
from collections import deque
from dataclasses import dataclass
from enum import Enum


logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere

@dataclass
class ComponentOutput:
    """Output from any component - standardized format."""
    forecast: float  # -20 to +20
    confidence: float  # 0 to 1 (how confident are we?)
    componentName: str  # Active strategy
    parameters: Dict[str, Any]  # Parameters used
    weight: float  # Weight of the component in ensemble
    debug_info: Dict[str, Any]  # For logging and analysis

@dataclass
class StrategyOutput:
    """Output from any strategy - standardized format."""
    forecast: float  # -20 to +20
    confidence: float  # 0 to 1 (how confident are we?)
    regime: str  # What market condition did we detect?
    strategy: Optional[Any]  # Active strategy
    debug_info: Dict[str, Any]  # For logging and analysis


    def __post_init__(self):
        """Ensure values are in valid ranges."""
        self.forecast = np.clip(self.forecast, -20, 20)
        self.confidence = np.clip(self.confidence, 0.0, 1.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for backwards compatibility."""
        return {
            'forecast': self.forecast,
            'confidence': self.confidence,
            'regime': self.regime,
            'strategy': self.strategy,
            'debug_info': self.debug_info
        }
    
    def get(self, key: str, default=None):
        """Dict-like access for backwards compatibility."""
        return getattr(self, key, default)

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

# >>>>>>>> Below base strategy from more granular to main strategy <<<<<<<<

class SubStrategyComponent(ABC):
    """
    Base class for sub-strategy components.
    Each component generates a forecast independently.
    """
    
    def __init__(self, name: str, weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        self.name = name
        self.weight = weight
        self.parameters = parameters if parameters is not None else {}
        self.standardized_forecast = self.parameters.get('standardized_forecast', True)
        self.data = None


        #For standardization setup
        self.rolling_forecast = RollingBuffer(9999999)
        self.standardization_ready = 50
        self.standardization_count = 0

        #For standardization per mean
        self.rolling_forecast.register_indicator('raw_forecast_mean', 
        
                                                 lambda df: df['raw_forecast'].mean())
        #For standardization per period
        self.standardized_forecast_per_time = self.parameters.get('standardized_forecast_per_time', False)
        self.standardize_target_prob = 0.2
        self.rolling_forecast.register_indicator('raw_forecast_abs_q_target',
                                                 lambda df: df['raw_forecast'].abs().quantile(1.0 - self.standardize_target_prob))
        
        
        self.basic_forecast = 0.0
        self.confidence = 0.0
        self.debug_info = {}
        
        self.active = True
        self.performance_window = 50
        self.recent_performance = []

    @abstractmethod
    def is_ready(self) -> bool:
        """Check if component has enough data."""
        pass

    def is_ready_with_standardization(self) -> bool:
        return self.is_ready() and self.standardization_count > self.standardization_ready
        

    @abstractmethod
    def update(self, data: pd.DataFrame):
        """Update component with new data."""
        pass
    
    def generate_forecast(self) -> ComponentOutput:
        if not self.is_ready():
            return ComponentOutput(0.0, 0.0, self.name, self.parameters, self.weight, {'error': 'not_ready'})
        
        if self.standardized_forecast:
            if self.is_ready_with_standardization():
                forecast = self.standardize_forecast(self.basic_forecast)
                if self.standardized_forecast_per_time: logger.debug(f"{self.name} // Forecast period standardized return: {forecast}") 
                else: logger.debug(f"{self.name} // Forecast mean standardized return: {forecast}")  
            else:
                logger.info(f"✅ {self.name} Standardization heating so no forecast ({self.standardization_count}/{self.standardization_ready})")
                return ComponentOutput(0.0, 0.0, self.name, self.parameters, self.weight, {'error': 'not_ready'})
        else: 
            forecast = self.basic_forecast
            logger.info(f"{self.name} // Forecast non-standardized return : {forecast}")
        return ComponentOutput(
            forecast=float(forecast),
            confidence=float(self.confidence),
            componentName=self.name,
            parameters=self.parameters,
            weight=self.weight,
            debug_info=self.debug_info
        )
    
    @abstractmethod
    def get_required_periods(self) -> int:
        """Minimum data periods required. As every strategy has updates functions based on data requiring specific data lenght"""
        pass

    def store_raw_forecast(self, forecast) -> int:
        """Store raw forecast for standardization of forecast output."""
        raw_forecast = forecast/(self.data['stddev_24'].iloc[-1] * self.data['close'].iloc[-1])
        self.rolling_forecast.add_data({'raw_forecast': abs(raw_forecast)})
        self.standardization_count += 1

        #For checking
        if self.standardization_count > self.standardization_ready:
            self.rolling_forecast.add_data({"outbound_standardized_forecast_history": abs(self.standardize_forecast(forecast, bound=False))})
            self.rolling_forecast.add_data({"standardized_forecast_history": abs(self.standardize_forecast(forecast))})
            
            
            df = self.rolling_forecast.get_df()
            forecast_mean = df['outbound_standardized_forecast_history'].mean()
            forecast_above_threshold=df['outbound_standardized_forecast_history'].abs() > 10
            prob_above_threshold = forecast_above_threshold.mean() * 100  # e.g. 21.3%
            if self.standardized_forecast_per_time: logger.debug(f"✅ {self.name} raw forecast stored (forecast_prob : {prob_above_threshold}%)")
            else: logger.debug(f"✅ {self.name} raw forecast stored (forecast_mean : {forecast_mean})")
        
        else: logger.info(f"✅ {self.name} Standardization heating so no check ({self.standardization_count}/{self.standardization_ready})")
        
        return raw_forecast

    def standardize_forecast(self, forecast, bound=True) -> int:
        """Store raw forecast for standardization of forecast output."""
        raw_forecast = forecast/(self.data['stddev_24'].iloc[-1] * self.data['close'].iloc[-1])
        

        if self.standardized_forecast_per_time:
            # Use quantile-based scaling
            q = float(self.rolling_forecast['raw_forecast_abs_q_target'])
            # We want |scaled_raw| > 10 with prob ~= target_prob ⇒ 10 sits at that quantile
            forecast_scalar = 10.0 / q
            logger.debug(f"For {self.name} // q={q}, scalar={forecast_scalar}")

        else:
            forecast_scalar = 10 / self.rolling_forecast['raw_forecast_mean']
        
        outbound_standardized_forecast = raw_forecast * forecast_scalar
        

        if bound : 
            standardized_forecast = self.bound_forecast(outbound_standardized_forecast)
            logger.debug(f"{self.name} // Forecast standardized from {raw_forecast} to {standardized_forecast} (before clipping: {outbound_standardized_forecast})")
        else: standardized_forecast = outbound_standardized_forecast

        return standardized_forecast
    
    def bound_forecast(self, forecast) -> int:
        """Clip forecast to valid range."""
        return np.clip(forecast, -20, 20)
    
class CompositeStrategy(SubStrategyComponent):
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
        self.data = data
        
        for component in self.components:
            component.update(data)
        logger.debug(f"✅ Updated Components: {', '.join(comp.name for comp in self.components)}") 

    def is_ready(self) -> bool:
        """Check if all components are ready."""
        if self.data is None:
            return False
        
        return all(comp.is_ready_with_standardization() for comp in self.components)
    
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
        logger.info(f"   🎯 Strategy {self.name} ensemble:")
        for c in component_forecasts:
            logger.info(f"      {c['name']}: {c['forecast']:+.2f} × {c['weight']:.2f} = {c['weighted_contribution']:+.2f}")
        logger.info(f"      Final: {final_forecast:+.2f}")
        
        return float(final_forecast), 0.0, debug_info
    
    def get_required_periods(self) -> int:
        """Return maximum periods required by any component."""
        return max(comp.get_required_periods() for comp in self.components)

class MainStrategy(ABC):
    """Base class of the main strategy handling multiple regimes."""
    
    def __init__(self):

        self.data: Optional[pd.DataFrame] = None
        self.strategies = {
            MarketRegime.UNKNOWN: None
        }
        self.current_regime = MarketRegime.UNKNOWN
    
    @abstractmethod
    def update(self, data: pd.DataFrame):
        pass

    @abstractmethod
    def generate_forecast(self) -> Tuple[ float, # forecast 
                                         Optional[Any], # active strategy object 
                                         MarketRegime, # regime enum 
                                         float, # confidence 
                                         Dict[str, Any] # debug info
                                       ]:        
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """ Must return True only when: 
        - enough data is available 
        - regime detector is ready (if applicable)
        - active strategy is ready """
        pass

    def generate_signals(self) -> StrategyOutput:
        """Main method called by TradingBot. Could be used to modify output and standardize values.""" 
        
        # Check if strategy is ready before generating signals // Note: Might be reundant, each sub-strategy readiness is also checked inside generate_forecast
        if not self.is_ready():
            return StrategyOutput(
                forecast=0.0,
                confidence=0.0,
                regime="NOT_READY",
                strategy=None,
                debug_info={
                    "error": "Strategy not ready",
                    # "strategies_readiness_state": self._get_strategies_readiness()
                }
            )
        
        # Call your custom logic
        try:
            forecast,strategy, regime, confidence, debug = self.generate_forecast()
            return StrategyOutput(
                forecast=forecast,
                confidence=confidence,
                regime=regime.value if hasattr(regime, "value") else regime,
                strategy=strategy.name if strategy else None,
                debug_info=debug
            )
            
        except Exception as e:
            logger.error(f"❌ Error in {self.name}: {e}", exc_info=True)
            return StrategyOutput(
                forecast=0.0,
                confidence=0.0,
                regime="ERROR",
                strategy=None,
                debug_info={"error": str(e)}
            )

    def get_readiness_status(self) -> Dict[str, Any]: #Optional for Logging
        """
        Get detailed readiness status for debugging.
        
        Returns:
            Dict with readiness info for all components
        """
        status = {
            'buffer_size': self.data_buffer.size,
            'required_bars': self.required_bars,
            'buffer_ready': self.data_buffer.size >= self.required_bars,
            'regime_detector_ready': self.regime_detector.is_ready(),
            'regime_detector_bars': self.regime_detector.bars_received,
            'regime_detector_history': len(self.regime_detector.historical_metrics),
            'current_regime': self.current_regime.value,
            'strategies': {}
        } #Note: Not sure if all needed - to simplify ?
        
        for regime, strategy in self.strategies.items():
            if strategy is not None:
                status['strategies'][regime.value] = {
                    'name': strategy.name,
                    'ready': strategy.is_ready(),
                    'required_periods': strategy.get_required_periods()
                }
        
        status['overall_ready'] = self.is_ready()
        
        return status

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

# >>>>>>>> Below strategies modifiable <<<<<<<<


class RegimeToStrategyMapping():
    """Mapping of market regimes to sub-strategies."""
    @staticmethod 
    def get_mapping():
        return {
            MarketRegime.TRENDING: WeightedComponentStrategy(
                name="TrendFollowingStrategy",
                compo1_weight=0.3,
                compo2_weight=0.7
            ),
            MarketRegime.UNKNOWN: WeightedComponentStrategy(
                name="TrendFollowingStrategy",
                compo1_weight=0,
                compo2_weight=0,
                compo3_weight=1.0)
        }

class WeightedComponentStrategy(CompositeStrategy):
    """
    TREND‑FOLLOWING strategy for TRENDING regime.
    
    Combines:
    • PriceEvolutionOnPeriodComponent (70% weight): net trend % → position direction/size
    • MomentumDivergenceComponent (30% weight): short/long alignment → trend strength confirmation
    
    Economic logic:
    - Strong net trend + accelerating momentum → large position in trend direction
    - Strong net trend + decelerating momentum → smaller position
    - Weak trends → neutral forecast
    
    Example: +4% trend + positive alignment → ~+10 forecast → 50% LONG
    
    """
    
    def __init__(self,
                 compo1_weight: float = 1,
                 compo2_weight: float = 0,
                 compo3_weight: float = 0,
                 name="TrendFollowingStrategy"): #Weight array as class input with weight retrieval (get) , with array weight normalization to 1, 
        
        components = [
            PriceEvolutionOnPeriodComponent(           # Your class!   
                name="PriceEvo20",
                weight=compo1_weight,
                parameters={
                    'comparison_period': 20,
                    'scaling_factor': 2.0   # Tune: 1% trend → +2 forecast
                    }
                ),
            MomentumDivergenceComponent(               # Your class!
                name="MomentumDiv5x20",
                weight=compo2_weight,
                parameters={
                    'short_period': 5,
                    'long_period': 20,
                    'scaling_factor': 1.5   # Amplification strength
                    }
                ),
            BuyAndHoldStrategy(               # Your class!
                name="BuyAndHold",
                weight=compo3_weight,
                parameters={
                    "standardized_forecast": False,
                    "standardized_forecast_per_time": False}
                )
            ]
        super().__init__(components, name="WeightedComponentStrategy")




class WeightedComponentRegimeDetector(CompositeStrategy):
    """
    Detects market regimes using RELATIVE comparisons.
    NO fixed thresholds - compares current to recent historical behavior.
    """
    def __init__(self):
        """

        """

        components = [
            PriceEvolutionOnPeriodComponent(
                name="RegimeTrend50",
                weight=0.4,
                parameters={'comparison_period': 50, 
                            "scaling_factor": 1.0,
                            "standardized_forecast": True,
                            "standardized_forecast_per_time": True}  # Stable regime window
            ),
            VolatilityFromStdDevComponent(
                name="RegimeVol20", 
                weight=0.3,
                parameters={'vol_period': 20,
                            "scaling_factor": 1.0,
                            "standardized_forecast": True,
                            "standardized_forecast_per_time": True}  # Short-term volatility
            ),
            EMADiff(
                name="EmaDiff_20_50", 
                weight=0.3,
                parameters={'ST_EMA_period': 20,
                            "LT_EMA_period": 50,
                            "standardized_forecast": True,
                            "standardized_forecast_per_time": True}  # Short-term volatility
            )
        ]
        super().__init__(components, name="RegimeDetector")

        # For Logging - Track regime state
        self.current_regime = MarketRegime.UNKNOWN
        self.previous_regime = MarketRegime.UNKNOWN
        self.regime_change_count = 0
        self.bars_in_current_regime = 0


        logger.info(f"🔧 RegimeDetector initialized")
    
    def classify_regime(self) -> Tuple[MarketRegime, Dict[str, Any]]:
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

        # Get score 
        forecast_regime, confidence_regime, debug_info = self.generate_forecast()
        
        debug_info = {
            'forecast_regime': forecast_regime,
        }
        # ====================================
        # REGIME CLASSIFICATION RULES #COuld be managed as a proper function
        # ====================================
        
        # Favorable: Score >= 4 out of 5
        if forecast_regime  >= 10.0:  # Tune: trend + vol threshold
            self.current_regime = MarketRegime.TRENDING
        
        # Everything else is unknown
        else:
            self.current_regime = MarketRegime.UNKNOWN
        
        # Track regime changes
        self.track_regime_change(forecast_regime, debug_info)

        return self.current_regime, debug_info

    def track_regime_change(self, forecast_regime: float = 0.0, debug_info: Optional[Dict[str, Any]] = None):
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



# >>>>>>>>>>> Component implementations <<<<<<<<<<<

# ============================================================================
# COMPONENT 1: MA DIVERGENCE: fast_period / slow_period / min_divergence / scaling_factor
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
        self.scaling_factor = parameters.get('scaling_factor', 1)



        logger.info(f"   ├─ {name}: MA {self.fast_period}/{self.slow_period}, "
                   f"min_div={self.min_divergence}%, scale={self.scaling_factor}")

    def update(self, data: pd.DataFrame):
        """Calculate MA divergence."""
        self.data = data

        if self.is_ready():
            close_prices = data['close'].values
            fast_ma = np.mean(close_prices[-self.fast_period:])
            slow_ma = np.mean(close_prices[-self.slow_period:])
            divergence_pct = ((fast_ma / slow_ma) - 1) * 100

            self.basic_forecast = -divergence_pct
            self.store_raw_forecast(self.basic_forecast)

            self.confidence = min(abs(divergence_pct) / self.min_divergence, 1.0) * 100
            
            self.debug_info = {
                'basic_forecast': float(self.basic_forecast),
                'fast_ma': float(fast_ma),
                'slow_ma': float(slow_ma),
                }


    def is_ready(self) -> bool:
        """Check if enough data."""
        if self.data is None:
            return False
        return len(self.data) >= self.slow_period
    
        
    def get_required_periods(self) -> int:
        return self.slow_period


# ============================================================================
# COMPONENT 2: MOMENTUM CONFIRMATION: short_period / long_period / scaling_factor
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
        self.scaling_factor = self.parameters.get('scaling_factor', 0)
        
        
        logger.info(f"   ├─ {name}: Comparing {self.short_period}-bar vs {self.long_period}-bar momentum")
    
    def update(self, data: pd.DataFrame):
        """Calculate momentum over different timeframes."""
        self.data = data
        
        if self.is_ready():
            prices = data['close'].values
            
            # Short-term momentum (last 3 bars)
            recent_avg = np.mean(prices[-self.short_period:])
            base_price = prices[-(self.short_period + 1)]
            short_momentum = (recent_avg / base_price - 1) * 100
            
            # Longer-term momentum (last 10 bars)
            longer_avg = np.mean(prices[-self.long_period:])
            base_longer = prices[-(self.long_period + 1)]
            long_momentum = (longer_avg / base_longer - 1) * 100
    
            momentum_divergence = short_momentum - long_momentum

            self.basic_forecast = momentum_divergence
            self.store_raw_forecast(self.basic_forecast)

            self.confidence = min(abs(momentum_divergence) / 0.5, 1.0) * 100  # Tune: 0.5% divergence → full confidence

            self.debug_info = {
                'basic_forecast': float(self.basic_forecast),
                'short_momentum': float(short_momentum),
                'long_momentum': float(long_momentum)
                }

    def is_ready(self) -> bool:
        """Check if enough data."""
        if self.data is None:
            return False
        return len(self.data) >= self.long_period + 1
    
 

    def get_required_periods(self) -> int:
        return self.long_period + 1

# ============================================================================
# COMPONENT 3: BUY AND HOLD STRATE
# ============================================================================

class BuyAndHoldStrategy(SubStrategyComponent):
    """
    Simple buy-and-hold strategy.
    """
    
    def __init__(self, name: str = "BuyAndHold",  weight: float = 1.0, parameters: Optional[Dict[str, Any]] = {},):
        super().__init__(name, weight, parameters=parameters)

    def update(self, data: pd.DataFrame):
        """No update needed for buy-and-hold."""
        self.data = data
        if self.is_ready():
            self.basic_forecast = 10
            self.store_raw_forecast(self.basic_forecast)

            self.confidence = min(abs(10) / 10.0, 1.0)

            self.debug_info = {
                'basic_forecast': float(self.basic_forecast),
            }

    def is_ready(self) -> bool:
        """Check if enough data."""
        return self.data is not None and True
    
 
    def get_required_periods(self) -> int:
        return 0

# ============================================================================
# COMPONENT 4: PRICE PERCENTAGE INDICATOR: comparison_period, scaling_factor
# ============================================================================

class PriceEvolutionOnPeriodComponent(SubStrategyComponent):
    """
    TRENDING REGIME - Primary trend signal generator.
    
    GOAL: Measure net directional momentum over recent window to determine position direction and size.
    
    RATIONALE for TRENDING regime: In trending markets, price tends to continue in the direction
    of its recent net move. This component captures that by measuring percent change comparing to N bars ago
    and scaling directly to forecast (-20 to +20).
    
    Example: +5% move over 20 bars → +10 forecast → 50% LONG allocation.
    
    Parameters:
        comparison_period: bars to measure net trend (shorter = more responsive)
    """
    def __init__(self, name: str = "PriceEvolutionOnPeriodComponent", weight: float = 0.7, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.comparison_period = self.parameters.get('comparison_period', 20)
        self.scaling_factor = self.parameters.get('scaling_factor', 20)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values

            # Percentage of change compared to N bars ago
            trend_pct = (close[-1] - close[-(self.comparison_period+1)]) / close[-(self.comparison_period+1)] * 100

            self.basic_forecast = trend_pct
            self.store_raw_forecast(self.basic_forecast)

            self.confidence = min(abs(trend_pct) / 10.0, 1.0)

            self.debug_info = {
                'basic_forecast': float(self.basic_forecast),
            }
    
    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.comparison_period + 1

    def get_required_periods(self) -> int:
        return self.comparison_period + 1


# ============================================================================
# COMPONENT 5: DIVERGENCE CHECK BETWEEN MA INDICATOR: short_period, long_period
# ============================================================================

class MomentumDivergenceComponent(SubStrategyComponent):
    """
    TRENDING REGIME - Secondary trend confirmation.
    
    GOAL: Confirm primary trend direction by checking if short-term momentum aligns with longer-term trend.
    
    RATIONALE for TRENDING regime: Healthy trends have short-term acceleration in the same direction
    as the longer-term move. Divergence suggests weakening trend → reduce position size.
    
    alignment = short_trend * long_trend:
    - Positive: acceleration (strong trend) → amplify forecast
    - Negative: deceleration (weakening) → dampen forecast
    - Zero: neutral → no change
    
    Parameters:
        short_period: recent momentum (5 bars)
        long_period: background trend (20 bars)
    """
    def __init__(self, name: str = "TrendConfirm5x20", weight: float = 0.3, parameters: Optional[Dict[str, Any]] = {}):
        super().__init__(name, weight, parameters=parameters)

        self.short_period = self.parameters.get('short_period', 5)
        self.long_period = self.parameters.get('long_period', 20)
        self.scaling_factor = self.parameters.get('scaling_factor', 1.5)


    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            short_trend = (close[-1] - close[-self.short_period]) / close[-self.short_period] * 100
            long_trend = (close[-1] - close[-self.long_period]) / close[-self.long_period] * 100
            alignment = float(short_trend * long_trend)
            self.basic_forecast = alignment
            self.store_raw_forecast(self.basic_forecast)

            self.confidence = min(abs(alignment) / 20.0, 1.0)
            
            self.debug_info = {
                'basic_forecast': float(self.basic_forecast),
                'short_trend_pct': float(short_trend),
                'long_trend_pct': float(long_trend)
                }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.long_period

    def get_required_periods(self) -> int:
        return self.long_period


# ============================================================================
# COMPONENT 6: VOLATILITY INDICATOR: vol_period, scaling_factor
# ============================================================================

class VolatilityFromStdDevComponent(SubStrategyComponent):
    """
    Volatility filter based on standard deviation of price returns.

    """
    def __init__(self, name="RegimeVol", weight=0.3, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = self.parameters.get('vol_period', 20)
        self.scaling_factor = self.parameters.get('scaling_factor', 1.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            rets = np.diff(close[-self.vol_period:]) / close[-self.vol_period+1:]
            vol_pct = np.std(rets) * 100
            self.basic_forecast = vol_pct
            self.store_raw_forecast(self.basic_forecast)

            self.confidence = min(vol_pct / 5.0, 1.0)

            self.debug_info = {
                'basic_forecast': float(self.basic_forecast)
                }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.vol_period


    def get_required_periods(self) -> int:
        return self.vol_period
   


# ============================================================================
# COMPONENT 7: EMA differences
# ============================================================================

class EMADiff(SubStrategyComponent):
    """
    Forcast based on ShortVSLong gap

    """
    def __init__(self, name="RegimeVol", weight=0.3, parameters=None):
        super().__init__(name, weight, parameters or {}) 
        self.ST_EMA_period = self.parameters.get('ST_EMA_period', 12)
        self.LT_EMA_period = self.parameters.get('LT_EMA_period', 26)
        #9;26;55; 20;50;200

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values

            ST_EMA = data['close'].ewm(span=self.ST_EMA_period).mean().iloc[-1]
            LT_EMA = data['close'].ewm(span=self.LT_EMA_period).mean().iloc[-1]
            EMA_diff = ST_EMA - LT_EMA

            self.basic_forecast = EMA_diff
            self.store_raw_forecast(self.basic_forecast)

            self.confidence = min(self.basic_forecast / 5.0, 1.0)

            self.debug_info = {
                'basic_forecast': float(self.basic_forecast)
                }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.LT_EMA_period


    def get_required_periods(self) -> int:
        return self.LT_EMA_period
   
  

# >>>>> Below tools/technical_indicators. <<<<<<<<<<

class RollingBuffer:
    def __init__(self, max_size: int = 500):
        self.max_size = max_size
        self.bars = deque(maxlen=max_size)  # O(1) fixed-size FIFO
        self.indicators = {}  # {'stddev_24': lambda df: df['close'].rolling(24).std()}

    def add_data(self, data_dict: dict):
        """Add new bar/data row, auto-update indicators."""
        self.bars.append(data_dict)
        self._update_indicators()

    def register_indicator(self, name: str, func):
        """Register indicator func(df) -> pd.Series."""
        self.indicators[name] = func

    def _update_indicators(self):
        """Lazy recompute all indicators on current df."""
        if not self.bars:
            return
        df = pd.DataFrame(self.bars)
        for name, func in self.indicators.items():
            df[name] = func(df)
        # Update bars with computed df (keep latest indicators)
        self.bars = deque(df.to_dict('records'), maxlen=self.max_size)

    def get_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.bars)

    def __getitem__(self, key):
        df = self.get_df()
        return df[key].iloc[-1] if isinstance(key, str) else df[key]

    @property
    def size(self):
        return len(self.bars)

