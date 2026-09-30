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
                # CUL-273: nan_policy="propagate_invalid" (base class default).
                # A NaN RSI (e.g. loss==0 -> rs undefined, or a gap-contaminated
                # window) is a genuinely unmeasurable bar, not "the market is
                # neutral" -- 50.0 was a fabricated value silently indistinguishable
                # from a real, measured neutral reading. Propagate NaN instead;
                # strategy_engine.py::forecast() already refuses to build a
                # forecast from a NaN component value (treats it as not-ready
                # for this bar, same as the existing not_ready_component path).
                self._raw_value = float('nan')
                self.confidence = 0.0
                self.debug_info = {'current_rsi': None, 'nan_policy': 'propagate_invalid'}
                return
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

    consumes_feeds = ("funding_rate",)

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
            # CUL-273: nan_policy="propagate_invalid". This IS a settlement
            # bar (already past the boundary check above) with a genuinely
            # missing/unmeasurable funding print -- a data-quality gap, not
            # "no signal fired." Distinct from the two legitimate 0.0-return
            # cases above/below (non-settlement bar; funding present but under
            # threshold) -- those are real "nothing to report" readings and
            # keep returning 0.0. This one propagates NaN instead of silently
            # reusing the same 0.0 a real non-event would produce.
            self._raw_value = float('nan')
            self.debug_info = {'nan_policy': 'propagate_invalid', 'reason': 'funding_rate_missing_at_settlement'}
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


class FundingRateGradedComponent(SubStrategyComponent):
    """
    Graded sibling of FundingRateMeanReversionComponent (D-051: a forecast
    component must be graded). Every bar:

        raw_value = -funding_rate x 10000

    i.e. the latest funding print in basis points, sign flipped (contrarian:
    negative when longs pay). No threshold and no scaling_factor: the value is
    in natural units and the config's transforms scale it.

    No lookahead: 'funding_rate' is merged onto the bars by a backward as-of
    join, so bar t carries the latest print at or before its timestamp.
    A missing column or a NaN print gives NaN (a data gap, never a fabricated
    0.0 reading).
    """

    consumes_feeds = ("funding_rate",)

    def __init__(self, name="FundingRateGraded", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        if "funding_rate" not in data.columns:
            self._raw_value = float('nan')
            self.debug_info = {'nan_policy': 'propagate_invalid', 'reason': 'funding_rate_column_missing'}
            return

        funding_rate = float(data["funding_rate"].iloc[-1])
        self._raw_value = -funding_rate * 10000.0
        self.confidence = 1.0
        self.debug_info = {"funding_rate": funding_rate}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= 1

    def get_required_periods(self) -> int:
        return 1


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

    consumes_feeds = ("fear_greed",)

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
            # CUL-273: nan_policy="propagate_invalid". This IS the daily
            # boundary bar (already past the check above) with a genuinely
            # missing fear/greed print -- a data-quality gap, not "no signal
            # today." Distinct from the non-boundary-bar 0.0 return above,
            # which is a real "nothing to report" reading, not a gap.
            self._raw_value = float('nan')
            self.debug_info = {'nan_policy': 'propagate_invalid', 'reason': 'fear_greed_missing_at_boundary'}
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


class FearGreedGradedComponent(SubStrategyComponent):
    """
    Graded sibling of FearGreedContrarianComponent (D-051). Every bar:

        raw_value = 50 - fear_greed

    in index points, -50..+50: contrarian, positive in fear (index below 50),
    negative in greed. No thresholds and no scaling_factor: the config's
    transforms scale it.

    No lookahead: 'fear_greed' is merged with the feed's +1 day shift, so a bar
    sees the prior day's published value. A missing column or a NaN value gives
    NaN (a data gap, never a fabricated 0.0 reading).
    """

    consumes_feeds = ("fear_greed",)

    def __init__(self, name="FearGreedGraded", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        if "fear_greed" not in data.columns:
            self._raw_value = float('nan')
            self.debug_info = {'nan_policy': 'propagate_invalid', 'reason': 'fear_greed_column_missing'}
            return

        fg = float(data["fear_greed"].iloc[-1])
        self._raw_value = 50.0 - fg
        self.confidence = 1.0
        self.debug_info = {"fear_greed": fg}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= 1

    def get_required_periods(self) -> int:
        return 1


# ============================================================================
# COMPONENT: MACD HISTOGRAM CROSSOVER  (H-MACD, run_053)
# edge_source.category: persistent_behavioral_bias
# ============================================================================

class MacdHistogramCrossoverComponent(SubStrategyComponent):
    """
    MACD(12,26,9) histogram zero-crossing detector with directional state.

    histogram = (EMA_fast - EMA_slow) - EMA_signal(EMA_fast - EMA_slow)

    Fires +scaling_factor the bar the histogram crosses from <=0 to >0 (bullish),
    -scaling_factor the bar it crosses from >=0 to <0 (bearish), 0 on all other
    bars (event-pulse signal, matching FundingRateMeanReversionComponent /
    FearGreedContrarianComponent convention — activation_rate is meant to be
    measured on these active bars only).

    Existing EMADiff computes only the MACD line (ST_EMA - LT_EMA): no signal
    line, no cross-bar state, no direction. This component adds the signal line
    and a stateful sign comparison against the previous bar's histogram sign,
    which a stateless transform op cannot express.
    """

    def __init__(self, name="MacdHistCrossover", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self.fast_period = int(params.get("fast_period", 12))
        self.slow_period = int(params.get("slow_period", 26))
        self.signal_period = int(params.get("signal_period", 9))
        self.scaling_factor = float(params.get("scaling_factor", 10.0))
        self._raw_value = 0.0
        self._prev_histogram_sign = None  # None until the first ready bar is observed

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        close = data['close']
        fast_ema = close.ewm(span=self.fast_period, adjust=False).mean()
        slow_ema = close.ewm(span=self.slow_period, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()
        histogram = macd_line - signal_line

        current_hist = float(histogram.iloc[-1])
        current_sign = 1 if current_hist > 0 else (-1 if current_hist < 0 else 0)

        crossover_direction = 0
        # Skip the very first observed bar: with no real previous sign, comparing
        # against a placeholder would fabricate a spurious crossover at warm-up.
        if self._prev_histogram_sign is not None:
            if self._prev_histogram_sign <= 0 and current_sign > 0:
                crossover_direction = 1
            elif self._prev_histogram_sign >= 0 and current_sign < 0:
                crossover_direction = -1

        if crossover_direction != 0:
            self._raw_value = float(np.clip(crossover_direction * self.scaling_factor, -20.0, 20.0))
            self.confidence = 1.0
        else:
            self.confidence = 0.0

        self.debug_info = {
            'macd_line': float(macd_line.iloc[-1]),
            'signal_line': float(signal_line.iloc[-1]),
            'histogram': current_hist,
            'crossover_direction': crossover_direction,
        }

        self._prev_histogram_sign = current_sign

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.slow_period + self.signal_period


class MacdHistogramGradedComponent(SubStrategyComponent):
    """
    Graded sibling of MacdHistogramCrossoverComponent (D-051). Every bar:

        macd      = EMA_fast(close) - EMA_slow(close)
        signal    = EMA_signal(macd)
        raw_value = (macd - signal) / close x 100

    the MACD histogram as a percent of the current close (price-free, so it is
    comparable across assets). EMAs use span = period, adjust=False, over the
    bar window the component is given (as the crossover component). Stateless:
    no memory of earlier bars' signs. No scaling_factor: the config's transforms
    scale it.

    No lookahead: every EMA runs over closes up to and including bar t. A NaN
    latest close gives NaN.
    """

    def __init__(self, name="MacdHistogramGraded", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self.fast_period = int(params.get("fast_period", 12))
        self.slow_period = int(params.get("slow_period", 26))
        self.signal_period = int(params.get("signal_period", 9))
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        close = data['close']
        fast_ema = close.ewm(span=self.fast_period, adjust=False).mean()
        slow_ema = close.ewm(span=self.slow_period, adjust=False).mean()
        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()
        histogram = float(macd_line.iloc[-1] - signal_line.iloc[-1])
        last_close = float(close.iloc[-1])

        self._raw_value = histogram / last_close * 100.0
        self.confidence = 1.0
        self.debug_info = {'histogram': histogram, 'close': last_close}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.slow_period + self.signal_period


# ============================================================================
# COMPONENT: SMA TREND, LONG-ONLY (P4_ts_trend, SMA(100)-daily)
# edge_source.category: persistent_behavioral_bias
# ============================================================================

class SmaTrendLongOnlyComponent(SubStrategyComponent):
    """
    Canonical time-series momentum: long (full allocation) when close > SMA(L),
    flat otherwise. Long-only (no shorts) -- this component NEVER outputs a
    negative raw_value. Designed for daily bars per the registered brief
    (lookback_L=100 calendar days, not swept; single fixed formulation, not the
    alternative "trailing L-day return > 0" framing -- that is a separate
    registered trial per the brief's own hypothesis_space note).

    ENGINE LIMITATION (documented, not silently approximated away): the brief
    specifies "execution: next-day open after signal change." This engine's
    ExecutionHandler fills exclusively at the CURRENT bar's close
    (data['close'].iloc[-1], hardcoded throughout execution/execution_handler.py)
    -- there is no next-bar-open fill mode anywhere in the engine. The closest
    faithful approximation without new engine work: this component's raw_value
    at bar T reflects the long/flat state determined from data THROUGH bar
    T-1's close (a one-bar lag), so a crossover detected on day T-1's close
    only takes effect starting day T's processing -- filled at day T's CLOSE,
    not day T's OPEN. This is NOT identical to next-day-open execution (open
    vs close differ, sometimes materially, around gaps) -- see
    pre_registration.yaml's known_engine_caveat for this run.

    standardized_forecast forced False (matching FundingRateMeanReversionComponent
    / FearGreedContrarianComponent / MacdHistogramCrossoverComponent convention):
    this is a binary long/flat state, not a magnitude-scaled correlation signal,
    so generic stddev_24-based normalization does not apply and is skipped
    entirely -- main_strategy.py's std_dev_period is never consulted for this
    component's output.
    """

    def __init__(self, name="SmaTrendLongOnly", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self.lookback_L = int(params.get("lookback_L", 100))
        self.scaling_factor = float(params.get("scaling_factor", 10.0))
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        close = data['close']
        sma = close.rolling(self.lookback_L).mean()

        # One-bar lag (see class docstring "ENGINE LIMITATION") -- use the
        # PRIOR bar's fully-formed close/SMA, not the current bar's, so the
        # signal a bar acts on was already determined before that bar started.
        prior_close = float(close.iloc[-2])
        prior_sma   = float(sma.iloc[-2])
        is_long     = prior_close > prior_sma

        self._raw_value = self.scaling_factor if is_long else 0.0
        self.confidence = 1.0
        self.debug_info = {
            'prior_close': prior_close,
            'prior_sma': prior_sma,
            'is_long': is_long,
        }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.lookback_L + 1   # +1 for the one-bar lag (bar T-1 must be fully formed)


# ============================================================================
# COMPONENT: GATED SMA TREND, LONG-ONLY (P4_ts_trend_r1_er_gate, entry-latch)
# edge_source.category: persistent_behavioral_bias
# ============================================================================

class GatedSmaTrendLongOnlyComponent(SubStrategyComponent):
    """
    SMA(100) long-only trend-following, gated by Kaufman Efficiency Ratio
    ER(er_period) at entry ONLY -- an entry-only LATCH, not a continuous
    regime gate. Built for the P4_ts_trend_r1_er_gate refinement after
    backtest_specification's first attempt (wiring the gate through
    regime_detector/strategies.regimes dispatch) was found to implement a
    continuous ER trailing stop instead: that wiring re-evaluates whether
    ANY forecast is produced every bar based on the CURRENT regime, so an
    ER drop mid-position forced an exit -- a different hypothesis than the
    one registered. This component keeps the gate check confined to the
    single bar it belongs on.

    LATCH SEMANTICS:
    - The gate (ER(er_period) >= gate_threshold) is checked EXACTLY ONCE
      per episode: on the bar the SMA(lookback_L) signal transitions from
      off to on (a fresh cross-up). Internal state (`_in_position`,
      `_prior_signal`) persists across `update()` calls -- the same
      stateful-component pattern already used by
      MacdHistogramCrossoverComponent's prior-histogram-sign tracking.
    - If the gate check on that bar PASSES: the position is latched in
      (`_in_position = True`) and held at `scaling_factor` for every
      subsequent bar the SMA signal remains on, REGARDLESS of what ER does
      afterward. In-position ER changes have no effect -- there is no
      re-check, no early exit, no re-gating while the episode is open.
    - If the gate check on that bar FAILS: the entry is skipped ENTIRELY
      for this episode (output 0). This is NOT a deferred entry -- the
      component does not re-check the gate on a later bar while the SMA
      signal stays on; the only way back in is a fresh off-then-on
      transition (a real cross-down followed by a real cross-up).
    - Exit is the unchanged parent rule: the bar the SMA signal goes off
      (cross-down), `_in_position` clears and output returns to 0 --
      identical to SmaTrendLongOnlyComponent's own exit behavior.

    ER BASIS: Kaufman ER_t(er_period) = abs(close_t - close_{t-n}) /
    sum(abs(close_i - close_i-1)), computed RAW (no smoothing -- unlike
    EfficiencyRatioRegimeComponent's EWM-smoothed regime-detector version;
    the brief's gate_definition specifies the unsmoothed formula), over a
    window ending at the SAME prior bar (T-1) the SMA comparison uses --
    identical one-bar lag, no lookahead, no cross-contamination between the
    two indicators' effective "as-of" bar.

    ENGINE CAVEAT (verbatim from the brief's execution_convention, inherited
    unchanged from SmaTrendLongOnlyComponent -- the gate does not change
    this): "Execution: next-day open after signal change. Engine caveat:
    this backtester fills at bar close, not next-bar open -- see
    strategies/strategy_components.py::SmaTrendLongOnlyComponent's docstring
    for the one-bar-lag approximation actually used; not identical to true
    next-open execution." This component's raw_value at bar T reflects the
    long/flat/gate state determined from data THROUGH bar T-1's close (the
    same one-bar lag), so a signal or gate decision made on day T-1's close
    only takes effect starting day T's processing -- filled at day T's
    CLOSE, not day T's OPEN.

    Parameterized (lookback_L, scaling_factor, er_period, gate_threshold) so
    a separate ER(10) run (S1, the brief's secondary robustness check) can
    reuse this same class with er_period=10 -- a distinct registered trial,
    not a sweep run through this component.
    """

    def __init__(self, name="GatedSmaTrendLongOnly", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self.lookback_L = int(params.get("lookback_L", 100))
        self.scaling_factor = float(params.get("scaling_factor", 10.0))
        self.er_period = int(params.get("er_period", 20))
        self.gate_threshold = float(params.get("gate_threshold", 0.30))
        self._raw_value = 0.0
        self._in_position = False
        self._prior_signal = False  # False until the first computable bar --
                                     # matches SmaTrendLongOnlyComponent/
                                     # MacdHistogramCrossoverComponent's
                                     # "no fabricated transition at warmup" rule

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        close = data['close']
        sma = close.rolling(self.lookback_L).mean()

        # One-bar lag (see class docstring "ENGINE CAVEAT") -- identical
        # convention to SmaTrendLongOnlyComponent: use bar T-1's fully-formed
        # close/SMA, not bar T's.
        prior_close = float(close.iloc[-2])
        prior_sma = float(sma.iloc[-2])
        is_long_signal = prior_close > prior_sma

        # Kaufman ER(er_period), RAW (unsmoothed), same one-bar lag: window
        # ends at the same prior bar (T-1) the SMA comparison uses.
        close_vals = close.values
        er_window = close_vals[-(self.er_period + 2):-1]  # er_period+1 closes ending at T-1
        raw_change = abs(float(er_window[-1]) - float(er_window[0]))
        path_length = float(np.sum(np.abs(np.diff(er_window))))
        prior_er = raw_change / path_length if path_length != 0 else 0.0

        entered_this_bar = False
        gate_rejected_this_bar = False

        if is_long_signal and not self._prior_signal:
            # Transition bar (signal off -> on): the ONLY point the gate is
            # ever evaluated. No deferred entry, no re-check on later bars.
            if prior_er >= self.gate_threshold:
                self._in_position = True
                entered_this_bar = True
            else:
                self._in_position = False
                gate_rejected_this_bar = True
        elif not is_long_signal:
            # Signal-off bar (cross-down, or signal never triggered): flat,
            # latch cleared -- unchanged parent exit rule.
            self._in_position = False
        # else: signal still on, not a transition bar -- _in_position is left
        # exactly as it was (the latch: hold if in, stay skipped if rejected).

        if self._in_position:
            self._raw_value = self.scaling_factor
        else:
            self._raw_value = 0.0
        self.confidence = 1.0

        self.debug_info = {
            'prior_close': prior_close,
            'prior_sma': prior_sma,
            'is_long_signal': is_long_signal,
            'prior_er': prior_er,
            'gate_threshold': self.gate_threshold,
            'in_position': self._in_position,
            'entered_this_bar': entered_this_bar,
            'gate_rejected_this_bar': gate_rejected_this_bar,
        }

        self._prior_signal = is_long_signal

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        # SMA needs lookback_L+1 (one-bar lag); ER needs er_period+2 (er_period+1
        # closes ending at the SAME prior bar, one-bar lag) -- take the binding one.
        return max(self.lookback_L + 1, self.er_period + 2)


# ============================================================================
# COMPONENT: WHALE LARGE-TRADE IMBALANCE  (roadmap Phase 2.3, dispatch W13)
# edge_source.category: structural_forced_flow
# ============================================================================

#: Bar-DataFrame columns this component reads. Both are registered aux-feed
#: names in `data/feed_registry.py::WHALE_FOOTPRINT_FEEDS`, and both live in
#: `RESERVED_FEED_REGISTRY` rather than `FEED_REGISTRY` -- a caller must opt in
#: BY NAME and the campaign_data_policy designation gate still decides
#: (feed_registry.py:51-93). Naming them here creates no read path of its own.
WHALE_LT_IMBALANCE_COLUMN = "whale_lt_imbalance"
WHALE_ATTESTED_COLUMN = "whale_attested"


class WhaleLargeTradeImbalanceComponent(SubStrategyComponent):
    """
    HYPOTHESIS -- ONE FALSIFIABLE CLAIM
    -----------------------------------
    SUSTAINED LARGE-TRADE ORDER-FLOW IMBALANCE PREDICTS SHORT-HORIZON
    CONTINUATION. Precisely: when `whale_lt_imbalance` (the signed share of a
    bar's large-trade notional, in [-1, +1] -- see
    `strategy-research/tools/recorder/whale_features.py` definition (a)) holds ONE
    sign with magnitude >= `min_abs_imbalance` on each of `persistence_bars`
    consecutive FULLY-ATTESTED bars, the next bar's return carries that same
    sign more often than the opposite one.

    FALSIFIED IF the rank correlation between this component's forecast and the
    next bar's return is <= 0 over the bars where it is active. The claim is
    directional and one-sided on purpose: a negative correlation would falsify
    CONTINUATION and support the opposite mechanism (large prints marking
    exhaustion), which is a different hypothesis and would need its own
    registration -- it is not this one "with the sign flipped".

    NOTHING IN THIS CLASS EVALUATES THAT CLAIM. It builds the instrument that
    lets a separately-gated evaluation put the question, exactly as
    `whale_features.py` does one level down. There is no return, no
    correlation and no P&L anywhere in this file.

    SIGN CONVENTION: `whale_lt_imbalance` > 0 means large-trade notional was
    net TAKER-BUY (whale_features.py "SIGN IS THE TAKER'S SIDE"). Continuation
    therefore maps a positive imbalance to a POSITIVE (long) forecast -- the
    forecast is NOT negated. A mean-reversion reading of the same feature is a
    different component, not a `scaling_factor: -10.0` variant of this one:
    inverting the sign inverts the hypothesis, and the docstring above would
    then be a lie about what the config is testing.

    WHAT "SUSTAINED" MEANS, AND WHY N=3
    ------------------------------------
    `persistence_bars` (default 3) is the number of consecutive attested bars
    the imbalance must hold. It is a REGISTERED DEFAULT, chosen from the
    hypothesis wording before any evaluation, NOT tuned against data -- no IC,
    correlation or return was computed at any point in choosing it. The
    reasoning: at N=1 "sustained" is vacuous (one bar is a single reading). At
    N=2 the claim rests on one repetition, which cannot be told apart from a
    single large order worked across a bar boundary -- the exact artifact the
    hypothesis has to exclude to be about sustained FLOW rather than one
    print. N=3 is the smallest window that requires the imbalance to survive
    two independent bar boundaries.

    `min_abs_imbalance` (default 0.5) is likewise derived from the feature's
    own algebra, not from data. LTI = (B - S) / (B + S) over large-trade
    notional, so |LTI| >= 0.5 is exactly "at least 3:1 one-directional", the
    natural reading of "imbalanced". Any pre-registration consuming this
    component must FREEZE both values in its own (c) frozen-parameters block.

    NaN HANDLING -- EXPLICIT, AND THE POINT OF THE COMPONENT
    --------------------------------------------------------
    `_raw_value` is NaN whenever the component ABSTAINS, and NaN is appended to
    the engine's history deque as an abstention. This is the framework's
    documented mechanism, not an invention: `DOC/STRATEGY_FRAMEWORK.md`
    invariant 1 -- "NaN appends are legal and intentional ... never inject 0.0
    placeholders into history deques".

    Zero is NOT abstention here. `whale_lt_imbalance` = 0 asserts that whale
    flow was measured and was BALANCED, which is a claim; `whale_features.py`
    already refuses to emit 0.0 for an unmeasured bar for exactly this reason
    (its definition (a): "Not 0.0: zero asserts that whale flow was balanced,
    which is a measurement, and there was none to measure"). This component
    keeps that distinction rather than collapsing it one layer up. The five
    states, exhaustively:

      1. Fewer than `persistence_bars` bars buffered -> `is_ready()` is False
         and the engine appends nothing (normal warmup).
      2. A required column is absent from the bar DataFrame -> ABSTAIN (NaN).
         The feed was not wired; the component has measured nothing. A 0.0 here
         would make a missing aux feed indistinguishable from measured-balanced
         flow, which is how a wiring bug becomes a scientific result.
      3. Any bar in the persistence window is UNATTESTED (`whale_attested` != 1)
         -> ABSTAIN (NaN). Includes the current bar. An unattested bar's feature
         columns are already NaN upstream (whale_features.py NaN-s
         `_VALUE_COLUMNS` when a coverage gap intersects the bar).
      4. Any bar in the window has a NaN imbalance while attested (no trade
         reached the pair's own large-trade threshold tau) -> ABSTAIN (NaN).
         Whale flow existed to be measured only if a whale traded.
      5. All `persistence_bars` bars measured -> a real result: the mean
         imbalance scaled to forecast units if the sustained condition holds,
         and EXACTLY 0.0 if it does not. 0.0 is correct here and is the only
         place it is: the flow WAS measured on every bar of the window and was
         not sustainedly one-directional. That is an inactive measurement, the
         same kind `FundingRateMeanReversionComponent` emits below its
         threshold -- not an abstention.

    State 3 is why `is_ready()` deliberately does NOT consult attestation. The
    engine appends to the history deque only when `is_ready()` is True
    (strategy_engine.py:77-82), and `apply_transform_pipeline` seeds from
    `history.iloc[-1]` (registry.py:105). A component that went not-ready on an
    unattested bar would append nothing, and the next forecast would be
    computed from the last ATTESTED bar's value -- a silent stale carry, which
    is the other failure the dispatch that built this forbids. Readiness is a
    bar-count question; attestation is a value question, and it is answered in
    the value.

    CONSEQUENCE, STATED RATHER THAN HIDDEN: NaN propagates. A NaN raw value
    makes this component's post-pipeline value NaN and hence the whole
    per-regime ensemble sum NaN (strategy_engine.py:97-122), so a bar this
    component abstains on produces a NaN forecast for the regime, not a partial
    forecast from the other components. That is the honest reading -- the bar's
    forecast is undefined, not zero -- and it is why this component belongs in
    a single-component config for its own univariate test. Mixing it into a
    multi-component ensemble makes its abstentions silence the other
    components too; do that only deliberately.

    TWO BLOCKERS ON THE CURRENT CAPTURE, RECORDED HERE SO NEITHER IS MISREAD AS
    AN INVITATION TO LOWER A THRESHOLD (dispatch W14 step 3; W13 first noted
    (a) alone, W14 adds (b) and the registered resolution for both).

    (a) THIS COMPONENT CANNOT FIRE. Dispatch W11 measured attested bars
    arriving in runs of at most 2 consecutive bars (`prereg_whale_footprint_v2
    .yaml`: `avg_holding_bars_primary.w11_measurement_attempt`), against a
    registered `persistence_bars` of 3 -- so state 3 (any unattested bar in
    the window) applies to every bar and the output is NaN throughout.

    (b) THE UNIVARIATE PRE-REGISTRATION ITSELF IS ALSO BLOCKED, by a separate
    gate on the raw feature column: `prereg_whale_footprint_v2.yaml`'s
    `required_coverage_floor` (0.80) is not currently met (measured
    `attested_bar_fraction` 0.4178 whole-capture / 0.5455 post-hole steady
    state -- see that file's `required_coverage_floor.w11_status`). This is
    the OTHER hypothesis test (univariate, on the raw column -- see this
    file's own hypothesis statement above), which the pre-registration gates
    independently of this component; the director explicitly REJECTED routing
    that test through this component's sustained-subset forecast (dispatch
    W14, R4) because they are different hypotheses.

    BOTH SHARE ONE ROOT CAUSE: reconnect churn in the recorder (~6
    ws_disconnects/10h, each destroying a whole 1h bar's attestation --
    `prereg_whale_footprint_v2.yaml`: `required_coverage_floor.w11_status`).
    THE REGISTERED FIX FOR BOTH IS HOST MIGRATION -- moving the recorder off
    its current host/network -- NOT threshold relaxation. Concretely: NOT
    lowering `persistence_bars` below 3 (that would fit this component's
    parameter to the capture's gap structure rather than to the hypothesis),
    and NOT lowering `required_coverage_floor` in the pre-registration (that
    file's own `w11_status` already explains why: the floor's job is to catch
    this exact regression, and lowering it to wherever the metric currently
    sits turns a tripped alarm into a new normal). No threshold anywhere was
    changed by this note.

    DATA PATH: the normal aux-feed path and no other. Both columns arrive on the
    bar DataFrame via `DataManager.register_feed()` ->
    `_premerge_aux_feeds()` -> `_merge_asof_with_causality_guard()`
    (data_manager.py:704-786), which enforces the W9 `window_seconds`
    declaration -- `FEED_WINDOW_SECONDS[<whale feed>] == bar_seconds`
    (feed_registry.py:46-95), the forward window
    `[timestamp, timestamp + bar_seconds)` the features actually aggregate. The
    guard refuses to attach a value whose declared window ends after the bar it
    targets. This component reads the merged column and adds no loader of its
    own, exactly as `FundingRateMeanReversionComponent` reads `funding_rate`.
    """

    consumes_feeds = (WHALE_LT_IMBALANCE_COLUMN, WHALE_ATTESTED_COLUMN)

    def __init__(self, name="WhaleLTImbalance", weight=1.0, parameters=None):
        params = parameters or {}
        params.setdefault("standardized_forecast", False)
        super().__init__(name, weight, params)
        self.persistence_bars = int(params.get("persistence_bars", 3))
        self.min_abs_imbalance = float(params.get("min_abs_imbalance", 0.5))
        self.scaling_factor = float(params.get("scaling_factor", 10.0))
        if self.persistence_bars < 1:
            raise ValueError(
                f"persistence_bars must be >= 1, got {self.persistence_bars} -- "
                "a sustained-imbalance component with a non-positive window has "
                "no hypothesis to encode."
            )
        # Abstention is the SAFE START. Before the first update() the component
        # has measured nothing, and 0.0 would be a claim about that nothing.
        self._raw_value = float("nan")

    def _abstain(self, reason: str, **detail):
        self._raw_value = float("nan")
        self.confidence = 0.0
        self.debug_info = {"abstained": True, "abstain_reason": reason, **detail}

    def update(self, data: pd.DataFrame):
        self.data = data
        # Reset to ABSTAIN, not to 0.0 -- every early return below is a
        # "measured nothing" case, and the default must say so.
        self._raw_value = float("nan")
        self.debug_info = {}

        if not self.is_ready():
            return

        missing = [
            c for c in (WHALE_LT_IMBALANCE_COLUMN, WHALE_ATTESTED_COLUMN)
            if c not in data.columns
        ]
        if missing:
            self._abstain("aux_feed_columns_absent", missing_columns=missing)
            return

        n = self.persistence_bars
        window_imbalance = data[WHALE_LT_IMBALANCE_COLUMN].iloc[-n:].astype(float).values
        window_attested = data[WHALE_ATTESTED_COLUMN].iloc[-n:].astype(float).values

        # Attestation is all-or-nothing per bar and the window is a conjunction:
        # a single unattested bar means the persistence claim is unverifiable,
        # not false. Episodes are never joined across an unattested gap -- same
        # rule tools/recorder/whale_persistence.py applies to the same feature.
        n_unattested = int(np.sum(~(window_attested == 1.0)))
        if n_unattested:
            self._abstain(
                "window_not_fully_attested",
                persistence_bars=n,
                unattested_bars_in_window=n_unattested,
            )
            return

        n_unmeasured = int(np.sum(np.isnan(window_imbalance)))
        if n_unmeasured:
            # Attested but NaN: no trade in that bar reached the pair's own
            # trailing large-trade threshold. Nothing to measure, so nothing is
            # asserted (whale_features.py definition (a)).
            self._abstain(
                "no_large_trade_in_window",
                persistence_bars=n,
                unmeasured_bars_in_window=n_unmeasured,
            )
            return

        # From here the whole window is MEASURED: any output is a real result,
        # 0.0 included.
        signs = np.sign(window_imbalance)
        same_sign = bool(np.all(signs == signs[0])) and signs[0] != 0.0
        all_above_threshold = bool(np.all(np.abs(window_imbalance) >= self.min_abs_imbalance))
        sustained = same_sign and all_above_threshold

        mean_imbalance = float(np.mean(window_imbalance))
        if sustained:
            # Continuation: forecast carries the imbalance's own sign. |mean| is
            # in [min_abs_imbalance, 1] here, so the emitted forecast spans
            # [+-min_abs_imbalance*sf, +-sf] and the clip is a guard, not the
            # normal path -- the -20..+20 pipeline convention is respected by
            # construction at the default sf=10.0.
            self._raw_value = float(np.clip(mean_imbalance * self.scaling_factor, -20.0, 20.0))
            self.confidence = float(min(abs(mean_imbalance), 1.0))
        else:
            self._raw_value = 0.0
            self.confidence = 0.0

        self.debug_info = {
            "abstained": False,
            "persistence_bars": n,
            "window_imbalance": [float(v) for v in window_imbalance],
            "mean_imbalance": mean_imbalance,
            "same_sign": same_sign,
            "all_above_threshold": all_above_threshold,
            "sustained": sustained,
            "min_abs_imbalance": self.min_abs_imbalance,
        }

    def is_ready(self) -> bool:
        # Bar-count ONLY -- attestation must NOT be consulted here. See the
        # class docstring, "State 3 is why is_ready() deliberately does not
        # consult attestation": a not-ready bar appends nothing, and the next
        # forecast would then be seeded from the last attested bar's value.
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.persistence_bars
