from strategies.strategy_base import (
    SubStrategyComponent,
    ComponentOutput,
)
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import logging
import numpy as np

logger = logging.getLogger("trading_bot")

# >>>>>>>>>>> Component implementations <<<<<<<<<<<

class RSquaredRegimeComponent(SubStrategyComponent):
    """
    Measures linear trend strength using the R-squared (Coefficient of Determination)
    of closing prices over time.
    Outputs a value between 0.0 (pure noise/chop) and 1.0 (perfect straight line).
    """
    def __init__(self, name: str = "RSquared_Regime", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 48)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values[-self.period:]
            x = np.arange(self.period)
            correlation_matrix = np.corrcoef(x, close)
            r_squared = correlation_matrix[0, 1] ** 2
            self._raw_value = r_squared
            self.confidence = 1.0
            self.debug_info = {'r_squared': float(r_squared)}

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
        self.period = self.parameters.get('period', 24)
        self.smooth_period = self.parameters.get('smooth_period', 5)
        self.er_history = []

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            raw_change = abs(close[-1] - close[-(self.period + 1)])
            path_length = np.sum(np.abs(np.diff(close[-(self.period + 1):])))
            raw_er = float(raw_change / path_length) if path_length != 0 else 0.0
            self.er_history.append(raw_er)
            if len(self.er_history) > self.smooth_period * 3:
                self.er_history.pop(0)
            er_series = pd.Series(self.er_history)
            smoothed_er = float(er_series.ewm(span=self.smooth_period, adjust=False).mean().iloc[-1])
            self._raw_value = smoothed_er
            self.confidence = 1.0
            self.debug_info = {'er_raw': raw_er, 'er_smoothed': smoothed_er}

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
                raw_percentile = float(np.sum(vols <= current_vol) / len(vols))
            else:
                raw_percentile = 0.5
            self.rank_history.append(raw_percentile)
            if len(self.rank_history) > self.smooth_period * 3:
                self.rank_history.pop(0)
            rank_series = pd.Series(self.rank_history)
            smoothed_rank = float(rank_series.ewm(span=self.smooth_period, adjust=False).mean().iloc[-1])
            self._raw_value = smoothed_rank
            self.confidence = 1.0
            self.debug_info = {
                'vol_raw_rank': raw_percentile,
                'vol_percentile_smoothed': smoothed_rank
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.lookback_period + self.vol_period

    def get_required_periods(self) -> int:
        return self.lookback_period + self.vol_period

class ADXDirectionalComponent(SubStrategyComponent):
    """
    Regime detector component using ADX Directional Movement Index.
    DI-Ratio = (+DI - -DI) / (+DI + -DI), range [-1, +1].
    During downtrend pauses: -DI stays elevated → |DI-Ratio| > 0.35 → TRENDING maintained,
    blocking the "ER collapse → false RANGING" failure mode. Requires OHLCV (high/low).
    """
    def __init__(self, name: str = "ADX_Directional", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.period = self.parameters.get('period', 24)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            high = data['high'].values
            low = data['low'].values
            close = data['close'].values

            h_diff = np.diff(high)
            l_diff = np.diff(low)
            plus_dm = np.where((h_diff > -l_diff) & (h_diff > 0), h_diff, 0.0)
            minus_dm = np.where((-l_diff > h_diff) & (-l_diff > 0), -l_diff, 0.0)

            tr = np.maximum(
                high[1:] - low[1:],
                np.maximum(np.abs(high[1:] - close[:-1]), np.abs(low[1:] - close[:-1]))
            )

            alpha = 1.0 / self.period
            n = len(tr)
            tr_s = np.zeros(n)
            pdm_s = np.zeros(n)
            mdm_s = np.zeros(n)
            tr_s[0], pdm_s[0], mdm_s[0] = tr[0], plus_dm[0], minus_dm[0]
            for i in range(1, n):
                tr_s[i] = tr_s[i-1] + alpha * (tr[i] - tr_s[i-1])
                pdm_s[i] = pdm_s[i-1] + alpha * (plus_dm[i] - pdm_s[i-1])
                mdm_s[i] = mdm_s[i-1] + alpha * (minus_dm[i] - mdm_s[i-1])

            eps = 1e-10
            plus_di = 100.0 * pdm_s / (tr_s + eps)
            minus_di = 100.0 * mdm_s / (tr_s + eps)

            p_di = float(plus_di[-1])
            m_di = float(minus_di[-1])
            di_sum = p_di + m_di
            di_ratio = float((p_di - m_di) / (di_sum + eps))

            dx = np.abs(plus_di - minus_di) / (plus_di + minus_di + eps) * 100.0
            adx_s = np.zeros(n)
            adx_s[0] = dx[0]
            for i in range(1, n):
                adx_s[i] = adx_s[i-1] + alpha * (dx[i] - adx_s[i-1])

            self._raw_value = di_ratio
            self.confidence = 1.0
            self.debug_info = {
                'adx_value': float(adx_s[-1]),
                'di_ratio': di_ratio,
                'plus_di': p_di,
                'minus_di': m_di,
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.period + 1

    def get_required_periods(self) -> int:
        return self.period + 1

class VarianceRatioComponent(SubStrategyComponent):
    """
    Regime detector component using the Variance Ratio test (Lo-MacKinlay).
    VR(k) = σ²(k) / [k × σ²(1)] on overlapping log returns.
    VR ≥ 1.10 → positive autocorrelation (trending).
    VR ≤ 0.90 → negative autocorrelation (mean-reverting / ranging).
    VR ≈ 1.0 → random walk (trend pause, ambiguous).
    Uses close prices only. Requires window + k bars minimum.
    """
    def __init__(self, name: str = "VR5_100", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.k = self.parameters.get('k', 5)
        self.window = self.parameters.get('window', 100)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values[-(self.window + self.k):]
            log_returns = np.diff(np.log(close))

            var1 = float(np.var(log_returns[-self.window:], ddof=1))

            k_returns = np.array([
                np.sum(log_returns[i:i + self.k])
                for i in range(len(log_returns) - self.k + 1)
            ])
            var_k = float(np.var(k_returns[-self.window:], ddof=1))

            eps = 1e-12
            vr = var_k / (self.k * var1 + eps)

            self._raw_value = vr
            self.confidence = 1.0
            self.debug_info = {'vr5': vr, 'var1': var1, 'var_k': var_k}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.window + self.k

    def get_required_periods(self) -> int:
        return self.window + self.k

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
            trend_pct = (close[-1] - close[-(self.period + 1)]) / close[-(self.period + 1)] * 100
            self._raw_value = float(trend_pct * self.scaling_factor)
            self.confidence = 1.0
            self.debug_info = {
                'trend_pct': float(trend_pct),
                'scaling_factor': float(self.scaling_factor),
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
        self.long_only = self.parameters.get('long_only', False)
        self.entry_threshold = self.parameters.get('entry_threshold', 0.0)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close']
            delta = close.diff()
            gain = delta.clip(lower=0).ewm(alpha=1/self.period, adjust=False).mean()
            loss = -delta.clip(upper=0).ewm(alpha=1/self.period, adjust=False).mean()
            rs = gain / loss
            rsi_series = 100.0 - (100.0 / (1.0 + rs))
            current_rsi = float(rsi_series.iloc[-1])
            if pd.isna(current_rsi):
                current_rsi = 50.0
            pullback_score = (50.0 - current_rsi) * self.scaling_factor
            if self.long_only:
                pullback_score = max(0.0, pullback_score)
            self._raw_value = float(pullback_score)
            self.confidence = 1.0
            self.debug_info = {'current_rsi': float(current_rsi)}

    def generate_forecast(self) -> ComponentOutput:
        output = super().generate_forecast()
        if self.entry_threshold > 0 and abs(output.forecast) < self.entry_threshold:
            return ComponentOutput(0.0, 0.0, self.name, self.parameters, self.weight,
                                   {**output.debug_info, 'threshold_filtered': True})
        return output

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
            fast_ema = close.ewm(span=self.fast_period, adjust=False).mean().iloc[-1]
            slow_ema = close.ewm(span=self.slow_period, adjust=False).mean().iloc[-1]
            spread_pct = ((fast_ema - slow_ema) / slow_ema) * 100.0
            self._raw_value = float(spread_pct * self.scaling_factor)
            self.confidence = 1.0
            self.debug_info = {
                'fast_ema': float(fast_ema),
                'slow_ema': float(slow_ema),
                'spread_pct': float(spread_pct),
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
            baseline_ema = close.ewm(span=self.period, adjust=False).mean().iloc[-1]
            rolling_std = close.rolling(window=self.period).std().iloc[-1]
            current_price = close.iloc[-1]
            if rolling_std > 0:
                z_score = (current_price - baseline_ema) / rolling_std
            else:
                z_score = 0.0
            self._raw_value = -float(z_score * self.scaling_factor)
            self.confidence = 1.0
            self.debug_info = {
                'baseline_ema': float(baseline_ema),
                'z_score': float(z_score),
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
            macro_ema = close.ewm(span=self.period, adjust=False).mean().iloc[-1]
            current_price = close.iloc[-1]
            distance_pct = ((current_price - macro_ema) / macro_ema) * 100.0
            self._raw_value = float(distance_pct * self.scaling_factor)
            self.confidence = 1.0
            self.debug_info = {
                'macro_ema': float(macro_ema),
                'distance_pct': float(distance_pct),
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
            recent_high = close.rolling(window=self.period).max().iloc[-1]
            recent_low = close.rolling(window=self.period).min().iloc[-1]
            current_price = close.iloc[-1]
            if recent_high == recent_low:
                normalized_pos = 0.5
            else:
                normalized_pos = (current_price - recent_low) / (recent_high - recent_low)
            oscillator = (normalized_pos * 2.0) - 1.0
            self._raw_value = float(oscillator * self.scaling_factor)
            self.confidence = 1.0
            self.debug_info = {
                'recent_high': float(recent_high),
                'recent_low': float(recent_low),
                'oscillator': float(oscillator),
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
            avg_volume = pd.Series(volume).rolling(window=self.vol_period).mean().iloc[-1]
            current_volume = volume[-1]
            price_change = close[-1] - close[-2]
            if price_change > 0 and current_volume < avg_volume:
                weakness = 1.0 - (current_volume / avg_volume)
                self._raw_value = -float(weakness * self.scaling_factor)
            else:
                self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {
                'avg_volume': float(avg_volume),
                'current_volume': float(current_volume),
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
            tr1 = high - low
            tr2 = (high - close.shift(1)).abs()
            tr3 = (low - close.shift(1)).abs()
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = true_range.rolling(window=self.atr_period).mean().iloc[-1]
            baseline_ema = close.ewm(span=self.ema_period, adjust=False).mean().iloc[-1]
            upper_band = baseline_ema + (self.atr_multiplier * atr)
            lower_band = baseline_ema - (self.atr_multiplier * atr)
            current_price = close.iloc[-1]
            if current_price > baseline_ema:
                band_distance = upper_band - baseline_ema
                oscillator = (current_price - baseline_ema) / band_distance if band_distance > 0 else 0
            else:
                band_distance = baseline_ema - lower_band
                oscillator = (current_price - baseline_ema) / band_distance if band_distance > 0 else 0
            oscillator = max(-1.2, min(1.2, oscillator))
            self._raw_value = float(oscillator * self.scaling_factor)
            self.confidence = 1.0
            self.debug_info = {
                'baseline_ema': float(baseline_ema),
                'upper_band': float(upper_band),
                'lower_band': float(lower_band),
                'atr': float(atr),
                'oscillator': float(oscillator),
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= max(self.ema_period, self.atr_period) + 1

    def get_required_periods(self) -> int:
        return max(self.ema_period, self.atr_period) + 1

# ============================================================================
# COMPONENT : BUY AND HOLD STRATEGY
# ============================================================================

class BuyAndHoldStrategy(SubStrategyComponent):
    """Simple buy-and-hold strategy."""

    def __init__(self, name: str = "BuyAndHold", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = {}):
        super().__init__(name, weight, parameters=parameters)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            self._raw_value = 10
            self.confidence = 1.0
            self.debug_info = {}

    def is_ready(self) -> bool:
        return self.data is not None

    def get_required_periods(self) -> int:
        return 0

# ============================================================================
# COMPONENT : PRICE PERCENTAGE INDICATOR
# ============================================================================

class PriceEvolutionOnPeriodComponent(SubStrategyComponent):
    """
    TRENDING REGIME - Primary trend signal generator.
    Measures net directional momentum over recent window.
    """
    def __init__(self, name: str = "PriceEvolutionOnPeriodComponent", weight: float = 0.7, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.comparison_period = self.parameters.get('comparison_period', 20)
        self.scaling_factor = self.parameters.get('scaling_factor', 20)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close'].values
            trend_pct = (close[-1] - close[-(self.comparison_period+1)]) / close[-(self.comparison_period+1)] * 100
            self._raw_value = trend_pct
            self.confidence = min(abs(trend_pct) / 10.0, 1.0)
            self.debug_info = {}

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
    Confirms primary trend direction by checking short-term vs long-term momentum alignment.
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
            self._raw_value = alignment
            self.confidence = min(abs(alignment) / 20.0, 1.0)
            self.debug_info = {
                'short_trend_pct': float(short_trend),
                'long_trend_pct': float(long_trend),
            }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.long_period

    def get_required_periods(self) -> int:
        return self.long_period

# ============================================================================
# COMPONENT VOLATILITY INDICATOR
# ============================================================================

class VolatilityFromStdDevComponent(SubStrategyComponent):
    """Volatility filter based on standard deviation of price returns."""

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
            self._raw_value = vol_pct
            self.confidence = min(vol_pct / 5.0, 1.0)
            self.debug_info = {}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.vol_period

    def get_required_periods(self) -> int:
        return self.vol_period

# ============================================================================
# COMPONENT EMA DIFFERENCES
# ============================================================================

class EMADiff(SubStrategyComponent):
    """Forecast based on Short vs Long EMA gap."""

    def __init__(self, name="RegimeVol", weight=0.3, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.ST_EMA_period = self.parameters.get('ST_EMA_period', 12)
        self.LT_EMA_period = self.parameters.get('LT_EMA_period', 26)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            ST_EMA = data['close'].ewm(span=self.ST_EMA_period).mean().iloc[-1]
            LT_EMA = data['close'].ewm(span=self.LT_EMA_period).mean().iloc[-1]
            self._raw_value = ST_EMA - LT_EMA
            self.confidence = min(self._raw_value / 5.0, 1.0)
            self.debug_info = {}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.LT_EMA_period

    def get_required_periods(self) -> int:
        return self.LT_EMA_period


# ============================================================================
# COMPONENT: FUNDING RATE MEAN REVERSION  (H-041-A, Improvement 01)
# edge_source.category: structural_forced_flow
# ============================================================================

class FundingRateMeanReversionComponent(SubStrategyComponent):
    """
    Fires at 8h Binance funding settlement boundaries (UTC hour 0, 8, 16)
    when |funding_rate| > threshold.

    Forecast = -sign(funding_rate) * scaling_factor at active bars; 0 elsewhere.
    Relies on 'funding_rate' column being merged into the bar DataFrame by the
    prescreen loader or data_manager before update() is called.

    threshold=0.0 is a legitimate, intentional design (continuous mode: fire at every
    settlement regardless of magnitude, not just extremes) — NOT an error condition.
    F5a (2026-07-04): this previously raised ZeroDivisionError in the confidence
    calculation whenever threshold=0.0, silently swallowed by main_strategy.update()'s
    broad exception handler, which made every continuous-mode config appear to have
    zero active bars (a bug artifact, not a real "no signal" result — see run_044,
    the F5 fixture for this exact failure).
    """

    def __init__(self, name="FundingMR", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self.threshold = float(params.get("threshold", 0.001))
        self.scaling_factor = float(params.get("scaling_factor", 10.0))
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        if "funding_rate" not in data.columns:
            return

        # Settlement boundary: UTC hour must be divisible by 8
        try:
            ts = pd.Timestamp(data["timestamp"].iloc[-1])
            if ts.hour % 8 != 0:
                return
        except Exception:
            return

        funding_rate = data["funding_rate"].iloc[-1]
        if funding_rate is None or (hasattr(funding_rate, "__float__") and np.isnan(float(funding_rate))):
            return
        funding_rate = float(funding_rate)

        if abs(funding_rate) <= self.threshold:
            return

        # Mean-reversion: negative forecast when funding is positive (longs pay)
        signal = -np.sign(funding_rate) * self.scaling_factor
        self._raw_value = float(np.clip(signal, -20.0, 20.0))
        if self.threshold > 0:
            self.confidence = min(abs(funding_rate) / (self.threshold * 3.0), 1.0)
        else:
            # Continuous mode: no threshold reference to scale "how extreme" against —
            # every settlement bar is an equally legitimate signal instance.
            self.confidence = 1.0
        self.debug_info = {
            "funding_rate": funding_rate,
            "at_settlement": True,
            "raw_signal": signal,
        }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= 2

    def get_required_periods(self) -> int:
        return 2


# ============================================================================
# COMPONENT: FEAR & GREED CONTRARIAN  (H-041-C, Improvement 01)
# edge_source.category: persistent_behavioral_bias
# ============================================================================

class FearGreedContrarianComponent(SubStrategyComponent):
    """
    Contrarian sentiment signal firing at daily boundary bars (UTC hour == 0).
    Uses the previous day's Fear & Greed index value (after +1 day A8.4 shift).

    Fires when fear_greed < fear_threshold (→ long, contrarian against fear) or
    fear_greed > greed_threshold (→ short, contrarian against greed).
    Zero on all other bars.

    Requires 'fear_greed' column merged into bar DataFrame by prescreen loader.
    """

    def __init__(self, name="FGContrarian", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self.fear_threshold = float(params.get("fear_threshold", 25.0))
        self.greed_threshold = float(params.get("greed_threshold", 75.0))
        self.scaling_factor = float(params.get("scaling_factor", 10.0))
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        if "fear_greed" not in data.columns:
            return

        # Signal fires only at the daily boundary bar (UTC midnight)
        try:
            ts = pd.Timestamp(data["timestamp"].iloc[-1])
            if ts.hour != 0:
                return
        except Exception:
            return

        fg = data["fear_greed"].iloc[-1]
        if fg is None or (hasattr(fg, "__float__") and np.isnan(float(fg))):
            return
        fg = float(fg)

        if fg < self.fear_threshold:
            signal = self.scaling_factor          # contrarian: buy into fear
        elif fg > self.greed_threshold:
            signal = -self.scaling_factor         # contrarian: sell into greed
        else:
            return

        self._raw_value = float(np.clip(signal, -20.0, 20.0))
        self.confidence = min(abs(fg - 50.0) / 50.0, 1.0)
        self.debug_info = {
            "fear_greed": fg,
            "at_daily_boundary": True,
            "raw_signal": signal,
        }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= 2

    def get_required_periods(self) -> int:
        return 2
