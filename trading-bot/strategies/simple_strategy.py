from strategies.strategy_base import (
    SubStrategyComponent,
    CompositeStrategy,
    CompositeStrategyForRegime,
    MainStrategy,
    StrategyOutput,
    MarketRegime,
    ComponentOutput,
    RollingBuffer
)
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import logging
import numpy as np

logger = logging.getLogger("trading_bot")  # Use the logger set up elsewhere

class WeightedComponentRegimeDetector(CompositeStrategyForRegime):
    """
    Multi-Variate Regime Detector utilizing Smoothed ER and Volatility Percentile.
    Maps the market into three distinct states: TRENDING, CHOP, and MEAN_REVERSION.
    """
    def __init__(self):
        components = [
            EfficiencyRatioRegimeComponent(
                name="ER_24_Smooth5", 
                weight=0.5, 
                parameters={'period': 24, 'smooth_period': 5}
            ),
            VolatilityPercentileRegimeComponent(
                name="VolRank_20_100_Smooth5", 
                weight=0.5, 
                parameters={'vol_period': 20, 'lookback_period': 100, 'smooth_period': 5}
            )
        ]
        super().__init__(components, name="RegimeDetector")

        self.current_regime = MarketRegime.UNKNOWN
        self.previous_regime = MarketRegime.UNKNOWN
        self.bars_in_current_regime = 0
        self.regime_change_count = 0

        # LOCKED ER THRESHOLDS (Direction)
        self.er_trend_enter = 0.30  
        self.er_trend_exit = 0.12   

        # LOCKED VOLATILITY THRESHOLDS (Energy)
        self.vol_chop_enter = 0.35  
        self.vol_chop_exit = 0.45   

        logger.info(f"🔧 Multi-Variate RegimeDetector initialized (Synthesis)")

    def classify_regime(self) -> Tuple[MarketRegime, Dict[str, Any]]:
        if not self.is_ready():
            return MarketRegime.UNKNOWN, {}

        self.previous_regime = self.current_regime
        forecast_regime, confidence_regime, debug_info = self.generate_forecast()
        
        try:
            er_smoothed = debug_info['components']['ER_24_Smooth5']['er_smoothed']
            vol_smoothed = debug_info['components']['VolRank_20_100_Smooth5']['vol_percentile_smoothed']
        except KeyError as e:
            logger.error(f"Regime metrics missing: {e}")
            return self.current_regime, debug_info

        new_regime = self.current_regime

        # ====================================
        # 3-STATE MACHINE LOGIC
        # ====================================
        if self.current_regime == MarketRegime.TRENDING:
            # Drop out of trend if efficiency dies
            if er_smoothed < self.er_trend_exit:
                if vol_smoothed <= self.vol_chop_enter:
                    new_regime = MarketRegime.CHOP
                else:
                    new_regime = MarketRegime.MEAN_REVERSION
                    
        elif self.current_regime == MarketRegime.CHOP:
            # Wake up from chop if energy returns or trend explodes
            if er_smoothed >= self.er_trend_enter:
                new_regime = MarketRegime.TRENDING
            elif vol_smoothed > self.vol_chop_exit:
                new_regime = MarketRegime.MEAN_REVERSION
                
        else: # Currently MEAN_REVERSION or UNKNOWN
            # Pick a direction if metrics cross thresholds
            if er_smoothed >= self.er_trend_enter:
                new_regime = MarketRegime.TRENDING
            elif vol_smoothed <= self.vol_chop_enter:
                new_regime = MarketRegime.CHOP

        self.current_regime = new_regime
        debug_info['regime_metrics'] = {
            'er_smoothed': er_smoothed,
            'vol_smoothed': vol_smoothed
        }
        
        self.track_regime_change(forecast_regime, debug_info)

        return self.current_regime, debug_info

class RegimeToStrategyMapping():
    """Mapping of market regimes to sub-strategies."""
    @staticmethod 
    def get_mapping():
        return {
            MarketRegime.TRENDING: WeightedComponentStrategy(
                name="TrendFollowing",
                compo1_weight=1.0
            ),
            MarketRegime.MEAN_REVERSION: None,
            MarketRegime.CHOP: None,
            MarketRegime.UNKNOWN: None,
        }
    
class WeightedComponentStrategy(CompositeStrategy):
    """
    TREND-FOLLOWING strategy mapped exclusively to the TRENDING regime.
    Powered strictly by an isolated Volatility-Adjusted Keltner Breakout.
    """
    def __init__(self, name="TrendFollowingStrategy", compo1_weight: float = 1.0): 
        components = [
            KeltnerBreakoutComponent(  
                name="KeltnerBreakout_20_1.5",
                weight=compo1_weight,
                parameters={
                    'ema_period': 20,
                    'atr_period': 20,
                    'atr_multiplier': 1.5,
                    'scaling_factor': 20.0
                }
            )
        ]
        super().__init__(components, name=name)







    
# >>>>>>>>>>> Component implementations <<<<<<<<<<<

class RSquaredRegimeComponent(SubStrategyComponent):
    """
    Measures linear trend strength using the R-squared (Coefficient of Determination) 
    of closing prices over time. 
    Outputs a value between 0.0 (pure noise/chop) and 1.0 (perfect straight line).
    """
    def __init__(self, name: str = "RSquared_Regime", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 48)  # 48H lookback default
        self.standardized_forecast = False  # Maintain raw 0.0-1.0 scale for thresholding

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            # Get the last 'period' closing prices
            close = data['close'].values[-self.period:]
            
            # Create a time array [0, 1, 2, ..., n-1]
            x = np.arange(self.period)
            
            # Calculate R-squared via Pearson correlation coefficient squared
            correlation_matrix = np.corrcoef(x, close)
            r_squared = correlation_matrix[0, 1] ** 2
            
            self.basic_forecast = r_squared
            
            self.confidence = 1.0
            
            self.debug_info = {
                'r_squared': float(r_squared)
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period

    def get_required_periods(self) -> int:
        return self.period

class EfficiencyRatioRegimeComponent(SubStrategyComponent):
    """
    Measures trend efficiency using Kaufman's Efficiency Ratio (ER).
    Outputs a smoothed value between 0.0 (pure chop) and 1.0 (perfectly directional trend).
    """
    def __init__(self, name: str = "ER_Regime", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        # TWEAK: Increased lookback to 24 hours to capture a full daily cycle
        self.period = self.parameters.get('period', 24)
        self.smooth_period = self.parameters.get('smooth_period', 5)
        self.standardized_forecast = False  # Maintain raw 0.0-1.0 scale
        self.er_history = []

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            
            # Raw ER Math
            raw_change = abs(close[-1] - close[-(self.period + 1)])
            path_length = np.sum(np.abs(np.diff(close[-(self.period + 1):])))
            raw_er = float(raw_change / path_length) if path_length != 0 else 0.0
            
            # Smoothing Logic
            self.er_history.append(raw_er)
            if len(self.er_history) > self.smooth_period * 3:
                self.er_history.pop(0)
                
            er_series = pd.Series(self.er_history)
            smoothed_er = float(er_series.ewm(span=self.smooth_period, adjust=False).mean().iloc[-1])
            
            self.basic_forecast = smoothed_er
            
            self.confidence = 1.0
            
            self.debug_info = {
                'er_raw': raw_er,
                'er_smoothed': smoothed_er
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period + 1

    def get_required_periods(self) -> int:
        return self.period + 1

class VolatilityPercentileRegimeComponent(SubStrategyComponent):
    """
    Calculates the Smoothed percentile rank of current volatility.
    Outputs a value between 0.0 (dead chop) and 1.0 (explosive volatility).
    """
    def __init__(self, name: str = "VolRank_Regime", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = self.parameters.get('vol_period', 20)
        self.lookback_period = self.parameters.get('lookback_period', 100)
        self.smooth_period = self.parameters.get('smooth_period', 5)
        self.standardized_forecast = False
        self.rank_history = []

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            
            # Calculate returns over the necessary total window
            total_lookback = self.lookback_period + self.vol_period
            rets = np.diff(close[-total_lookback:]) / close[-total_lookback+1:]
            
            # Calculate rolling volatility (standard deviation of returns)
            vols = pd.Series(rets).rolling(self.vol_period).std().dropna().values
            current_vol = vols[-1]
            
            # Percentile Rank: How many past vol readings is current vol greater than?
            if len(vols) > 0:
                raw_percentile = float(np.sum(vols <= current_vol) / len(vols))
            else:
                raw_percentile = 0.5
                
            # Smoothing Logic
            self.rank_history.append(raw_percentile)
            if len(self.rank_history) > self.smooth_period * 3:
                self.rank_history.pop(0)
                
            rank_series = pd.Series(self.rank_history)
            smoothed_rank = float(rank_series.ewm(span=self.smooth_period, adjust=False).mean().iloc[-1])
                
            self.basic_forecast = smoothed_rank
            
            self.confidence = 1.0
            self.debug_info = {
                'vol_raw_rank': raw_percentile,
                'vol_percentile_smoothed': smoothed_rank
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.lookback_period + self.vol_period

    def get_required_periods(self) -> int:
        return self.lookback_period + self.vol_period

class PriceEvolutionComponent(SubStrategyComponent):
    """
    TRENDING REGIME - Primary directional alpha generator.
    Measures the net percentage price change over a specific window and scales it into a forecast.
    """
    def __init__(self, name: str = "PriceEvo", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 20)
        self.scaling_factor = self.parameters.get('scaling_factor', 2.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values

            # Calculate net percentage change
            trend_pct = (close[-1] - close[-(self.period + 1)]) / close[-(self.period + 1)] * 100

            # Apply scaling factor for the final basic forecast
            self.basic_forecast = float(trend_pct * self.scaling_factor)
            self.store_raw_forecast(self.basic_forecast)

            self.confidence = 1.0

            self.debug_info = {
                'trend_pct': float(trend_pct),
                'scaling_factor': float(self.scaling_factor),
                'basic_forecast': float(self.basic_forecast)
            }
    
    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period + 1

    def get_required_periods(self) -> int:
        return self.period + 1

class RSIPullbackComponent(SubStrategyComponent):
    """
    HEDGE FOR TRENDING REGIME.
    Acts as a micro mean-reversion filter. When the market is overextended in the 
    direction of the trend, this outputs a contrarian forecast to dampen the primary signal.
    """
    def __init__(self, name: str = "RSIPullback", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 14)
        self.scaling_factor = self.parameters.get('scaling_factor', 0.4) 

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close']
            
            # Calculate Wilder's RSI
            delta = close.diff()
            gain = delta.clip(lower=0).ewm(alpha=1/self.period, adjust=False).mean()
            loss = -delta.clip(upper=0).ewm(alpha=1/self.period, adjust=False).mean()
            
            rs = gain / loss
            rsi_series = 100.0 - (100.0 / (1.0 + rs))
            current_rsi = float(rsi_series.iloc[-1])
            
            if pd.isna(current_rsi):
                current_rsi = 50.0

            # Invert RSI around the 50 midline to create a pullback score.
            # E.g., RSI = 80 (Overbought) -> 50 - 80 = -30 -> * 0.4 = -12.0 forecast
            # E.g., RSI = 30 (Oversold) -> 50 - 30 = +20 -> * 0.4 = +8.0 forecast
            pullback_score = (50.0 - current_rsi) * self.scaling_factor

            self.basic_forecast = float(pullback_score)
            self.store_raw_forecast(self.basic_forecast)
            
            self.confidence = 1.0
            
            self.debug_info = {
                'current_rsi': float(current_rsi),
                'basic_forecast': float(self.basic_forecast)
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period + 1

    def get_required_periods(self) -> int:
        return self.period + 1

class EMASpreadComponent(SubStrategyComponent):
    """
    TRENDING REGIME - Primary Directional Alpha.
    Measures the percentage spread between a Fast EMA and a Slow EMA.
    Provides a smoothed, persistent directional forecast that ignores single-candle noise.
    """
    def __init__(self, name: str = "EMASpread", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.fast_period = self.parameters.get('fast_period', 9)
        self.slow_period = self.parameters.get('slow_period', 21)
        self.scaling_factor = self.parameters.get('scaling_factor', 5.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close']
            
            # Calculate Exponential Moving Averages
            fast_ema = close.ewm(span=self.fast_period, adjust=False).mean().iloc[-1]
            slow_ema = close.ewm(span=self.slow_period, adjust=False).mean().iloc[-1]
            
            # Percentage spread between Fast and Slow EMA
            spread_pct = ((fast_ema - slow_ema) / slow_ema) * 100.0
            
            # Scale the spread into our forecast range
            self.basic_forecast = float(spread_pct * self.scaling_factor)
            self.store_raw_forecast(self.basic_forecast)
            
            self.confidence = 1.0
            
            self.debug_info = {
                'fast_ema': float(fast_ema),
                'slow_ema': float(slow_ema),
                'spread_pct': float(spread_pct),
                'basic_forecast': float(self.basic_forecast)
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.slow_period

    def get_required_periods(self) -> int:
        return self.slow_period

class PriceOverextensionHedgeComponent(SubStrategyComponent):
    """
    HEDGE FOR TRENDING REGIME.
    Measures the Z-Score of the current price relative to a baseline EMA.
    When price deviates too far (exhaustion climax), it outputs a contrarian 
    forecast to dynamically reduce position size and protect profits.
    """
    def __init__(self, name: str = "OverextensionHedge", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 21)
        self.scaling_factor = self.parameters.get('scaling_factor', 2.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close']
            
            # Calculate Baseline EMA and Rolling Standard Deviation
            baseline_ema = close.ewm(span=self.period, adjust=False).mean().iloc[-1]
            rolling_std = close.rolling(window=self.period).std().iloc[-1]
            
            current_price = close.iloc[-1]
            
            # Calculate Z-Score (How many standard deviations is price away from the EMA?)
            if rolling_std > 0:
                z_score = (current_price - baseline_ema) / rolling_std
            else:
                z_score = 0.0
                
            # Invert the Z-Score to create a contrarian hedging force.
            # E.g., Price violently spikes up (Z-Score +3.5) -> Hedge outputs -7.0
            # This dampens the bullish EMA spread, locking in profits.
            hedge_forecast = -float(z_score * self.scaling_factor)
            
            self.basic_forecast = hedge_forecast
            self.store_raw_forecast(self.basic_forecast)
            
            self.confidence = 1.0
            
            self.debug_info = {
                'baseline_ema': float(baseline_ema),
                'z_score': float(z_score),
                'basic_forecast': float(self.basic_forecast)
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period

    def get_required_periods(self) -> int:
        return self.period

class MacroTrendFilterComponent(SubStrategyComponent):
    """
    HEDGE FOR TRENDING REGIME.
    Measures the structural macro trend using a high-timeframe equivalent EMA (e.g., 200-period).
    Outputs a baseline directional forecast to prevent shorting in a macro bull market 
    and prevent longing in a macro bear market.
    """
    def __init__(self, name: str = "MacroTrendFilter", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 200)
        self.scaling_factor = self.parameters.get('scaling_factor', 2.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close']
            
            # Calculate the Macro Baseline
            macro_ema = close.ewm(span=self.period, adjust=False).mean().iloc[-1]
            current_price = close.iloc[-1]
            
            # Percentage distance from Macro EMA
            distance_pct = ((current_price - macro_ema) / macro_ema) * 100.0
            
            # Scale into a baseline forecast
            self.basic_forecast = float(distance_pct * self.scaling_factor)
            self.store_raw_forecast(self.basic_forecast)
            
            self.confidence = 1.0
            
            self.debug_info = {
                'macro_ema': float(macro_ema),
                'distance_pct': float(distance_pct),
                'basic_forecast': float(self.basic_forecast)
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period

    def get_required_periods(self) -> int:
        return self.period

class DonchianBreakoutComponent(SubStrategyComponent):
    """
    TRENDING REGIME - Primary Directional Alpha.
    Measures where the current close sits within the recent N-period High-Low range.
    Zero-lag breakout detection that naturally neutralizes during pullbacks.
    """
    def __init__(self, name: str = "DonchianBreakout", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 48)
        self.scaling_factor = self.parameters.get('scaling_factor', 20.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close']
            
            # Use rolling max/min of close to avoid wick noise, 
            # while mapping the true structural range.
            recent_high = close.rolling(window=self.period).max().iloc[-1]
            recent_low = close.rolling(window=self.period).min().iloc[-1]
            current_price = close.iloc[-1]
            
            if recent_high == recent_low:
                normalized_pos = 0.5  # Dead flat market
            else:
                # Calculate position from 0.0 (Absolute Low) to 1.0 (Absolute High)
                normalized_pos = (current_price - recent_low) / (recent_high - recent_low)
                
            # Shift the oscillator to range between -1.0 and +1.0
            oscillator = (normalized_pos * 2.0) - 1.0
            
            # Scale to forecast (e.g., -20 to +20)
            self.basic_forecast = float(oscillator * self.scaling_factor)
            self.store_raw_forecast(self.basic_forecast)
            
            self.confidence = 1.0
            
            self.debug_info = {
                'recent_high': float(recent_high),
                'recent_low': float(recent_low),
                'oscillator': float(oscillator),
                'basic_forecast': float(self.basic_forecast)
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period

    def get_required_periods(self) -> int:
        return self.period

class VolumeExpansionHedgeComponent(SubStrategyComponent):
    """
    HEDGE FOR TRENDING REGIME.
    Addresses the specific weakness of fakeout LONG breakouts.
    Measures short-term volume against a longer-term baseline.
    If the market pushes higher on declining/weak volume (Bull Trap), 
    this component outputs a contrarian forecast to block the long signal.
    """
    def __init__(self, name: str = "VolumeExpansionHedge", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = self.parameters.get('vol_period', 24)
        self.scaling_factor = self.parameters.get('scaling_factor', 20.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            volume = data['volume'].values
            close = data['close'].values
            
            # Calculate volume baseline
            avg_volume = pd.Series(volume).rolling(window=self.vol_period).mean().iloc[-1]
            current_volume = volume[-1]
            
            # Check micro price direction
            price_change = close[-1] - close[-2]
            
            # We only want to hedge weak LONGs. 
            # If price is up but volume is below average, output a negative forecast.
            if price_change > 0 and current_volume < avg_volume:
                # Calculate how weak the volume is (0.0 to 1.0)
                weakness = 1.0 - (current_volume / avg_volume)
                self.basic_forecast = -float(weakness * self.scaling_factor)
            else:
                self.basic_forecast = 0.0
                
            self.store_raw_forecast(self.basic_forecast)
            self.confidence = 1.0
            
            self.debug_info = {
                'avg_volume': float(avg_volume),
                'current_volume': float(current_volume),
                'basic_forecast': float(self.basic_forecast)
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.vol_period + 1

    def get_required_periods(self) -> int:
        return self.vol_period + 1

class KeltnerBreakoutComponent(SubStrategyComponent):
    """
    TRENDING REGIME - Primary Directional Alpha.
    Uses Volatility-Adjusted Keltner Channels to filter out slow-grind fakeouts.
    Only generates strong forecasts when price forcefully breaks the ATR bands.
    """
    def __init__(self, name: str = "KeltnerBreakout", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.ema_period = self.parameters.get('ema_period', 20)
        self.atr_period = self.parameters.get('atr_period', 20)
        self.atr_multiplier = self.parameters.get('atr_multiplier', 1.5)
        self.scaling_factor = self.parameters.get('scaling_factor', 20.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            high = data['high']
            low = data['low']
            close = data['close']
            
            # Calculate ATR (Average True Range)
            tr1 = high - low
            tr2 = (high - close.shift(1)).abs()
            tr3 = (low - close.shift(1)).abs()
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = true_range.rolling(window=self.atr_period).mean().iloc[-1]
            
            # Calculate Keltner Baseline (EMA)
            baseline_ema = close.ewm(span=self.ema_period, adjust=False).mean().iloc[-1]
            
            # Calculate Keltner Bands
            upper_band = baseline_ema + (self.atr_multiplier * atr)
            lower_band = baseline_ema - (self.atr_multiplier * atr)
            current_price = close.iloc[-1]
            
            # Calculate normalized penetration (-1.0 to 1.0)
            if current_price > baseline_ema:
                # How far toward (or past) the upper band? 1.0 = exactly on upper band
                band_distance = upper_band - baseline_ema
                oscillator = (current_price - baseline_ema) / band_distance if band_distance > 0 else 0
            else:
                # How far toward (or past) the lower band? -1.0 = exactly on lower band
                band_distance = baseline_ema - lower_band
                oscillator = (current_price - baseline_ema) / band_distance if band_distance > 0 else 0
                
            # Cap the oscillator dynamically around the band breaks to prevent infinite scaling
            oscillator = max(-1.2, min(1.2, oscillator))
            
            # Scale to forecast (e.g., -24 to +24, which the backend will clip to -20 to +20)
            self.basic_forecast = float(oscillator * self.scaling_factor)
            self.store_raw_forecast(self.basic_forecast)
            
            self.confidence = 1.0
            
            self.debug_info = {
                'baseline_ema': float(baseline_ema),
                'upper_band': float(upper_band),
                'lower_band': float(lower_band),
                'atr': float(atr),
                'oscillator': float(oscillator),
                'basic_forecast': float(self.basic_forecast)
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= max(self.ema_period, self.atr_period) + 1

    def get_required_periods(self) -> int:
        return max(self.ema_period, self.atr_period) + 1

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

