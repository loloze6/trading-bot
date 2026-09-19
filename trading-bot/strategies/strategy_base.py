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
    

class MarketRegime(Enum):
    TRENDING = "trending"                   
    MEAN_REVERSION = "mean_reversion"       
    CHOP = "chop"                           
    UNKNOWN = "unknown"

# >>>>>>>> Below base strategy from more granular to main strategy <<<<<<<<

class StrategyNode(ABC):
    """Minimal shared interface for leaf components and composites."""
    
    def __init__(self, name: str, weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        self.name = name
        self.weight = weight
        self.parameters = parameters if parameters is not None else {}
        self.data = None

    @abstractmethod
    def is_ready(self) -> bool: ...

    def is_ready_with_standardization(self) -> bool:
        """Default: no standardization required. Override in SubStrategyComponent."""
        return self.is_ready()

    @abstractmethod
    def update(self, data: pd.DataFrame): ...

    @abstractmethod
    def generate_forecast(self): ...

    @abstractmethod
    def get_required_periods(self) -> int: ...

class SubStrategyComponent(StrategyNode):
    """
    Base class for sub-strategy components.
    Each component generates a forecast independently.
    """

    #: Aux-feed columns this component reads from the bar DataFrame. Empty by
    #: default; subclasses that consume `data[...]` aux columns override it.
    #: Drives required_feeds() on both engines / AdvancedStrategy and the V1
    #: registration guard in core/backtester.py.
    consumes_feeds: tuple[str, ...] = ()

    def __init__(self, name: str, weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters)
        
        #For standardization setup
        self.rolling_forecast = RollingBuffer(500)
        self.standardization_count = 0
        self.standardization_ready = 50
        self.standardized_forecast = self.parameters.get('standardized_forecast', True)
        self.standardized_forecast_per_time = self.parameters.get('standardized_forecast_per_time', False)

        #For standardization per mean or per period
        self.rolling_forecast.register_calculated_column('raw_forecast_mean', 
            lambda df: df['raw_forecast'].mean())
        self.standardize_target_prob = 0.2
        self.rolling_forecast.register_calculated_column('raw_forecast_abs_q_target',
            lambda df: df['raw_forecast'].abs().quantile(1.0 - self.standardize_target_prob))
        
        
        #Output state
        self.basic_forecast = 0.0
        self.confidence = 0.0
        self.debug_info = {}


    def is_ready_with_standardization(self) -> bool:
        # Components that don't use standardization (e.g. regime detectors with 0-1 scale)
        # are ready as soon as the underlying data check passes.
        if not self.standardized_forecast:
            return self.is_ready()
        return self.is_ready() and self.standardization_count > self.standardization_ready
        
    def generate_forecast(self) -> ComponentOutput:
        if not self.is_ready():
            return ComponentOutput(0.0, 0.0, self.name, self.parameters, self.weight, {'error': 'not_ready'})
        
        if self.standardized_forecast:
            if self.is_ready_with_standardization():
                forecast = self.standardize_forecast(
                    self.basic_forecast,
                    raw_forecast=getattr(self, '_last_raw_forecast', None))
            else:
                logger.debug(f"✅ {self.name} Standardization heating so no forecast ({self.standardization_count}/{self.standardization_ready})")
                return ComponentOutput(0.0, 0.0, self.name, self.parameters, self.weight, {'error': 'not_ready'})
        else: 
            forecast = self.basic_forecast
            #Log only if parameter of logger for trading_refinement is True
            if logger.strategy_refinement : logger.debug(f"{self.name} // Forecast non-standardized return : {forecast}") 
        return ComponentOutput(
            forecast=float(forecast),
            confidence=float(self.confidence),
            componentName=self.name,
            parameters=self.parameters,
            weight=self.weight,
            debug_info=self.debug_info
        )

    def store_raw_forecast(self, forecast) -> int:
        """Store raw forecast for standardization of forecast output."""
        raw_forecast = forecast/(self.data['stddev_24'].iloc[-1] * self.data['close'].iloc[-1])
        self._last_raw_forecast = raw_forecast

        self.standardization_count += 1
        
        row = {'raw_forecast': abs(raw_forecast)}

        #For checking
        if self.standardization_count > self.standardization_ready:
            row['outbound_standardized_forecast_history'] = abs(self.standardize_forecast(forecast, raw_forecast, bound=False))
            row['standardized_forecast_history'] = abs(self.standardize_forecast(forecast, raw_forecast))

        self.rolling_forecast.add_data(row)

        
            # df = self.rolling_forecast.get_df()
            # forecast_mean = df['outbound_standardized_forecast_history'].mean()
            # forecast_above_threshold=df['outbound_standardized_forecast_history'].abs() > 10
            # prob_above_threshold = forecast_above_threshold.mean() * 100  # e.g. 21.3%
            # if self.standardized_forecast_per_time: logger.debug (f"✅ {self.name} raw forecast stored (forecast_prob : {prob_above_threshold}%)")
            # else: logger.debug (f"✅ {self.name} raw forecast stored (forecast_mean : {forecast_mean})")


        if self.standardization_count <= self.standardization_ready:
            logger.debug(f"✅ No storage // {self.name} Standardization heating ({self.standardization_count}/{self.standardization_ready})")

        return raw_forecast

    def standardize_forecast(self, forecast, raw_forecast: Optional[float] = None, bound=True) -> int:
        """Store raw forecast for standardization of forecast output."""
        if raw_forecast is None:
            raw_forecast = forecast / (self.data['stddev_24'].iloc[-1] * self.data['close'].iloc[-1])
            

        if self.standardized_forecast_per_time:
            # Use quantile-based scaling
            q = float(self.rolling_forecast['raw_forecast_abs_q_target'])
            # We want |scaled_raw| > 10 with prob ~= target_prob ⇒ 10 sits at that quantile
            forecast_scalar = 10.0 / q

        else:
            forecast_scalar = 10 / self.rolling_forecast['raw_forecast_mean']
                
        outbound = raw_forecast * forecast_scalar
        
        return self.bound_forecast(outbound) if bound else outbound
    
    def bound_forecast(self, forecast) -> int:
        """Clip forecast to valid range."""
        return np.clip(forecast, -20, 20)

    def raw_value(self) -> float:
        return self._raw_value

class CompositeStrategy(StrategyNode):
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
        
        total_weight = sum(c.weight for c in components)            
        for comp in components:
            comp.weight = comp.weight / total_weight
            logger.debug(f"   • {comp.name}: weight={comp.weight:.2f}")

        
        # Normalize weights        
        logger.debug(f"✅ Strategy initialized with {len(components)} components")

        # #For regime tracking
        # self.current_regime = MarketRegime.UNKNOWN
        # self.previous_regime = MarketRegime.UNKNOWN
        # self.bars_in_current_regime = 0
        # self.regime_change_count = 0
        # self._boom_crash_bars = 0
 
    def update(self, data: pd.DataFrame):
        """Update all components with new data."""
        self.data = data
        for component in self.components:
            component.update(data)

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
            component_output = component.generate_forecast()
            component_forecasts.append({
                'name': component_output.componentName,
                'forecast': component_output.forecast,
                'weight': component_output.weight,
                'weighted_contribution': component_output.forecast * component_output.weight,
                'confidence': component_output.confidence,
                'parameters': component_output.parameters,
            })

            debug_info['components'][component.name] = component_output.debug_info
        
        # Calculate weighted ensemble
        final_forecast = sum(c['weighted_contribution'] for c in component_forecasts)
        
        # Clip to range
        final_forecast = np.clip(final_forecast, -20, 20)
        
        # Add ensemble info to debug
        debug_info['ensemble'] = component_forecasts
        debug_info['final_forecast'] = final_forecast
        
        # Log ensemble
        if logger.strategy_refinement: logger.debug(f"   🎯 Strategy {self.name} ensemble:")
        for c in component_forecasts:
            if logger.strategy_refinement : logger.debug(f"      {c['name']}: {c['forecast']:+.2f} × {c['weight']:.2f} = {c['weighted_contribution']:+.2f}")
        if logger.strategy_refinement : logger.debug(f"      Final: {final_forecast:+.2f}")
        
        return float(final_forecast), 0.0, debug_info
    
    def get_required_periods(self) -> int:
        """Return maximum periods required by any component."""
        return max(comp.get_required_periods() for comp in self.components)

    def track_regime_change(self, forecast_regime: float = 0.0, debug_info: Optional[Dict[str, Any]] = None):
        # Increment bars in regime
        if self.current_regime == self.previous_regime:
            self.bars_in_current_regime += 1
        else:
            # REGIME CHANGE DETECTED
            self.bars_in_current_regime = 1
            self.regime_change_count += 1
            
            logger.debug("=" * 80)
            logger.debug(f"🔄 REGIME CHANGE #{self.regime_change_count}")
            logger.debug(f"   Previous: {self.previous_regime.value}")
            logger.debug(f"   New:      {self.current_regime.value}")
            logger.debug(f"   Score:    {forecast_regime}")
            logger.debug("-" * 80)

        
        # Log periodic status (every 50 bars when no change)
        if self.bars_in_current_regime % 50 == 0:
            logger.debug(
                f"📊 Regime Status: {self.current_regime.value} "
                f"(for {self.bars_in_current_regime} bars, score: {forecast_regime})"
            )

class MainStrategy(ABC):
    """Base class of the main strategy handling multiple regimes."""
    
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


# >>>>> Below tools/technical_indicators. self.rolling_forecast<<<<<<< <<<

class RollingBuffer:
    """Fixed-size bar buffer with lazy indicator computation.

    Design:
      - `bars` deque holds raw bar dicts only (no indicator keys mixed in).
      - Indicators are recomputed lazily on the first `get_df()` / `__getitem__`
        call after any `add_data()`, then cached until the next `add_data()`.
      - `add_data()` is O(1); a full rebuild costs one O(n) DataFrame construction
        per tick regardless of how many components read from the buffer.
    """

    def __init__(self, max_size: int = 500):
        self.max_size = max_size
        self.bars: deque = deque(maxlen=max_size)
        self.indicators: Dict[str, Any] = {}
        self._cached_df: Optional[pd.DataFrame] = None

    def add_data(self, data_dict: dict):
        self.bars.append(data_dict)
        self._cached_df = None  # invalidate cache

    def register_calculated_column(self, name: str, func):
        self.indicators[name] = func
        self._cached_df = None  # invalidate cache

    def get_df(self) -> pd.DataFrame:
        if self._cached_df is None:
            if not self.bars:
                return pd.DataFrame()
            df = pd.DataFrame(self.bars)
            for name, func in self.indicators.items():
                df[name] = func(df)
            self._cached_df = df
        return self._cached_df

    def __getitem__(self, key):
        df = self.get_df()
        return df[key].iloc[-1] if isinstance(key, str) else df[key]

    @property
    def size(self):
        return len(self.bars)

    def clear(self):
        """CUL-271: drop all buffered bars (a large-gap segment split needs the
        strategy to re-warm from scratch rather than blend pre/post-gap data).
        Indicator registrations survive; only accumulated data is dropped."""
        self.bars.clear()
        self._cached_df = None

