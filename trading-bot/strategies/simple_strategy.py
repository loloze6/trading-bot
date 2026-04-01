from strategies.strategy_base import (
    SubStrategyComponent,
    CompositeStrategy,
    CompositeStrategyForRegime,
    MainStrategy,
    StrategyOutput,
    MarketRegime,
    RegimeMetrics,
    ComponentOutput,
    RollingBuffer
)
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from abc import ABC, abstractmethod
import logging
import numpy as np
from collections import deque
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere

class WeightedComponentRegimeDetector(CompositeStrategyForRegime):
    """
    Regime Detector utilizing smoothed inputs to prevent state whipsawing.
    """
    def __init__(self):


        components = [
            EfficiencyRatioComponent(
                name="ER_14_Smooth5", 
                weight=0.5, 
                parameters={'period': 14, 'smooth_period': 5}
            ),
            VolatilityPercentileComponent(
                name="VolRank_14_100_Smooth5", 
                weight=0.5, 
                parameters={'vol_period': 14, 'lookback_period': 100, 'smooth_period': 5}
            )
        ]
        super().__init__(components, name="RegimeDetector")

        # TIGHTENED HYSTERESIS THRESHOLDS (Faster response, relying on EMA to kill noise)
        self.er_trend_enter = 0.25     
        self.er_trend_exit = 0.18      
        self.vol_chop_enter = 0.40     
        self.vol_chop_exit = 0.50      

        logger.info(f"🔧 Smoothed 3-State RegimeDetector initialized")

    def classify_regime(self) -> Tuple[MarketRegime, Dict[str, Any]]:
        if not self.is_ready():
            return MarketRegime.UNKNOWN, {}

        self.previous_regime = self.current_regime
        forecast_regime, confidence_regime, debug_info = self.generate_forecast()
        
        try:
            er = debug_info['components']['ER_14_Smooth5']['er_smoothed']
            vol_rank = debug_info['components']['VolRank_14_100_Smooth5']['vol_percentile_smoothed']
        except KeyError as e:
            logger.error(f"Regime metrics missing: {e}")
            return self.current_regime, debug_info

        new_regime = self.current_regime

        if self.current_regime == MarketRegime.TRENDING:
            if er < self.er_trend_exit:
                new_regime = MarketRegime.UNKNOWN
        elif self.current_regime == MarketRegime.CHOP:
            if vol_rank > self.vol_chop_exit:
                new_regime = MarketRegime.UNKNOWN
        elif self.current_regime == MarketRegime.MEAN_REVERSION:
            if er >= self.er_trend_enter:
                new_regime = MarketRegime.TRENDING
            elif vol_rank <= self.vol_chop_enter:
                new_regime = MarketRegime.CHOP

        if new_regime == MarketRegime.UNKNOWN:
            if er >= self.er_trend_enter:
                new_regime = MarketRegime.TRENDING
            elif vol_rank <= self.vol_chop_enter:
                new_regime = MarketRegime.CHOP
            else:
                new_regime = MarketRegime.MEAN_REVERSION

        self.current_regime = new_regime
        debug_info['regime_metrics'] = {'er_smoothed': er, 'vol_rank_smoothed': vol_rank}
        
        self.track_regime_change(forecast_regime, debug_info)

        return self.current_regime, debug_info

class RegimeToStrategyMapping():
    """Mapping of market regimes to sub-strategies."""
    @staticmethod 
    def get_mapping():
        return {
            MarketRegime.TRENDING: WeightedComponentStrategy(
                name="BuyHold",
                compo1_weight=0,
                compo3_weight=1.0
            ),
            MarketRegime.MEAN_REVERSION: WeightedComponentStrategy(
                name="BuyHold",
                compo1_weight=0,
                compo2_weight=0,
                compo3_weight=1.0),
            MarketRegime.CHOP: WeightedComponentStrategy(
                name="BuyHold",
                compo1_weight=0,
                compo2_weight=0,
                compo3_weight=1.0),
            MarketRegime.UNKNOWN: WeightedComponentStrategy(
                name="BuyHold",
                compo1_weight=0,
                compo2_weight=0,
                compo3_weight=1.0),
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


# >>>>>>>>>>> Component implementations <<<<<<<<<<<

# ============================================================================
# COMPONENT : BUY AND HOLD STRATE 
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
# COMPONENT : PRICE PERCENTAGE INDICATOR 
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
# COMPONENT DIVERGENCE CHECK BETWEEN MA INDICATOR 
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
# COMPONENT VOLATILITY INDICATOR 
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
# COMPONENT EMA differences 
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

# ============================================================================
# COMPONENT Kaufman's Efficiency Ratio
# ============================================================================

class EfficiencyRatioComponent(SubStrategyComponent):
    """
    Calculates Smoothed Kaufman's Efficiency Ratio (ER).
    """
    def __init__(self, name: str = "Smoothed_ER", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 14)  # Shortened from 20 to reduce lag
        self.smooth_period = self.parameters.get('smooth_period', 5) # EMA smoothing
        self.standardized_forecast = False 
        self.er_history = []

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            
            raw_change = abs(close[-1] - close[-(self.period + 1)])
            path_length = np.sum(np.abs(np.diff(close[-(self.period + 1):])))
            
            raw_er = raw_change / path_length if path_length != 0 else 0.0
            self.er_history.append(raw_er)
            
            # Keep history manageable
            if len(self.er_history) > self.smooth_period * 3:
                self.er_history.pop(0)
                
            # Apply EMA smoothing to the ER
            er_series = pd.Series(self.er_history)
            smoothed_er = er_series.ewm(span=self.smooth_period, adjust=False).mean().iloc[-1]
            
            self.basic_forecast = smoothed_er * 10 
            self.store_raw_forecast(self.basic_forecast)
            
            self.confidence = 1.0
            self.debug_info = {'er_smoothed': float(smoothed_er)}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period + 1

    def get_required_periods(self) -> int:
        return self.period + 1

# ============================================================================
# COMPONENT Percentile rank of current volatility
# ============================================================================

class VolatilityPercentileComponent(SubStrategyComponent):
    """
    Calculates the Smoothed percentile rank of current volatility.
    """
    def __init__(self, name: str = "Smoothed_VolRank", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = self.parameters.get('vol_period', 14) # Shortened from 20
        self.lookback_period = self.parameters.get('lookback_period', 100)
        self.smooth_period = self.parameters.get('smooth_period', 5)
        self.standardized_forecast = False
        self.rank_history = []

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            
            total_lookback = self.lookback_period + self.vol_period
            rets = np.diff(close[-total_lookback:]) / close[-total_lookback+1:]
            
            vols = pd.Series(rets).rolling(self.vol_period).std().dropna().values
            current_vol = vols[-1]
            
            if len(vols) > 0:
                raw_percentile = np.sum(vols <= current_vol) / len(vols)
            else:
                raw_percentile = 0.5
                
            self.rank_history.append(raw_percentile)
            if len(self.rank_history) > self.smooth_period * 3:
                self.rank_history.pop(0)
                
            rank_series = pd.Series(self.rank_history)
            smoothed_rank = rank_series.ewm(span=self.smooth_period, adjust=False).mean().iloc[-1]
                
            self.basic_forecast = smoothed_rank * 10
            self.store_raw_forecast(self.basic_forecast)
            
            self.confidence = 1.0
            self.debug_info = {'vol_percentile_smoothed': float(smoothed_rank)}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.lookback_period + self.vol_period

    def get_required_periods(self) -> int:
        return self.lookback_period + self.vol_period

