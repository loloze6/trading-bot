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
    TRENDING = "trending"                   
    MEAN_REVERSION = "mean_reversion"       
    CHOP = "chop"                           
    UNKNOWN = "unknown"

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

class CompositeStrategyForRegime(CompositeStrategy):
    """
    Composite strategy that combines multiple sub-strategy components for a specific regime.
    Loop on components to 
    - initialize
    - update
    - check readiness
    - generate weighted forecast
    """
    
    def __init__(self, 
                 components: List[SubStrategyComponent],
                 name: str = "CompositeStrategyForRegime"):
        super().__init__(components, name)
        self.current_regime = MarketRegime.UNKNOWN
        self.previous_regime = MarketRegime.UNKNOWN
        self.bars_in_current_regime = 0
        self.regime_change_count = 0

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

