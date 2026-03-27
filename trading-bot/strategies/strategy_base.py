# core/strategy_base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import logging
import numpy as np
from collections import deque
from dataclasses import dataclass
from enum import Enum
from strategies.regime_detector import  MarketRegime

logger = logging.getLogger("trading_bot.strategies")


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
            'buffer_size': self.data_buffer.get_size(),
            'required_bars': self.required_bars,
            'buffer_ready': self.data_buffer.get_size() >= self.required_bars,
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

class RollingDataBuffer:
    """Stores OHLCV bars and returns as DataFrame."""
    
    def __init__(self, max_size: int):
        self.max_size = max_size
        # self.rw: deque[float] = deque(maxlen=max_size)  # Fixed-size deque
        self.data = []  # List of dicts: [{timestamp, open, high, low, close, volume}, ...]

    # def add(self, item: float) -> None:
    #     """Adds new data, removing oldest if full"""
    #     self.rw.append(item)

    def add(self, bar: Dict[str, Any]):
        """Add new bar (as dict)."""
        self.data.append(bar)
        if len(self.data) > self.max_size:
            self.data.pop(0)

    def get_size(self) -> int:
        """Return current buffer size."""
        return len(self.data)
    
    # def get_series(self, x: Optional[int] = None) -> pd.Series:
    #     """Retrieves data as a Pandas Series, optionally returning last X elements"""
    #     return pd.Series(list(self.rw)[-x:] if x else list(self.rw))
    
    def get_dataframe(self) -> pd.DataFrame:
        """Return all bars as DataFrame."""
        return pd.DataFrame(self.data)
    
    def is_full(self) -> bool:
        """Check if buffer is at capacity."""
        return len(self.data) >= self.max_size
    
    # def get_data(self, x: Optional[int] = None) -> float:
    #     """Retrieves the most recently added element"""
    #     return self.data[-x] if x else self.data[-1]

    """Utility class for calculating technical indicators."""
    
    @staticmethod
    def add_moving_averages(df: pd.DataFrame, windows: List[int]) -> pd.DataFrame:
        """
        Add simple moving averages to dataframe.
        
        Args:
            df: DataFrame with price data
            windows: List of periods for moving averages
            
        Returns:
            DataFrame with added moving average columns
        """
        df_copy = df.copy()
        for window in windows:
            df_copy[f'sma_{window}'] = df_copy['close'].rolling(window=window).mean()
        return df_copy
    
    @staticmethod
    def add_exponential_moving_averages(df: pd.DataFrame, windows: List[int]) -> pd.DataFrame:
        """
        Add exponential moving averages to dataframe.
        
        Args:
            df: DataFrame with price data
            windows: List of periods for moving averages
            
        Returns:
            DataFrame with added EMA columns
        """
        df_copy = df.copy()
        for window in windows:
            df_copy[f'ema_{window}'] = df_copy['close'].ewm(span=window, adjust=False).mean()
        return df_copy
    
    @staticmethod
    def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """
        Add Relative Strength Index to dataframe.
        
        Args:
            df: DataFrame with price data
            window: RSI calculation period
            
        Returns:
            DataFrame with added RSI column
        """
        df_copy = df.copy()
        delta = df_copy['close'].diff()
        
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        
        rs = avg_gain / avg_loss
        df_copy[f'rsi_{window}'] = 100 - (100 / (1 + rs))
        
        return df_copy
    
    @staticmethod
    def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """
        Add MACD (Moving Average Convergence Divergence) to dataframe.
        
        Args:
            df: DataFrame with price data
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            
        Returns:
            DataFrame with added MACD columns
        """
        df_copy = df.copy()
        
        # Calculate MACD components
        ema_fast = df_copy['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df_copy['close'].ewm(span=slow, adjust=False).mean()
        
        df_copy['macd_line'] = ema_fast - ema_slow
        df_copy['macd_signal'] = df_copy['macd_line'].ewm(span=signal, adjust=False).mean()
        df_copy['macd_histogram'] = df_copy['macd_line'] - df_copy['macd_signal']
        
        return df_copy
    
    @staticmethod
    def add_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: float = 2.0) -> pd.DataFrame:
        """
        Add Bollinger Bands to dataframe.
        
        Args:
            df: DataFrame with price data
            window: Moving average period
            num_std: Number of standard deviations for bands
            
        Returns:
            DataFrame with added Bollinger Bands columns
        """
        df_copy = df.copy()
        
        # Calculate Bollinger Bands
        df_copy['bb_middle'] = df_copy['close'].rolling(window=window).mean()
        df_copy['bb_std'] = df_copy['close'].rolling(window=window).std()
        
        df_copy['bb_upper'] = df_copy['bb_middle'] + (df_copy['bb_std'] * num_std)
        df_copy['bb_lower'] = df_copy['bb_middle'] - (df_copy['bb_std'] * num_std)
        
        # Calculate Bandwidth and %B
        df_copy['bb_bandwidth'] = (df_copy['bb_upper'] - df_copy['bb_lower']) / df_copy['bb_middle']
        df_copy['bb_percent_b'] = (df_copy['close'] - df_copy['bb_lower']) / (df_copy['bb_upper'] - df_copy['bb_lower'])
        
        return df_copy
    
    @staticmethod
    def add_atr(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """
        Add Average True Range to dataframe.
        
        Args:
            df: DataFrame with price data
            window: ATR calculation period
            
        Returns:
            DataFrame with added ATR column
        """
        df_copy = df.copy()
        
        # Calculate True Range
        df_copy['tr1'] = abs(df_copy['high'] - df_copy['low'])
        df_copy['tr2'] = abs(df_copy['high'] - df_copy['close'].shift())
        df_copy['tr3'] = abs(df_copy['low'] - df_copy['close'].shift())
        
        df_copy['true_range'] = df_copy[['tr1', 'tr2', 'tr3']].max(axis=1)
        df_copy[f'atr_{window}'] = df_copy['true_range'].rolling(window=window).mean()
        
        # Drop intermediate columns
        df_copy.drop(['tr1', 'tr2', 'tr3', 'true_range'], axis=1, inplace=True)
        
        return df_copy
    
    @staticmethod
    def add_stochastic_oscillator(df: pd.DataFrame, k_window: int = 14, d_window: int = 3) -> pd.DataFrame:
        """
        Add Stochastic Oscillator to dataframe.
        
        Args:
            df: DataFrame with price data
            k_window: %K period
            d_window: %D period (simple moving average of %K)
            
        Returns:
            DataFrame with added Stochastic Oscillator columns
        """
        df_copy = df.copy()
        
        # Calculate %K
        df_copy['lowest_low'] = df_copy['low'].rolling(window=k_window).min()
        df_copy['highest_high'] = df_copy['high'].rolling(window=k_window).max()
        
        df_copy['%K'] = 100 * ((df_copy['close'] - df_copy['lowest_low']) / 
                              (df_copy['highest_high'] - df_copy['lowest_low']))
        
        # Calculate %D
        df_copy['%D'] = df_copy['%K'].rolling(window=d_window).mean()
        
        # Drop intermediate columns
        df_copy.drop(['lowest_low', 'highest_high'], axis=1, inplace=True)
        
        return df_copy
    
    @staticmethod
    def add_volume_indicators(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        Add volume-based indicators to dataframe.
        
        Args:
            df: DataFrame with price and volume data
            window: Calculation period
            
        Returns:
            DataFrame with added volume indicators
        """
        df_copy = df.copy()
        
        # Volume Moving Average
        df_copy['volume_sma'] = df_copy['volume'].rolling(window=window).mean()
        
        # Money Flow Index
        df_copy['typical_price'] = (df_copy['high'] + df_copy['low'] + df_copy['close']) / 3
        df_copy['money_flow'] = df_copy['typical_price'] * df_copy['volume']
        
        # Determine positive and negative money flow
        df_copy['price_change'] = df_copy['typical_price'].diff()
        df_copy['positive_flow'] = np.where(df_copy['price_change'] > 0, df_copy['money_flow'], 0)
        df_copy['negative_flow'] = np.where(df_copy['price_change'] < 0, df_copy['money_flow'], 0)
        
        # Calculate MFI
        positive_flow_sum = df_copy['positive_flow'].rolling(window=window).sum()
        negative_flow_sum = df_copy['negative_flow'].rolling(window=window).sum()
        
        mf_ratio = positive_flow_sum / negative_flow_sum
        df_copy['mfi'] = 100 - (100 / (1 + mf_ratio))
        
        # Cleanup
        df_copy.drop(['typical_price', 'money_flow', 'price_change', 'positive_flow', 'negative_flow'], 
                    axis=1, inplace=True)
        
        return df_copy