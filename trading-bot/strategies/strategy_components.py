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

    D-191: `average` "ema" (default) is the EMA spread above, unchanged.
    `average` "sma" swaps both averages for simple means of the last
    fast_period / slow_period closes including the current one (as
    MovingAverageDistanceComponent's "sma"): (SMA_fast - SMA_slow) / SMA_slow
    x 100 x scaling_factor. A NaN close inside either SMA window gives NaN.
    "sma" is ready at max(fast_period, slow_period) bars; "ema" keeps
    slow_period. An unknown `average` raises when the component is built.
    """

    AVERAGES = ("ema", "sma")

    def __init__(self, name: str = "EMASpread", weight: float = 1.0, parameters: Optional[Dict[str, Any]] = None):
        super().__init__(name, weight, parameters or {})
        self.fast_period = self.parameters.get('fast_period', 9)
        self.slow_period = self.parameters.get('slow_period', 21)
        self.scaling_factor = self.parameters.get('scaling_factor', 5.0)
        self.average = self.parameters.get('average', 'ema')
        if self.average not in self.AVERAGES:
            raise ValueError(f"EMASpreadComponent: average must be one of "
                             f"{self.AVERAGES}, got {self.average!r}")
        if self.average == "sma":
            # Safety review: on "sma" a period that is not an integer >= 1
            # would slice the wrong window (0 -> whole buffer, negative ->
            # iloc[k:], 9.7 -> truncated to 9). Integral floats (50.0) are
            # accepted as ints; bools are refused. "ema" is not checked.
            self.fast_period = self._sma_period('fast_period', self.fast_period)
            self.slow_period = self._sma_period('slow_period', self.slow_period)

    @staticmethod
    def _sma_period(key: str, value: Any) -> int:
        if isinstance(value, (bool, np.bool_)):
            ok = False
        elif isinstance(value, (int, np.integer)):
            ok = True
        elif isinstance(value, (float, np.floating)):
            ok = bool(np.isfinite(value)) and float(value).is_integer()
        else:
            ok = False
        if not ok or int(value) < 1:
            raise ValueError(f"EMASpreadComponent: {key} must be an integer >= 1 "
                             f"when average is 'sma', got {value!r}")
        return int(value)

    def update(self, data: pd.DataFrame):
        self.data = data
        if self.is_ready():
            close = data['close']
            if self.average == "sma":
                self._update_sma(close)
                return
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

    def _update_sma(self, close: pd.Series):
        # skipna=False: a NaN close in either window gives a NaN spread.
        fast_sma = close.iloc[-int(self.fast_period):].mean(skipna=False)
        slow_sma = close.iloc[-int(self.slow_period):].mean(skipna=False)
        spread_pct = ((fast_sma - slow_sma) / slow_sma) * 100.0
        self._raw_value = float(spread_pct * self.scaling_factor)
        self.confidence = 1.0
        self.debug_info = {
            'fast_sma': float(fast_sma),
            'slow_sma': float(slow_sma),
            'spread_pct': float(spread_pct),
            'average': 'sma',
        }

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        if self.average == "sma":
            return max(int(self.fast_period), int(self.slow_period))
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


class MovingAverageDistanceComponent(SubStrategyComponent):
    """
    Percent distance of the close from its moving average, on every bar:

        raw_value = (close[t] - MA[t]) / MA[t] x 100

    MA is the simple average of the last `period` closes (average: "sma") or
    their EMA (average: "ema", span = period, adjust=False -- the same EMA as
    MacroTrendFilterComponent, which this replaces for new configs). Graded and
    signed: positive above the average, negative below. No lag: MA includes
    bar t's close (the engine decides and fills at the bar's close). No
    scaling_factor: the config's transforms scale it.

    NaN: an SMA window that holds a NaN close, or a NaN latest close, gives
    NaN. An unknown `average` or a `period` below 2 raises when the component
    is built.
    """

    AVERAGES = ("sma", "ema")

    def __init__(self, name="MovingAverageDistance", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 50))
        self.average = self.parameters.get("average", "sma")
        if self.average not in self.AVERAGES:
            raise ValueError(f"MovingAverageDistanceComponent: average must be one of "
                             f"{self.AVERAGES}, got {self.average!r}")
        if self.period < 2:
            raise ValueError(f"MovingAverageDistanceComponent: period must be >= 2, got {self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        close = data['close']
        if self.average == "sma":
            ma = float(close.iloc[-self.period:].mean(skipna=False))
        else:
            ma = float(close.ewm(span=self.period, adjust=False).mean().iloc[-1])
        last_close = float(close.iloc[-1])

        self._raw_value = (last_close - ma) / ma * 100.0
        self.confidence = 1.0
        self.debug_info = {'moving_average': ma, 'close': last_close}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period


class DonchianBreakoutComponent(SubStrategyComponent):
    """
    Where the close sits against its window's channel, on every bar:

        W = bars t-period+1 .. t (bar t included)
        source = "close" (default): H = max(close[W]), L = min(close[W])
        source = "high_low":        H = max(high[W]),  L = min(low[W])
        form = "position" (default):
            pos = (close[t] - L) / (H - L)   (pos = 0.5 when H = L)
            raw_value = (2 x pos - 1) x scaling_factor
        form = "below_proximity":
            mid = (H + L) / 2
            D = (mid - close[t]) / mid x 100
            raw_value = 1 / (1 + D) if close[t] < mid, else 0.0     (scaling_factor not used)

    Range and sign: "position" is -sf to +sf, signed, positive above the middle of the window, 0 at the middle
    or for a zero range. "below_proximity" is 0 to below 1, never negative, with no direction. It is 0 at or above
    the middle (a zero range puts the close on the middle) and rises toward 1 as a close below the middle
    climbs back to it. It jumps from near 1 to 0 where the close crosses the middle.
    The default form "position" is the original output, unchanged.
    Warm-up: period rows, bar t included.
    NaN: a NaN in any value read gives NaN. With "below_proximity", a mid not above 0 gives NaN (never on real bars).
    Building the component raises for a period below 1, a source other than "close" or "high_low", or a
    form other than "position" or "below_proximity".

    WHY THIS CANNOT LEAK: it reads only the last `period` rows of data (bar t is the last row): the closes, or the
    highs and lows plus close[t]; all of them are known at bar t's close.
    """

    def __init__(self, name="DonchianBreakout", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        if self.period < 1:
            raise ValueError(f"DonchianBreakoutComponent: period must be >= 1, got {self.period}")
        self.scaling_factor = float(self.parameters.get("scaling_factor", 20.0))
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high_low"):
            raise ValueError(
                f"DonchianBreakoutComponent: source must be 'close' or 'high_low', got {self.source!r}")
        self.form = self.parameters.get("form", "position")
        if self.form not in ("position", "below_proximity"):
            raise ValueError(
                f"DonchianBreakoutComponent: form must be 'position' or 'below_proximity', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.period
        close = data['close'].astype(float)
        c = float(close.iloc[-1])
        if self.source == "high_low":
            hi = data['high'].astype(float).iloc[-n:]
            lo = data['low'].astype(float).iloc[-n:]
            if hi.isna().any() or lo.isna().any() or np.isnan(c):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            H = float(hi.max())
            L = float(lo.min())
        else:
            win = close.iloc[-n:]
            if win.isna().any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            H = float(win.max())
            L = float(win.min())
        if self.form == "position":
            rng = H - L
            pos = 0.5 if rng == 0 else (c - L) / rng
            self._raw_value = float((2.0 * pos - 1.0) * self.scaling_factor)
        else:
            mid = (H + L) / 2.0
            if not mid > 0:
                self._raw_value = float("nan")
            elif c < mid:
                d = (mid - c) / mid * 100.0
                self._raw_value = float(1.0 / (1.0 + d))
            else:
                self._raw_value = 0.0
        self.confidence = 1.0
        self.debug_info = {'high': H, 'low': L, 'close': c, 'form': self.form, 'source': self.source}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

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


class FundingRateComponent(SubStrategyComponent):
    """
    Graded version of FundingRateMeanReversionComponent (D-051). Every bar:

        raw_value = -funding_rate x 10000

    the latest funding print in basis points, sign flipped (contrarian:
    negative when longs pay). No threshold and no scaling_factor: natural
    units, the config's transforms scale it. The print's size is
    venue-dependent (Binance prints every 8h; Kraken Futures hourly).

    Data: 'funding_rate', merged by DataManager with fill 'carry_forward'
    (CUL-355), so every bar carries the latest print known at or before it.
    No lookahead: a print is never attached before its own timestamp. A
    missing column, None or NaN gives NaN (a data gap -- never a fabricated
    0.0, which would read as a real "no funding" print).
    """

    consumes_feeds = ("funding_rate",)

    def __init__(self, name="FundingRate", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        value = data["funding_rate"].iloc[-1] if "funding_rate" in data.columns else None
        if value is None or pd.isna(value):
            self._raw_value = float('nan')
            self.debug_info = {'nan_policy': 'propagate_invalid', 'reason': 'funding_rate_missing'}
            return

        funding_rate = float(value)
        self._raw_value = -funding_rate * 10000.0
        self.confidence = 1.0
        self.debug_info = {"funding_rate": funding_rate}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        # 2, not 1: the strategy engine needs 2 history values before it
        # forecasts, and a component's history buffer is sized from this.
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

    Requires the 'fear_greed' column, merged onto the bars by DataManager with
    the feed's one-day publication delay (FEED_DELAY_SECONDS, CUL-356).
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


class FearGreedComponent(SubStrategyComponent):
    """
    Graded version of FearGreedContrarianComponent (D-051). Every bar:

        raw_value = 50 - fear_greed

    in index points, -50..+50: contrarian, positive in fear (index below 50),
    negative in greed. No thresholds and no scaling_factor: the config's
    transforms scale it.

    Data: 'fear_greed', merged by DataManager with fill 'carry_forward'
    (CUL-355) and a one-day publication delay (CUL-356): every bar of day D
    carries day D-1's value. A missing column, None or NaN gives NaN (never a
    fabricated 50, which would read as a real neutral reading).
    """

    consumes_feeds = ("fear_greed",)

    def __init__(self, name="FearGreed", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}

        if not self.is_ready():
            return

        value = data["fear_greed"].iloc[-1] if "fear_greed" in data.columns else None
        if value is None or pd.isna(value):
            self._raw_value = float('nan')
            self.debug_info = {'nan_policy': 'propagate_invalid', 'reason': 'fear_greed_missing'}
            return

        fg = float(value)
        self._raw_value = 50.0 - fg
        self.confidence = 1.0
        self.debug_info = {"fear_greed": fg}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        # 2, not 1: the strategy engine needs 2 history values before it forecasts.
        return 2


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


class MacdHistogramComponent(SubStrategyComponent):
    """
    The MACD histogram as a percent of the close, on every bar -- the graded
    version of MacdHistogramCrossoverComponent (D-051):

        macd      = EMA_fast(close) - EMA_slow(close)
        signal    = EMA_signal(macd)
        raw_value = (macd - signal) / close x 100

    Price-free, so comparable across assets. EMAs use span = period,
    adjust=False, over the bar window the component is given (as the crossover
    component); the value depends slightly on that window's length. Stateless:
    no memory of earlier bars. No scaling_factor: the config's transforms
    scale it.

    No lookahead: every EMA runs over closes up to and including bar t. A NaN
    latest close gives NaN.
    """

    def __init__(self, name="MacdHistogram", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.fast_period = int(self.parameters.get("fast_period", 12))
        self.slow_period = int(self.parameters.get("slow_period", 26))
        self.signal_period = int(self.parameters.get("signal_period", 9))
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


# --- strategy_designer_v2 components (approved by the operator, 2026-11-14) ---

class MovingAverageSlopeComponent(SubStrategyComponent):
    """
    Percent change of a moving average over the last `lookback` bars, on every bar:

        raw_value = (MA[t] - MA[t - lookback]) / MA[t - lookback] x 100

    MA is the simple average of `period` closes (average: "sma") or their EMA (average: "ema", span = period,
    adjust=False). Graded and signed: positive while the average rises, negative while it falls. No lag beyond the
    average's own: MA[t] includes bar t's close. No scaling_factor: the config's transforms scale it.
    """

    AVERAGES = ("sma", "ema")

    def __init__(self, name="MovingAverageSlope", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 200))
        self.lookback = int(self.parameters.get("lookback", 20))
        self.average = self.parameters.get("average", "sma")
        if self.average not in self.AVERAGES:
            raise ValueError(f"MovingAverageSlopeComponent: average must be one of {self.AVERAGES}, got {self.average!r}")
        if self.period < 2 or self.lookback < 1:
            raise ValueError("MovingAverageSlopeComponent: period must be >= 2 and lookback >= 1")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close']
        if self.average == "sma":
            ma_now = float(close.iloc[-self.period:].mean(skipna=False))
            ma_then = float(close.iloc[-(self.period + self.lookback):-self.lookback].mean(skipna=False))
        else:
            ema = close.ewm(span=self.period, adjust=False).mean()
            ma_now, ma_then = float(ema.iloc[-1]), float(ema.iloc[-1 - self.lookback])
        self._raw_value = (ma_now - ma_then) / ma_then * 100.0
        self.confidence = 1.0
        self.debug_info = {'moving_average': ma_now, 'moving_average_then': ma_then}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.lookback


class MovingAverageAgeComponent(SubStrategyComponent):
    """
    How long the current side of a moving average has lasted, signed, on every bar:

        raw_value = +n while the close (or the fast average) has been above the slow average for the last n bars,
                    -n while it has been below it for the last n bars,

    n counting bar t itself and capped at `max_bars`. The slow average is the SMA of `period` closes; with
    `fast_period` set, the fast SMA of `fast_period` closes is compared with it instead of the close (for example
    50 and 200: the age of a golden or death cross). Signed. A regime measure, not a forecast source: it jumps at the
    cross (from +max_bars to -1). No lag: both averages include bar t's close.
    """

    def __init__(self, name="MovingAverageAge", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 200))
        fp = self.parameters.get("fast_period")
        self.fast_period = int(fp) if fp not in (None, "", 0) else None
        self.max_bars = int(self.parameters.get("max_bars", 120))
        if self.period < 2 or self.max_bars < 1 or (self.fast_period is not None and not 1 <= self.fast_period < self.period):
            raise ValueError("MovingAverageAgeComponent: period >= 2, max_bars >= 1, and 1 <= fast_period < period")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].iloc[-(self.period + self.max_bars):]
        slow = close.rolling(self.period).mean().iloc[-self.max_bars:]
        fast = close.rolling(self.fast_period).mean().iloc[-self.max_bars:] if self.fast_period else close.iloc[-self.max_bars:]
        above = (fast > slow).to_numpy()
        side = above[-1]
        n = 0
        for v in above[::-1]:
            if v != side:
                break
            n += 1
        self._raw_value = float(n if side else -n)
        self.confidence = 1.0
        self.debug_info = {'bars_on_side': n, 'above': bool(side)}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.max_bars


class WeekdayComponent(SubStrategyComponent):
    """
    The coming bar's weekday, as a regime measure, on every bar:

        raw_value = weekday of (timestamp[t] + one bar's spacing), UTC: 0 Monday ... 6 Sunday

    Known at bar t's close: no lookahead. For a regime rule (for example "eq 5": the coming bar is stamped Saturday);
    not a bet in itself.
    """

    def __init__(self, name="Weekday", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        ts = pd.to_datetime(data["timestamp"].iloc[-2:], utc=True)
        self._raw_value = float((ts.iloc[-1] + (ts.iloc[-1] - ts.iloc[-2])).weekday())
        self.confidence = 1.0
        self.debug_info = {'coming_weekday': int(self._raw_value)}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 2


class DistanceFromHighComponent(SubStrategyComponent):
    """
    The close's percent distance from the extreme of a recent window, on every bar:

        W = the last `period` rows, bar t included (exclude_current 0),
            or rows t-period .. t-1, bar t excluded (exclude_current 1)
        column: "close" with source "close"; with source "high", the bar's extreme on the
                `extreme` side: the `high` column (extreme "high") or the `low` column (extreme "low")
        R = max(column over W) with extreme "high" (default), min(column over W) with extreme "low"
        form "percent" (default):  raw_value = (close[t] - R) / R x 100
        form "proximity":          raw_value = (1 / (1 + D)) ** power,
                                   D = max(0, (R - close[t]) / R x 100)  (extreme "high")
                                   D = max(0, (close[t] - R) / R x 100)  (extreme "low")

    The defaults (extreme "high") give the original output, unchanged. With period 20, source "high",
    exclude_current 1 and extreme "low", the output is
    (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100.

    Range and sign: graded. "high", "percent": 0 to -100 with exclude_current 0; -100 and up, signed,
    with exclude_current 1. "low", "percent": 0 and up with exclude_current 0 (the close is never below
    its own bar's low); -100 and up, signed, with exclude_current 1: negative and larger in size the
    further the close falls below the prior low. "proximity": above 0, up to 1.
    Warm-up: period + exclude_current rows, bar t included.

    NaN: a NaN in the window, a NaN close[t], or an R not above 0 gives NaN. Building the component
    raises for a period below 2, a source other than "close" or "high", an exclude_current other than
    0 or 1, a form other than "percent" or "proximity", a power not above 0, or an extreme other than
    "high" or "low".

    WHY THIS CANNOT LEAK: it reads only the close of the last row (bar t) and the close, high or low of
    the last period + exclude_current rows, all known at bar t's close; no later row is read.
    """

    def __init__(self, name="DistanceFromHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 60))
        if self.period < 2:
            raise ValueError(f"DistanceFromHighComponent: period must be >= 2, got {self.period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high"):
            raise ValueError(f"DistanceFromHighComponent: source must be 'close' or 'high', got {self.source!r}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"DistanceFromHighComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.form = self.parameters.get("form", "percent")
        if self.form not in ("percent", "proximity"):
            raise ValueError(f"DistanceFromHighComponent: form must be 'percent' or 'proximity', got {self.form!r}")
        self.power = float(self.parameters.get("power", 1.0))
        if not self.power > 0:
            raise ValueError(f"DistanceFromHighComponent: power must be above 0, got {self.power}")
        self.extreme = self.parameters.get("extreme", "high")
        if self.extreme not in ("high", "low"):
            raise ValueError(f"DistanceFromHighComponent: extreme must be 'high' or 'low', got {self.extreme!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        col = "close" if self.source == "close" else self.extreme
        values = data[col].astype(float)
        if self.exclude_current:
            win = values.iloc[-(self.period + 1):-1]
        else:
            win = values.iloc[-self.period:]
        c = float(data["close"].astype(float).iloc[-1])
        if win.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        ref = float(win.max()) if self.extreme == "high" else float(win.min())
        if not ref > 0:
            self._raw_value = float("nan")
        elif self.form == "percent":
            self._raw_value = float((c - ref) / ref * 100.0)
        else:
            if self.extreme == "high":
                d = max(0.0, (ref - c) / ref * 100.0)
            else:
                d = max(0.0, (c - ref) / ref * 100.0)
            self._raw_value = float((1.0 / (1.0 + d)) ** self.power)
        self.confidence = 1.0
        self.debug_info = {'reference': ref, 'extreme': self.extreme, 'column': col}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current



def trailing_return_stds(owner, r, vol_period: int, count: int) -> list:
    """The std (ddof 1) of each of the last `count` windows of `vol_period` returns, newest first:

        stds[k] = np.std(r[m - k - vol_period : m - k], ddof=1),  k = 0 .. count - 1,  m = len(r)

    Topic 33 (2026-11-20; measured: 82 % of a book whose components average 720 such stds, recomputed on every
    bar). The values of the previous call are reused when this call's returns are the previous call's shifted by one
    (the same values, compared byte for byte): stds[k] for k >= 1 is then the previous stds[k - 1], np.std on the same
    returns. Only stds[0] is computed. Otherwise all are computed. The list is the one the loop gives, value for value.
    `owner` (the component) keeps the previous call's returns and stds.

    WHY THIS CANNOT LEAK: it reads only `r`, which the caller builds from closes at or before bar t; a reused std
    was computed from the same returns.
    """
    m = len(r)
    prev = getattr(owner, "_trailing_stds_memo", None)
    if (prev is not None and prev[1] == (vol_period, count) and len(prev[0]) == m
            and prev[0][1:].tobytes() == r[:-1].tobytes()):
        stds = [float(np.std(r[m - vol_period:m], ddof=1))] + prev[2][:-1]
    else:
        stds = [float(np.std(r[m - k - vol_period:m - k], ddof=1)) for k in range(count)]
    owner._trailing_stds_memo = (np.array(r, dtype=float, copy=True), (vol_period, count), stds)
    return stds


class VolatilityScaledReturnComponent(SubStrategyComponent):
    """
    A past move against the coin's usual move, on every bar:

        e = t - lag                                           (lag 0: bar t itself)
        ret = close[e] / close[e - period] - 1
        s(i) = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1, j = i-vol_period+1 .. i
        m = mean(s(e - vol_lookback + 1) .. s(e))             (vol_lookback 1: m = s(e))
        raw_value = ret / (m x sqrt(period)),  0 when m = 0

    The defaults (period 1, vol_period 20, lag 0, vol_lookback 1) give the original output, unchanged.
    With vol_lookback above 1 the base is the average usual move over the lookback. With period 24,
    vol_period 168 and vol_lookback 720 the output equals the 24-bar return in usual moves times
    s(t) / mean of s over the last 720 bars.
    Range: unbounded and signed, like the move: positive after a rise, negative after a fall. Graded.
    Warm-up: max(period + 1, vol_period + vol_lookback) + lag rows, bar t included.
    NaN: a NaN close among those rows gives NaN. A flat base (m = 0, never seen on real bars) gives 0.
    Building the component raises for a period below 1, a vol_period below 2, a lag below 0 or a
    vol_lookback below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last
    max(period + 1, vol_period + vol_lookback) + lag rows of data, all at or before bar t (the last row).
    """

    def __init__(self, name="VolScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 1))
        if self.period < 1:
            raise ValueError(f"VolatilityScaledReturnComponent: period must be >= 1, got {self.period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"VolatilityScaledReturnComponent: vol_period must be >= 2, got {self.vol_period}")
        self.lag = int(self.parameters.get("lag", 0))
        if self.lag < 0:
            raise ValueError(f"VolatilityScaledReturnComponent: lag must be >= 0, got {self.lag}")
        self.vol_lookback = int(self.parameters.get("vol_lookback", 1))
        if self.vol_lookback < 1:
            raise ValueError(
                f"VolatilityScaledReturnComponent: vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()
        n = len(c)
        req = self.get_required_periods()
        used = c[n - req:n - self.lag]
        if np.isnan(used).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        e = n - 1 - self.lag
        ret = c[e] / c[e - self.period] - 1.0
        span = c[e - self.vol_lookback + 1 - self.vol_period:e + 1]   # the closes of the vol_lookback windows
        sds = trailing_return_stds(self, span[1:] / span[:-1] - 1.0, self.vol_period, self.vol_lookback)
        m = float(np.mean(sds))
        if not m > 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float(ret / (m * np.sqrt(self.period)))
        self.confidence = 1.0
        self.debug_info = {'return': float(ret), 'current_std': sds[0], 'mean_std': m}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + 1, self.vol_period + self.vol_lookback) + self.lag


class BarsSinceHighComponent(SubStrategyComponent):
    """
    How recent the last new closing high is, as a regime measure, on every bar:

        raw_value = max(0, max_bars - k)

    k is the number of bars since the last bar whose close was the highest of its prior `lookback` closes (k = 0 on
    that bar). Graded: `max_bars` on the day of a new high, falling by one each bar after it, 0 once the high is older
    than `max_bars` bars. For a regime rule ("a new high within the last `max_bars` bars"), not a forecast source:
    it jumps from 0 to `max_bars` on the day of a new high. Closes only, no lookahead.
    """

    def __init__(self, name="BarsSinceHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.lookback = int(self.parameters.get("lookback", 20))
        self.max_bars = int(self.parameters.get("max_bars", 20))
        if self.lookback < 2 or self.max_bars < 1:
            raise ValueError("BarsSinceHighComponent: lookback >= 2 and max_bars >= 1")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].iloc[-(self.lookback + self.max_bars + 1):].astype(float).to_numpy()
        n = len(close)
        for k in range(0, self.max_bars + 1):
            i = n - 1 - k
            prior = close[i - self.lookback:i]
            if len(prior) == self.lookback and close[i] > prior.max():
                self._raw_value = float(max(0, self.max_bars - k))
                self.debug_info = {'bars_since_high': k}
                break
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.lookback + self.max_bars + 1


class VolumeRatioComponent(SubStrategyComponent):
    """
    Recent volume against its own longer base, on every bar:

        R = volume[t - short_period + 1 .. t]                             (bar t included)
        short_statistic = "mean" (default): num = mean(R)
        short_statistic = "median":         num = median(R)  (average of the two middle values for an even count)
        W = volume[t - period - exclude_current + 1 .. t - exclude_current]  (the base ends exclude_current bars before t)
            exclude_current = 0 (default): W = volume[t - period + 1 .. t]
            exclude_current = 1:           W = volume[t - period .. t - 1]
            exclude_current = 49, period 120: W = volume[t - 168 .. t - 49]
        statistic = "mean" (default):  den = mean(W)
        statistic = "median":          den = median(W)  (average of the two middle values for an even count)
        form = "ratio" (default):  raw_value = num / den
        form = "centred":          raw_value = num / den - 1
        form = "log":              raw_value = ln(num / den)

    The defaults (exclude_current 0, short_period 1, form "ratio", statistic "mean", short_statistic "mean") give
    volume[t] / mean volume, the original output, unchanged; exclude_current 0 and 1 are the original windows.
    exclude_current above 1 lags the base: with period 120, exclude_current 49 and short_period 48 the output is
    mean(volume[t-47..t]) / mean(volume[t-168..t-49]), falling as recent volume thins against the earlier base.
    With period 72, short_period 72 and short_statistic "median" the output is median / mean of the last 72 volumes
    (0 to 2, nearing 1 as the volume spreads evenly).
    Graded, with no direction. With form "ratio" the value is non-negative and equals 1 when the numerator equals
    the base. With both statistics "mean" and exclude_current 0 it is at most period / short_period. form
    "centred" shifts the value down by 1, and form "log" gives the natural log of the ratio.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the rows up to and including bar t (the last row of
    data), over at most the last period + exclude_current rows; a bar's volume is known at that bar's close.

    NaN: a NaN volume in either window, or a base of 0, gives NaN. With form "log", a recent statistic of 0 gives
    NaN (zero volume, never seen on real bars). A missing `volume` column raises.
    Building the component raises for a period below 2, an exclude_current that is not an integer >= 0, a
    short_period below 1 or above period, a form other than "ratio", "centred" or "log", or a statistic or
    short_statistic other than "mean" or "median".
    """

    def __init__(self, name="VolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(f"VolumeRatioComponent: period must be >= 2, got {self.period}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        try:
            ex_int = int(ex)
        except (TypeError, ValueError):
            raise ValueError(f"VolumeRatioComponent: exclude_current must be an integer >= 0, got {ex!r}")
        if ex_int != ex or ex_int < 0:
            raise ValueError(f"VolumeRatioComponent: exclude_current must be an integer >= 0, got {ex!r}")
        self.exclude_current = ex_int
        self.short_period = int(self.parameters.get("short_period", 1))
        if self.short_period < 1 or self.short_period > self.period:
            raise ValueError(
                f"VolumeRatioComponent: short_period must be between 1 and period, got {self.short_period}")
        self.form = self.parameters.get("form", "ratio")
        if self.form not in ("ratio", "centred", "log"):
            raise ValueError(f"VolumeRatioComponent: form must be 'ratio', 'centred' or 'log', got {self.form!r}")
        st = self.parameters.get("statistic", "mean")
        if st not in ("mean", "median"):
            raise ValueError(f"VolumeRatioComponent: statistic must be 'mean' or 'median', got {st!r}")
        self.statistic = st
        sst = self.parameters.get("short_statistic", "mean")
        if sst not in ("mean", "median"):
            raise ValueError(f"VolumeRatioComponent: short_statistic must be 'mean' or 'median', got {sst!r}")
        self.short_statistic = sst
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        vol = data['volume'].astype(float)
        recent = vol.iloc[-self.short_period:]
        if recent.isna().any():
            num = float("nan")
        elif self.short_statistic == "median":
            num = float(np.median(recent.to_numpy()))
        else:
            num = float(recent.mean(skipna=False))
        ex = self.exclude_current
        start = len(vol) - self.period - ex
        stop = len(vol) - ex
        base = vol.iloc[start:stop]
        if base.isna().any():
            den = float("nan")
        elif self.statistic == "median":
            den = float(np.median(base.to_numpy()))
        else:
            den = float(base.mean(skipna=False))
        if np.isnan(num) or np.isnan(den) or not den > 0:
            self._raw_value = float("nan")
        elif self.form == "log":
            self._raw_value = float(np.log(num / den)) if num > 0 else float("nan")
        else:
            self._raw_value = float(num / den - (1.0 if self.form == "centred" else 0.0))
        self.confidence = 1.0
        self.debug_info = {'recent_volume': num, 'base_volume': den, 'statistic': self.statistic,
                           'short_statistic': self.short_statistic, 'exclude_current': ex}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current


class RsiChangeFromPriorLowComponent(SubStrategyComponent):
    """
    The RSI now against the RSI at the earlier lowest close, on every bar:

        s = bar of the lowest close among bars t-lookback .. t-exclude-1 (the most recent such bar on a tie)
        raw_value = RSI(t) - RSI(s)

        RSI(i) = 100 x G / (G + L)   (50 when G + L = 0, no movement at all)
        G, L   = EWM (alpha = 1/rsi_period, adjust=False, seeded with the first value) of the gains max(d, 0) and the
                 losses max(-d, 0) of the rsi_window one-bar close changes d ending at bar i (closes i-rsi_window .. i)

    Range -100 to +100, signed: positive when the RSI now is above the RSI at the earlier closing low (the momentum
    side of a bullish divergence), negative when it is below. Graded in RSI points. It does not test whether the close is
    at or below that low. Warm-up: lookback + rsi_window + 1 rows (131 at the defaults).

    NaN: a NaN close anywhere in the last lookback + rsi_window + 1 rows gives NaN. Nonsensical settings raise at
    construction.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last lookback + rsi_window + 1 rows, the last of
    which is bar t; every RSI is computed from closes at or before its own bar.
    """

    def __init__(self, name="RsiChangeFromPriorLow", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.rsi_period = int(self.parameters.get("rsi_period", 14))
        self.lookback = int(self.parameters.get("lookback", 30))
        self.exclude = int(self.parameters.get("exclude", 3))
        self.rsi_window = int(self.parameters.get("rsi_window", 100))
        if self.rsi_period < 1:
            raise ValueError(f"RsiChangeFromPriorLowComponent: rsi_period must be >= 1, got {self.rsi_period}")
        if self.lookback < 2:
            raise ValueError(f"RsiChangeFromPriorLowComponent: lookback must be >= 2, got {self.lookback}")
        if self.exclude < 0 or self.exclude >= self.lookback:
            raise ValueError(
                f"RsiChangeFromPriorLowComponent: exclude must be in [0, lookback), got {self.exclude}")
        if self.rsi_window < self.rsi_period:
            raise ValueError(
                f"RsiChangeFromPriorLowComponent: rsi_window must be >= rsi_period, got {self.rsi_window}")
        self._raw_value = 0.0

    def _rsi(self, closes, i):
        alpha = 1.0 / self.rsi_period
        seg = closes[i - self.rsi_window:i + 1]
        d = np.diff(seg)
        gains = np.where(d > 0, d, 0.0)
        losses = np.where(d < 0, -d, 0.0)
        g = gains[0]
        l = losses[0]
        for k in range(1, len(d)):
            g = (1.0 - alpha) * g + alpha * gains[k]
            l = (1.0 - alpha) * l + alpha * losses[k]
        if g + l == 0:
            return 50.0
        return 100.0 * g / (g + l)

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = data['close'].iloc[-self.get_required_periods():].astype(float).to_numpy()
        if np.isnan(closes).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = len(closes)
        t = n - 1
        s = t - self.lookback
        for i in range(t - self.lookback, t - self.exclude):
            if closes[i] <= closes[s]:
                s = i
        rsi_now = self._rsi(closes, t)
        rsi_low = self._rsi(closes, s)
        self._raw_value = float(rsi_now - rsi_low)
        self.confidence = 1.0
        self.debug_info = {'rsi_now': rsi_now, 'rsi_at_low': rsi_low, 'bars_since_low': t - s,
                           'low_close': float(closes[s])}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.lookback + self.rsi_window + 1


class RangeCompressionRatioComponent(SubStrategyComponent):
    """
    How narrow a short stretch of bars is against a longer base, on every bar.

        exclude_current = 0 (default): short = bars t-short_period+1 .. t,  long = bars t-long_period+1 .. t
        exclude_current = 1:           short = bars t-short_period .. t-1,  long = bars t-long_period .. t-1
        exclude_current = 2:           short = bars t-short_period .. t-1,  long = bars t-long_period+1 .. t
        S = max(high[short]) - min(low[short])
        base = "range" (default):    B = max(high[long]) - min(low[long])
        base = "mean_bar_range":     B = mean(high[i] - low[i] for i in long)
        ratio = S / B
        form = "compression" (default): raw_value = 1 - ratio   (0.0 when B == 0)
        form = "width":                 raw_value = ratio       (1.0 when B == 0)

    Range & sign: base "range": 0 to 1, never negative, no direction ("compression" near 1 when the short band is
    very narrow, 0 when it spans the whole long range; "width" the reverse). base "mean_bar_range": "width" is 0 and
    up, unbounded (the stretch counted in average bar ranges); "compression" is 1 minus that, up to 1, signed,
    rising as the stretch narrows. Graded.
    Warm-up: long_period + 1 rows when exclude_current is 1, else long_period rows (bar t included); the short
    window needs short_period + 1 rows at most, never more than long_period since short_period < long_period.
    exclude_current 0 and 1 and base "range" are the original outputs, unchanged. exclude_current 2 leaves bar t
    out of the stretch only, so bar t's own move cannot widen it, while the base of average bar ranges includes it.

    NaN: a NaN high or low in any row read (long window or short window) gives NaN. A missing column raises.
    Building the component raises for short_period < 1, short_period >= long_period, exclude_current not 0, 1 or 2,
    form other than "compression" or "width", base other than "range" or "mean_bar_range".

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the last long_period + 1 rows at most of
    data, the last row being bar t; no later row exists in the data it is given.
    """

    def __init__(self, name="RangeCompression", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 20))
        self.long_period = int(self.parameters.get("long_period", 100))
        if self.short_period < 1:
            raise ValueError(f"RangeCompressionRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"RangeCompressionRatioComponent: short_period must be < long_period, "
                f"got {self.short_period} and {self.long_period}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1, 2):
            raise ValueError(f"RangeCompressionRatioComponent: exclude_current must be 0, 1 or 2, got {ex!r}")
        self.exclude_current = int(ex)
        self.form = self.parameters.get("form", "compression")
        if self.form not in ("compression", "width"):
            raise ValueError(
                f"RangeCompressionRatioComponent: form must be 'compression' or 'width', got {self.form!r}")
        self.base = self.parameters.get("base", "range")
        if self.base not in ("range", "mean_bar_range"):
            raise ValueError(
                f"RangeCompressionRatioComponent: base must be 'range' or 'mean_bar_range', got {self.base!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float)
        low = data['low'].astype(float)
        sp = self.short_period
        lp = self.long_period
        if self.exclude_current == 1:
            lh, ll = high.iloc[-(lp + 1):-1], low.iloc[-(lp + 1):-1]
            sh, sl = high.iloc[-(sp + 1):-1], low.iloc[-(sp + 1):-1]
        elif self.exclude_current == 2:
            lh, ll = high.iloc[-lp:], low.iloc[-lp:]
            sh, sl = high.iloc[-(sp + 1):-1], low.iloc[-(sp + 1):-1]
        else:
            lh, ll = high.iloc[-lp:], low.iloc[-lp:]
            sh, sl = high.iloc[-sp:], low.iloc[-sp:]
        if lh.isna().any() or ll.isna().any() or sh.isna().any() or sl.isna().any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        s_range = float(sh.max() - sl.min())
        if self.base == "mean_bar_range":
            b = float((lh - ll).mean())
        else:
            b = float(lh.max() - ll.min())
        if b == 0:
            self._raw_value = 0.0 if self.form == "compression" else 1.0
        else:
            ratio = s_range / b
            self._raw_value = float(1.0 - ratio) if self.form == "compression" else float(ratio)
        self.confidence = 1.0
        self.debug_info = {'short_range': s_range, 'base': b, 'base_kind': self.base,
                           'exclude_current': self.exclude_current}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.long_period + (1 if self.exclude_current == 1 else 0)


class LowerWickComponent(SubStrategyComponent):
    """
    The current bar's lower wick (the part of the bar below its body), relative to a base, on every bar:

        wick[t] = min(open[t], close[t]) - low[t]
        relative_to "range" (default): raw_value = wick[t] / (high[t] - low[t]); 0.0 when high[t] == low[t]
        relative_to "close":           raw_value = wick[t] / close[t] x 100   (percent of price)

    Graded and non-negative on real bars: 0 when the body's bottom is the bar's low (no lower wick), growing
    continuously as the low sits further below the body ("range": up to 1, the whole range below the body). No
    direction. One measure, the lower wick; the setting is its base (merged on 2026-11-17 from LowerWickShareComponent
    and LowerWickPercentComponent, the operator's rule: one component per measure, its base a setting).

    Warm-up: 1 bar (bar t itself). NaN: a NaN open, high, low or close on bar t gives NaN, never a number. A missing
    column raises. A `relative_to` other than "range" or "close" raises when the component is built.

    WHY THIS CANNOT LEAK: it reads only the `open`, `high`, `low` and `close` of the last row of the data (bar t), all
    known at bar t's close; no earlier or later row is used.
    """

    def __init__(self, name="LowerWick", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.relative_to = str(self.parameters.get("relative_to", "range"))
        if self.relative_to not in ("range", "close"):
            raise ValueError(f"LowerWickComponent: relative_to must be 'range' or 'close', got {self.relative_to!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        row = data.iloc[-1]
        o, h, l, c = (float(row[k]) for k in ("open", "high", "low", "close"))
        if np.isnan(o) or np.isnan(h) or np.isnan(l) or np.isnan(c):
            value = float("nan")
        elif self.relative_to == "range":
            rng = h - l
            value = (min(o, c) - l) / rng if rng > 0 else 0.0
        else:
            value = (min(o, c) - l) / c * 100.0 if c != 0 else float("nan")
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'open': o, 'high': h, 'low': l, 'close': c, 'relative_to': self.relative_to}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1


class CloseLocationInRangeComponent(SubStrategyComponent):
    """
    Where the current bar's close sits inside the bar's own range, measured from one end:

        reference = "low" (default): raw_value = (close[t] - low[t]) / (high[t] - low[t])
        reference = "high":          raw_value = (high[t] - close[t]) / (high[t] - low[t])
        high[t] == low[t] (zero range): raw_value = 0.5 with either reference

    The default "low" is the original output: 0 when the close is at the bar's low, 1 at its high.
    Setting "high" gives 1 minus that: 0 when the close is at the bar's high, growing to 1 as the close
    nears the bar's low.
    Graded. The value lies in 0 to 1 and is never negative when the close lies inside [low, high], as it does
    on real bars. It has no sign. It is 0.5 at mid-range.
    Warm-up: 1 row (bar t only).

    WHY THIS CANNOT LEAK: it reads only the `high`, `low` and `close` values of the last row of data (bar t),
    all of which are known at bar t's close; no earlier or later row is read.

    NaN: a NaN high, low or close on bar t gives NaN. A zero range gives 0.5, because there is no range to
    place the close in. A missing column raises.
    Building the component raises for a reference other than "low" or "high".
    """

    def __init__(self, name="CloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        ref = self.parameters.get("reference", "low")
        if ref not in ("low", "high"):
            raise ValueError(
                f"CloseLocationInRangeComponent: reference must be 'low' or 'high', got {ref!r}")
        self.reference = ref
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        h = float(data['high'].iloc[-1])
        l = float(data['low'].iloc[-1])
        c = float(data['close'].iloc[-1])
        if np.isnan(h) or np.isnan(l) or np.isnan(c):
            self._raw_value = float("nan")
        else:
            rng = h - l
            if rng == 0:
                self._raw_value = 0.5
            elif self.reference == "high":
                self._raw_value = float((h - c) / rng)
            else:
                self._raw_value = float((c - l) / rng)
        self.confidence = 1.0
        self.debug_info = {'high': h, 'low': l, 'close': c, 'reference': self.reference}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1


class OpenToLowDropComponent(SubStrategyComponent):
    """
    The depth of the bar's intrabar fall below its open, on every bar:

        raw_value = (open[t] - low[t]) / open[t] x 100

    Graded and non-negative on real bars (low <= open): 0 when the bar never traded below its open, larger the
    deeper the fall from the open to the low, at most 100. It carries no direction. The unit is percent of the open.
    Warm-up: 1 row (bar t only).

    WHY THIS CANNOT LEAK: it reads only the `open` and `low` columns of the last row of data, which is bar t. Both
    are known at that bar's close.

    NaN: a NaN open or low at bar t gives NaN. An open that is not above 0, which never happens on real bars, also
    gives NaN. A missing column raises.
    """

    def __init__(self, name="OpenToLowDrop", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        o = float(data['open'].iloc[-1])
        lo = float(data['low'].iloc[-1])
        if np.isnan(o) or np.isnan(lo) or not o > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float((o - lo) / o * 100.0)
        self.confidence = 1.0
        self.debug_info = {'open': o, 'low': lo}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1


class RsiAboveMidlineShareComponent(SubStrategyComponent):
    """
    How persistently the RSI has held one side of its midline over the last `window` bars:

        raw_value = (number of bars i in t-window+1 .. t on the counted side) / window - 0.5

        counted side: RSI(i) > 50, i.e. G(i) > L(i)   (side = "above", default, today's output)
                      RSI(i) < 50, i.e. G(i) < L(i)   (side = "below")

        RSI(i) = 100 x G / (G + L). G and L are the EWMs (alpha = 1/period, adjust=False, seeded at the first change)
        of the gains max(d, 0) and losses max(-d, 0) of the rsi_window one-bar close changes d ending at bar i
        (closes i-rsi_window .. i). When G + L = 0 the RSI is 50, which is neither above nor below 50.

    Range: -0.5 to +0.5 in steps of 1/window, signed. It is +0.5 when every bar of the window is on the counted side
    and -0.5 when none is. Graded: it grows by 1/window for each further bar on the counted side.
    Warm-up: window + rsi_window rows, bar t included (the oldest RSI needs rsi_window changes, so rsi_window + 1
    closes).

    NaN: a NaN close anywhere in the last window + rsi_window rows gives NaN. A missing `close` column raises.
    These settings raise when the component is built: period < 1, window < 1, rsi_window < period, and a side other
    than "above" or "below".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + rsi_window rows of data, the last
    row being bar t. Each RSI(i) uses closes up to bar i <= t.
    """

    def __init__(self, name="RsiMidlineShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 14))
        self.window = int(self.parameters.get("window", 30))
        self.rsi_window = int(self.parameters.get("rsi_window", 100))
        self.side = self.parameters.get("side", "above")
        if self.period < 1:
            raise ValueError(f"RsiAboveMidlineShareComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"RsiAboveMidlineShareComponent: window must be >= 1, got {self.window}")
        if self.rsi_window < self.period:
            raise ValueError(
                f"RsiAboveMidlineShareComponent: rsi_window must be >= period, got {self.rsi_window} < {self.period}")
        if self.side not in ("above", "below"):
            raise ValueError(f"RsiAboveMidlineShareComponent: side must be 'above' or 'below', got {self.side!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.window + self.rsi_window
        closes = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(closes).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        alpha = 1.0 / self.period
        count = 0
        for j in range(self.window):
            seg = closes[j:j + self.rsi_window + 1]
            diffs = np.diff(seg)
            gains = np.where(diffs > 0, diffs, 0.0)
            losses = np.where(diffs < 0, -diffs, 0.0)
            g = gains[0]
            l = losses[0]
            for k in range(1, len(diffs)):
                g = (1.0 - alpha) * g + alpha * gains[k]
                l = (1.0 - alpha) * l + alpha * losses[k]
            if self.side == "above":
                if g > l:
                    count += 1
            else:
                if g < l:
                    count += 1
        self._raw_value = float(count) / self.window - 0.5
        self.confidence = 1.0
        self.debug_info = {'bars_on_side': count, 'window': self.window, 'side': self.side}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.rsi_window


class RsiMidlineAgeComponent(SubStrategyComponent):
    """
    How long the RSI has held its side of the midline 50, on every bar:

        RSI(i) = 100 x G(i) / (G(i) + L(i)); G(i), L(i) = EWM (alpha 1/period, adjust=False, seeded at the first
        change) of the gains max(d, 0) and losses max(-d, 0) of the `rsi_window` one-bar close changes d ending at
        bar i. G + L = 0 is RSI 50.
        up(i) = G(i) > L(i)    (RSI > 50; an RSI of exactly 50 counts on the lower side)
        n = length of the run of bars ending at t with the same up/down side as bar t, capped at max_bars
        raw_value = +n if up(t) else -n

    Range: -max_bars .. -1 and +1 .. +max_bars, integers, never 0. Positive on the upper side, negative on the lower
    side. The size grows by one for each further bar on the same side.
    Warm-up: max_bars + rsi_window rows, bar t included.
    NaN: a NaN close anywhere in the last max_bars + rsi_window rows gives NaN. `period` < 1, `max_bars` < 1 or
    `rsi_window` < `period` raises when the component is built. (A `tie_side` setting, added by the components step,
    was removed on 2026-11-17: it changed nothing on real data, rule 2.)

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max_bars + rsi_window rows of data, the last
    being bar t; every RSI it uses ends at a bar i <= t.
    """

    def __init__(self, name="RsiMidlineAge", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 14))
        self.max_bars = int(self.parameters.get("max_bars", 60))
        self.rsi_window = int(self.parameters.get("rsi_window", 100))
        if self.period < 1:
            raise ValueError(f"RsiMidlineAgeComponent: period must be >= 1, got {self.period}")
        if self.max_bars < 1:
            raise ValueError(f"RsiMidlineAgeComponent: max_bars must be >= 1, got {self.max_bars}")
        if self.rsi_window < self.period:
            raise ValueError(f"RsiMidlineAgeComponent: rsi_window must be >= period, got {self.rsi_window}")
        self._raw_value = 0.0

    def _up(self, closes: np.ndarray) -> bool:
        d = np.diff(closes)
        gains = np.where(d > 0, d, 0.0)
        losses = np.where(d < 0, -d, 0.0)
        a = 1.0 / self.period
        g = float(gains[0])
        l = float(losses[0])
        for k in range(1, len(d)):
            g = (1.0 - a) * g + a * float(gains[k])
            l = (1.0 - a) * l + a * float(losses[k])
        return g > l

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        sides = []
        for j in range(self.max_bars):
            end = len(c) - j
            sides.append(self._up(c[end - self.rsi_window - 1:end]))
        side = sides[0]
        n = 1
        while n < self.max_bars and sides[n] == side:
            n += 1
        self._raw_value = float(n if side else -n)
        self.confidence = 1.0
        self.debug_info = {'up': bool(side), 'run': n}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.max_bars + self.rsi_window


class HighProximityMomentumComponent(SubStrategyComponent):
    """
    A return weighted by how close the close is to its recent high, on every bar:

        H[t]  = max(close[t - period + 1 .. t])                      (bar t included)
        R     = (close[t] - close[t - return_period]) / close[t - return_period] x 100
        proximity "convex" (default): W = (1 / (1 + D)) ^ power,  D = (H[t] - close[t]) / H[t] x 100
        proximity "ratio":            W = (close[t] / H[t]) ^ power
        raw_value = W x R

    Range and sign: unbounded and signed, with the same sign as R. Since 0 < W <= 1 for positive closes, its size
    is at most |R|. It equals R at a new high and shrinks the further the close sits below the high. Graded.
    Warm-up: max(period, return_period + 1) rows, bar t included.
    NaN: a NaN close in the last period rows or at close[t - return_period] gives NaN. A highest close or base
    close not above 0 also gives NaN.
    Building the component raises for a period below 2, a power not above 0, a return_period below 1, or a
    proximity other than "convex" or "ratio".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the rows up to and including bar t (the last row of
    data): the last period closes and the close return_period rows before bar t.
    """

    def __init__(self, name="HighProximityMomentum", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"HighProximityMomentumComponent: period must be >= 2, got {self.period}")
        self.power = float(self.parameters.get("power", 2.0))
        if not self.power > 0:
            raise ValueError(f"HighProximityMomentumComponent: power must be > 0, got {self.power}")
        self.return_period = int(self.parameters.get("return_period", 30))
        if self.return_period < 1:
            raise ValueError(
                f"HighProximityMomentumComponent: return_period must be >= 1, got {self.return_period}")
        self.proximity = self.parameters.get("proximity", "convex")
        if self.proximity not in ("convex", "ratio"):
            raise ValueError(
                f"HighProximityMomentumComponent: proximity must be 'convex' or 'ratio', got {self.proximity!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()
        win = c[-self.period:]
        base = float(c[-(self.return_period + 1)])
        ct = float(c[-1])
        self.confidence = 1.0
        if np.isnan(win).any() or np.isnan(base) or np.isnan(ct):
            self._raw_value = float("nan")
            return
        h = float(np.max(win))
        if not h > 0 or not base > 0:
            self._raw_value = float("nan")
            return
        if self.proximity == "convex":
            d = (h - ct) / h * 100.0
            w = float(np.power(1.0 / (1.0 + d), self.power))
        else:
            w = float(np.power(ct / h, self.power))
        ret = (ct - base) / base * 100.0
        self._raw_value = float(w * ret)
        self.debug_info = {'high': h, 'weight': w, 'return_pct': ret}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.return_period + 1)


class HighProximityVolatilityRatioComponent(SubStrategyComponent):
    """
    Closeness to the high close, times how calm current volatility is against its past:

        H    = max(close[t - period + 1 .. t])
        P    = 100 + (close[t] - H) / H x 100
        r(j) = close[j] / close[j - 1] - 1
        s(i) = std (ddof 1) of r(i - vol_period + 1 .. i)
        R    = mean(s(t - vol_lookback + 1 .. t)) / s(t)
        raw_value = P x R

    Graded, non-negative, unbounded above, no direction. P is 100 at a new high and lower the deeper the close
    sits below it. R is above 1 when today's volatility is below its past mean.
    Warm-up: max(period, vol_lookback + vol_period) rows, bar t included (385 at the defaults).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, vol_lookback + vol_period)
    rows of data, the last row being bar t; a close is known at its bar's close.

    NaN: a NaN close in those rows gives NaN, and so do an H not above 0 or a current std s(t) of 0.
    Building the component raises for period < 2, vol_period < 2 or vol_lookback < 1.
    """

    def __init__(self, name="HighProximityVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"HighProximityVolatilityRatioComponent: period must be >= 2, got {self.period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"HighProximityVolatilityRatioComponent: vol_period must be >= 2, got {self.vol_period}")
        self.vol_lookback = int(self.parameters.get("vol_lookback", 365))
        if self.vol_lookback < 1:
            raise ValueError(
                f"HighProximityVolatilityRatioComponent: vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        high = float(np.max(c[-self.period:]))
        last = float(c[-1])
        if not high > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        prox = 100.0 + (last - high) / high * 100.0
        rets = c[1:] / c[:-1] - 1.0
        stds = pd.Series(rets).rolling(self.vol_period).std(ddof=1).to_numpy()[-self.vol_lookback:]
        s_now = float(stds[-1])
        mean_s = float(np.mean(stds))
        if np.isnan(s_now) or np.isnan(mean_s) or not s_now > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(prox * mean_s / s_now)
        self.confidence = 1.0
        self.debug_info = {'proximity': prox, 'std_now': s_now, 'std_mean': mean_s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.vol_lookback + self.vol_period)


class VolatilityRankedFallComponent(SubStrategyComponent):
    """
    Today's fall in usual moves, weighted by how high volatility stands against its recent past:

        r(j)  = close[j] / close[j-1] - 1
        s(i)  = std (ddof 1) of r(i - vol_period + 1 .. i)
        fall  = max(0, -r(t) / s(t))
        rank  = (number of i in t - lookback + 1 .. t with s(i) <= s(t)) / lookback
        raw_value = fall x rank

    Range and sign: 0 and up, unbounded above, never negative. It is 0 on an up or flat bar. On a down bar it
    grows with the depth of the fall measured in usual moves, and with the rank of today's volatility. The rank
    is above 0 (s(t) counts itself) and at most 1. Graded, one-sided, no short side.
    Warm-up: lookback + vol_period rows, bar t included.
    NaN: a NaN close anywhere in the last lookback + vol_period rows gives NaN. A current std s(t) that is not
    above 0 also gives NaN (20 equal returns, never seen on real bars).
    Building the component raises for a vol_period below 2 or a lookback below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last lookback + vol_period rows of data, which
    end at bar t (the last row); every return and every std uses closes at or before bar t.
    """

    def __init__(self, name="VolRankedFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"VolatilityRankedFallComponent: vol_period must be >= 2, got {self.vol_period}")
        self.lookback = int(self.parameters.get("lookback", 120))
        if self.lookback < 1:
            raise ValueError(f"VolatilityRankedFallComponent: lookback must be >= 1, got {self.lookback}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).iloc[-n:].to_numpy()
        self.confidence = 1.0
        if np.isnan(c).any():
            self._raw_value = float("nan")
            return
        r = c[1:] / c[:-1] - 1.0
        stds = trailing_return_stds(self, r, self.vol_period, self.lookback)[::-1]   # oldest first
        s_t = stds[-1]
        if not s_t > 0:
            self._raw_value = float("nan")
            return
        rank = sum(1 for x in stds if x <= s_t) / float(self.lookback)
        fall = max(0.0, -float(r[-1]) / s_t)
        self._raw_value = float(fall * rank)
        self.debug_info = {'return': float(r[-1]), 'std': s_t, 'fall': fall, 'rank': rank}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.lookback + self.vol_period


class VolumeWeightedScaledReturnComponent(SubStrategyComponent):
    """
    The bar's return in usual moves, weighted by the bar's volume against its average, on every bar:

        r(j)  = close[j] / close[j-1] - 1
        s     = std (ddof 1) of r(t - vol_period + 1) .. r(t)              (bar t's return included)
        z     = r(t) / s        (0 when s = 0)
        v     = volume[t] / mean(volume[t - volume_period + 1 .. t])       (bar t included)
        raw_value = z x v

    Graded, signed, unbounded: positive after a rise, negative after a fall. The size grows with the size of
    the move in the coin's usual moves and with how heavy the bar's volume was against its average. v is above
    0 and at most volume_period. The fall-positive reading is its mirror, given exactly by the `negate` step.
    Warm-up: max(vol_period + 1, volume_period) rows, bar t included.

    NaN: a NaN close in the last vol_period + 1 rows, or a NaN volume in the last volume_period rows, gives NaN.
    A mean volume not above 0 gives NaN (never seen on real bars). A flat return window (s = 0, never seen on
    real bars) gives 0. Building the component raises for a vol_period below 2 or a volume_period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last vol_period + 1 rows and the `volume`
    column of the last volume_period rows of data, all up to and including bar t (the last row). A bar's close
    and volume are known at that bar's close.
    """

    def __init__(self, name="VolumeWeightedScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"VolumeWeightedScaledReturnComponent: vol_period must be >= 2, got {self.vol_period}")
        self.volume_period = int(self.parameters.get("volume_period", 30))
        if self.volume_period < 2:
            raise ValueError(
                f"VolumeWeightedScaledReturnComponent: volume_period must be >= 2, got {self.volume_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float).iloc[-(self.vol_period + 1):].to_numpy()
        vol = data['volume'].astype(float).iloc[-self.volume_period:].to_numpy()
        if np.isnan(close).any() or np.isnan(vol).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = close[1:] / close[:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        den = float(vol.mean())
        if not den > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        ratio = float(vol[-1] / den)
        z = 0.0 if s == 0 else float(rets[-1] / s)
        self._raw_value = float(z * ratio)
        self.confidence = 1.0
        self.debug_info = {'scaled_return': z, 'volume_ratio': ratio, 'return_std': s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.vol_period + 1, self.volume_period)


class FallCloseLocationComponent(SubStrategyComponent):
    """
    The size of today's fall in usual moves, weighted by how near the close is to the bar's low:

        r(j)  = close[j] / close[j-1] - 1
        s     = std (ddof 1) of r(t - vol_period + 1) .. r(t)          (bar t's return included)
        fall  = max(0, -r(t) / s)                                       (0 when s = 0)
        loc   = (high[t] - close[t]) / (high[t] - low[t])               (0.5 when high[t] = low[t])
        raw_value = fall x loc

    Graded and one-sided. The value is 0 and up, unbounded above and never negative. It is 0 on up bars
    and on flat bars. It grows with the depth of the fall in usual moves and as the close nears the bar's
    low; loc is 0 to 1 on real bars. No direction.
    Warm-up: vol_period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads the `close` column of the last vol_period + 1 rows up to and including bar t
    (the last row of data), and the `high` and `low` of bar t only; all are known at bar t's close.

    NaN: a NaN close in the last vol_period + 1 rows, or a NaN high or low on bar t, gives NaN. A base close
    that is not above 0 also gives NaN. A flat return window (s = 0, never seen on real bars) gives 0.
    Building the component raises for a vol_period below 2.
    """

    def __init__(self, name="FallCloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 60))
        if self.vol_period < 2:
            raise ValueError(f"FallCloseLocationComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float).iloc[-(self.vol_period + 1):].to_numpy()
        high = float(data['high'].iloc[-1])
        low = float(data['low'].iloc[-1])
        if np.isnan(close).any() or np.isnan(high) or np.isnan(low):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        prev = close[:-1]
        if not (prev > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = close[1:] / prev - 1.0
        s = float(np.std(rets, ddof=1))
        r = float(rets[-1])
        z = -r / s if s > 0 else 0.0
        fall = z if z > 0 else 0.0
        rng = high - low
        loc = 0.5 if rng == 0 else (high - float(close[-1])) / rng
        self._raw_value = float(fall * loc)
        self.confidence = 1.0
        self.debug_info = {'return': r, 'std': s, 'fall_usual_moves': fall, 'close_location_from_high': loc}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.vol_period + 1


class StallUnderHighCountComponent(SubStrategyComponent):
    """
    How many of the last `window` bars closed just under their prior high:

        H(i) = max(close[i - period] .. close[i - 1])          (bar i excluded)
        stall(i) = 1 if close[i] < H(i) and (H(i) - close[i]) / H(i) x 100 <= band, else 0
        raw_value = sum of stall(i) for i = t - window + 1 .. t

    Range: 0 to window (integers), never negative, no direction. 0 when no bar of the window sat in the band
    under its prior high, window when every bar did. A bar at or above its prior high (a new closing high) is
    not counted, and neither is a bar more than `band` percent below it.
    Warm-up: window + period rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data, the last
    of which is bar t; each H(i) uses the closes strictly before bar i, and i <= t.

    NaN: a NaN close anywhere in the last window + period rows gives NaN; an H(i) not above 0 gives NaN (never on
    real bars). A missing `close` column raises.
    Building the component raises for a window below 1, a period below 2, or a band not above 0.
    """

    def __init__(self, name="StallUnderHighCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 60))
        if self.window < 1:
            raise ValueError(f"StallUnderHighCountComponent: window must be >= 1, got {self.window}")
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"StallUnderHighCountComponent: period must be >= 2, got {self.period}")
        self.band = float(self.parameters.get("band", 10.0))
        if not self.band > 0:
            raise ValueError(f"StallUnderHighCountComponent: band must be above 0, got {self.band}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        count = 0
        for k in range(self.window):
            idx = self.period + k
            h = float(np.max(c[k:idx]))
            if not h > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            x = float(c[idx])
            if x < h and (h - x) / h * 100.0 <= self.band:
                count += 1
        self._raw_value = float(count)
        self.confidence = 1.0
        self.debug_info = {'stall_count': count, 'band': self.band}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period


class VolatilityRatioToAverageComponent(SubStrategyComponent):
    """
    The current return volatility against its own recent average, on every bar:

        r[j]  = close[j] / close[j-1] - 1
        s(i)  = std (ddof 1) of r[i - vol_period + 1 .. i]       (vol_period returns ending at bar i, r[i] included)
        raw_value = s(t) / mean(s(t - vol_lookback + 1) .. s(t))

    Range: 0 and up, at most vol_lookback (the mean includes s(t)), never negative. There is no direction. The value is
    1 when the current volatility equals its mean over the lookback, above 1 when it is higher and below 1 when it is
    lower. It is graded: it grows continuously with the current volatility.
    Warm-up: vol_lookback + vol_period rows, bar t included (80 at the defaults).

    NaN: a NaN close anywhere in the last vol_lookback + vol_period rows gives NaN. A mean of s equal to 0 (every
    return window flat, never seen on real bars) gives NaN. A missing `close` column raises.
    Building the component raises for a vol_period below 2 or a vol_lookback below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last vol_lookback + vol_period rows of data, the last
    of which is bar t; a bar's close is known at that bar's close.
    """

    def __init__(self, name="VolRatioToAvg", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"VolatilityRatioToAverageComponent: vol_period must be >= 2, got {self.vol_period}")
        self.vol_lookback = int(self.parameters.get("vol_lookback", 60))
        if self.vol_lookback < 1:
            raise ValueError(f"VolatilityRatioToAverageComponent: vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[1:] / c[:-1] - 1.0
        stds = trailing_return_stds(self, r, self.vol_period, self.vol_lookback)
        s_t = stds[0]
        avg = float(np.mean(stds))
        if np.isnan(s_t) or np.isnan(avg) or not avg > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(s_t / avg)
        self.confidence = 1.0
        self.debug_info = {'current_std': s_t, 'mean_std': avg}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.vol_lookback + self.vol_period


class RankWeightedScaledMoveComponent(SubStrategyComponent):
    """
    The day's move against the coin's mean absolute move, weighted by how low today's volatility ranks:

        r(j)  = close[j] / close[j-1] - 1
        m     = mean(abs(r(j))) over j = t-abs_period+1 .. t
        s(i)  = std (ddof 1) of r(i-vol_period+1) .. r(i)
        rank  = (number of i in t-lookback+1 .. t with s(i) <= s(t)) / lookback
        raw_value = r(t) / m x (1 - rank)        (r(t) / m taken as 0 when m = 0)

    Range and sign: signed like the day's move. Its size is at most abs_period x (1 - 1/lookback), because
    |r(t)| <= abs_period x m and the rank counts s(t) itself. It grows with the move in mean absolute moves and as
    the volatility rank falls; it tends to 0 when today's volatility ranks highest. Graded.
    Warm-up: max(lookback + vol_period, abs_period + 1) rows, bar t included (120 at the defaults).
    NaN: a NaN close in those rows gives NaN. A flat window (m = 0, never seen on real bars) gives 0.
    Building the component raises for abs_period < 1, vol_period < 2 or lookback < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(lookback + vol_period, abs_period + 1)
    rows of data, the last row being bar t; every return used ends at or before bar t.
    """

    def __init__(self, name="RankWeightedScaledMove", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.abs_period = int(self.parameters.get("abs_period", 60))
        if self.abs_period < 1:
            raise ValueError(f"RankWeightedScaledMoveComponent: abs_period must be >= 1, got {self.abs_period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"RankWeightedScaledMoveComponent: vol_period must be >= 2, got {self.vol_period}")
        self.lookback = int(self.parameters.get("lookback", 100))
        if self.lookback < 2:
            raise ValueError(f"RankWeightedScaledMoveComponent: lookback must be >= 2, got {self.lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).iloc[-n:].to_numpy()
        self.confidence = 1.0
        if np.isnan(c).any():
            self._raw_value = float("nan")
            return
        r = c[1:] / c[:-1] - 1.0
        if np.isnan(r).any() or np.isinf(r).any():
            self._raw_value = float("nan")
            return
        r_t = float(r[-1])
        m = float(np.mean(np.abs(r[-self.abs_period:])))
        move = 0.0 if m == 0 else r_t / m
        stds = trailing_return_stds(self, r, self.vol_period, self.lookback)
        s_t = stds[0]
        rank = float(sum(1 for s in stds if s <= s_t)) / self.lookback
        self._raw_value = float(move * (1.0 - rank))
        self.debug_info = {'move_in_mean_abs': move, 'mean_abs_return': m, 'std_t': s_t, 'vol_rank': rank}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.lookback + self.vol_period, self.abs_period + 1)


class RiseBeyondLargestMovesComponent(SubStrategyComponent):
    """
    The part of a window's log rise that its k largest up-bars do not account for, on every bar:

        R = ln(close[t]) - ln(close[t - period])                      (the period-bar log return)
        r_j = ln(close[j]) - ln(close[j - 1]),  j = t - period + 1 .. t
        T = sum of the k largest positive r_j (all positive r_j if fewer than k are positive; 0 if none)
        raw_value = max(0, R - T)

    This is the same value as max(R, 0) x (1 - min(T / R, 1)) for R > 0, and 0 for R <= 0, because T >= 0.
    Graded, no direction: 0 and up, never negative, at most R. It is 0 when the window did not rise or when
    its k biggest up-bars carry all of the rise. It grows as the rise gets larger and less of it sits in those bars.
    Units: natural-log return.
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close in the last period + 1 rows gives NaN. A close that is not above 0 there gives NaN
    (never seen on real bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, or a k of period or more (with every bar
    counted, T >= R and the output would be 0 on every bar).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t (the last
    row) included. No later row exists in the data it is given.
    """

    def __init__(self, name="RiseBeyondLargestMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"RiseBeyondLargestMovesComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k >= self.period:
            raise ValueError(
                f"RiseBeyondLargestMovesComponent: k must be between 1 and period - 1, got {self.k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        logc = np.log(c)
        lr = np.diff(logc)
        total_rise = float(logc[-1] - logc[0])
        pos = np.sort(lr[lr > 0])[::-1][:self.k]
        top = float(pos.sum()) if pos.size else 0.0
        self._raw_value = float(max(0.0, total_rise - top))
        self.confidence = 1.0
        self.debug_info = {'log_rise': total_rise, 'top_k_up_sum': top}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1


class LossShareBeyondLargestComponent(SubStrategyComponent):
    """
    Share of a window's summed one-bar losses not carried by its k largest losses, signed by the window's net return:

        r[j] = close[j] / close[j-1] - 1,                 j = t-period+1 .. t
        losses = { -r[j] : r[j] < 0 }
        L = sum(losses)
        T = sum of the k largest losses (all of them if there are k or fewer)
        S = 1 - T / L    (S = 0 when there are k or fewer losses, which includes L = 0)
        raw_value = sign(close[t] / close[t-period] - 1) x S

    Range: -1 to +1, exclusive. The value is negative over a net fall, positive over a net rise and 0 when the net
    return is 0. Its size is 0 when the k biggest losing bars carry all the losses. It grows towards 1 as the
    losses spread over many small bars.
    Graded: S is continuous in the closes. The sign flips where the net return crosses 0.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN close in the last period + 1 rows gives NaN. A close not above 0 there also gives NaN (never on
    real bars).
    Building the component raises for period < 2, k < 1, or k >= period (every return counted: always 0).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, which end at bar t
    (the last row); a bar's close is known at that bar's close.
    """

    def __init__(self, name="LossShareBeyondLargest", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"LossShareBeyondLargestComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1:
            raise ValueError(f"LossShareBeyondLargestComponent: k must be >= 1, got {self.k}")
        if self.k >= self.period:
            raise ValueError(
                f"LossShareBeyondLargestComponent: k must be below period, got k={self.k}, period={self.period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data["close"].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[1:] / c[:-1] - 1.0
        losses = -r[r < 0]
        if len(losses) <= self.k:
            share = 0.0
        else:
            total = float(losses.sum())
            top = float(np.sort(losses)[::-1][:self.k].sum())
            share = max(0.0, 1.0 - top / total) if total > 0 else 0.0
        net = c[-1] / c[0] - 1.0
        self._raw_value = float(np.sign(net) * share)
        self.confidence = 1.0
        self.debug_info = {"loss_count": int(len(losses)), "share": share, "net_return": float(net)}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1


class TopGainsShareOfRiseComponent(SubStrategyComponent):
    """
    How much of the window's net rise its few largest up-bars carry, on every bar:

        R = close[t] / close[t - period] - 1                       (net simple rise)
        r[j] = close[j] / close[j - 1] - 1,  j = t - period + 1 .. t
        T = sum of the k largest r[j] > 0 (all the positive ones if there are fewer than k)
        share = min(T / R, 1) if R > 0 else 0
        form = "share" (default): raw_value = share
        form = "residual":        raw_value = 1 - share if R > 0 else 0

    The default "share" is the original output, unchanged. It runs 0 to 1, never negative, with no direction.
    It is near 0 for a grind of many small up-bars, 1 when the k largest up-bars carry the whole rise or more,
    and 0 when the window did not rise.
    "residual" runs 0 to below 1, never negative, with no direction. A rise needs at least one positive
    return, so T > 0. It is 0 when the window did not rise or when the top k up-bars carry the whole rise, and
    it grows towards 1 as the rise is spread over many small up-bars. It is continuous in the closes,
    including where R crosses 0.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t (the
    last row) included; a bar's close is known at that bar's close.

    NaN: a NaN close in the last period + 1 rows gives NaN. A close not above 0 there gives NaN (never on real
    bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, a k >= period, or a form other than
    "share" or "residual".
    """

    def __init__(self, name="TopGainsShareOfRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopGainsShareOfRiseComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1:
            raise ValueError(f"TopGainsShareOfRiseComponent: k must be >= 1, got {self.k}")
        if self.k >= self.period:
            raise ValueError(
                f"TopGainsShareOfRiseComponent: k must be below period, got k={self.k}, period={self.period}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "residual"):
            raise ValueError(
                f"TopGainsShareOfRiseComponent: form must be 'share' or 'residual', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rise = float(c[-1] / c[0] - 1.0)
        rets = c[1:] / c[:-1] - 1.0
        pos = np.sort(rets[rets > 0])[::-1][:self.k]
        top = float(pos.sum()) if pos.size else 0.0
        if rise > 0:
            share = min(top / rise, 1.0)
            value = share if self.form == "share" else 1.0 - share
        else:
            share = 0.0
            value = 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'net_rise': rise, 'top_gains': top, 'share': share, 'form': self.form}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1


class TopLossesShareOfFallComponent(SubStrategyComponent):
    """
    How much of the window's net fall its k largest one-bar losses make up, on every bar:

        F = close[t - period] - close[t]                                (the net fall, price units)
        losses = close[j-1] - close[j] for j = t-period+1 .. t where that change is > 0
        T = sum of the k largest losses (all of them if there are fewer than k)
        form = "share" (default):  raw_value = T / F                          if F > 0, else 0.0
        form = "weighted":         raw_value = (T / F) * (F / close[t-period] * 100)   if F > 0, else 0.0

    Graded, never negative, no direction (a long-only rebound reading). "share" is near k / period for a fall
    spread evenly over many bars. It reaches 1 or more when a few bars carry the whole fall, or when gains offset
    part of it. It is 0 when the window did not fall, and it grows without bound as a falling window's net fall
    nears 0. "weighted" adds the size of the fall: it is the top losses as a percent of the window's first close.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data (bars t-period .. t),
    the last row being bar t; each close is known at its bar's close.

    NaN: a NaN close in the last period + 1 rows gives NaN. With "weighted", a close[t-period] not above 0 gives NaN
    (never on real bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, or a form other than "share" or "weighted".
    """

    def __init__(self, name="TopLossesShareOfFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopLossesShareOfFallComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1:
            raise ValueError(f"TopLossesShareOfFallComponent: k must be >= 1, got {self.k}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "weighted"):
            raise ValueError(f"TopLossesShareOfFallComponent: form must be 'share' or 'weighted', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        fall = float(c[0] - c[-1])
        if not fall > 0:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {'net_fall': fall, 'top_losses': 0.0}
            return
        d = np.diff(c)
        losses = -d[d < 0]
        top = float(np.sort(losses)[::-1][:self.k].sum())
        share = top / fall
        if self.form == "weighted":
            if not c[0] > 0:
                self._raw_value = float("nan")
            else:
                self._raw_value = float(share * (fall / c[0] * 100.0))
        else:
            self._raw_value = float(share)
        self.confidence = 1.0
        self.debug_info = {'net_fall': fall, 'top_losses': top, 'share': share}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1


class TopVolumesShareComponent(SubStrategyComponent):
    """
    Share of the window's volume carried by its heaviest bars, on every bar:

        W = volume[t - period + 1 .. t]                     (bar t included)
        T = sum of the top_k largest values of W
        raw_value = T / sum(W)

    Range: top_k / period (every bar the same volume) up to 1 (all the volume in top_k bars); never negative;
    no direction. Graded: continuous in the volumes, growing as the volume bunches into a few bars.
    Warm-up: period rows, bar t included.

    NaN: a NaN volume anywhere in W gives NaN; a sum(W) not above 0 gives NaN (never on real bars, whose volume
    is positive). A missing `volume` column raises.
    Building the component raises for period < 2, top_k < 1, or top_k >= period.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the last `period` rows of data, the last row being
    bar t; a bar's volume is known at that bar's close.
    """

    def __init__(self, name="TopVolumesShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopVolumesShareComponent: period must be >= 2, got {self.period}")
        self.top_k = int(self.parameters.get("top_k", 3))
        if self.top_k < 1:
            raise ValueError(f"TopVolumesShareComponent: top_k must be >= 1, got {self.top_k}")
        if self.top_k >= self.period:
            raise ValueError(
                f"TopVolumesShareComponent: top_k must be below period, got top_k={self.top_k}, "
                f"period={self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        w = data['volume'].astype(float).iloc[-self.period:].to_numpy()
        if np.isnan(w).any():
            self._raw_value = float("nan")
        else:
            total = float(np.sum(w))
            if not total > 0:
                self._raw_value = float("nan")
            else:
                top = float(np.sum(np.sort(w)[-self.top_k:]))
                self._raw_value = float(top / total)
                self.debug_info = {'top_volume_sum': top, 'total_volume': total}
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period


class HoursToSettlementComponent(SubStrategyComponent):
    """
    The hours from the coming bar's start to the next funding settlement (00:00, 08:00, 16:00 UTC):

        spacing = timestamp[t] - timestamp[t-1]
        coming  = timestamp[t] + spacing                (the start of the coming bar)
        h       = UTC hour of coming
        raw_value = 8 - (h mod 8)

    Range: 1 to 8, integers, never negative, with no direction. It is 1 when the coming bar starts one hour
    before a settlement and 8 when it starts on a settlement. It grows the further the coming bar is from the
    next settlement.
    Warm-up: 2 rows (bar t and bar t-1, for the spacing).
    NaN: a NaN/NaT timestamp on bar t or t-1 gives NaN; a spacing not above 0 gives NaN (never on real bars).
    Naive timestamps are read as UTC. Numeric timestamps are read as epoch seconds, ms, us or ns by their size.

    WHY THIS CANNOT LEAK: it reads only the `timestamp` column of the last two rows (bar t-1 and bar t); the
    coming bar's start is bar t's stamp plus the spacing already seen, known at bar t's close.
    """

    def __init__(self, name="HoursToSettlement", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    @staticmethod
    def _seconds(x):
        if x is None:
            return float("nan")
        if isinstance(x, (bool, np.bool_)):
            return float("nan")
        if isinstance(x, (int, float, np.integer, np.floating)):
            v = float(x)
            if v != v:
                return float("nan")
            a = abs(v)
            if a > 1e17:
                return v / 1e9
            if a > 1e14:
                return v / 1e6
            if a > 1e11:
                return v / 1e3
            return v
        ts = pd.Timestamp(x)
        if pd.isna(ts):
            return float("nan")
        if ts.tzinfo is None:
            ts = ts.tz_localize("UTC")
        else:
            ts = ts.tz_convert("UTC")
        return ts.value / 1e9

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        s_prev = self._seconds(data["timestamp"].iloc[-2])
        s_now = self._seconds(data["timestamp"].iloc[-1])
        if np.isnan(s_prev) or np.isnan(s_now) or not (s_now - s_prev) > 0:
            self._raw_value = float("nan")
        else:
            coming = s_now + (s_now - s_prev)
            hour = int(np.floor(coming / 3600.0)) % 24
            self._raw_value = float(8 - (hour % 8))
            self.debug_info = {"coming_hour_utc": hour, "spacing_seconds": s_now - s_prev}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return 2


class HourOfDayComponent(SubStrategyComponent):
    """
    The UTC hour of the coming bar's start:

        spacing = timestamp[t] - timestamp[t-1]
        next    = timestamp[t] + spacing
        raw_value = hour of `next` in UTC, 0 .. 23

    Range: integers 0 to 23, never negative. It carries no direction. It rises by one each hour and
    returns from 23 to 0 at midnight UTC. It is a calendar regime measure for a rule such as
    `between` 21.5 and 23.5 (coming bars stamped 22:00 and 23:00). It is not a bet in itself.
    On 1d bars stamped at hour 0 it reads 0 on every bar.
    Warm-up: 2 rows (bars t-1 and t).
    NaN: a NaN/NaT timestamp on bar t or t-1 gives NaN. A spacing not above 0 gives NaN (never on real bars).
    Naive timestamps are read as UTC. Numeric timestamps are read as epoch seconds, ms, µs or ns by size.

    WHY THIS CANNOT LEAK: it reads only the `timestamp` column of the last two rows (bars t-1 and t). Both are
    known at bar t's close, and the coming bar's start is extrapolated from them without reading any later row.
    """

    _NS_PER_HOUR = 3_600_000_000_000

    def __init__(self, name="HourOfDay", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    @staticmethod
    def _to_ns(x):
        if x is None:
            return None
        if isinstance(x, (int, float, np.integer, np.floating)) and not isinstance(x, bool):
            v = float(x)
            if v != v:
                return None
            a = abs(v)
            if a < 1e11:
                return int(round(v * 1e9))
            if a < 1e14:
                return int(round(v * 1e6))
            if a < 1e17:
                return int(round(v * 1e3))
            return int(v)
        ts = pd.Timestamp(x)
        if pd.isna(ts):
            return None
        if ts.tz is None:
            ts = ts.tz_localize("UTC")
        return int(ts.value)

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n0 = self._to_ns(data['timestamp'].iloc[-2])
        n1 = self._to_ns(data['timestamp'].iloc[-1])
        if n0 is None or n1 is None or not (n1 - n0) > 0:
            self._raw_value = float("nan")
        else:
            nxt = n1 + (n1 - n0)
            self._raw_value = float((nxt // self._NS_PER_HOUR) % 24)
        self.confidence = 1.0
        self.debug_info = {'hour_of_coming_bar': self._raw_value}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return 2


class NarrowRangeBreakoutComponent(SubStrategyComponent):
    """
    A break out of a narrow stretch, scaled by how narrow the stretch is, on every bar:

        stretch = bars t-period .. t-1                      (bar t excluded)
        H = max(high over the stretch), L = min(low over the stretch), S = H - L
        B = mean(high[i] - low[i]) over the last base_period bars, bar t included
        side = "above" (default): brk = max(0, close[t] - H)
        side = "below":           brk = max(0, L - close[t])
        raw_value = brk / close[t] x 100 x B / S            (0.0 when S = 0)

    Range & sign: 0 and up, unbounded above, never negative; no direction. "above" is 0 when the close is at or
    below the prior high. "below" is 0 when the close is at or above the prior low. Both grow with the size of
    the break and with how narrow the stretch is against the average bar range. side "above" is the original
    output, unchanged; use `negate` on "below" for a short-side forecast.
    Warm-up: max(base_period, period + 1) rows, bar t included.
    NaN: a NaN high or low in the stretch or in the last base_period rows, or a NaN close[t], gives NaN. A
    close[t] not above 0 gives NaN (never on real bars). S = 0 (period identical flat bars) gives 0.0.
    Building the component raises for a period below 1, a base_period below 1, or a side other than "above"
    or "below".

    WHY THIS CANNOT LEAK: it reads only the high, low and close of the rows up to and including bar t (the last
    row of data): highs and lows of the last max(base_period, period + 1) rows and the close of bar t, all known
    at bar t's close.
    """

    def __init__(self, name="NarrowRangeBreakout", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 12))
        if self.period < 1:
            raise ValueError(f"NarrowRangeBreakoutComponent: period must be >= 1, got {self.period}")
        self.base_period = int(self.parameters.get("base_period", 180))
        if self.base_period < 1:
            raise ValueError(f"NarrowRangeBreakoutComponent: base_period must be >= 1, got {self.base_period}")
        side = self.parameters.get("side", "above")
        if side not in ("above", "below"):
            raise ValueError(f"NarrowRangeBreakoutComponent: side must be 'above' or 'below', got {side!r}")
        self.side = side
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close_t = float(data['close'].astype(float).to_numpy()[-1])
        sh = high[-(self.period + 1):-1]
        sl = low[-(self.period + 1):-1]
        bh = high[-self.base_period:]
        bl = low[-self.base_period:]
        if (np.isnan(sh).any() or np.isnan(sl).any() or np.isnan(bh).any() or np.isnan(bl).any()
                or np.isnan(close_t)):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if not close_t > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        hi = float(np.max(sh))
        lo = float(np.min(sl))
        s = hi - lo
        b = float(np.mean(bh - bl))
        if s == 0:
            value = 0.0
            brk = 0.0
        else:
            if self.side == "below":
                brk = max(0.0, lo - close_t)
            else:
                brk = max(0.0, close_t - hi)
            value = brk / close_t * 100.0 * b / s
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'prior_high': hi, 'prior_low': lo, 'stretch_range': s,
                           'mean_bar_range': b, 'break': brk, 'side': self.side}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.base_period, self.period + 1)


class BreakoutInMeanRangesComponent(SubStrategyComponent):
    """
    The close's distance beyond or under a high, counted in mean bar ranges, on every bar:

        stretch:  high_current = 0 (default): H = max(high[t - period .. t - 1])    (bar t excluded)
                  high_current = 1:           H = max(high[t - period + 1 .. t])    (bar t included)
        base:     base_exclude_current = 0 (default): B = mean(high[i] - low[i]), i = t - base_period + 1 .. t
                  base_exclude_current = 1:           B = mean(high[i] - low[i]), i = t - base_period .. t - 1
        side = "above" (default): raw_value = max(0, close[t] - H) / B
        side = "below":           raw_value = max(0, H - close[t]) / B
        raw_value = 0.0 when B = 0

    The defaults (side "above", high_current 0, base_exclude_current 0) are the original output, unchanged.
    With period 1, base_period 20, side "below", high_current 1 and base_exclude_current 1 the output is
    (high[t] - close[t]) / mean(high[i] - low[i], i = t-20 .. t-1): 0 with the close at the bar's high, growing
    as the close sits lower in a bar whose range is wide against the prior 20 bars' mean range.
    Range: 0 and up, unbounded above, never negative; no direction; graded (linear in the close).
    Warm-up: max(base_period + base_exclude_current, period + 1 - high_current) rows, bar t included.
    NaN: a NaN high in the stretch, a NaN high or low in the base rows, or a NaN close[t] gives NaN.
    B = 0 (base_period zero-range bars in a row, never on real bars) reads 0.0.
    Building the component raises for period < 1, base_period < 1, a side other than "above" or "below",
    a high_current or base_exclude_current other than 0 or 1.

    WHY THIS CANNOT LEAK: it reads only the high, low and close of the rows up to and including bar t (the last
    row of data): highs of bars t-period .. t, lows and highs of bars t-base_period-1 .. t at most, and close[t].
    """

    def __init__(self, name="BreakoutInMeanRanges", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 12))
        if self.period < 1:
            raise ValueError(f"BreakoutInMeanRangesComponent: period must be >= 1, got {self.period}")
        self.base_period = int(self.parameters.get("base_period", 180))
        if self.base_period < 1:
            raise ValueError(f"BreakoutInMeanRangesComponent: base_period must be >= 1, got {self.base_period}")
        self.side = self.parameters.get("side", "above")
        if self.side not in ("above", "below"):
            raise ValueError(f"BreakoutInMeanRangesComponent: side must be 'above' or 'below', got {self.side!r}")
        hc = self.parameters.get("high_current", 0)
        if isinstance(hc, bool):
            hc = int(hc)
        if hc not in (0, 1):
            raise ValueError(f"BreakoutInMeanRangesComponent: high_current must be 0 or 1, got {hc!r}")
        self.high_current = int(hc)
        bx = self.parameters.get("base_exclude_current", 0)
        if isinstance(bx, bool):
            bx = int(bx)
        if bx not in (0, 1):
            raise ValueError(f"BreakoutInMeanRangesComponent: base_exclude_current must be 0 or 1, got {bx!r}")
        self.base_exclude_current = int(bx)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        n = len(close)
        if self.high_current == 1:
            stretch = high[n - self.period:n]
        else:
            stretch = high[n - 1 - self.period:n - 1]
        b_stop = n - self.base_exclude_current
        b_start = b_stop - self.base_period
        bh = high[b_start:b_stop]
        bl = low[b_start:b_stop]
        c = close[-1]
        if np.isnan(stretch).any() or np.isnan(bh).any() or np.isnan(bl).any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(np.max(stretch))
        B = float(np.mean(bh - bl))
        if B == 0:
            value = 0.0
        elif self.side == "above":
            value = max(0.0, c - H) / B
        else:
            value = max(0.0, H - c) / B
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'H': H, 'B': B, 'close': float(c), 'side': self.side,
                           'high_current': self.high_current, 'base_exclude_current': self.base_exclude_current}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.base_period + self.base_exclude_current, self.period + 1 - self.high_current)


class NarrowRangeBreakoutRangeRatioComponent(SubStrategyComponent):
    """
    A narrow-range upward breakout, weighted by how quiet the recent bars are against the long average bar range:

        H = max(high[t-period .. t-1])                  (the stretch, bar t excluded)
        S = H - min(low[t-period .. t-1])
        B = mean(high[i] - low[i]) over the last base_period bars, bar t included
        L = mean(high[i] - low[i]) over the last ratio_long_period bars, bar t included
        Q = mean(high[i] - low[i]) over the last ratio_short_period bars, bar t included
        raw_value = max(0, close[t] - H) / close[t] x 100 x B / S x L / Q
        raw_value = 0.0 when S = 0 or Q = 0

    This equals NarrowRangeBreakoutComponent(period, base_period) x L / Q.
    Range and sign: 0 and up, unbounded above, never negative, no direction. It is 0 when the close is at or below
    the prior high. It grows with the size of the break, the narrowness of the stretch, and the quietness of the
    last ratio_short_period bars against the last ratio_long_period bars.
    Graded: continuous in the close at the prior high.
    Warm-up: max(base_period, period + 1, ratio_long_period) rows, bar t included (360 at the defaults).

    NaN: a NaN high or low in any row read, or a NaN close[t], gives NaN. A close[t] not above 0 gives NaN.
    Building the component raises for a period, base_period or ratio_short_period below 1, and for a
    ratio_short_period at or above ratio_long_period.

    WHY THIS CANNOT LEAK: it reads only the high, low and close columns of the last
    max(base_period, period + 1, ratio_long_period) rows of data, bar t (the last row) included. The stretch uses
    rows t-period .. t-1. Every value it reads is known at bar t's close.
    """

    def __init__(self, name="NarrowRangeBreakoutRangeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 12))
        self.base_period = int(self.parameters.get("base_period", 180))
        self.ratio_long_period = int(self.parameters.get("ratio_long_period", 360))
        self.ratio_short_period = int(self.parameters.get("ratio_short_period", 42))
        if self.period < 1:
            raise ValueError(f"NarrowRangeBreakoutRangeRatioComponent: period must be >= 1, got {self.period}")
        if self.base_period < 1:
            raise ValueError(
                f"NarrowRangeBreakoutRangeRatioComponent: base_period must be >= 1, got {self.base_period}")
        if self.ratio_short_period < 1:
            raise ValueError(
                f"NarrowRangeBreakoutRangeRatioComponent: ratio_short_period must be >= 1, "
                f"got {self.ratio_short_period}")
        if self.ratio_short_period >= self.ratio_long_period:
            raise ValueError(
                f"NarrowRangeBreakoutRangeRatioComponent: ratio_short_period must be below ratio_long_period, "
                f"got {self.ratio_short_period} and {self.ratio_long_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data["high"].astype(float).to_numpy()
        low = data["low"].astype(float).to_numpy()
        close_t = float(data["close"].astype(float).to_numpy()[-1])
        p = self.period
        st_h = high[-(p + 1):-1]
        st_l = low[-(p + 1):-1]
        rng = high - low
        b_win = rng[-self.base_period:]
        l_win = rng[-self.ratio_long_period:]
        q_win = rng[-self.ratio_short_period:]
        if (np.isnan(close_t) or np.isnan(st_h).any() or np.isnan(st_l).any()
                or np.isnan(b_win).any() or np.isnan(l_win).any() or np.isnan(q_win).any()):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if not close_t > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(np.max(st_h))
        S = H - float(np.min(st_l))
        B = float(np.mean(b_win))
        L = float(np.mean(l_win))
        Q = float(np.mean(q_win))
        brk = max(0.0, close_t - H)
        if S <= 0 or Q <= 0:
            value = 0.0
        else:
            value = brk / close_t * 100.0 * B / S * L / Q
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"prior_high": H, "stretch_range": S, "base_mean_range": B,
                           "long_mean_range": L, "short_mean_range": Q}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.base_period, self.period + 1, self.ratio_long_period)


class MeanBarRangeRatioComponent(SubStrategyComponent):
    """
    Long-run average bar range against the recent average bar range, on every bar:

        L = mean(high[i] - low[i]) for i = t - long_period + 1 .. t     (bar t included)
        Q = mean(high[i] - low[i]) for i = t - short_period + 1 .. t    (bar t included)
        raw_value = L / Q

    Range and sign: short_period / long_period and up, unbounded above, never negative, no direction. The short
    window lies inside the long one, so L >= Q x short_period / long_period. The value is 1 when the recent bars are
    as wide as the long average, grows as the recent bars get quieter, and falls below 1 as they get wider. Graded:
    continuous in the highs and lows.
    Warm-up: long_period rows, bar t included.

    NaN: a NaN high or low in the last long_period rows gives NaN. Q = 0 needs short_period zero-range bars in a
    row (never seen on real bars) and gives NaN. A missing column raises.
    Building the component raises for a short_period below 1 or a short_period at or above long_period.

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the last long_period rows of data, the last
    of which is bar t; a bar's high and low are known at that bar's close.
    """

    def __init__(self, name="MeanBarRangeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.long_period = int(self.parameters.get("long_period", 360))
        self.short_period = int(self.parameters.get("short_period", 42))
        if self.short_period < 1:
            raise ValueError(f"MeanBarRangeRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"MeanBarRangeRatioComponent: short_period must be below long_period, got "
                f"{self.short_period} >= {self.long_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).iloc[-self.long_period:].to_numpy()
        low = data['low'].astype(float).iloc[-self.long_period:].to_numpy()
        rng = high - low
        if np.isnan(rng).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        long_mean = float(rng.mean())
        short_mean = float(rng[-self.short_period:].mean())
        if not short_mean > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(long_mean / short_mean)
        self.confidence = 1.0
        self.debug_info = {'long_mean_range': long_mean, 'short_mean_range': short_mean}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.long_period




class IchimokuCloudPositionComponent(SubStrategyComponent):
    """
    Where the close sits against the Ichimoku cloud, on every bar.

        e = t - displacement
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A = (M(tenkan_period) + M(kijun_period)) / 2,  B = M(senkou_period)
        top = max(A, B),  bottom = min(A, B)

        edge = "top" (default):  d = close[t] - top,  edge value = top
        edge = "nearest":        d = close[t] - top     (edge value top)    when close[t] > top
                                 d = close[t] - bottom  (edge value bottom) when close[t] < bottom
                                 d = 0                  (edge value bottom) when bottom <= close[t] <= top

        base = "edge" (default): raw_value = d / edge value x 100
        base = "close":          raw_value = d / close[t] x 100

    The defaults ("top", "edge") give the original output, unchanged.
    Range: with base "edge" it is -100 and up; with base "close" it is below +100 and unbounded below.
    Signed: positive above the cloud. With "nearest" it is negative below the cloud and 0 inside it, and it is
    continuous at both edges. Graded.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement rows, bar t included.

    NaN: a NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN. A divisor that is not
    above 0 gives NaN; this never happens on real bars.
    Building raises for any period < 1, a displacement < 0, an edge other than "top" or "nearest", or a base
    other than "edge" or "close".

    WHY THIS CANNOT LEAK: it reads the high and low of rows up to bar e = t - displacement, and the close of
    bar t, the last row of data. It reads no row after t.
    """

    def __init__(self, name="IchimokuCloudPosition", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        for nm, p in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if p < 1:
                raise ValueError(f"IchimokuCloudPositionComponent: {nm} must be >= 1, got {p}")
        if self.displacement < 0:
            raise ValueError(f"IchimokuCloudPositionComponent: displacement must be >= 0, got {self.displacement}")
        self.edge = self.parameters.get("edge", "top")
        if self.edge not in ("top", "nearest"):
            raise ValueError(f"IchimokuCloudPositionComponent: edge must be 'top' or 'nearest', got {self.edge!r}")
        self.base = self.parameters.get("base", "edge")
        if self.base not in ("edge", "close"):
            raise ValueError(f"IchimokuCloudPositionComponent: base must be 'edge' or 'close', got {self.base!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        h = data['high'].astype(float).to_numpy()
        lo = data['low'].astype(float).to_numpy()
        c = float(data['close'].astype(float).iloc[-1])
        e = len(data) - 1 - self.displacement

        def mid(p):
            hw = h[e - p + 1:e + 1]
            lw = lo[e - p + 1:e + 1]
            if np.isnan(hw).any() or np.isnan(lw).any():
                return float("nan")
            return (float(hw.max()) + float(lw.min())) / 2.0

        a = (mid(self.tenkan_period) + mid(self.kijun_period)) / 2.0
        b = mid(self.senkou_period)
        self.confidence = 1.0
        if np.isnan(a) or np.isnan(b) or np.isnan(c):
            self._raw_value = float("nan")
            return
        top = max(a, b)
        bottom = min(a, b)
        if self.edge == "top":
            d, ref = c - top, top
        elif c > top:
            d, ref = c - top, top
        elif c < bottom:
            d, ref = c - bottom, bottom
        else:
            d, ref = 0.0, bottom
        div = ref if self.base == "edge" else c
        if not div > 0:
            self._raw_value = float("nan")
            return
        self._raw_value = float(d / div * 100.0)
        self.debug_info = {'span_a': a, 'span_b': b, 'top': top, 'bottom': bottom,
                           'edge': self.edge, 'base': self.base}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement


class IchimokuCloudSlopeComponent(SubStrategyComponent):
    """
    The slope of the Ichimoku cloud's mid level over `lookback` bars, on every bar:

        for a bar i, e = i - displacement and
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A(i) = (M(tenkan_period) + M(kijun_period)) / 2,  B(i) = M(senkou_period)
        C(i) = (A(i) + B(i)) / 2                       (the leading spans plotted at bar i)
        S = (C(t) - C(t - lookback)) / C(t - lookback) x 100
        form = "percent" (default):  raw_value = S
        form = "proximity":          raw_value = 1 / (1 + D),  D = max(0, -S)

    Range and sign. With "percent" the value is -100 and up, unbounded above, and signed. It is positive while the
    cloud's mid level rises, negative while it falls. With "proximity" it runs above 1/101 up to 1 and is never
    negative. It is 1 when the cloud is flat or rising and shrinks toward 0 as the cloud falls faster. Graded, and
    continuous in the highs and lows. The default "percent" is the original output, unchanged.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement + lookback rows, bar t included.

    NaN: a NaN high or low in any window used for C(t) or C(t - lookback) gives NaN. A C(t - lookback) not above 0
    gives NaN, which never happens on real bars.
    Building the component raises for any period below 1, a displacement below 0, a lookback below 1, or a form
    other than "percent" or "proximity".

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of rows up to bar t - displacement (the last
    row of data is bar t), over windows ending at bars t - displacement and t - lookback - displacement; it never
    reads a row after bar t.
    """

    def __init__(self, name="IchimokuCloudSlope", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        for label, p in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                         ("senkou_period", self.senkou_period)):
            if p < 1:
                raise ValueError(f"IchimokuCloudSlopeComponent: {label} must be >= 1, got {p}")
        self.displacement = int(self.parameters.get("displacement", 26))
        if self.displacement < 0:
            raise ValueError(f"IchimokuCloudSlopeComponent: displacement must be >= 0, got {self.displacement}")
        self.lookback = int(self.parameters.get("lookback", 26))
        if self.lookback < 1:
            raise ValueError(f"IchimokuCloudSlopeComponent: lookback must be >= 1, got {self.lookback}")
        self.form = self.parameters.get("form", "percent")
        if self.form not in ("percent", "proximity"):
            raise ValueError(
                f"IchimokuCloudSlopeComponent: form must be 'percent' or 'proximity', got {self.form!r}")
        self._raw_value = 0.0

    @staticmethod
    def _mid(high, low, e, p):
        h = high[e - p + 1:e + 1]
        l = low[e - p + 1:e + 1]
        if np.isnan(h).any() or np.isnan(l).any():
            return float("nan")
        return (float(np.max(h)) + float(np.min(l))) / 2.0

    def _cloud_mid(self, high, low, i):
        e = i - self.displacement
        m_t = self._mid(high, low, e, self.tenkan_period)
        m_k = self._mid(high, low, e, self.kijun_period)
        m_s = self._mid(high, low, e, self.senkou_period)
        a = (m_t + m_k) / 2.0
        return (a + m_s) / 2.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        t = len(high) - 1
        c_now = self._cloud_mid(high, low, t)
        c_then = self._cloud_mid(high, low, t - self.lookback)
        if np.isnan(c_now) or np.isnan(c_then) or not c_then > 0:
            self._raw_value = float("nan")
        else:
            s = (c_now - c_then) / c_then * 100.0
            if self.form == "proximity":
                d = max(0.0, -s)
                self._raw_value = float(1.0 / (1.0 + d))
            else:
                self._raw_value = float(s)
        self.confidence = 1.0
        self.debug_info = {'cloud_mid_now': c_now, 'cloud_mid_then': c_then, 'form': self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement + self.lookback


class IchimokuCloudWidthComponent(SubStrategyComponent):
    """
    Thickness of the Ichimoku cloud plotted at bar t, against the current close:

        e = t - displacement
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A = (M(tenkan_period) + M(kijun_period)) / 2          (leading span A plotted at bar t)
        B = M(senkou_period)                                  (leading span B plotted at bar t)
        W = abs(A - B) / close[t] x 100
        form = "width" (default):  raw_value = W
        form = "proximity":        raw_value = 1 / (1 + W)

    "width": 0 and up, unbounded above, never negative, no direction; 0 when the spans meet.
    "proximity": above 0, up to 1, never negative, no direction; 1 when the spans meet, growing smoothly
    as the cloud thins against the price. The default "width" is the original output, unchanged.
    Graded and continuous in the highs and lows.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement rows, bar t included.

    NaN: a NaN high or low in any span window ending at bar e, or a NaN close[t], gives NaN; a close[t]
    not above 0 gives NaN (never on real bars). Building the component raises for any period below 1, a
    displacement below 0, or a form other than "width" or "proximity".

    WHY THIS CANNOT LEAK: the spans read only the high and low of bars up to e = t - displacement, and the
    divisor is close[t], the last row of data; no row after bar t is read.
    """

    def __init__(self, name="IchimokuCloudWidth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        for nm, p in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if p < 1:
                raise ValueError(f"IchimokuCloudWidthComponent: {nm} must be >= 1, got {p}")
        if self.displacement < 0:
            raise ValueError(
                f"IchimokuCloudWidthComponent: displacement must be >= 0, got {self.displacement}")
        self.form = self.parameters.get("form", "width")
        if self.form not in ("width", "proximity"):
            raise ValueError(
                f"IchimokuCloudWidthComponent: form must be 'width' or 'proximity', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        e = len(data) - 1 - self.displacement

        def mid(p):
            h = high[e - p + 1:e + 1]
            l = low[e - p + 1:e + 1]
            if np.isnan(h).any() or np.isnan(l).any():
                return float("nan")
            return (float(np.max(h)) + float(np.min(l))) / 2.0

        a = (mid(self.tenkan_period) + mid(self.kijun_period)) / 2.0
        b = mid(self.senkou_period)
        c = float(close[-1])
        if np.isnan(a) or np.isnan(b) or np.isnan(c) or not c > 0:
            self._raw_value = float("nan")
        else:
            w = abs(a - b) / c * 100.0
            self._raw_value = float(w) if self.form == "width" else float(1.0 / (1.0 + w))
        self.confidence = 1.0
        self.debug_info = {'span_a': a, 'span_b': b, 'close': c, 'form': self.form}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement


class IchimokuCloudCrossAgeComponent(SubStrategyComponent):
    """
    How long the close has stayed outside the Ichimoku cloud since it crossed through it from the other side:

        for each bar i: e = i - displacement
            M(p)   = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
            A      = (M(tenkan_period) + M(kijun_period)) / 2,  B = M(senkou_period)
            top    = max(A, B),  bottom = min(A, B)
            side(i) = +1 if close[i] > top, -1 if close[i] < bottom, 0 otherwise (inside or on an edge)
        sides are read for bars i = t-window+1 .. t
        s = side(t); n = number of consecutive bars ending at t with side s
        q = side of the nearest bar before that run (inside the window) whose side is not 0
        raw_value = s * min(n, max_bars)  if s != 0 and q == -s
                    0                     otherwise (inside the cloud, re-exit on the same side,
                                                     or no earlier outside bar in the window)

    Range: integers -max_bars .. +max_bars. Positive above the cloud after a cross up from below, negative
    below it after a cross down from above. Its size grows by one per bar spent on that side. A regime measure
    for rules (it jumps at a cross), not a forecast source.
    Warm-up: window + max(tenkan_period, kijun_period, senkou_period) + displacement - 1 rows (327 at the
    defaults), bar t included.
    NaN: a NaN high or low in any span window, or a NaN close, used for a side in the window gives NaN.

    WHY THIS CANNOT LEAK: it reads only the high, low and close columns of the last
    get_required_periods() rows of data, bar t (the last row) included. The cloud at bar i uses only bars up to
    i - displacement, and the side of bar i uses close[i]; no row after t is read.
    """

    def __init__(self, name="IchimokuCloudCrossAge", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        self.max_bars = int(self.parameters.get("max_bars", 120))
        self.window = int(self.parameters.get("window", 250))
        for nm, v in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if v < 1:
                raise ValueError(f"IchimokuCloudCrossAgeComponent: {nm} must be >= 1, got {v}")
        if self.displacement < 0:
            raise ValueError(f"IchimokuCloudCrossAgeComponent: displacement must be >= 0, got {self.displacement}")
        if self.max_bars < 1:
            raise ValueError(f"IchimokuCloudCrossAgeComponent: max_bars must be >= 1, got {self.max_bars}")
        if self.window <= self.max_bars:
            raise ValueError(
                f"IchimokuCloudCrossAgeComponent: window must be > max_bars, got {self.window} <= {self.max_bars}")
        self._offset = max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement - 1
        self._raw_value = 0.0

    @staticmethod
    def _mid(h, l, e, p):
        hw = h[e - p + 1:e + 1]
        lw = l[e - p + 1:e + 1]
        if np.isnan(hw).any() or np.isnan(lw).any():
            return float("nan")
        return (float(hw.max()) + float(lw.min())) / 2.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        rows = self.get_required_periods()
        h = data["high"].astype(float).to_numpy()[-rows:]
        l = data["low"].astype(float).to_numpy()[-rows:]
        c = data["close"].astype(float).to_numpy()[-rows:]
        sides = []
        for i in range(self._offset, rows):
            e = i - self.displacement
            a = (self._mid(h, l, e, self.tenkan_period) + self._mid(h, l, e, self.kijun_period)) / 2.0
            b = self._mid(h, l, e, self.senkou_period)
            ci = c[i]
            if np.isnan(a) or np.isnan(b) or np.isnan(ci):
                self._raw_value = float("nan")
                self.confidence = 1.0
                self.debug_info = {"nan": True}
                return
            top = max(a, b)
            bottom = min(a, b)
            if ci > top:
                sides.append(1)
            elif ci < bottom:
                sides.append(-1)
            else:
                sides.append(0)
        s = sides[-1]
        value = 0.0
        n = 0
        prior = 0
        if s != 0:
            j = len(sides) - 1
            while j >= 0 and sides[j] == s:
                n += 1
                j -= 1
            while j >= 0 and sides[j] == 0:
                j -= 1
            prior = sides[j] if j >= 0 else 0
            if prior == -s:
                value = float(s * min(n, self.max_bars))
        self._raw_value = value
        self.confidence = 1.0
        self.debug_info = {"side": s, "run": n, "prior_side": prior}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.window + self._offset


class IchimokuBelowCloudDistancePerWidthComponent(SubStrategyComponent):
    """
    Distance of the close below the Ichimoku cloud bottom, per (1 + cloud width), on every bar:

        e = t - displacement
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A = (M(tenkan_period) + M(kijun_period)) / 2,  B = M(senkou_period)
        bottom = min(A, B)
        D = max(0, bottom - close[t]) / close[t] x 100       (distance below the bottom, percent of close)
        W = abs(A - B) / close[t] x 100                        (cloud width, percent of close)
        raw_value = D / (1 + W)

    Range and sign: 0 and up, unbounded above, never negative. The value is 0 inside the cloud (edges included)
    or above it, continuous at the bottom edge, and grows as the close falls further below a thinner cloud.
    Graded, one-sided.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement rows (78 at the defaults), bar t
    included.
    NaN: a NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN; a close[t] not above 0
    gives NaN (never on real bars).

    WHY THIS CANNOT LEAK: it reads high and low only on bars up to e = t - displacement, and the close of bar t,
    the last row of data; every value is known at bar t's close.
    """

    def __init__(self, name="Ichimoku Below Cloud Per Width", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        for nm, p in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if p < 1:
                raise ValueError(f"IchimokuBelowCloudDistancePerWidthComponent: {nm} must be >= 1, got {p}")
        if self.displacement < 0:
            raise ValueError(
                f"IchimokuBelowCloudDistancePerWidthComponent: displacement must be >= 0, got {self.displacement}")
        self._raw_value = 0.0

    def _mid(self, high, low, e, p):
        h = high.iloc[e - p + 1:e + 1]
        l = low.iloc[e - p + 1:e + 1]
        if h.isna().any() or l.isna().any():
            return float("nan")
        return (float(h.max()) + float(l.min())) / 2.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float)
        low = data['low'].astype(float)
        close_t = float(data['close'].astype(float).iloc[-1])
        n = len(data)
        e = n - 1 - self.displacement
        mt = self._mid(high, low, e, self.tenkan_period)
        mk = self._mid(high, low, e, self.kijun_period)
        ms = self._mid(high, low, e, self.senkou_period)
        a = (mt + mk) / 2.0
        b = ms
        if np.isnan(a) or np.isnan(b) or np.isnan(close_t) or not close_t > 0:
            self._raw_value = float("nan")
        else:
            bottom = min(a, b)
            dist = max(0.0, bottom - close_t) / close_t * 100.0
            width = abs(a - b) / close_t * 100.0
            self._raw_value = float(dist / (1.0 + width))
            self.debug_info = {'span_a': a, 'span_b': b, 'distance_below_pct': dist, 'width_pct': width}
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement




class SwingHighProximityComponent(SubStrategyComponent):
    """
    How near the close sits below the nearest swing-high level above it, on every bar:

        W = rows t - period + 1 .. t                                      (bar t included)
        swing high: a bar i of W with i - side and i + side inside W (i = t-period+1+side .. t-side)
                    and high[i] >= high[j] for every j in i-side .. i+side, j != i
        levels = { high[i] : i a swing high }
        A = { L in levels : L >= close[t] }
        A empty:     raw_value = 0.0
        otherwise:   L = min(A), D = (L - close[t]) / L x 100,
                     raw_value = (1 / (1 + D)) ** power

    Range 0 to 1, never negative, no direction. The value is above 0 and up to 1 when a level exists at or above
    the close, nearing 1 as the close rises to that level from below (1 when the close equals it). It is 0 when no
    swing high in the window is at or above the close. Graded in the gap; the value jumps when the close crosses a
    level (to the next level up, or to 0).
    Warm-up: period rows, bar t included.

    WHY THIS CANNOT LEAK: it reads the `high` column of the last `period` rows of data (bar t the last row) and
    close[t]; a swing high at bar i is confirmed with highs up to i + side <= t, so no row after t is read.

    NaN: a NaN high in the window or a NaN close[t] gives NaN; a level L not above 0 gives NaN (never on real bars).
    Building the component raises for side < 1, period < 2 x side + 1, or power not above 0.
    """

    def __init__(self, name="SwingHighProximity", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        self.power = float(self.parameters.get("power", 1.0))
        if self.side < 1:
            raise ValueError(f"SwingHighProximityComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"SwingHighProximityComponent: period must be >= 2 x side + 1, got {self.period}")
        if not self.power > 0:
            raise ValueError(f"SwingHighProximityComponent: power must be above 0, got {self.power}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        highs = data['high'].astype(float).iloc[-self.period:].to_numpy()
        c = float(data['close'].astype(float).iloc[-1])
        if np.isnan(highs).any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = len(highs)
        s = self.side
        levels = []
        for j in range(s, n - s):
            neigh = np.concatenate([highs[j - s:j], highs[j + 1:j + s + 1]])
            if highs[j] >= neigh.max():
                levels.append(float(highs[j]))
        above = [lv for lv in levels if lv >= c]
        if not above:
            value = 0.0
            level = float("nan")
        else:
            level = min(above)
            if not level > 0:
                value = float("nan")
            else:
                d = (level - c) / level * 100.0
                value = float((1.0 / (1.0 + d)) ** self.power)
        self._raw_value = value
        self.confidence = 1.0
        self.debug_info = {'level': level, 'n_swing_highs': len(levels), 'close': c}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period


class SwingHighClusterCountComponent(SubStrategyComponent):
    """
    How many swing turns cluster at the nearest swing level on one side of the close.

        W = the last `period` bars ending at bar t (exclude_current 0)
            or bars t-period .. t-1 (exclude_current 1)
        swing point: a bar i of W with `side` bars of W before it and `side` after it, such that
            pivot "high" (default): high[i] >= each of those highs, price p[i] = high[i]
            pivot "low":            low[i]  <  each of those lows,  price p[i] = low[i]
        level "above" (default): L = min(p[i] for swing points with p[i] >= close[t])
        level "below":           L = max(p[i] for swing points with p[i] <  close[t])
        N = number of swing points with abs(p[i] - L) / L * 100 <= band   (L's own included)
        form "count" (default): raw_value = N
        form "proximity":       raw_value = N * (1 / (1 + D)) ** power,
            D = (L - close[t]) / L * 100 ("above") or (close[t] - L) / L * 100 ("below")
        raw_value = 0.0 when no swing point lies on the chosen side of close[t].

    The defaults (pivot "high", exclude_current 0) give the original output, unchanged. With pivot "low",
    exclude_current 1, period 90 and level "above", the value is the number of swing lows of bars t-90 .. t-1
    within `band` percent of the nearest swing-low level at or above the close: the touch count of the
    support the close sits under.
    Range: "count" gives 0, or an integer from 1 to period - 2*side; "proximity" gives 0 to N. Never negative,
    no direction. Graded: it grows by one with each further turn near the level.
    Warm-up: period + exclude_current rows, bar t included.
    NaN: a NaN high (pivot "high") or low (pivot "low") anywhere in W, or a NaN close[t], gives NaN.
    An L not above 0 gives NaN (never on real bars).
    Building the component raises for side < 1, period < 2*side + 1, band not above 0, an unknown form, power
    not above 0, an unknown level, a pivot other than "high" or "low", or an exclude_current other than 0 or 1.

    WHY THIS CANNOT LEAK: it reads the high or low column of the rows of W only, which are at most the last
    period + exclude_current rows of data and end at bar t or t-1. It also reads close[t], the last row. A swing
    point is confirmed only by bars inside W, all at or before bar t.
    """

    def __init__(self, name="SwingHighClusterCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        if self.side < 1:
            raise ValueError(f"SwingHighClusterCountComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"SwingHighClusterCountComponent: period must be >= 2*side+1, got {self.period}")
        self.band = float(self.parameters.get("band", 2.0))
        if not self.band > 0:
            raise ValueError(f"SwingHighClusterCountComponent: band must be > 0, got {self.band}")
        self.form = self.parameters.get("form", "count")
        if self.form not in ("count", "proximity"):
            raise ValueError(
                f"SwingHighClusterCountComponent: form must be 'count' or 'proximity', got {self.form!r}")
        self.power = float(self.parameters.get("power", 1.0))
        if not self.power > 0:
            raise ValueError(f"SwingHighClusterCountComponent: power must be > 0, got {self.power}")
        self.level = self.parameters.get("level", "above")
        if self.level not in ("above", "below"):
            raise ValueError(
                f"SwingHighClusterCountComponent: level must be 'above' or 'below', got {self.level!r}")
        self.pivot = self.parameters.get("pivot", "high")
        if self.pivot not in ("high", "low"):
            raise ValueError(
                f"SwingHighClusterCountComponent: pivot must be 'high' or 'low', got {self.pivot!r}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(
                f"SwingHighClusterCountComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        col = "high" if self.pivot == "high" else "low"
        p = data[col].astype(float).to_numpy()
        end = len(p) - self.exclude_current
        w = p[end - self.period:end]
        close_t = float(data["close"].astype(float).iloc[-1])
        if np.isnan(w).any() or np.isnan(close_t):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        s = self.side
        prices = []
        for j in range(s, self.period - s):
            v = w[j]
            nb = np.concatenate([w[j - s:j], w[j + 1:j + s + 1]])
            if self.pivot == "high":
                ok = bool(np.all(v >= nb))
            else:
                ok = bool(np.all(v < nb))
            if ok:
                prices.append(float(v))
        if self.level == "above":
            cands = [x for x in prices if x >= close_t]
        else:
            cands = [x for x in prices if x < close_t]
        if not cands:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {"swing_points": len(prices), "level": None, "count": 0}
            return
        L = min(cands) if self.level == "above" else max(cands)
        if not L > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = 0
        for x in prices:
            if abs(x - L) / L * 100.0 <= self.band:
                n += 1
        if self.form == "count":
            val = float(n)
        else:
            if self.level == "above":
                d = (L - close_t) / L * 100.0
            else:
                d = (close_t - L) / L * 100.0
            val = float(n * (1.0 / (1.0 + d)) ** self.power)
        self._raw_value = val
        self.confidence = 1.0
        self.debug_info = {"swing_points": len(prices), "level": L, "count": n}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current


class SwingLowTouchNearnessComponent(SubStrategyComponent):
    """
    Nearness-weighted count of the swing lows close to the current close, while the close is falling:

        swing low: a bar i in t-period+1+side .. t-side whose low[i] < low[j] for every j in
                   i-side .. i-1 and i+1 .. i+side (all inside the last `period` bars, bar t included)
        D_i = abs(close[t] - low[i]) / close[t] x 100                    (percent of the close)
        w_i = max(0, 1 - D_i / band)                                     (1 on the level, 0 at the band's edge)
        G   = 1 if close[t] < close[t - fall_period] else 0
        raw_value = G x sum of w_i over the swing lows

    Range: 0 up to the number of swing lows (at most period - 2 x side). It is never negative and has no
    direction. It is 0 with no swing low within `band` percent of the close, and 0 when the close is not below
    its value fall_period bars ago. It grows continuously with each further nearby swing low and with the
    nearness of the close to each one.
    Warm-up: max(period, fall_period + 1) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `low` column of the last `period` rows and the `close` of the last
    row (bar t) and of the row fall_period rows before it. A swing low at bar i is confirmed with lows up to
    bar i + side <= t, all known at bar t's close.

    NaN: a NaN low in the window, or a NaN close[t] or close[t - fall_period], gives NaN. A close[t] not above 0
    gives NaN (never on real bars).
    Building the component raises for side < 1, period < 2 x side + 1, band not above 0, or fall_period < 1.
    """

    def __init__(self, name="SwingLowTouchNearness", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        self.band = float(self.parameters.get("band", 1.5))
        self.fall_period = int(self.parameters.get("fall_period", 5))
        if self.side < 1:
            raise ValueError(f"SwingLowTouchNearnessComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"SwingLowTouchNearnessComponent: period must be >= 2 x side + 1, got {self.period}")
        if not self.band > 0:
            raise ValueError(f"SwingLowTouchNearnessComponent: band must be above 0, got {self.band}")
        if self.fall_period < 1:
            raise ValueError(
                f"SwingLowTouchNearnessComponent: fall_period must be >= 1, got {self.fall_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        lows = data['low'].astype(float).iloc[-self.period:].to_numpy()
        closes = data['close'].astype(float)
        c_t = float(closes.iloc[-1])
        c_base = float(closes.iloc[-(self.fall_period + 1)])
        if np.isnan(lows).any() or np.isnan(c_t) or np.isnan(c_base) or not c_t > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        k = self.side
        n = len(lows)
        total = 0.0
        swings = 0
        for i in range(k, n - k):
            neighbours = np.concatenate([lows[i - k:i], lows[i + 1:i + k + 1]])
            if np.all(lows[i] < neighbours):
                swings += 1
                d = abs(c_t - lows[i]) / c_t * 100.0
                w = 1.0 - d / self.band
                if w > 0:
                    total += w
        gate = 1.0 if c_t < c_base else 0.0
        self._raw_value = float(gate * total)
        self.confidence = 1.0
        self.debug_info = {'swing_lows': swings, 'weighted_touches': total, 'falling': bool(gate)}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.fall_period + 1)


class ResistanceBreakTouchCountComponent(SubStrategyComponent):
    """
    The touch count of the resistance level the close has just broken, times the margin of the break, on every bar:

        W = close[t - period + 1 .. t]                                  (bar t included)
        swing high: bar i in t - period + 1 + side .. t - side with
                    close[i] >= close[j] for j = i - side .. i - 1 and
                    close[i] >  close[j] for j = i + 1 .. i + side        (all inside W)
        L = the highest swing-high close with close[t - cross_period] <= L < close[t]
        N = the number of swing highs i with abs(close[i] - L) / L x 100 <= band (L's own included)
        raw_value = N x (close[t] - L) / L x 100,   0.0 when no swing high satisfies the crossing condition

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 when no level was crossed upward
    within the last cross_period bars, and it grows with the level's touch count and with the close's percent
    distance above it.
    Warm-up: max(period, cross_period + 1) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, cross_period + 1) rows of data,
    bar t (the last row) included. A swing high at bar i is confirmed by the closes of bars i+1 .. i+side, which all
    lie at or before bar t.

    NaN: a NaN close in the last max(period, cross_period + 1) rows gives NaN. An L not above 0 gives NaN (never on
    real bars). A missing `close` column raises.
    Building the component raises for a side below 1, a period below 2 x side + 1, a band not above 0, or a
    cross_period below 1.
    """

    def __init__(self, name="ResistanceBreakTouchCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        self.band = float(self.parameters.get("band", 2.0))
        self.cross_period = int(self.parameters.get("cross_period", 1))
        if self.side < 1:
            raise ValueError(f"ResistanceBreakTouchCountComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"ResistanceBreakTouchCountComponent: period must be >= 2 x side + 1, got {self.period}")
        if not self.band > 0:
            raise ValueError(f"ResistanceBreakTouchCountComponent: band must be above 0, got {self.band}")
        if self.cross_period < 1:
            raise ValueError(
                f"ResistanceBreakTouchCountComponent: cross_period must be >= 1, got {self.cross_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        w = c[-self.period:]
        s = self.side
        highs = []
        for k in range(s, self.period - s):
            v = w[k]
            if np.all(v >= w[k - s:k]) and np.all(v > w[k + 1:k + s + 1]):
                highs.append(float(v))
        c_now = float(c[-1])
        c_before = float(c[-1 - self.cross_period])
        crossed = [h for h in highs if c_before <= h < c_now]
        if not crossed:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {'swing_highs': len(highs), 'level': None, 'touches': 0}
            return
        level = max(crossed)
        if not level > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        touches = sum(1 for h in highs if abs(h - level) / level * 100.0 <= self.band)
        self._raw_value = float(touches * (c_now - level) / level * 100.0)
        self.confidence = 1.0
        self.debug_info = {'swing_highs': len(highs), 'level': level, 'touches': touches}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.cross_period + 1)


class TouchWeightedSupportBreakDepthComponent(SubStrategyComponent):
    """
    How far the close sits under the most-touched support level of the prior bars, weighted by that level's
    touch count:

        W = bars t-period .. t-1                                   (bar t excluded)
        swing low: bar i of W, i in t-period+side .. t-1-side, with low[i] < low[i-k] and low[i] < low[i+k]
                   for k = 1 .. side (strictly lower; all those bars inside W)
        N_j = #{swing lows i : abs(low[i] - low[j]) / low[j] x 100 <= band}   (j's own included)
        candidates = swing lows j with low[j] >= close[t]
        L = low[j] of the candidate with the largest N_j (a tie goes to the lowest low[j]); N = that N_j
        raw_value = N x (L - close[t]) / L x 100, or 0.0 when there is no candidate

    Range: 0 and up, never negative, below N x 100. It has no direction. It is 0 when the close is above every
    swing low of W, and it grows with the close's percent depth under the level and with the level's touch count.
    Graded: continuous in close[t] while the chosen level stays the same, and 0 at the level itself. It jumps where
    the close crosses another swing low.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads the `low` column of bars t-period .. t-1 and the `close` of bar t (the last row
    of data), nothing later; a swing low is confirmed only by the side bars after it inside W, all before bar t.

    NaN: a NaN low in W or a NaN close[t] gives NaN; a candidate level not above 0 gives NaN (never on real bars).
    Building the component raises for a side below 1, a period below 2 x side + 1, or a band not above 0.
    """

    def __init__(self, name="TouchWeightedSupportBreakDepth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        self.band = float(self.parameters.get("band", 2.0))
        if self.side < 1:
            raise ValueError(f"TouchWeightedSupportBreakDepthComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"TouchWeightedSupportBreakDepthComponent: period must be >= 2 x side + 1, got {self.period}")
        if not self.band > 0:
            raise ValueError(f"TouchWeightedSupportBreakDepthComponent: band must be above 0, got {self.band}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.period
        lows = data['low'].astype(float).to_numpy()[-(n + 1):-1]
        c = float(data['close'].astype(float).iloc[-1])
        self.confidence = 1.0
        if np.isnan(lows).any() or np.isnan(c):
            self._raw_value = float("nan")
            return
        swings = []
        for i in range(self.side, n - self.side):
            v = lows[i]
            ok = True
            for k in range(1, self.side + 1):
                if not (v < lows[i - k] and v < lows[i + k]):
                    ok = False
                    break
            if ok:
                swings.append(float(v))
        best_n = 0
        best_level = None
        for level in swings:
            if level < c:
                continue
            if not level > 0:
                self._raw_value = float("nan")
                return
            cnt = sum(1 for p in swings if abs(p - level) / level * 100.0 <= self.band)
            if cnt > best_n or (cnt == best_n and best_level is not None and level < best_level):
                best_n = cnt
                best_level = level
        if best_level is None:
            self._raw_value = 0.0
        else:
            self._raw_value = float(best_n * (best_level - c) / best_level * 100.0)
        self.debug_info = {'level': best_level, 'touches': best_n, 'swing_lows': len(swings)}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1


class VolatilityScaledDistanceFromHighComponent(SubStrategyComponent):
    """
    Distance of the close from its prior closing high, in usual one-bar moves:

        H = max(close[t - period .. t - 1])                     (bar t excluded)
        r[j] = close[j] / close[j-1] - 1, j = t - vol_period + 1 .. t   (bar t's return included)
        s = std(r, ddof 1)
        raw_value = (close[t] - H) / H / s        (0 when s = 0)

    Range & sign: unbounded and signed. It is 0 when the close equals the prior high, positive when the close
    is above it and negative below it. Its size is the distance counted in usual one-bar moves. Graded.
    Warm-up: max(period, vol_period) + 1 rows, bar t included.
    NaN: a NaN close in the last max(period, vol_period) + 1 rows gives NaN. An H or a return base close not
    above 0 gives NaN (never on real bars). A flat return window (s = 0, never on real bars) gives 0.
    Building the component raises for a period below 1 or a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, vol_period) + 1 rows of data,
    which end at bar t (the last row). H uses bars t-period .. t-1, and s uses the returns ending at bar t,
    and every one of those closes is known at bar t's close.
    """

    def __init__(self, name="VolScaledDistFromHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"VolatilityScaledDistanceFromHighComponent: period must be >= 1, got {self.period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        prior = c[-(self.period + 1):-1]
        high = float(np.max(prior))
        bases = c[-(self.vol_period + 1):-1]
        if not high > 0 or not (bases > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = c[-self.vol_period:] / bases - 1.0
        s = float(np.std(rets, ddof=1))
        if s == 0:
            value = 0.0
        else:
            value = (float(c[-1]) - high) / high / s
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'prior_high': high, 'return_std': s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.vol_period) + 1




class PastPredictivePowerWeightedCompositeComponent(SubStrategyComponent):
    """
    Four price effects, weighted by how well each predicted the realised forward return over a past window.

    Signals on bar i (closes only):
        s1(i) = close[i] / close[i - return_period] - 1                         (momentum)
        s2(i) = -(close[i] / close[i - reversal_period] - 1)                    (reversal)
        s3(i) = close[i] / max(close[i - high_period + 1 .. i]) - 1             (distance from high)
        s4(i) = -std_ddof1(r[i - vol_period + 1 .. i]), r[j] = close[j]/close[j-1] - 1   (volatility level)
    z_k(t) = (s_k(t) - mean(s_k[t-z_window+1 .. t])) / std_ddof1(same window), 0 when that std is 0.
    Training rows: i = t - corr_lookback .. t - horizon, y(i) = close[i + horizon] / close[i] - 1.
    w_k = Pearson corr(s_k(i), y(i)) over the training rows, 0 when either side is flat.
    weighting "correlation" (default): sum_k w_k z_k(t) / sum_k |w_k|, 0 when sum |w_k| = 0.
    weighting "best":   sign(w_k*) z_k*(t), k* = argmax |w_k| (first of s1..s4 on a tie); 0 when all w_k = 0.
    weighting "single": w_k z_k(t), k the effect named by `signal`
                        ("momentum" s1, "reversal" s2, "high" s3, "volatility" s4).
    weighting "regression": 100 sum_k b_k x_k(t), x_k = (s_k - m_k) / sd_k with m_k, sd_k (ddof 1) over the
                        training rows (signals with sd_k = 0 dropped), b_k the OLS slopes of y on the x_k with an
                        intercept; 0 when every signal is dropped.

    Range & sign: "correlation", "best" and "single" are signed, with abs at most max |z_k(t)| (about 19.05 at
    z_window 365). "single" grows with the effect's strength and with |w_k|, and its sign flips when the effect
    recently worked in reverse. "regression" is unbounded and signed.
    Warm-up: max(z_window - 1, corr_lookback) + max(return_period, reversal_period, high_period - 1, vol_period)
    + 1 rows (455), bar t included.
    NaN: a NaN close, or a close not above 0, in the last warm-up rows gives NaN.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last warm-up rows of data, ending at bar t.
    The latest forward return used is y(t - horizon) = close[t] / close[t - horizon] - 1, which is fully realised
    at bar t's close.
    """

    _SIGNALS = ("momentum", "reversal", "high", "volatility")

    def __init__(self, name="PastPredictivePowerComposite", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.return_period = int(p.get("return_period", 28))
        self.reversal_period = int(p.get("reversal_period", 1))
        self.high_period = int(p.get("high_period", 90))
        self.vol_period = int(p.get("vol_period", 30))
        self.z_window = int(p.get("z_window", 365))
        self.corr_lookback = int(p.get("corr_lookback", 365))
        self.horizon = int(p.get("horizon", 5))
        self.weighting = p.get("weighting", "correlation")
        self.signal = p.get("signal", "momentum")
        if self.return_period < 1:
            raise ValueError(f"return_period must be >= 1, got {self.return_period}")
        if self.reversal_period < 1:
            raise ValueError(f"reversal_period must be >= 1, got {self.reversal_period}")
        if self.high_period < 2:
            raise ValueError(f"high_period must be >= 2, got {self.high_period}")
        if self.vol_period < 2:
            raise ValueError(f"vol_period must be >= 2, got {self.vol_period}")
        if self.z_window < 2:
            raise ValueError(f"z_window must be >= 2, got {self.z_window}")
        if self.horizon < 1:
            raise ValueError(f"horizon must be >= 1, got {self.horizon}")
        if self.corr_lookback - self.horizon < 2:
            raise ValueError("corr_lookback - horizon must be >= 2")
        if self.weighting not in ("correlation", "best", "single", "regression"):
            raise ValueError(f"unknown weighting {self.weighting!r}")
        if self.signal not in self._SIGNALS:
            raise ValueError(f"unknown signal {self.signal!r}")
        if self.weighting == "regression" and self.corr_lookback - self.horizon < 5:
            raise ValueError("regression needs corr_lookback - horizon >= 5")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        self.confidence = 1.0
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            return
        t = n - 1
        first = t - max(self.z_window - 1, self.corr_lookback)
        S = np.full((4, n), np.nan)
        for i in range(first, n):
            S[0, i] = c[i] / c[i - self.return_period] - 1.0
            S[1, i] = -(c[i] / c[i - self.reversal_period] - 1.0)
            S[2, i] = c[i] / np.max(c[i - self.high_period + 1:i + 1]) - 1.0
            r = c[i - self.vol_period + 1:i + 1] / c[i - self.vol_period:i] - 1.0
            S[3, i] = -float(np.std(r, ddof=1))

        z = np.zeros(4)
        for k in range(4):
            win = S[k, t - self.z_window + 1:t + 1]
            sd = float(np.std(win, ddof=1))
            z[k] = (S[k, t] - float(win.mean())) / sd if sd > 0 else 0.0

        tr = np.arange(t - self.corr_lookback, t - self.horizon + 1)
        y = c[tr + self.horizon] / c[tr] - 1.0
        X = S[:, tr]

        w = np.zeros(4)
        dy = y - y.mean()
        syy = float(np.sum(dy * dy))
        for k in range(4):
            dx = X[k] - X[k].mean()
            sxx = float(np.sum(dx * dx))
            if sxx > 0 and syy > 0:
                w[k] = float(np.sum(dx * dy)) / np.sqrt(sxx * syy)

        if self.weighting == "correlation":
            den = float(np.sum(np.abs(w)))
            out = float(np.sum(w * z)) / den if den > 0 else 0.0
        elif self.weighting == "best":
            a = np.abs(w)
            if not (a > 0).any():
                out = 0.0
            else:
                k = int(np.argmax(a))
                out = float(np.sign(w[k]) * z[k])
        elif self.weighting == "single":
            k = self._SIGNALS.index(self.signal)
            out = float(w[k] * z[k])
        else:
            cols, xt = [], []
            for k in range(4):
                m = float(X[k].mean())
                sd = float(np.std(X[k], ddof=1))
                if sd > 0:
                    cols.append((X[k] - m) / sd)
                    xt.append((S[k, t] - m) / sd)
            if not cols:
                out = 0.0
            else:
                A = np.column_stack([np.ones(len(y))] + cols)
                coef = np.linalg.lstsq(A, y, rcond=None)[0]
                out = 100.0 * float(np.dot(coef[1:], np.array(xt)))

        self._raw_value = float(out)
        self.debug_info = {'weights': w.tolist(), 'z': z.tolist(), 'weighting': self.weighting,
                           'signal': self.signal}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return (max(self.z_window - 1, self.corr_lookback)
                + max(self.return_period, self.reversal_period, self.high_period - 1, self.vol_period) + 1)


class SignalPredictivePowerComponent(SubStrategyComponent):
    """
    Trailing predictive power of one signal: how well it has forecast the return that followed it.

        L = corr_lookback, h = horizon
        training rows: i = t-L .. t-h  (L - h + 1 rows)
        y(i) = close[i+h] / close[i] - 1
        signal = "momentum" (default): s(i) = close[i] / close[i-return_period] - 1
        signal = "reversal":           s(i) = -(close[i] / close[i-reversal_period] - 1)
        signal = "high":               s(i) = close[i] / max(close[i-high_period+1 .. i]) - 1
        signal = "volatility":         s(i) = -std (ddof 1) of the vol_period returns close[j]/close[j-1]-1,
                                              j = i-vol_period+1 .. i
        raw_value = Pearson corr of s(i) with y(i) over the training rows; 0 when s or y is flat there

    Range: -1 to +1, signed. It is positive when a high signal was followed by a higher return (the signal worked).
    It is negative when the signal worked in reverse, and near 0 when it did not predict.
    It is graded and continuous in the closes.
    Warm-up: corr_lookback + D + 1 rows, bar t included. D is the chosen signal's lag: return_period,
    reversal_period, high_period - 1 or vol_period (394 at the defaults).

    NaN: a NaN close, or a close not above 0, in those rows gives NaN.
    Building the component raises for return_period < 1, reversal_period < 1, high_period < 2, vol_period < 2,
    horizon < 1, corr_lookback - horizon < 2, or a signal other than "momentum", "reversal", "high" or
    "volatility".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last corr_lookback + D + 1 rows, bar t being the
    last row. The latest forward return y(t-h) = close[t]/close[t-h] - 1 ends at bar t, so no row after t is read.
    """

    def __init__(self, name="SignalPredictivePower", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.return_period = int(p.get("return_period", 28))
        self.reversal_period = int(p.get("reversal_period", 1))
        self.high_period = int(p.get("high_period", 90))
        self.vol_period = int(p.get("vol_period", 30))
        self.corr_lookback = int(p.get("corr_lookback", 365))
        self.horizon = int(p.get("horizon", 5))
        self.signal = p.get("signal", "momentum")
        if self.return_period < 1:
            raise ValueError(f"SignalPredictivePowerComponent: return_period must be >= 1, got {self.return_period}")
        if self.reversal_period < 1:
            raise ValueError(
                f"SignalPredictivePowerComponent: reversal_period must be >= 1, got {self.reversal_period}")
        if self.high_period < 2:
            raise ValueError(f"SignalPredictivePowerComponent: high_period must be >= 2, got {self.high_period}")
        if self.vol_period < 2:
            raise ValueError(f"SignalPredictivePowerComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.horizon < 1:
            raise ValueError(f"SignalPredictivePowerComponent: horizon must be >= 1, got {self.horizon}")
        if self.corr_lookback - self.horizon < 2:
            raise ValueError("SignalPredictivePowerComponent: corr_lookback - horizon must be >= 2")
        if self.signal not in ("momentum", "reversal", "high", "volatility"):
            raise ValueError(f"SignalPredictivePowerComponent: unknown signal {self.signal!r}")
        self._raw_value = 0.0

    def _lag(self):
        if self.signal == "momentum":
            return self.return_period
        if self.signal == "reversal":
            return self.reversal_period
        if self.signal == "high":
            return self.high_period - 1
        return self.vol_period

    def _signal_at(self, c, pos):
        if self.signal == "momentum":
            return c[pos] / c[pos - self.return_period] - 1.0
        if self.signal == "reversal":
            return -(c[pos] / c[pos - self.reversal_period] - 1.0)
        if self.signal == "high":
            return c[pos] / np.max(c[pos - self.high_period + 1:pos + 1]) - 1.0
        r = c[pos - self.vol_period + 1:pos + 1] / c[pos - self.vol_period:pos] - 1.0
        return -float(np.std(r, ddof=1))

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        d = self._lag()
        h = self.horizon
        xs = []
        ys = []
        for k in range(self.corr_lookback - h + 1):
            pos = d + k
            xs.append(self._signal_at(c, pos))
            ys.append(c[pos + h] / c[pos] - 1.0)
        x = np.array(xs, dtype=float)
        y = np.array(ys, dtype=float)
        if x.max() == x.min() or y.max() == y.min():
            corr = 0.0
        else:
            dx = x - x.mean()
            dy = y - y.mean()
            den = float(np.sqrt(np.sum(dx * dx) * np.sum(dy * dy)))
            corr = 0.0 if not den > 0 else float(np.clip(np.sum(dx * dy) / den, -1.0, 1.0))
        self._raw_value = float(corr)
        self.confidence = 1.0
        self.debug_info = {"signal": self.signal, "rows": len(xs), "signal_now": float(self._signal_at(c, n - 1))}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.corr_lookback + self._lag() + 1


class ExcessPredictivePowerZComponent(SubStrategyComponent):
    """
    The excess past predictive power of one signal, times that signal's current z-score:

        signal = "high" (default): s(i) = close[i] / max(close[i-high_period+1 .. i]) - 1
        signal = "volatility":     s(i) = -std (ddof 1) of r[j] = close[j] / close[j-1] - 1, j = i-vol_period+1 .. i
        y(i) = close[i+horizon] / close[i] - 1
        w(u) = Pearson corr of s(i) with y(i) over i = u-corr_lookback .. u-horizon (0 when either side is flat)
        wbar(t) = mean of w(t-mean_window) .. w(t-1)
        z(t) = (s(t) - mean) / std (ddof 1) of s over bars t-z_window+1 .. t (0 when s is flat there)
        raw_value = (w(t) - wbar(t)) x z(t)

    Signed. Its absolute value is at most 2 x (z_window-1)/sqrt(z_window), about 38.1. It is positive when the
    signal's power is above its usual level and the signal sits above its mean, or when the power is below usual
    and the signal sits below its mean. Graded, continuous in the closes. signal "high" is the original output,
    unchanged. vol_period is read only by "volatility".
    Warm-up: max(mean_window + corr_lookback, z_window - 1) + D + 1 rows, bar t included, with D = high_period - 1
    ("high") or vol_period ("volatility"). That is 820 at the defaults and 761 for "volatility" with vol_period 30.

    NaN: a NaN close, or a close not above 0, in the last (warm-up) rows gives NaN.
    Building raises for high_period < 2, horizon < 1, corr_lookback - horizon < 2, z_window < 2, mean_window < 1,
    vol_period < 2, or a signal other than "high" or "volatility".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last (warm-up) rows of data, ending at bar t (the
    last row). The forward return y(i) is used only for i <= u - horizon <= t - horizon, so the latest close it
    reads is close[t].
    """

    def __init__(self, name="ExcessPredictivePowerZ", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.high_period = int(p.get("high_period", 90))
        self.corr_lookback = int(p.get("corr_lookback", 365))
        self.horizon = int(p.get("horizon", 5))
        self.z_window = int(p.get("z_window", 365))
        self.mean_window = int(p.get("mean_window", 365))
        self.signal = p.get("signal", "high")
        self.vol_period = int(p.get("vol_period", 30))
        if self.high_period < 2:
            raise ValueError(f"ExcessPredictivePowerZComponent: high_period must be >= 2, got {self.high_period}")
        if self.horizon < 1:
            raise ValueError(f"ExcessPredictivePowerZComponent: horizon must be >= 1, got {self.horizon}")
        if self.corr_lookback - self.horizon < 2:
            raise ValueError("ExcessPredictivePowerZComponent: corr_lookback - horizon must be >= 2")
        if self.z_window < 2:
            raise ValueError(f"ExcessPredictivePowerZComponent: z_window must be >= 2, got {self.z_window}")
        if self.mean_window < 1:
            raise ValueError(f"ExcessPredictivePowerZComponent: mean_window must be >= 1, got {self.mean_window}")
        if self.vol_period < 2:
            raise ValueError(f"ExcessPredictivePowerZComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.signal not in ("high", "volatility"):
            raise ValueError(
                f"ExcessPredictivePowerZComponent: signal must be 'high' or 'volatility', got {self.signal!r}")
        self._raw_value = 0.0

    def _lead(self):
        return self.high_period - 1 if self.signal == "high" else self.vol_period

    @staticmethod
    def _corr(x, y):
        if x.max() == x.min() or y.max() == y.min():
            return 0.0
        xm = x - x.mean()
        ym = y - y.mean()
        den = np.sqrt(np.sum(xm * xm) * np.sum(ym * ym))
        if not den > 0:
            return 0.0
        return float(np.sum(xm * ym) / den)

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n_rows = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n_rows:]
        if np.isnan(c).any() or (c <= 0).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        t = n_rows - 1
        D = self._lead()
        L, h, zw, mw = self.corr_lookback, self.horizon, self.z_window, self.mean_window

        s = np.full(n_rows, np.nan)
        if self.signal == "high":
            win = np.lib.stride_tricks.sliding_window_view(c, self.high_period)
            s[D:] = c[D:] / win.max(axis=1) - 1.0
        else:
            r = c[1:] / c[:-1] - 1.0
            win = np.lib.stride_tricks.sliding_window_view(r, self.vol_period)
            s[D:] = -win.std(axis=1, ddof=1)

        y = np.full(n_rows, np.nan)
        y[: n_rows - h] = c[h:] / c[: n_rows - h] - 1.0

        def w_at(u):
            lo, hi = u - L, u - h + 1
            return self._corr(s[lo:hi], y[lo:hi])

        w_t = w_at(t)
        wbar = float(np.mean([w_at(u) for u in range(t - mw, t)]))

        zs = s[t - zw + 1: t + 1]
        if zs.max() == zs.min():
            z = 0.0
        else:
            sd = float(np.std(zs, ddof=1))
            z = float((s[t] - zs.mean()) / sd) if sd > 0 else 0.0

        self._raw_value = float((w_t - wbar) * z)
        self.confidence = 1.0
        self.debug_info = {"w": w_t, "wbar": wbar, "z": z, "signal": self.signal}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.mean_window + self.corr_lookback, self.z_window - 1) + self._lead() + 1


class VolScaledBreakAboveHighComponent(SubStrategyComponent):
    """
    How far the close has broken above the prior high, in usual step-bar moves, on every bar:

        H = max(high[t - period] .. high[t - 1])                         (bar t excluded)
        m = mean over k = 0 .. steps-1 of abs(close[t - k*step] / close[t - (k+1)*step] - 1)
        raw_value = max(0, close[t] - H) / close[t] / m                  (0 when m = 0)

    With the defaults (period 480, step 24, steps 30) on 1h bars: the break above the prior 20-day high,
    as a fraction of the close, divided by the mean absolute daily return over the last 30 daily steps.
    Range: 0 and up, unbounded above, never negative. It is 0 while close[t] <= H and grows continuously
    as the close sits further above the prior high, in usual moves. Graded, one-sided, with no direction.
    m = 0 happens only when close[t] = close[t-step]. Then high[t-step] >= close[t] lies inside the prior
    window, so the numerator is 0 too, and the output is 0.
    Warm-up: max(period + 1, step * steps + 1) rows, bar t included (721 at the defaults).

    WHY THIS CANNOT LEAK: it reads the `high` column of rows t-period .. t-1 and the `close` column of
    rows t, t-step, ..., t-steps*step, all at or before bar t (the last row of data). Each value is known
    at its bar's close.

    NaN: a NaN high in the prior window, a NaN close[t] or a NaN among the closes used gives NaN. A close
    not above 0 among them gives NaN (never on real bars). Building the component raises for a period,
    step or steps below 1.
    """

    def __init__(self, name="VolScaledBreakAboveHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 480))
        if self.period < 1:
            raise ValueError(f"VolScaledBreakAboveHighComponent: period must be >= 1, got {self.period}")
        self.step = int(self.parameters.get("step", 24))
        if self.step < 1:
            raise ValueError(f"VolScaledBreakAboveHighComponent: step must be >= 1, got {self.step}")
        self.steps = int(self.parameters.get("steps", 30))
        if self.steps < 1:
            raise ValueError(f"VolScaledBreakAboveHighComponent: steps must be >= 1, got {self.steps}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        n = len(close)
        prior = high[n - 1 - self.period:n - 1]
        c = close[n - 1]
        if np.isnan(prior).any() or np.isnan(c) or not c > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        h = float(prior.max())
        idx = [n - 1 - k * self.step for k in range(self.steps + 1)]
        pts = close[idx]
        if np.isnan(pts).any() or not (pts > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        moves = np.abs(pts[:-1] / pts[1:] - 1.0)
        m = float(moves.mean())
        brk = max(0.0, c - h) / c
        self._raw_value = float(brk / m) if m > 0 else 0.0
        self.confidence = 1.0
        self.debug_info = {'prior_high': h, 'break_frac': brk, 'mean_abs_move': m}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period + 1, self.step * self.steps + 1)


class MeanAbsReturnComponent(SubStrategyComponent):
    """
    The usual size of a `period`-bar move, on every bar:

        r(i) = close[i] / close[i - period] - 1,  i = t - window + 1 .. t   (bar t included)
        raw_value = (1 / window) x sum over those i of abs(r(i))

    The returns overlap: one is taken ending at each of the last `window` bars.
    Range & sign: 0 and up, unbounded above, never negative; no direction. It grows with the coin's
    usual `period`-bar move. Units: a fraction of price (a simple return, not percent).
    Warm-up: window + period rows, bar t included (744 at the defaults).
    NaN: a NaN close anywhere in the last window + period rows gives NaN. A close not above 0 there
    gives NaN (never on real bars). A missing `close` column raises.
    Building the component raises for a period below 1 or a window below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data.
    Those are bars t - window - period + 1 .. t, and the last row is bar t. A bar's close is known at
    that bar's close.
    """

    def __init__(self, name="MeanAbsReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        if self.period < 1:
            raise ValueError(f"MeanAbsReturnComponent: period must be >= 1, got {self.period}")
        self.window = int(self.parameters.get("window", 720))
        if self.window < 1:
            raise ValueError(f"MeanAbsReturnComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.window + self.period
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
        else:
            r = c[self.period:] / c[:-self.period] - 1.0
            self._raw_value = float(np.mean(np.abs(r)))
        self.confidence = 1.0
        self.debug_info = {'period': self.period, 'window': self.window}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.window + self.period


class MeanAbsScaledFallTimesRiseComponent(SubStrategyComponent):
    """
    A fall in usual moves times a prior rise, on every bar:

        F = close[t] / close[t - fall_period] - 1
        m = mean over i = t-window+1 .. t of abs(close[i] / close[i - fall_period] - 1)   (bar t included)
        R = close[t - rise_lag] / close[t - rise_lag - rise_period] - 1
        raw_value = max(0, -F / m) x max(0, R) x 100      (first factor 0 when m = 0)

    rise_lag 0 (default) ends the rise at bar t: this is the original output, unchanged. rise_lag 1 ends it at bar t-1,
    so it is the rise before the falling bar.
    Range: 0 and up, unbounded above, never negative, no direction. It is 0 unless the fall_period-bar return is negative
    and R is positive, and it grows with both.
    Warm-up: max(window + fall_period, rise_period + rise_lag + 1) rows, bar t included (744 at the defaults).
    NaN: a NaN close in those rows gives NaN; a close not above 0 there gives NaN (never on real bars). m = 0 gives 0.
    Building the component raises for fall_period < 1, window < 1, rise_period < 1 or rise_lag < 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window + fall_period,
    rise_period + rise_lag + 1) rows of data, the last of which is bar t; no later row exists in data.
    """

    def __init__(self, name="MeanAbsScaledFallTimesRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.fall_period = int(self.parameters.get("fall_period", 24))
        self.window = int(self.parameters.get("window", 720))
        self.rise_period = int(self.parameters.get("rise_period", 720))
        self.rise_lag = int(self.parameters.get("rise_lag", 0))
        if self.fall_period < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: fall_period must be >= 1, got {self.fall_period}")
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: window must be >= 1, got {self.window}")
        if self.rise_period < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: rise_period must be >= 1, got {self.rise_period}")
        if self.rise_lag < 0:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: rise_lag must be >= 0, got {self.rise_lag}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        last = len(c) - 1
        fp = self.fall_period
        fall = c[last] / c[last - fp] - 1.0
        cur = c[len(c) - self.window:]
        prev = c[len(c) - self.window - fp:len(c) - fp]
        m = float(np.mean(np.abs(cur / prev - 1.0)))
        first = 0.0 if m == 0 else max(0.0, -fall / m)
        rise = c[last - self.rise_lag] / c[last - self.rise_lag - self.rise_period] - 1.0
        second = max(0.0, rise)
        self._raw_value = float(first * second * 100.0)
        self.confidence = 1.0
        self.debug_info = {'fall': float(fall), 'mean_abs_move': m, 'rise': float(rise)}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.window + self.fall_period, self.rise_period + self.rise_lag + 1)


class HighProximityScaledReturnComponent(SubStrategyComponent):
    """
    The return_period-bar return in usual return_period-bar moves, weighted by the nearness of the close to
    its recent closing high:

        H = max(close[t - period + 1 .. t])                                   (bar t included)
        D = max(0, (H - close[t]) / H * 100)                                  (percent below the high)
        W = (1 / (1 + D)) ** power
        r(i) = close[i] / close[i - return_period] - 1
        m = mean(abs(r(i)) for i in t - window + 1 .. t)                      (bar t included)
        raw_value = W * r(t) / m        (0 when m == 0)

    Range & sign: signed like r(t), unbounded in practice. abs(value) <= window, because r(t) is one of the
    window returns in m and W <= 1. At a new high W = 1; W shrinks toward 0 far below the high.
    Graded: continuous in the closes.
    Warm-up: max(period, window + return_period) rows, bar t included (744 at the defaults).
    NaN: a NaN close, or a close not above 0, in those rows gives NaN. m == 0 gives 0.
    Building the component raises for period < 2, return_period < 1, window < 1 or power not above 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, window + return_period)
    rows of data, the last of which is bar t; a close is known at its bar's close.
    """

    def __init__(self, name="HighProximityScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 720))
        if self.period < 2:
            raise ValueError(f"HighProximityScaledReturnComponent: period must be >= 2, got {self.period}")
        self.return_period = int(self.parameters.get("return_period", 24))
        if self.return_period < 1:
            raise ValueError(
                f"HighProximityScaledReturnComponent: return_period must be >= 1, got {self.return_period}")
        self.window = int(self.parameters.get("window", 720))
        if self.window < 1:
            raise ValueError(f"HighProximityScaledReturnComponent: window must be >= 1, got {self.window}")
        self.power = float(self.parameters.get("power", 2.0))
        if not self.power > 0:
            raise ValueError(f"HighProximityScaledReturnComponent: power must be above 0, got {self.power}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        high = float(c[-self.period:].max())
        dist = max(0.0, (high - c[-1]) / high * 100.0)
        w = (1.0 / (1.0 + dist)) ** self.power
        rets = c[self.return_period:] / c[:-self.return_period] - 1.0
        recent = rets[-self.window:]
        m = float(np.abs(recent).mean())
        ret = float(recent[-1])
        self._raw_value = 0.0 if m == 0 else float(w * ret / m)
        self.confidence = 1.0
        self.debug_info = {'high': high, 'distance_pct': dist, 'weight': w, 'return': ret, 'mean_abs': m}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period, self.window + self.return_period)


class MeanAbsScaledReturnComponent(SubStrategyComponent):
    """
    The period-bar return in multiples of the coin's usual period-bar move, on every bar:

        r(i) = close[i] / close[i - period] - 1
        m    = mean(abs(r(i)) for i = t - window + 1 .. t)       (overlapping returns, bar t included)
        raw_value = r(t) / m        (0.0 when m = 0)

    Graded and signed like the period-bar return: negative after a fall, more negative the deeper the fall in
    usual moves; positive after a rise. Its size is at most `window`, because r(t) is one of the averaged returns.
    Warm-up: window + period rows, bar t included (the oldest return needs close[t - window + 1 - period]).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data, the last
    row being bar t; a bar's close is known at that bar's close.

    NaN: a NaN close in the last window + period rows gives NaN, and so does a close not above 0 there (never on
    real bars). m = 0 (every return flat, never on real bars) gives 0.0; the return is then 0 as well.
    Building the component raises for a period below 1 or a window below 1.
    """

    def __init__(self, name="MeanAbsScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        if self.period < 1:
            raise ValueError(f"MeanAbsScaledReturnComponent: period must be >= 1, got {self.period}")
        self.window = int(self.parameters.get("window", 720))
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledReturnComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[self.period:] / c[:-self.period] - 1.0
        m = float(np.mean(np.abs(r)))
        ret = float(r[-1])
        self._raw_value = float(ret / m) if m > 0 else 0.0
        self.confidence = 1.0
        self.debug_info = {'return': ret, 'mean_abs_return': m}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period




class MeanAbsoluteMoveRankComponent(SubStrategyComponent):
    """
    Rank of the mean absolute one-bar move within its own recent past, on every bar:

        r[j]  = close[j] / close[j-1] - 1
        m(i)  = mean(abs(r[j]) for j = i - period + 1 .. i)        (bar i's return included)
        raw_value = (number of i in t - lookback + 1 .. t with m(i) <= m(t)) / lookback

    Range: above 0, up to 1, in steps of 1/lookback. It is never negative and has no direction. It is 1 when
    today's mean absolute move is the highest of the lookback. It is 1/lookback when it is the lowest, because
    the count includes m(t) itself. It grows as the mean absolute move rises above its usual level. Stateless
    and unsmoothed.
    Warm-up: period + lookback rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + lookback rows of data, the last
    of which is bar t; every m(i) ends at a bar i <= t.

    NaN: a NaN close in the last period + lookback rows gives NaN. A close not above 0 there gives NaN (never on
    real bars).
    Building the component raises for a period below 1 or a lookback below 2.
    """

    def __init__(self, name="MeanAbsMoveRank", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 168))
        if self.period < 1:
            raise ValueError(f"MeanAbsoluteMoveRankComponent: period must be >= 1, got {self.period}")
        self.lookback = int(self.parameters.get("lookback", 720))
        if self.lookback < 2:
            raise ValueError(f"MeanAbsoluteMoveRankComponent: lookback must be >= 2, got {self.lookback}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        a = np.abs(c[1:] / c[:-1] - 1.0)          # n - 1 = period + lookback - 1 returns
        m = np.empty(self.lookback)
        for k in range(self.lookback):
            m[k] = float(np.sum(a[k:k + self.period])) / self.period
        cur = m[-1]
        rank = float(np.sum(m <= cur)) / self.lookback
        self._raw_value = float(rank)
        self.confidence = 1.0
        self.debug_info = {'mean_abs_move': float(cur), 'rank': rank}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.lookback




class LowProximityScaledRiseComponent(SubStrategyComponent):
    """
    Today's rise in usual one-bar moves, weighted by the nearness of the close to its recent closing low:

        r(j)  = close[j] / close[j-1] - 1
        s     = std (ddof 1) of r(j), j = t-vol_period+1 .. t        (bar t's return included)
        Lo    = min(close[t-period+1 .. t])                          (bar t included)
        D     = (close[t] - Lo) / Lo x 100                           (>= 0, since Lo includes close[t])
        raw_value = max(0, r(t) / s) x 1 / (1 + D)                   (first factor 0 when s = 0)

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 on down and flat bars and grows with
    the size of the rise in usual moves and with the nearness of the close to its low. The weight is in (0, 1] and
    equals 1 at the low.
    Warm-up: max(vol_period + 1, period) rows, bar t included.
    NaN: a NaN close in the last max(vol_period + 1, period) rows gives NaN. A Lo or a return base close not above
    0 gives NaN (never on real bars). s = 0 gives 0.
    Building raises for vol_period < 2 or period < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(vol_period + 1, period) rows of data,
    the last of which is bar t; no later row exists in what it is given.
    """

    def __init__(self, name="LowProximityScaledRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"LowProximityScaledRiseComponent: vol_period must be >= 2, got {self.vol_period}")
        self.period = int(self.parameters.get("period", 90))
        if self.period < 2:
            raise ValueError(f"LowProximityScaledRiseComponent: period must be >= 2, got {self.period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rc = c[-(self.vol_period + 1):]
        bases = rc[:-1]
        if not (bases > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = rc[1:] / bases - 1.0
        s = float(np.std(rets, ddof=1))
        lo = float(np.min(c[-self.period:]))
        if not lo > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        d = (float(c[-1]) - lo) / lo * 100.0
        w = 1.0 / (1.0 + d)
        first = max(0.0, float(rets[-1]) / s) if s > 0 else 0.0
        self._raw_value = float(first * w)
        self.confidence = 1.0
        self.debug_info = {"ret": float(rets[-1]), "std": s, "low": lo, "D": d, "weight": w}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.vol_period + 1, self.period)




class FallGatedRangeMultipleComponent(SubStrategyComponent):
    """
    The range of a fall stretch, in multiples of its own average, read at e = t - lag:

        e = t - lag                                          (lag 0, the default: e = t)
        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        M = mean(S(e-base_period+1) .. S(e))
        G = 1 when close[e] < close[e-fall_period], else 0
        raw_value = G x S(e) / M        (0.0 when M is 0)

    Range & sign: 0 and up, at most base_period (M includes S(e)), never negative, no direction. It is 1 when
    the stretch's range equals its mean and 0 when close[e] is not below close[e-fall_period]. lag 0 is the
    original output, unchanged.
    Warm-up: max(base_period + period - 1, fall_period + 1) + lag rows, bar t included.
    NaN: a NaN high or low in bars e-base_period-period+2 .. e, or a NaN close[e] or close[e-fall_period],
    gives NaN, whatever the gate. A mean of 0 gives 0.0 (S(e) is then 0 too).
    Building the component raises for period < 1, base_period < 1, fall_period < 1 or lag < 0.

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data), and of them
    only bars up to e = t - lag: high and low of bars e-base_period-period+2 .. e, and close of bars
    e-fall_period and e. Each is known at its bar's close.
    """

    def __init__(self, name="FallGatedRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.base_period = int(self.parameters.get("base_period", 180))
        self.fall_period = int(self.parameters.get("fall_period", 6))
        self.lag = int(self.parameters.get("lag", 0))
        if self.period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: period must be >= 1, got {self.period}")
        if self.base_period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: base_period must be >= 1, got {self.base_period}")
        if self.fall_period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: fall_period must be >= 1, got {self.fall_period}")
        if self.lag < 0:
            raise ValueError(f"FallGatedRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = len(data)
        e = n - 1 - self.lag
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        start = e - self.base_period - self.period + 2
        h = high[start:e + 1]
        lo = low[start:e + 1]
        c_e = close[e]
        c_b = close[e - self.fall_period]
        if np.isnan(h).any() or np.isnan(lo).any() or np.isnan(c_e) or np.isnan(c_b):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        hmax = pd.Series(h).rolling(self.period).max().to_numpy()[self.period - 1:]
        lmin = pd.Series(lo).rolling(self.period).min().to_numpy()[self.period - 1:]
        s = hmax - lmin
        s_e = float(s[-1])
        mean_s = float(np.mean(s))
        gate = 1.0 if c_e < c_b else 0.0
        if mean_s == 0:
            value = 0.0
        else:
            value = gate * s_e / mean_s
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'gate': gate, 'stretch_range': s_e, 'mean_range': mean_s, 'lag': self.lag}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.base_period + self.period - 1, self.fall_period + 1) + self.lag


class ScaledFallRangeMultipleComponent(SubStrategyComponent):
    """
    The fall of a stretch in usual moves, times its range in usual ranges, for the stretch ending `lag` bars back:

        e    = t - lag
        R    = close[e] / close[e - period] - 1
        m    = mean over i = e-window+1 .. e of abs(close[i] / close[i - period] - 1)
        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        B    = mean over i = e-window+1 .. e of S(i)
        raw_value = max(0, -R / m) x S(e) / B      (0 when m = 0 or B = 0)

    Range: 0 and up, unbounded in practice, never negative; no direction. It is 0 when the stretch did not fall.
    It grows with the depth of the fall in usual period-bar moves and with how many usual period-bar ranges the
    stretch spanned. Each factor is at most `window`.
    Warm-up: window + period + lag rows, bar t included.
    NaN: a NaN close among closes[e-window-period+1 .. e], or a NaN high or low among bars e-window-period+2 .. e,
    gives NaN. A close not above 0 there also gives NaN. m = 0 or B = 0 gives 0.0, because the fall or the range is
    then 0 too.
    Building it raises for period < 1, lag < 0 or window < 1.

    WHY THIS CANNOT LEAK: it reads only close, high and low of rows up to and including bar t - lag. These are at or
    before bar t, the last row of data, and each is known at that bar's close.
    """

    def __init__(self, name="ScaledFallRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        if self.period < 1:
            raise ValueError(f"ScaledFallRangeMultipleComponent: period must be >= 1, got {self.period}")
        self.lag = int(self.parameters.get("lag", 6))
        if self.lag < 0:
            raise ValueError(f"ScaledFallRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        self.window = int(self.parameters.get("window", 180))
        if self.window < 1:
            raise ValueError(f"ScaledFallRangeMultipleComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p, w = self.period, self.window
        c = data['close'].astype(float).to_numpy()
        h = data['high'].astype(float).to_numpy()
        lo = data['low'].astype(float).to_numpy()
        e = len(c) - 1 - self.lag
        cs = c[e - w - p + 1: e + 1]
        hs = h[e - w - p + 2: e + 1]
        ls = lo[e - w - p + 2: e + 1]
        self.confidence = 1.0
        if np.isnan(cs).any() or np.isnan(hs).any() or np.isnan(ls).any() or not (cs > 0).all():
            self._raw_value = float("nan")
            return
        rets = cs[p:] / cs[:-p] - 1.0
        m = float(np.mean(np.abs(rets)))
        hw = np.lib.stride_tricks.sliding_window_view(hs, p).max(axis=1)
        lw = np.lib.stride_tricks.sliding_window_view(ls, p).min(axis=1)
        ranges = hw - lw
        b = float(np.mean(ranges))
        r = float(rets[-1])
        s = float(ranges[-1])
        if m == 0 or b == 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float(max(0.0, -r / m) * s / b)
        self.debug_info = {'stretch_return': r, 'usual_move': m, 'stretch_range': s, 'usual_range': b}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period + self.lag


class FallGatedRangeMultipleVolatilityRatioComponent(SubStrategyComponent):
    """
    A fall-gated range multiple times a volatility ratio, on bar t:

        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        range_multiple = S(t) / mean(S(t-base_period+1) .. S(t))      (0.0 when that mean is 0)
        r[j] = close[j] / close[j-1] - 1
        s(i) = std (ddof 1) of r[i-vol_period+1 .. i]
        vol_ratio = s(t) / mean(s(t-vol_lookback+1) .. s(t))
        G = 1 if close[t] < close[t-fall_period] else 0
        raw_value = G x range_multiple x vol_ratio

    Range: 0 and up, at most base_period x vol_lookback, never negative; no direction. It is 0 when there is no
    fall over fall_period bars. While the fall lasts it grows continuously with the range multiple and with the
    volatility ratio. Graded inside the gate, and it jumps to 0 at the gate.

    Warm-up: max(base_period + period - 1, fall_period + 1, vol_lookback + vol_period) rows, bar t included
    (402 at the defaults).

    NaN: a NaN high or low in the last base_period + period - 1 rows, or a NaN close in the last
    vol_lookback + vol_period rows or at bar t-fall_period, gives NaN whatever the gate. A close not above 0
    among those rows gives NaN, and so does a mean of s equal to 0 (neither is ever seen on real bars).
    A mean range of 0 gives a range factor of 0.0.
    Building the component raises for period < 1, base_period < 1, fall_period < 1, vol_period < 2,
    or vol_lookback < 1.

    WHY THIS CANNOT LEAK: it reads only the high, low and close of the last get_required_periods() rows of data,
    ending at bar t (the last row), which are all known at bar t's close.
    """

    def __init__(self, name="FallGatedRangeVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.base_period = int(self.parameters.get("base_period", 180))
        self.fall_period = int(self.parameters.get("fall_period", 6))
        self.vol_period = int(self.parameters.get("vol_period", 42))
        self.vol_lookback = int(self.parameters.get("vol_lookback", 360))
        if self.period < 1:
            raise ValueError(f"FallGatedRangeMultipleVolatilityRatioComponent: period must be >= 1, got {self.period}")
        if self.base_period < 1:
            raise ValueError(
                f"FallGatedRangeMultipleVolatilityRatioComponent: base_period must be >= 1, got {self.base_period}")
        if self.fall_period < 1:
            raise ValueError(
                f"FallGatedRangeMultipleVolatilityRatioComponent: fall_period must be >= 1, got {self.fall_period}")
        if self.vol_period < 2:
            raise ValueError(
                f"FallGatedRangeMultipleVolatilityRatioComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.vol_lookback < 1:
            raise ValueError(
                f"FallGatedRangeMultipleVolatilityRatioComponent: vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        tail = data.iloc[-n:]
        high = tail["high"].astype(float).to_numpy()
        low = tail["low"].astype(float).to_numpy()
        close = tail["close"].astype(float).to_numpy()
        last = n - 1
        p, b, f = self.period, self.base_period, self.fall_period
        v, L = self.vol_period, self.vol_lookback

        hl_start = last - b - p + 2
        cl_start = last - L - v + 1
        if (np.isnan(high[hl_start:]).any() or np.isnan(low[hl_start:]).any()
                or np.isnan(close[cl_start:]).any() or np.isnan(close[last - f])):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if not (close[cl_start:] > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return

        ranges = np.empty(b)
        for k, i in enumerate(range(last - b + 1, last + 1)):
            ranges[k] = high[i - p + 1:i + 1].max() - low[i - p + 1:i + 1].min()
        mean_range = float(ranges.mean())
        range_multiple = float(ranges[-1] / mean_range) if mean_range != 0 else 0.0

        stds = np.empty(L)
        for k, i in enumerate(range(last - L + 1, last + 1)):
            rets = close[i - v + 1:i + 1] / close[i - v:i] - 1.0
            stds[k] = np.std(rets, ddof=1)
        mean_std = float(stds.mean())
        if not mean_std > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        vol_ratio = float(stds[-1] / mean_std)

        gate = 1.0 if close[last] < close[last - f] else 0.0
        self._raw_value = float(gate * range_multiple * vol_ratio)
        self.confidence = 1.0
        self.debug_info = {"gate": gate, "range_multiple": range_multiple, "vol_ratio": vol_ratio}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.base_period + self.period - 1, self.fall_period + 1, self.vol_lookback + self.vol_period)


class PriorFallTimesScaledFallRangeMultipleComponent(SubStrategyComponent):
    """
    The prior long fall that ended at the stretch's start, times the scaled fall and range multiple of the stretch:

        e = t - lag
        P = max(0, -(close[e-period] / close[e-period-prior_period] - 1)) x 100
        r(i) = close[i] / close[i-period] - 1
        m = mean(abs(r(i)), i = e-window+1 .. e)
        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        B = mean(S(i), i = e-window+1 .. e)
        F = max(0, -r(e) / m) x S(e) / B          (F = 0 when m = 0 or B = 0)
        raw_value = P x F

    F is ScaledFallRangeMultipleComponent(period, lag, window). The output is graded, 0 and up, never negative,
    with no direction. P is 0 to 100, and each multiple in F is at most window. It is 0 unless both the prior
    prior_period-bar return and the stretch's return are negative.
    Warm-up: max(lag + window + period, lag + period + prior_period + 1) rows, bar t included (553 at the defaults).
    NaN: a NaN close, high or low in any row read gives NaN, and so does a close not above 0 (never on real bars).
    m = 0 or B = 0 gives 0.
    Building the component raises for period < 1, lag < 0, window < 1, or prior_period < 1.

    WHY THIS CANNOT LEAK: it reads close at bars t-lag-window-period+1 .. t-lag and at bar
    t-lag-period-prior_period, and high and low at bars t-lag-window-period+2 .. t-lag. All of these are rows
    at or before bar t (the last row of data).
    """

    def __init__(self, name="PriorFallScaledFallRange", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.lag = int(self.parameters.get("lag", 6))
        self.window = int(self.parameters.get("window", 180))
        self.prior_period = int(self.parameters.get("prior_period", 540))
        if self.period < 1:
            raise ValueError(f"PriorFallTimesScaledFallRangeMultipleComponent: period must be >= 1, got {self.period}")
        if self.lag < 0:
            raise ValueError(f"PriorFallTimesScaledFallRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        if self.window < 1:
            raise ValueError(f"PriorFallTimesScaledFallRangeMultipleComponent: window must be >= 1, got {self.window}")
        if self.prior_period < 1:
            raise ValueError(
                f"PriorFallTimesScaledFallRangeMultipleComponent: prior_period must be >= 1, got {self.prior_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data["close"].astype(float).to_numpy()
        h = data["high"].astype(float).to_numpy()
        lo = data["low"].astype(float).to_numpy()
        n = len(c)
        t = n - 1
        p, w = self.period, self.window
        e = t - self.lag
        cw = c[e - w - p + 1: e + 1]
        hw = h[e - w - p + 2: e + 1]
        lw = lo[e - w - p + 2: e + 1]
        p0 = c[e - p - self.prior_period]
        p1 = c[e - p]
        if (np.isnan(cw).any() or np.isnan(hw).any() or np.isnan(lw).any() or np.isnan(p0)
                or (cw <= 0).any() or not p0 > 0):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = cw[p:] / cw[:-p] - 1.0
        m = float(np.mean(np.abs(r)))
        hmax = np.lib.stride_tricks.sliding_window_view(hw, p).max(axis=1)
        lmin = np.lib.stride_tricks.sliding_window_view(lw, p).min(axis=1)
        s = hmax - lmin
        b = float(np.mean(s))
        fall = max(0.0, -float(r[-1]))
        if m == 0 or b == 0:
            f = 0.0
        else:
            f = fall / m * float(s[-1]) / b
        prior = max(0.0, -(float(p1) / float(p0) - 1.0)) * 100.0
        self._raw_value = float(prior * f)
        self.confidence = 1.0
        self.debug_info = {"prior_fall_pct": prior, "scaled_fall_range_multiple": f, "m": m, "B": b}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.lag + self.window + self.period, self.lag + self.period + self.prior_period + 1)


class PriorSlideDiscountedScaledFallRangeMultipleComponent(SubStrategyComponent):
    """
    A delayed panic reading, discounted by the slide that came before it. With e = t - lag:

        m    = mean_{i=e-window+1..e} abs(close[i] / close[i-period] - 1)
        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        B    = mean_{i=e-window+1..e} S(i)
        F    = max(0, -(close[e] / close[e-period] - 1) / m) * S(e) / B     (0 when m = 0 or B = 0)
        R    = close[e] / close[e-prior_period] - 1
        u    = mean_{i=e-window+1..e} abs(close[i] / close[i-prior_period] - 1)
        Q    = 1 + min(0, R / u)                                            (1 when u = 0)
        raw_value = F * Q                                                   (0.0 when F = 0)

    F is ScaledFallRangeMultipleComponent(period, lag, window). Q is 1 when the prior return is 0 or above.
    Q falls by one for each usual prior_period-bar move of slide, so it is 0 at one usual move and negative
    beyond. Q >= 1 - window, because abs(R) is one of the averaged terms.
    Range: signed. 0 when the stretch ending at e did not fall. During a fall: positive while the prior slide
    is shallower than one usual move, negative when deeper. F is at most window * window.
    Warm-up: lag + window + max(period, prior_period) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads close over bars e-window+1-max(period, prior_period) .. e, and high and low
    over bars e-window-period+2 .. e, with e = t - lag <= t. Every row read is at or before bar t.

    NaN: a NaN close, high or low among the rows read gives NaN, and so does a close not above 0 there
    (never on real bars).
    Building the component raises for a period below 1, a lag below 0, a window below 1, or a prior_period
    below 1.
    """

    def __init__(self, name="PriorSlideDiscountedPanic", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.lag = int(self.parameters.get("lag", 6))
        self.window = int(self.parameters.get("window", 180))
        self.prior_period = int(self.parameters.get("prior_period", 42))
        if self.period < 1:
            raise ValueError(f"PriorSlideDiscountedScaledFallRangeMultipleComponent: period must be >= 1, got {self.period}")
        if self.lag < 0:
            raise ValueError(f"PriorSlideDiscountedScaledFallRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        if self.window < 1:
            raise ValueError(f"PriorSlideDiscountedScaledFallRangeMultipleComponent: window must be >= 1, got {self.window}")
        if self.prior_period < 1:
            raise ValueError(
                f"PriorSlideDiscountedScaledFallRangeMultipleComponent: prior_period must be >= 1, got {self.prior_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float).to_numpy()
        high = data["high"].astype(float).to_numpy()
        low = data["low"].astype(float).to_numpy()
        p, q, w = self.period, self.prior_period, self.window
        e = len(close) - 1 - self.lag
        c_lo = e - w + 1 - max(p, q)
        hl_lo = e - w - p + 2
        cw = close[c_lo:e + 1]
        hw = high[hl_lo:e + 1]
        lw = low[hl_lo:e + 1]
        if np.isnan(cw).any() or np.isnan(hw).any() or np.isnan(lw).any() or not (cw > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        idx = np.arange(e - w + 1, e + 1)
        m = float(np.mean(np.abs(close[idx] / close[idx - p] - 1.0)))
        s_vals = np.array([np.max(high[i - p + 1:i + 1]) - np.min(low[i - p + 1:i + 1]) for i in idx])
        b = float(np.mean(s_vals))
        r_fall = close[e] / close[e - p] - 1.0
        if m == 0 or b == 0:
            f = 0.0
        else:
            f = max(0.0, -r_fall / m) * float(s_vals[-1]) / b
        r_prior = close[e] / close[e - q] - 1.0
        u = float(np.mean(np.abs(close[idx] / close[idx - q] - 1.0)))
        factor = 1.0 if u == 0 else 1.0 + min(0.0, r_prior / u)
        self._raw_value = float(f * factor) if f > 0 else 0.0
        self.confidence = 1.0
        self.debug_info = {"fall_range_multiple": f, "prior_return": float(r_prior),
                           "prior_usual_move": u, "prior_factor": factor}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.lag + self.window + max(self.period, self.prior_period)


class NetMoveToRangeRatioComponent(SubStrategyComponent):
    """
    The net move over `period` bars per the range of the window, on every bar:

        move = abs(close[t] - close[t - period])
        source = "high_low" (default): H = max(high[t-period+1 .. t]), L = min(low[t-period+1 .. t])
        source = "close":              H = max(close[t-period+1 .. t]), L = min(close[t-period+1 .. t])
        raw_value = move / (H - L), and 0.0 when H - L = 0

    Range & sign: 0 and up, never negative, no direction. It is at most 1 whenever close[t-period] lies inside
    [L, H], as on almost every real bar, and can exceed 1 only when close[t-period] lies outside the window's
    range. Small for a flat market, 1 when the net move spans the whole range. Graded and continuous while the
    range is above 0.
    The default source "high_low" is the original output, unchanged. "close" divides by the closing range instead.
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close[t] or close[t-period], or a NaN in the range window (high and low for "high_low", closes for
    "close"), gives NaN. A range of 0 reads 0.0.
    Building the component raises for a period below 1 or a source other than "high_low" or "close".

    WHY THIS CANNOT LEAK: it reads only the rows t-period .. t of the data it is given (the last period + 1 rows,
    bar t being the last row): close[t-period] and close[t], and the high/low or close of the last period rows.
    All of them are known at bar t's close.
    """

    def __init__(self, name="NetMoveToRange", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 1:
            raise ValueError(f"NetMoveToRangeRatioComponent: period must be >= 1, got {self.period}")
        self.source = self.parameters.get("source", "high_low")
        if self.source not in ("high_low", "close"):
            raise ValueError(
                f"NetMoveToRangeRatioComponent: source must be 'high_low' or 'close', got {self.source!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float)
        c_now = float(close.iloc[-1])
        c_base = float(close.iloc[-(self.period + 1)])
        if self.source == "close":
            win = close.iloc[-self.period:]
            highs = win
            lows = win
        else:
            highs = data["high"].astype(float).iloc[-self.period:]
            lows = data["low"].astype(float).iloc[-self.period:]
        if np.isnan(c_now) or np.isnan(c_base) or highs.isna().any() or lows.isna().any():
            self._raw_value = float("nan")
        else:
            h = float(highs.max())
            l = float(lows.min())
            rng = h - l
            if rng == 0:
                self._raw_value = 0.0
            else:
                self._raw_value = float(abs(c_now - c_base) / rng)
            self.debug_info = {"net_move": abs(c_now - c_base), "range_high": h, "range_low": l,
                               "source": self.source}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1


class FlatnessWeightedRangePositionComponent(SubStrategyComponent):
    """
    Where the close sits in its recent range, weighted by how flat the window's net move is:

        p = period, window = bars t-p+1 .. t (bar t included)
        source = "close" (default): H = max(close[window]), L = min(close[window])
        source = "high_low":        H = max(high[window]),  L = min(low[window])
        pos  = (close[t] - L) / (H - L)
        flat = 1 - abs(close[t] - close[t-p]) / (H - L)
        raw_value = (2 x pos - 1) x flat          (0.0 when H = L)

    The default source "close" is the original output, unchanged. "high_low" measures the position and the
    flatness against the window's full high-low range (the Donchian channel proper).
    Range & sign: signed. It is positive above the window's middle, negative below it, and 0 at the middle or
    for a zero range. It is at most 1 in size whenever close[t-p] lies inside [L, H]. It is unbounded below,
    because flat turns negative when close[t-p] lies outside [L, H] by more than the range allows.
    Graded and continuous in the prices while the range is above 0.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN in any value read gives NaN. For "close" that is the last period + 1 closes. For "high_low"
    that is the high and low of the last period rows, close[t] and close[t-p]. A zero range gives 0.0.
    Building the component raises for a period below 2 or a source other than "close" or "high_low".

    WHY THIS CANNOT LEAK: it reads only the last period + 1 rows of data (bar t is the last row): the close of
    bar t-p, and the close (or high and low) of bars t-p+1 .. t, all known at bar t's close.
    """

    def __init__(self, name="FlatnessWeightedRangePosition", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(f"FlatnessWeightedRangePositionComponent: period must be >= 2, got {self.period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high_low"):
            raise ValueError(
                f"FlatnessWeightedRangePositionComponent: source must be 'close' or 'high_low', got {self.source!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        close = data["close"].astype(float).to_numpy()
        c_t = float(close[-1])
        c_b = float(close[-(p + 1)])
        if self.source == "close":
            win = close[-p:]
            if np.isnan(win).any() or np.isnan(c_b):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            H = float(win.max())
            L = float(win.min())
        else:
            hi = data["high"].astype(float).to_numpy()[-p:]
            lo = data["low"].astype(float).to_numpy()[-p:]
            if np.isnan(hi).any() or np.isnan(lo).any() or np.isnan(c_t) or np.isnan(c_b):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            H = float(hi.max())
            L = float(lo.min())
        rng = H - L
        if rng == 0:
            value = 0.0
        else:
            pos = (c_t - L) / rng
            flat = 1.0 - abs(c_t - c_b) / rng
            value = (2.0 * pos - 1.0) * flat
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"H": H, "L": L, "source": self.source}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1


class RangeShareHumpWeightedReturnComponent(SubStrategyComponent):
    """
    The period-bar return weighted by a hump of the net move's share of the window's high-low range:

        R = close[t] / close[t - period] - 1
        H = max(high[t - period + 1 .. t]),  L = min(low[t - period + 1 .. t])
        s = min(1, abs(close[t] - close[t - period]) / (H - L)),  s = 0 when H - L = 0
        raw_value = R x s x (1 - s)

    Range and sign: -0.25 and up, unbounded above. It is signed like the period-bar return, and its size is
    at most 0.25 x abs(R). It is 0 when the net move is 0, when the net move spans the whole range (s = 1),
    or for a zero range. For a given return it is largest at s = 0.5. Graded and continuous in the prices.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN close at bar t or t - period, or a NaN high or low in the last period rows, gives NaN.
    A close[t - period] not above 0 gives NaN (never on real bars). Building the component raises for a
    period below 1.

    WHY THIS CANNOT LEAK: it reads close of bars t and t - period and high and low of bars
    t - period + 1 .. t, all at or before the last row of data (bar t), and every one of them is known at bar
    t's close.
    """

    def __init__(self, name="RangeShareHumpReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 1:
            raise ValueError(f"RangeShareHumpWeightedReturnComponent: period must be >= 1, got {self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        close = data['close'].astype(float)
        high = data['high'].astype(float).iloc[-p:]
        low = data['low'].astype(float).iloc[-p:]
        c_t = float(close.iloc[-1])
        c_b = float(close.iloc[-(p + 1)])
        if np.isnan(c_t) or np.isnan(c_b) or high.isna().any() or low.isna().any() or not c_b > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rng = float(high.max()) - float(low.min())
        r = c_t / c_b - 1.0
        if rng > 0:
            s = min(1.0, max(0.0, abs(c_t - c_b) / rng))
        else:
            s = 0.0
        self._raw_value = float(r * s * (1.0 - s))
        self.confidence = 1.0
        self.debug_info = {'return': r, 'share': s, 'range': rng}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1


class NetMoveRangeAgeComponent(SubStrategyComponent):
    """
    How long the net move has held a large share of the window's high-low range, signed by the move:

        r(i) = abs(close[i] - close[i - period]) / (max(high[i-period+1 .. i]) - min(low[i-period+1 .. i]))
               (r(i) = 0.0 when that range is 0)
        n    = number of consecutive bars i ending at t (bar t included) with r(i) >= level, capped at max_bars
        raw_value = sign(close[t] - close[t - period]) * n

    Range: -max_bars .. +max_bars, integers. Positive while the period-bar return is up, negative while it is
    down. It is 0 when r(t) < level (and when the return is 0, since r(t) is then 0). Its size grows by one for
    each further bar on which the ratio holds at or above level.
    Warm-up: max_bars + period rows, bar t included.
    NaN: a NaN close in the last max_bars + period rows, or a NaN high or low in the last max_bars + period - 1
    rows, gives NaN.
    Building the component raises for period < 1, max_bars < 1, or level not above 0.

    WHY THIS CANNOT LEAK: it reads only the close, high and low of the last max_bars + period rows of data, the
    last of which is bar t; every value is known at bar t's close.
    """

    def __init__(self, name="NetMoveRangeAge", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 1:
            raise ValueError(f"NetMoveRangeAgeComponent: period must be >= 1, got {self.period}")
        self.level = float(self.parameters.get("level", 0.5))
        if not self.level > 0:
            raise ValueError(f"NetMoveRangeAgeComponent: level must be above 0, got {self.level}")
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(f"NetMoveRangeAgeComponent: max_bars must be >= 1, got {self.max_bars}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        m = self.max_bars
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        h = data['high'].astype(float).to_numpy()[-need:]
        lo = data['low'].astype(float).to_numpy()[-need:]
        if np.isnan(c).any() or np.isnan(h[1:]).any() or np.isnan(lo[1:]).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = 0
        for k in range(m):
            i = need - 1 - k
            rng = float(np.max(h[i - p + 1:i + 1]) - np.min(lo[i - p + 1:i + 1]))
            move = abs(float(c[i] - c[i - p]))
            r = move / rng if rng > 0 else 0.0
            if r >= self.level:
                n += 1
            else:
                break
        ret = float(c[-1] - c[-1 - p])
        sign = 1.0 if ret > 0 else (-1.0 if ret < 0 else 0.0)
        self._raw_value = float(sign * n)
        self.confidence = 1.0
        self.debug_info = {'run_length': n, 'net_move': ret}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.max_bars + self.period


class FallTimesFallComponent(SubStrategyComponent):
    """
    The product of two falls over two horizons, on every bar:

        F_s = max(0, -(close[t] / close[t - short_period] - 1))
        F_l = max(0, -(close[t] / close[t - long_period] - 1))
        raw_value = F_s x F_l x 100

    Range: 0 to below 100, never negative, no direction. It is 0 unless both returns are negative, and it
    grows with the size of each fall. It is graded and continuous in the closes, because the clips at 0 meet
    the product at 0.
    Warm-up: long_period + 1 rows, bar t included.

    NaN: a NaN close at t, t - short_period or t - long_period gives NaN. A base close not above 0 gives NaN
    (never on real bars).
    Building the component raises for a short_period below 1, a long_period below 1, or a short_period at
    or above long_period.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the rows up to and including bar t (the last
    row of data): close[t], close[t - short_period] and close[t - long_period].
    """

    def __init__(self, name="FallTimesFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 10))
        self.long_period = int(self.parameters.get("long_period", 60))
        if self.short_period < 1:
            raise ValueError(f"FallTimesFallComponent: short_period must be >= 1, got {self.short_period}")
        if self.long_period < 1:
            raise ValueError(f"FallTimesFallComponent: long_period must be >= 1, got {self.long_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"FallTimesFallComponent: short_period must be below long_period, got "
                f"{self.short_period} and {self.long_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float)
        c_t = float(close.iloc[-1])
        c_s = float(close.iloc[-(self.short_period + 1)])
        c_l = float(close.iloc[-(self.long_period + 1)])
        if np.isnan(c_t) or np.isnan(c_s) or np.isnan(c_l) or not c_s > 0 or not c_l > 0:
            self._raw_value = float("nan")
        else:
            f_s = max(0.0, -(c_t / c_s - 1.0))
            f_l = max(0.0, -(c_t / c_l - 1.0))
            self._raw_value = float(f_s * f_l * 100.0)
            self.debug_info = {"short_fall": f_s, "long_fall": f_l}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.long_period + 1




class DownStreakLossInUsualMovesComponent(SubStrategyComponent):
    """
    The move of the current one-sided streak of closes, counted in usual one-bar moves:

        side = "down" (default): n = number of consecutive bars i ending at t with close[i] < close[i-1]
        side = "up":             n = number of consecutive bars i ending at t with close[i] > close[i-1]
        n is capped at max_bars.
        base = "start" (default): P = close[t-n]
        base = "end":             P = close[t]
        m = mean(abs(close[j] / close[j-1] - 1)) over the last `window` one-bar returns, j = t-window+1 .. t
        side "down": raw_value = (close[t-n] - close[t]) / P / m
        side "up":   raw_value = (close[t] - close[t-n]) / P / m
        raw_value = 0.0 when n = 0 (bar t did not move to the counted side), and 0.0 when m = 0.

    With base "end" and side "down" the output is (close[t-n] / close[t] - 1) / m: the rise needed to recover the
    streak's loss, in usual one-bar moves. The defaults (side "down", base "start") are the original output,
    unchanged.
    Range: 0 and up, unbounded above, never negative; no direction. It is graded and continuous in the closes
    while the streak lasts.
    Warm-up: max(window, max_bars) + 1 rows, bar t included.

    NaN: a NaN close in the last max(window, max_bars) + 1 rows gives NaN, and so does a close not above 0 there
    (never on real bars). m = 0 gives 0.0 (never on real bars).
    Building the component raises for a window below 1, a max_bars below 1, a side other than "down" or "up", or a
    base other than "start" or "end".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window, max_bars) + 1 rows of data, the
    last of which is bar t; no row after t is read.
    """

    def __init__(self, name="DownStreakLoss", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 180))
        if self.window < 1:
            raise ValueError(f"DownStreakLossInUsualMovesComponent: window must be >= 1, got {self.window}")
        self.max_bars = int(self.parameters.get("max_bars", 180))
        if self.max_bars < 1:
            raise ValueError(f"DownStreakLossInUsualMovesComponent: max_bars must be >= 1, got {self.max_bars}")
        self.side = self.parameters.get("side", "down")
        if self.side not in ("down", "up"):
            raise ValueError(f"DownStreakLossInUsualMovesComponent: side must be 'down' or 'up', got {self.side!r}")
        self.base = self.parameters.get("base", "start")
        if self.base not in ("start", "end"):
            raise ValueError(f"DownStreakLossInUsualMovesComponent: base must be 'start' or 'end', got {self.base!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        last = len(c) - 1
        rets = c[last - self.window + 1:] / c[last - self.window:last] - 1.0
        m = float(np.mean(np.abs(rets)))
        n = 0
        i = last
        while n < self.max_bars:
            if self.side == "down":
                moved = c[i] < c[i - 1]
            else:
                moved = c[i] > c[i - 1]
            if not moved:
                break
            n += 1
            i -= 1
        if n == 0 or m == 0.0:
            value = 0.0
        else:
            start = float(c[last - n])
            end = float(c[last])
            diff = (start - end) if self.side == "down" else (end - start)
            divisor = start if self.base == "start" else end
            value = diff / divisor / m
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'streak_bars': n, 'mean_abs_return': m, 'side': self.side, 'base': self.base}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.window, self.max_bars) + 1


class DownStreakVolumeFadeComponent(SubStrategyComponent):
    """
    How volume fades across the current streak of down (or up) closes, on every bar:

        n = the number of consecutive bars i ending at t with close[i] < close[i-1] (side "down")
            or close[i] > close[i-1] (side "up"), capped at max_bars
        v = volume[t-n+1 .. t], x = 0 .. n-1
        n < 2:                          raw_value = 0
        statistic = "slope" (default):  raw_value = -b / mean(v),  b = sum((x-xm)(v-vm)) / sum((x-xm)^2)
        statistic = "log_ratio":        raw_value = ln(v[0] / v[n-1])
        statistic = "log_slope":        raw_value = -c,  c = sum((x-xm)(y-ym)) / sum((x-xm)^2),  y = ln(v)

    The defaults (side "down", statistic "slope") give the original output, unchanged.
    Graded and signed: positive and growing as volume fades across the streak, negative when it rises.
    "slope" lies strictly within (-6/(n+1), +6/(n+1)). "log_ratio" and "log_slope" are unbounded.
    "log_slope" is the per-bar decay rate of the log volume.
    A flat bar (equal close) ends either streak.
    Warm-up: max_bars + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` and `volume` columns of the last max_bars + 1 rows up to and
    including bar t (the last row of data); a bar's close and volume are known at that bar's close.

    NaN: a NaN close in the last max_bars + 1 rows gives NaN. With "slope", a NaN volume on a streak bar or a mean
    streak volume not above 0 gives NaN. With "log_ratio", a NaN volume or a volume not above 0 at the streak's
    first or last bar gives NaN. With "log_slope", a NaN volume or a volume not above 0 on any streak bar gives NaN.
    Building the component raises for max_bars below 2, a side other than "down" or "up", or a statistic other
    than "slope", "log_ratio" or "log_slope".
    """

    def __init__(self, name="DownStreakVolumeFade", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.max_bars = int(self.parameters.get("max_bars", 180))
        if self.max_bars < 2:
            raise ValueError(f"DownStreakVolumeFadeComponent: max_bars must be >= 2, got {self.max_bars}")
        self.side = self.parameters.get("side", "down")
        if self.side not in ("down", "up"):
            raise ValueError(f"DownStreakVolumeFadeComponent: side must be 'down' or 'up', got {self.side!r}")
        self.statistic = self.parameters.get("statistic", "slope")
        if self.statistic not in ("slope", "log_ratio", "log_slope"):
            raise ValueError(
                "DownStreakVolumeFadeComponent: statistic must be 'slope', 'log_ratio' or 'log_slope', "
                f"got {self.statistic!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        m = self.max_bars + 1
        close = data['close'].astype(float).to_numpy()[-m:]
        vol = data['volume'].astype(float).to_numpy()[-m:]
        self.confidence = 1.0
        if np.isnan(close).any():
            self._raw_value = float("nan")
            return
        n = 0
        j = len(close) - 1
        while n < self.max_bars and j >= 1:
            moved = close[j] < close[j - 1] if self.side == "down" else close[j] > close[j - 1]
            if not moved:
                break
            n += 1
            j -= 1
        self.debug_info = {'streak_bars': n, 'side': self.side, 'statistic': self.statistic}
        if n < 2:
            self._raw_value = 0.0
            return
        v = vol[-n:]
        x = np.arange(n, dtype=float)
        xd = x - x.mean()
        sxx = float(np.sum(xd * xd))
        if self.statistic == "slope":
            if np.isnan(v).any():
                self._raw_value = float("nan")
                return
            vm = float(v.mean())
            if not vm > 0:
                self._raw_value = float("nan")
                return
            b = float(np.sum(xd * (v - vm))) / sxx
            self._raw_value = float(-b / vm)
        elif self.statistic == "log_ratio":
            first, last = float(v[0]), float(v[-1])
            if np.isnan(first) or np.isnan(last) or not first > 0 or not last > 0:
                self._raw_value = float("nan")
                return
            self._raw_value = float(np.log(first / last))
        else:
            if np.isnan(v).any() or not (v > 0).all():
                self._raw_value = float("nan")
                return
            y = np.log(v)
            c = float(np.sum(xd * (y - y.mean()))) / sxx
            self._raw_value = float(-c)

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.max_bars + 1


class UpStreakGainTimesDepthBelowAverageComponent(SubStrategyComponent):
    """
    The up-streak's gain in usual one-bar moves, times the close's percent depth below its simple average:

        n = number of consecutive bars i ending at t with close[i] > close[i-1], capped at max_bars
        m = mean(abs(close[j] / close[j-1] - 1)) over the last `window` one-bar returns, bar t's included
        G = (close[t] - close[t-n]) / close[t-n] / m        (0 when n = 0 or m = 0)
        SMA = mean(close[t-ma_period+1 .. t])
        D = max(0, (SMA - close[t]) / SMA * 100)
        raw_value = G * D

    Range: 0 and up, unbounded above, never negative, with no direction. It is 0 when bar t did not close up
    or when the close is at or above its SMA. It grows with the streak's gain in usual moves and with the depth
    below the average. `negate` gives the short forecast.
    Warm-up: max(window + 1, max_bars + 1, ma_period) rows, bar t included.
    NaN: a NaN close in those rows gives NaN, and so does a close not above 0 there (never on real bars).
    m = 0 gives 0.
    Building the component raises for a window < 1, a max_bars < 1 or an ma_period < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window + 1, max_bars + 1, ma_period)
    rows of data, the last being bar t; a close is known at its bar's close.
    """

    def __init__(self, name="UpStreakGainDepth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 180))
        if self.window < 1:
            raise ValueError(f"UpStreakGainTimesDepthBelowAverageComponent: window must be >= 1, got {self.window}")
        self.max_bars = int(self.parameters.get("max_bars", 180))
        if self.max_bars < 1:
            raise ValueError(
                f"UpStreakGainTimesDepthBelowAverageComponent: max_bars must be >= 1, got {self.max_bars}")
        self.ma_period = int(self.parameters.get("ma_period", 180))
        if self.ma_period < 2:
            raise ValueError(
                f"UpStreakGainTimesDepthBelowAverageComponent: ma_period must be >= 2, got {self.ma_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = 0
        while n < self.max_bars and c[-1 - n] > c[-2 - n]:
            n += 1
        rets = c[-self.window:] / c[-self.window - 1:-1] - 1.0
        m = float(np.mean(np.abs(rets)))
        if n > 0 and m > 0:
            gain = (c[-1] - c[-1 - n]) / c[-1 - n] / m
        else:
            gain = 0.0
        sma = float(np.mean(c[-self.ma_period:]))
        depth = max(0.0, (sma - c[-1]) / sma * 100.0)
        self._raw_value = float(gain * depth)
        self.confidence = 1.0
        self.debug_info = {'streak': n, 'mean_abs_return': m, 'gain_usual_moves': float(gain),
                           'sma': sma, 'depth_pct': float(depth)}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.window + 1, self.max_bars + 1, self.ma_period)


class ThinVolumeScaledReturnComponent(SubStrategyComponent):
    """
    A return in usual moves, weighted by how thin recent volume is against an earlier base:

        r(i)  = close[i] / close[i - period] - 1
        m     = mean(abs(r(i))) over i = t - window + 1 .. t           (bar t included)
        Vr    = mean(volume[t - volume_period + 1 .. t])               (bar t included)
        Vb    = mean(volume[t - base_far .. t - base_near])
        raw_value = r(t) / m * Vb / Vr      (r(t) / m read as 0 when m = 0)

    Range & sign: unbounded, signed like the period-bar return. Its size grows with the move in usual
    moves and as recent volume falls below the base (Vb / Vr above 0, 1 when the means are equal).
    `negate` gives the reading signed against the move.
    Warm-up: max(window + period, base_far + 1) rows, bar t included (768 at the defaults).
    NaN: a NaN close in the last window + period rows, or a NaN volume in either volume window, gives NaN.
    A close not above 0 there gives NaN, and so does Vr not above 0 (neither happens on real bars).
    Building raises for period < 1, window < 1, volume_period < 1, base_near < volume_period,
    or base_far < base_near.

    WHY THIS CANNOT LEAK: it reads only the close and volume of the rows up to and including bar t (the last
    row of data): the closes of the last window + period rows and the volumes of bars t - base_far .. t.
    """

    def __init__(self, name="ThinVolumeScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        self.window = int(self.parameters.get("window", 720))
        self.volume_period = int(self.parameters.get("volume_period", 48))
        self.base_near = int(self.parameters.get("base_near", 49))
        self.base_far = int(self.parameters.get("base_far", 168))
        if self.period < 1:
            raise ValueError(f"ThinVolumeScaledReturnComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"ThinVolumeScaledReturnComponent: window must be >= 1, got {self.window}")
        if self.volume_period < 1:
            raise ValueError(
                f"ThinVolumeScaledReturnComponent: volume_period must be >= 1, got {self.volume_period}")
        if self.base_near < self.volume_period:
            raise ValueError(
                f"ThinVolumeScaledReturnComponent: base_near must be >= volume_period, got {self.base_near}")
        if self.base_far < self.base_near:
            raise ValueError(
                f"ThinVolumeScaledReturnComponent: base_far must be >= base_near, got {self.base_far}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float).to_numpy()
        vol = data["volume"].astype(float).to_numpy()
        n = len(close)
        c = close[-(self.window + self.period):]
        recent = vol[-self.volume_period:]
        base = vol[n - 1 - self.base_far: n - self.base_near]
        self.confidence = 1.0
        if np.isnan(c).any() or np.isnan(recent).any() or np.isnan(base).any() or (c <= 0).any():
            self._raw_value = float("nan")
            return
        r = c[self.period:] / c[:-self.period] - 1.0
        m = float(np.mean(np.abs(r)))
        vr = float(np.mean(recent))
        vb = float(np.mean(base))
        if not vr > 0:
            self._raw_value = float("nan")
            return
        scaled = 0.0 if m == 0 else float(r[-1]) / m
        self._raw_value = float(scaled * vb / vr)
        self.debug_info = {"return": float(r[-1]), "mean_abs_return": m,
                           "recent_volume": vr, "base_volume": vb}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.window + self.period, self.base_far + 1)


class RecentToPriorVolatilityWeightedReturnComponent(SubStrategyComponent):
    """
    A period-bar return weighted by recent volatility against a prior base, on every bar:

        R        = close[t] / close[t - period] - 1
        r[j]     = close[j] / close[j-1] - 1
        s_recent = std (ddof 1) of r[j], j = t-vol_period+1 .. t
        s_base   = std (ddof 1) of r[j], j = t-base_lag-base_period+1 .. t-base_lag
        return_scale = "percent" (default): raw_value = R x 100 x s_recent / s_base
        return_scale = "base_std":          raw_value = R / s_base x s_recent / s_base

    With period 1, vol_period 5, base_period 30, base_lag 0 and return_scale "base_std" the value is
    (close[t]/close[t-1] - 1) / s30 x s5 / s30.
    Range: unbounded, signed like the period-bar return, 0 when that return is 0. The size grows with the move
    and with the volatility ratio (0 and up, 1 at equal volatility). return_scale "percent" is the original
    output, unchanged.
    Warm-up: max(period, vol_period, base_lag + base_period) + 1 rows, bar t included.

    NaN: a NaN close in the last warm-up rows gives NaN, and so does a close not above 0 there (never on real
    bars) or an s_base of 0 (flat base returns, never on real bars).
    Building raises for period < 1, vol_period < 2, base_period < 2, base_lag < 0, or a return_scale other
    than "percent" or "base_std".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, vol_period,
    base_lag + base_period) + 1 rows of data, the last of which is bar t; each close is known at its bar's close.
    """

    def __init__(self, name="RecentToPriorVolWeightedReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        self.vol_period = int(self.parameters.get("vol_period", 48))
        self.base_period = int(self.parameters.get("base_period", 168))
        self.base_lag = int(self.parameters.get("base_lag", 48))
        self.return_scale = self.parameters.get("return_scale", "percent")
        if self.period < 1:
            raise ValueError(f"RecentToPriorVolatilityWeightedReturnComponent: period must be >= 1, got {self.period}")
        if self.vol_period < 2:
            raise ValueError(f"RecentToPriorVolatilityWeightedReturnComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.base_period < 2:
            raise ValueError(f"RecentToPriorVolatilityWeightedReturnComponent: base_period must be >= 2, got {self.base_period}")
        if self.base_lag < 0:
            raise ValueError(f"RecentToPriorVolatilityWeightedReturnComponent: base_lag must be >= 0, got {self.base_lag}")
        if self.return_scale not in ("percent", "base_std"):
            raise ValueError(
                f"RecentToPriorVolatilityWeightedReturnComponent: return_scale must be 'percent' or 'base_std', "
                f"got {self.return_scale!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        w = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-w:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[1:] / c[:-1] - 1.0
        recent = r[-self.vol_period:]
        if self.base_lag == 0:
            base = r[-self.base_period:]
        else:
            base = r[-(self.base_lag + self.base_period):-self.base_lag]
        s_recent = float(np.std(recent, ddof=1))
        s_base = float(np.std(base, ddof=1))
        ret = float(c[-1] / c[-1 - self.period] - 1.0)
        if not s_base > 0:
            self._raw_value = float("nan")
        elif self.return_scale == "base_std":
            self._raw_value = float(ret / s_base * s_recent / s_base)
        else:
            self._raw_value = float(ret * 100.0 * s_recent / s_base)
        self.confidence = 1.0
        self.debug_info = {"return": ret, "s_recent": s_recent, "s_base": s_base,
                           "return_scale": self.return_scale}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period, self.vol_period, self.base_lag + self.base_period) + 1


class RecentToPriorVolatilityRatioComponent(SubStrategyComponent):
    """
    Recent one-bar return volatility against an earlier base, on every bar:

        r[j] = close[j] / close[j-1] - 1
        s_recent = std (ddof 1) of r[j], j = t-vol_period+1 .. t
        s_base   = std (ddof 1) of r[j], j = t-base_lag-base_period+1 .. t-base_lag
        form "ratio" (default): raw_value = s_recent / s_base
        form "centred":         raw_value = s_recent / s_base - 1

    Range and sign: "ratio" is 0 and up, unbounded above, never negative, with no direction. It is 1 when the
    recent bars are as volatile as the base and grows continuously as they get more turbulent. "centred" is -1
    and up, signed, and 0 at equal volatility.
    Warm-up: max(vol_period, base_lag + base_period) + 1 rows, bar t included (217 at the defaults).
    NaN: a NaN close among the rows read gives NaN. A close not above 0 among them gives NaN. s_base = 0 gives NaN.
    Building raises for vol_period < 2, base_period < 2, base_lag < 0, or a form other than "ratio" or "centred".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(vol_period, base_lag + base_period) + 1
    rows of data, the last of which is bar t; no row after bar t is read.
    """

    def __init__(self, name="RecentToPriorVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 48))
        self.base_period = int(self.parameters.get("base_period", 168))
        self.base_lag = int(self.parameters.get("base_lag", 48))
        self.form = self.parameters.get("form", "ratio")
        if self.vol_period < 2:
            raise ValueError(f"RecentToPriorVolatilityRatioComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.base_period < 2:
            raise ValueError(f"RecentToPriorVolatilityRatioComponent: base_period must be >= 2, got {self.base_period}")
        if self.base_lag < 0:
            raise ValueError(f"RecentToPriorVolatilityRatioComponent: base_lag must be >= 0, got {self.base_lag}")
        if self.form not in ("ratio", "centred"):
            raise ValueError(f"RecentToPriorVolatilityRatioComponent: form must be 'ratio' or 'centred', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        last = len(c) - 1  # bar t

        def returns(first_j, last_j):
            prev = c[first_j - 1:last_j]
            cur = c[first_j:last_j + 1]
            if np.isnan(prev).any() or np.isnan(cur).any():
                return None
            if not (prev > 0).all() or not (cur > 0).all():
                return None
            return cur / prev - 1.0

        r_recent = returns(last - self.vol_period + 1, last)
        b_end = last - self.base_lag
        r_base = returns(b_end - self.base_period + 1, b_end)
        if r_recent is None or r_base is None:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        s_recent = float(np.std(r_recent, ddof=1))
        s_base = float(np.std(r_base, ddof=1))
        if not s_base > 0:
            self._raw_value = float("nan")
        else:
            ratio = s_recent / s_base
            self._raw_value = float(ratio - 1.0) if self.form == "centred" else float(ratio)
        self.confidence = 1.0
        self.debug_info = {"s_recent": s_recent, "s_base": s_base, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.vol_period, self.base_lag + self.base_period) + 1


class FailedBreakoutDepthComponent(SubStrategyComponent):
    """
    Depth of a close below the level of a recent breakout that failed, read at bar e = t - lag:

        e = t - lag                                   (lag 0, the default: e = t)
        candidates: exclude_current 0 (default): bars e-fail_window+1 .. e   (bar e included)
                    exclude_current 1:           bars e-fail_window .. e-1   (bar e excluded)
        H(j) = max(close[j-period] .. close[j-1])     (source "close", default)
             = max(high[j-period] .. high[j-1])       (source "high")
        j = the most recent candidate with close[j] > H(j)   (strictly higher: a tie is not a breakout)
        R = H(j)     (reference "prior_high", default)
          = low[j]   (reference "breakout_low")
        raw_value = max(0, R - close[e]) / R x 100,  or 0.0 when no candidate broke out

    Range and sign: 0 and up, below 100, never negative; no direction. It is 0 when no breakout lies in the window
    or when close[e] is at or above R. It grows linearly as close[e] sinks below the level.
    The defaults (reference "prior_high", exclude_current 0, lag 0) are the original output, unchanged.
    lag delays the whole reading: the value at t is the lag-0 value at bar t-lag.
    Warm-up: period + fail_window + exclude_current + lag rows, bar t included.

    NaN: source "close" reads closes of bars e-period-fail_window-exclude_current+1 .. e. Source "high" reads highs
    of bars e-period-fail_window-exclude_current+1 .. e-exclude_current-1 and closes of bars
    e-fail_window-exclude_current+1 .. e. reference "breakout_low" also reads low[j]. A NaN in any value read
    gives NaN, and so does an R not above 0 (never on real bars).
    Building the component raises for period < 1, fail_window < 1, a source other than "close" or "high", a
    reference other than "prior_high" or "breakout_low", an exclude_current other than 0 or 1, or a lag that is
    not an integer >= 0.

    WHY THIS CANNOT LEAK: it reads only rows up to bar e = t - lag (the last row of data minus lag), so it reads
    no row after bar t. Every high, low and close it reads is known at that bar's close.
    """

    def __init__(self, name="FailedBreakoutDepth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutDepthComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(f"FailedBreakoutDepthComponent: fail_window must be >= 1, got {self.fail_window}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high"):
            raise ValueError(f"FailedBreakoutDepthComponent: source must be 'close' or 'high', got {self.source!r}")
        self.reference = self.parameters.get("reference", "prior_high")
        if self.reference not in ("prior_high", "breakout_low"):
            raise ValueError(
                f"FailedBreakoutDepthComponent: reference must be 'prior_high' or 'breakout_low', got {self.reference!r}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"FailedBreakoutDepthComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        lag = self.parameters.get("lag", 0)
        if isinstance(lag, bool):
            lag = int(lag)
        try:
            lag_int = int(lag)
        except (TypeError, ValueError):
            raise ValueError(f"FailedBreakoutDepthComponent: lag must be an integer >= 0, got {lag!r}")
        if lag_int != lag or lag_int < 0:
            raise ValueError(f"FailedBreakoutDepthComponent: lag must be an integer >= 0, got {lag!r}")
        self.lag = lag_int
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        fw = self.fail_window
        ex = self.exclude_current
        n = len(data)
        e = n - 1 - self.lag
        close = data["close"].astype(float).to_numpy()
        first = e - p - fw - ex + 1
        if self.source == "close":
            src = close
            if np.isnan(close[first:e + 1]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        else:
            src = data["high"].astype(float).to_numpy()
            if np.isnan(src[first:e - ex]).any() or np.isnan(close[e - fw - ex + 1:e + 1]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        if ex == 0:
            candidates = range(e, e - fw, -1)
        else:
            candidates = range(e - 1, e - fw - 1, -1)
        found = None
        level = None
        for j in candidates:
            hj = float(np.max(src[j - p:j]))
            if close[j] > hj:
                found = j
                level = hj
                break
        if found is None:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {"breakout_bar": None, "e": e}
            return
        if self.reference == "breakout_low":
            r = float(data["low"].astype(float).iloc[found])
        else:
            r = level
        if np.isnan(r) or not r > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(max(0.0, r - close[e]) / r * 100.0)
        self.confidence = 1.0
        self.debug_info = {"breakout_bar": int(found), "e": e, "H": level, "R": r}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.fail_window + self.exclude_current + self.lag


class FailedBreakoutVolumeRatioComponent(SubStrategyComponent):
    """
    The volume of a failed breakout bar against its own average, on bar t:

        j = the most recent bar in t-fail_window+1 .. t (bar t included) with close[j] > H(j)
            source = "close" (default): H(j) = max(close[j-period] .. close[j-1])
            source = "high":            H(j) = max(high[j-period] .. high[j-1])
        failed breakout: such a j exists and close[t] < H(j)
        r = volume[j] / mean(volume[j-volume_period+1 .. j])
        form = "ratio" (default): raw_value = r
        form = "thin":            raw_value = max(0, 1 - r)
        raw_value = 0.0 when no bar of the window broke out, or when close[t] >= H(j)
        (so 0.0 when bar t itself breaks out).

    Range: "ratio" is 0, or above 0 up to volume_period (the mean includes volume[j]). "thin" is 0 to below 1:
    it is 0 when the breakout bar's volume is at or above its average and grows toward 1 as that volume thins.
    Both are never negative and have no direction. They are graded and continuous in the volumes.
    form "ratio" is the original output, unchanged.
    Warm-up: max(period + fail_window, volume_period + fail_window - 1) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only rows up to and including bar t (the last row of data). The closes
    (and highs) of bars t-period-fail_window+1 .. t and the volumes of bars j-volume_period+1 .. j are read,
    with j <= t. Each is known at its bar's close.

    NaN: a NaN close in the rows read (or a NaN high, with source "high") gives NaN. For a failed breakout,
    a NaN volume in bars j-volume_period+1 .. j, or a mean volume not above 0 (never on real bars), gives NaN.
    Building the component raises for period < 1, fail_window < 1, volume_period < 2, a source other than
    "close" or "high", or a form other than "ratio" or "thin".
    """

    def __init__(self, name="FailedBreakoutVolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutVolumeRatioComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutVolumeRatioComponent: fail_window must be >= 1, got {self.fail_window}")
        self.volume_period = int(self.parameters.get("volume_period", 20))
        if self.volume_period < 2:
            raise ValueError(
                f"FailedBreakoutVolumeRatioComponent: volume_period must be >= 2, got {self.volume_period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high"):
            raise ValueError(
                f"FailedBreakoutVolumeRatioComponent: source must be 'close' or 'high', got {self.source!r}")
        self.form = self.parameters.get("form", "ratio")
        if self.form not in ("ratio", "thin"):
            raise ValueError(
                f"FailedBreakoutVolumeRatioComponent: form must be 'ratio' or 'thin', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float).to_numpy()
        n = len(close)
        t = n - 1
        p = self.period
        fw = self.fail_window
        if self.source == "close":
            ref = close
            if np.isnan(close[n - p - fw:]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        else:
            ref = data['high'].astype(float).to_numpy()
            if np.isnan(ref[t - p - fw + 1:t]).any() or np.isnan(close[t - fw + 1:]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        j = None
        h_j = None
        for cand in range(t, t - fw, -1):
            h = float(np.max(ref[cand - p:cand]))
            if close[cand] > h:
                j = cand
                h_j = h
                break
        if j is None or not close[t] < h_j:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {'breakout_bar': j, 'prior_high': h_j}
            return
        vol = data['volume'].astype(float).to_numpy()
        win = vol[j - self.volume_period + 1:j + 1]
        if np.isnan(win).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        m = float(np.mean(win))
        if not m > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = float(vol[j] / m)
        if self.form == "thin":
            self._raw_value = float(max(0.0, 1.0 - r))
        else:
            self._raw_value = r
        self.confidence = 1.0
        self.debug_info = {'breakout_bar': j, 'prior_high': h_j, 'volume_ratio': r, 'form': self.form}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period + self.fail_window, self.volume_period + self.fail_window - 1)


class FailedBreakoutExcursionComponent(SubStrategyComponent):
    """
    How far a breakout pushed above the old high before the close fell back under it:

        j = the most recent bar in t-fail_window+1 .. t (bar t included) with close[j] > H(j),
            H(j) = max(close[j-period] .. close[j-1])
        peak_source = "high" (default): P = max(high[j .. t])
        peak_source = "close":          P = max(close[j .. t])
        raw_value = (P - H(j)) / H(j) x 100   when close[t] < H(j)
        raw_value = 0                          when no bar of the window broke out, or close[t] >= H(j)

    Range: 0, or above 0 and unbounded above (at least (close[j] - H(j)) / H(j) x 100 when non-zero,
    since P >= close[j]); never negative; no direction. Graded: it grows linearly with the peak's
    distance above the old high. peak_source "high" is the original output, unchanged.
    Warm-up: period + fail_window rows, bar t included.

    NaN: a NaN close in the last period + fail_window rows gives NaN; with peak_source "high", a NaN
    high in bars j .. t (read only for a failed breakout) gives NaN; an H(j) not above 0 gives NaN
    (never on real bars). Building raises for period < 1, fail_window < 1, or a peak_source other
    than "high" or "close".

    WHY THIS CANNOT LEAK: it reads only the close of the last period + fail_window rows up to and
    including bar t (the last row of data), and with peak_source "high" the high of bars j .. t;
    every one of these is known at bar t's close.
    """

    def __init__(self, name="FailedBreakoutExcursion", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutExcursionComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 4))
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutExcursionComponent: fail_window must be >= 1, got {self.fail_window}")
        self.peak_source = self.parameters.get("peak_source", "high")
        if self.peak_source not in ("high", "close"):
            raise ValueError(
                f"FailedBreakoutExcursionComponent: peak_source must be 'high' or 'close', got {self.peak_source!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        close = data['close'].astype(float).to_numpy()[-n:]
        self.confidence = 1.0
        if np.isnan(close).any():
            self._raw_value = float("nan")
            return
        t = n - 1
        j = None
        h = None
        for jj in range(t, t - self.fail_window, -1):
            hj = float(np.max(close[jj - self.period:jj]))
            if close[jj] > hj:
                j = jj
                h = hj
                break
        if j is None:
            self._raw_value = 0.0
            return
        if not h > 0:
            self._raw_value = float("nan")
            return
        if close[t] >= h:
            self._raw_value = 0.0
            return
        if self.peak_source == "high":
            highs = data['high'].astype(float).to_numpy()[-n:][j:]
            if np.isnan(highs).any():
                self._raw_value = float("nan")
                return
            p = float(np.max(highs))
        else:
            p = float(np.max(close[j:]))
        self._raw_value = float((p - h) / h * 100.0)
        self.debug_info = {'breakout_offset': t - j, 'old_high': h, 'peak': p,
                           'peak_source': self.peak_source}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.fail_window


class FailedBreakoutDepthInUsualMovesComponent(SubStrategyComponent):
    """
    Depth of a failed breakout's re-entry close under the old closing high, in usual one-bar moves:

        e = t - lag
        j = the most recent bar with close[j] > H(j), searched in
            exclude_current = 1 (default): e - fail_window .. e - 1   (bar e excluded)
            exclude_current = 0:           e - fail_window + 1 .. e   (bar e included)
        H(j) = max(close[j - period] .. close[j - 1])
        s(e) = std (ddof 1) of the vol_period returns close[i] / close[i-1] - 1, i = e - vol_period + 1 .. e
        raw_value = max(0, H(j) - close[e]) / H(j) / s(e)
        raw_value = 0 when no bar of the window broke out, or when s(e) = 0

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 when close[e] >= H(j), and so 0
    when bar e itself breaks out with exclude_current 0. It grows linearly as close[e] sinks below the old high.
    exclude_current 1 with lag 0 (the defaults) is the original output, unchanged.
    Warm-up: max(period + fail_window + exclude_current, vol_period + 1) + lag rows, bar t included.

    NaN: a NaN close, or a close not above 0, among rows t - warmup + 1 .. e gives NaN.
    s(e) = 0 gives 0 (never on real bars).
    Building raises for period < 1, fail_window < 1, vol_period < 2, exclude_current not 0 or 1,
    or lag not an integer >= 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of rows t - warmup + 1 .. t - lag, all at or before
    bar t (the last row of data); no row after bar t - lag is read.
    """

    def __init__(self, name="FailedBreakoutDepthInUsualMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutDepthInUsualMovesComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutDepthInUsualMovesComponent: fail_window must be >= 1, got {self.fail_window}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"FailedBreakoutDepthInUsualMovesComponent: vol_period must be >= 2, got {self.vol_period}")
        ex = self.parameters.get("exclude_current", 1)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(
                f"FailedBreakoutDepthInUsualMovesComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        lag = self.parameters.get("lag", 0)
        if isinstance(lag, bool):
            raise ValueError(f"FailedBreakoutDepthInUsualMovesComponent: lag must be an integer >= 0, got {lag!r}")
        try:
            lag_int = int(lag)
        except (TypeError, ValueError):
            raise ValueError(f"FailedBreakoutDepthInUsualMovesComponent: lag must be an integer >= 0, got {lag!r}")
        if lag_int != lag or lag_int < 0:
            raise ValueError(f"FailedBreakoutDepthInUsualMovesComponent: lag must be an integer >= 0, got {lag!r}")
        self.lag = lag_int
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()
        n = len(c)
        e = n - 1 - self.lag
        req = self.get_required_periods()
        seg = c[n - req:e + 1]
        if np.isnan(seg).any() or (seg <= 0).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        x = self.exclude_current
        j_found = None
        h_found = None
        for j in range(e - x, e - x - self.fail_window, -1):
            h = float(np.max(c[j - self.period:j]))
            if c[j] > h:
                j_found = j
                h_found = h
                break
        rets = c[e - self.vol_period + 1:e + 1] / c[e - self.vol_period:e] - 1.0
        s = float(np.std(rets, ddof=1))
        if j_found is None or not s > 0:
            value = 0.0
        else:
            value = max(0.0, h_found - float(c[e])) / h_found / s
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'breakout_bar_offset': None if j_found is None else int(n - 1 - j_found),
                           'old_high': h_found, 'std': s, 'lag': self.lag,
                           'exclude_current': self.exclude_current}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period + self.fail_window + self.exclude_current, self.vol_period + 1) + self.lag


class BreakoutLowDepthPerRunUpComponent(SubStrategyComponent):
    """
    Depth of the close under the low of the most recent breakout bar, discounted by the rise into that bar:

        H(j) = max(high[j - period] .. high[j - 1])              (bar j excluded)
        j    = the most recent bar in t - fail_window + 1 .. t with close[j] > H(j)
        D    = max(0, low[j] - close[t]) / low[j] x 100
        U    = max(0, close[j] / close[j - rise_period] - 1) x 100
        raw_value = D / (1 + U)
        raw_value = 0.0 when no bar of the window broke out.

    Range: 0 to below 100, never negative, no direction. It is 0 with no breakout in the window, or when
    close[t] >= low[j] (so 0 when bar t itself breaks out). It grows as the close sinks below the breakout
    bar's low and as the run-up into bar j shrinks (U = 0 for a flat or falling run-up). Graded.
    Warm-up: max(period, rise_period) + fail_window rows, bar t included.

    NaN: a NaN high in bars t-fail_window-period+1 .. t-1, a NaN close in bars t-fail_window+1 .. t, or a
    NaN low[j] or close[j - rise_period] for the chosen bar gives NaN. A low[j] or close[j - rise_period]
    not above 0 gives NaN (never on real bars).
    Building the component raises for period < 1, fail_window < 1 or rise_period < 1.

    WHY THIS CANNOT LEAK: it reads only high, low and close of rows up to and including bar t (the last row
    of data): highs of bars t-fail_window-period+1 .. t-1, closes of bars t-fail_window+1 .. t, and low[j],
    close[j - rise_period] with j <= t; every value is known at its bar's close.
    """

    def __init__(self, name="BreakoutLowDepthPerRunUp", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"BreakoutLowDepthPerRunUpComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(
                f"BreakoutLowDepthPerRunUpComponent: fail_window must be >= 1, got {self.fail_window}")
        self.rise_period = int(self.parameters.get("rise_period", 20))
        if self.rise_period < 1:
            raise ValueError(
                f"BreakoutLowDepthPerRunUpComponent: rise_period must be >= 1, got {self.rise_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].to_numpy(dtype=float)
        low = data['low'].to_numpy(dtype=float)
        close = data['close'].to_numpy(dtype=float)
        t = len(close) - 1
        p, fw, rp = self.period, self.fail_window, self.rise_period
        hs = high[t - fw - p + 1:t]
        cs = close[t - fw + 1:t + 1]
        self.confidence = 1.0
        if np.isnan(hs).any() or np.isnan(cs).any():
            self._raw_value = float("nan")
            return
        j = None
        for cand in range(t, t - fw, -1):
            h_prior = float(np.max(high[cand - p:cand]))
            if close[cand] > h_prior:
                j = cand
                break
        if j is None:
            self._raw_value = 0.0
            self.debug_info = {'breakout_bar': None}
            return
        lj = float(low[j])
        base = float(close[j - rp])
        if np.isnan(lj) or np.isnan(base) or not lj > 0 or not base > 0:
            self._raw_value = float("nan")
            return
        depth = max(0.0, lj - float(close[t])) / lj * 100.0
        rise = max(0.0, float(close[j]) / base - 1.0) * 100.0
        self._raw_value = float(depth / (1.0 + rise))
        self.debug_info = {'breakout_bar_offset': t - j, 'breakout_low': lj, 'depth_pct': depth,
                           'run_up_pct': rise}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.rise_period) + self.fail_window


class FailedBreakoutDepthVolatilityRatioComponent(SubStrategyComponent):
    """
    Depth of a failed closing breakout under the old high, weighted by how calm the recent bars are:

        j = the most recent bar with close[j] > H(j), H(j) = max(close[j-period] .. close[j-1]),
            searched in t-fail_window .. t-1      (exclude_current = 1, default; bar t excluded)
            or in       t-fail_window+1 .. t      (exclude_current = 0)
        depth = max(0, H(j) - close[t]) / H(j) x 100        (0 when no bar of the window broke out)
        r[i] = close[i] / close[i-1] - 1
        s_recent = std (ddof 1) of r[t-vol_period+1 .. t]
        s_base   = std (ddof 1) of r[t-base_vol_period+1 .. t]
        raw_value = depth x s_base / s_recent               (0 when s_recent = 0)

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 with no breakout in the window, or with
    close[t] at or above H(j). It grows as the close sinks under the old high and as the recent volatility falls
    below the longer one.
    Warm-up: max(period + fail_window + exclude_current, vol_period + 1, base_vol_period + 1) rows, bar t included
    (61 at the defaults).
    NaN: a NaN close in those rows gives NaN, and so does a close not above 0 there or an H(j) not above 0 (never on
    real bars). s_recent = 0 (a flat return window, never on real bars) gives 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last warm-up rows of data, the last of them being
    bar t; every breakout test, high and return uses closes at or before bar t.
    """

    def __init__(self, name="FailedBreakoutDepthVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutDepthVolatilityRatioComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutDepthVolatilityRatioComponent: fail_window must be >= 1, got {self.fail_window}")
        ex = self.parameters.get("exclude_current", 1)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(
                f"FailedBreakoutDepthVolatilityRatioComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"FailedBreakoutDepthVolatilityRatioComponent: vol_period must be >= 2, got {self.vol_period}")
        self.base_vol_period = int(self.parameters.get("base_vol_period", 60))
        if self.base_vol_period < 2:
            raise ValueError(
                f"FailedBreakoutDepthVolatilityRatioComponent: base_vol_period must be >= 2, "
                f"got {self.base_vol_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        t = n - 1
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.exclude_current == 1:
            lo, hi = t - self.fail_window, t - 1
        else:
            lo, hi = t - self.fail_window + 1, t
        depth = 0.0
        hj = None
        for j in range(hi, lo - 1, -1):
            h = float(np.max(c[j - self.period:j]))
            if c[j] > h:
                hj = h
                break
        if hj is not None:
            if not hj > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            depth = max(0.0, hj - c[t]) / hj * 100.0
        r = c[1:] / c[:-1] - 1.0
        s_recent = float(np.std(r[-self.vol_period:], ddof=1))
        s_base = float(np.std(r[-self.base_vol_period:], ddof=1))
        if s_recent == 0.0:
            value = 0.0
        else:
            value = depth * s_base / s_recent
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'old_high': hj, 'depth_pct': depth, 's_recent': s_recent, 's_base': s_base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + self.fail_window + self.exclude_current,
                   self.vol_period + 1, self.base_vol_period + 1)


class FailedBreakoutDepthRunUpDiscountComponent(SubStrategyComponent):
    """
    Depth of a failed closing breakout under the old high, discounted by the rally into the breakout:

        j    = the most recent bar in t-fail_window+1 .. t (bar t included) with close[j] > H(j),
               H(j) = max(close[j-period] .. close[j-1])
        R(j) = close[j] / close[j-rise_period] - 1
        m    = mean over i = t-window+1 .. t of abs(close[i] / close[i-rise_period] - 1)
        raw_value = max(0, H(j) - close[t]) / H(j) x 100 x max(0, 1 - R(j) / m)

    The value is 0 when no bar of the window broke out, when close[t] >= H(j) (so 0 when bar t itself breaks out),
    or when m = 0.
    Range: 0 and up, never negative, no direction. The depth is below 100, and the weight is 0 to 1 + 1/m: it is 0
    once the run-up is one usual rise_period-bar move or more, 1 for a flat run-up, and above 1 for a falling one.
    Graded: continuous in close[t] while the same breakout stays the most recent.
    Warm-up: max(period + fail_window, rise_period + fail_window, window + rise_period) rows, bar t included
    (140 at the defaults).
    NaN: a NaN close in those rows gives NaN, and so does a close not above 0 there (never on real bars).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last get_required_periods() rows of data, ending
    at bar t (the last row). Every H(j), R(j) and m uses closes at or before bar t.
    """

    def __init__(self, name="FailedBreakoutDepthRunUpDiscount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        self.fail_window = int(self.parameters.get("fail_window", 10))
        self.rise_period = int(self.parameters.get("rise_period", 20))
        self.window = int(self.parameters.get("window", 120))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutDepthRunUpDiscountComponent: period must be >= 1, got {self.period}")
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutDepthRunUpDiscountComponent: fail_window must be >= 1, got {self.fail_window}")
        if self.rise_period < 1:
            raise ValueError(
                f"FailedBreakoutDepthRunUpDiscountComponent: rise_period must be >= 1, got {self.rise_period}")
        if self.window < 1:
            raise ValueError(f"FailedBreakoutDepthRunUpDiscountComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        self.confidence = 1.0
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            return
        t = n - 1
        j = None
        hj = None
        for jj in range(t, t - self.fail_window, -1):
            h = float(np.max(c[jj - self.period:jj]))
            if c[jj] > h:
                j = jj
                hj = h
                break
        if j is None or not c[t] < hj:
            self._raw_value = 0.0
            self.debug_info = {"breakout_offset": None if j is None else t - j}
            return
        depth = (hj - c[t]) / hj * 100.0
        idx = np.arange(t - self.window + 1, t + 1)
        m = float(np.mean(np.abs(c[idx] / c[idx - self.rise_period] - 1.0)))
        if not m > 0:
            self._raw_value = 0.0
            return
        r = float(c[j] / c[j - self.rise_period] - 1.0)
        w = max(0.0, 1.0 - r / m)
        self._raw_value = float(depth * w)
        self.debug_info = {"breakout_offset": t - j, "old_high": hj, "depth": depth, "run_up": r,
                           "mean_abs_move": m, "weight": w}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + self.fail_window, self.rise_period + self.fail_window,
                   self.window + self.rise_period)


class VolatilityWeightedFallComponent(SubStrategyComponent):
    """
    Bar t's fall weighted by the coin's recent volatility:

        r[j] = close[j] / close[j-1] - 1,  j = t - vol_period + 1 .. t   (bar t's return included)
        s    = std(r, ddof=1)
        raw_value = max(0, -r[t]) x 100 x s

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 on up bars and flat bars, and it grows
    with the depth of bar t's fall (in percent) and with the volatility s of the last vol_period one-bar returns.
    Graded and continuous in the closes.
    Warm-up: vol_period + 1 rows, bar t included.

    NaN: a NaN close in the last vol_period + 1 rows gives NaN. A close not above 0 there also gives NaN (never on
    real bars). Building the component raises for a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last vol_period + 1 rows of data, bar t (the last
    row) included. Each close is known at its bar's close.
    """

    def __init__(self, name="VolatilityWeightedFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"VolatilityWeightedFallComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = data['close'].astype(float).iloc[-(self.vol_period + 1):].to_numpy()
        if np.isnan(closes).any() or (closes <= 0).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = closes[1:] / closes[:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        fall = max(0.0, -float(rets[-1])) * 100.0
        self._raw_value = float(fall * s)
        self.confidence = 1.0
        self.debug_info = {'fall_pct': fall, 'vol': s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.vol_period + 1


class BarBodySizeComponent(SubStrategyComponent):
    """
    The size of the current bar's body, the net move from its open, on bar t:

        B = abs(close[t] - open[t])
        relative_to = "open" (default):  body = B / open[t] x 100            (percent of the open)
        relative_to = "range":           body = B / (high[t] - low[t])       (0.0 when high[t] = low[t])
        form = "body" (default):         raw_value = body
        form = "flatness" (needs relative_to "range"):
                                         raw_value = 1 - B / (high[t] - low[t])   (1.0 when high[t] = low[t])

    form "body" is the original output, unchanged. form "flatness" is 1 minus the body's share of the range.
    It equals 1 when the close equals the open (or for a zero range) and 0 when the body spans the whole range.
    It grows continuously as the close nears the open. No config step gives 1 minus a value, hence the setting.

    Range & sign: "open" is 0 and up, never negative. "range" is 0 to 1 on real bars, never negative.
    "flatness" is 0 to 1 on real bars, never negative. None of them has a direction.
    Warm-up: 1 row (bar t only).

    NaN: a NaN in any value read gives NaN. With "open", an open not above 0 gives NaN (never on real bars).
    A missing column raises.
    Building the component raises for a relative_to other than "open" or "range", for a form other than "body"
    or "flatness", and for form "flatness" with relative_to "open".

    WHY THIS CANNOT LEAK: it reads only the open, close (and, for "range", the high and low) of the last row of
    data, bar t itself, all known at that bar's close.
    """

    def __init__(self, name="BarBodySize", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.relative_to = self.parameters.get("relative_to", "open")
        if self.relative_to not in ("open", "range"):
            raise ValueError(
                f"BarBodySizeComponent: relative_to must be 'open' or 'range', got {self.relative_to!r}")
        self.form = self.parameters.get("form", "body")
        if self.form not in ("body", "flatness"):
            raise ValueError(f"BarBodySizeComponent: form must be 'body' or 'flatness', got {self.form!r}")
        if self.form == "flatness" and self.relative_to != "range":
            raise ValueError("BarBodySizeComponent: form 'flatness' needs relative_to 'range'")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        o = float(data["open"].iloc[-1])
        c = float(data["close"].iloc[-1])
        if self.relative_to == "open":
            if np.isnan(o) or np.isnan(c) or not o > 0:
                value = float("nan")
            else:
                value = abs(c - o) / o * 100.0
        else:
            h = float(data["high"].iloc[-1])
            lo = float(data["low"].iloc[-1])
            if np.isnan(o) or np.isnan(c) or np.isnan(h) or np.isnan(lo):
                value = float("nan")
            else:
                rng = h - lo
                share = 0.0 if rng == 0 else abs(c - o) / rng
                value = (1.0 - share) if self.form == "flatness" else share
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"relative_to": self.relative_to, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return 1


class VolumeWeightedCloseLocationComponent(SubStrategyComponent):
    """
    Close location in the bar's range, weighted by the bar's volume against its average volume:

        base = volume[t - volume_period - exclude_current + 1 .. t - exclude_current]
            exclude_current = 0 (default): volume[t - volume_period + 1 .. t]  (bar t included)
            exclude_current = 1:           volume[t - volume_period .. t - 1]  (bar t excluded)
        ratio = volume[t] / mean(base)
        rng = high[t] - low[t]
        reference = "signed" (default): loc = 2 x (close[t] - low[t]) / rng - 1   (0 when rng = 0)
        reference = "low":              loc = (close[t] - low[t]) / rng            (0.5 when rng = 0)
        reference = "high":             loc = (high[t] - close[t]) / rng           (0.5 when rng = 0)
        raw_value = loc x ratio

    The defaults ("signed", exclude_current 0) give the original output, unchanged.
    Range: "signed" is signed, positive when the close is in the upper half of the bar. "low" and "high" are
    0 and up, never negative. "high" is 0 with the close at the high and grows as the close nears the low.
    With exclude_current 0 the ratio is at most volume_period; with exclude_current 1 it is unbounded above.
    Graded, continuous in the close and the volumes while rng > 0.
    Warm-up: volume_period + exclude_current rows, bar t included.

    NaN: a NaN high, low or close on bar t, a NaN volume[t], or a NaN volume in the base gives NaN. A base mean
    not above 0 gives NaN (never on real bars).
    Building the component raises for a volume_period below 2, an exclude_current other than 0 or 1, or a
    reference other than "signed", "low" or "high".

    WHY THIS CANNOT LEAK: it reads high, low and close of the last row (bar t) and volume over at most the last
    volume_period + exclude_current rows, all at or before bar t; every value is known at bar t's close.
    """

    def __init__(self, name="VolumeWeightedCloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 20))
        if self.volume_period < 2:
            raise ValueError(
                f"VolumeWeightedCloseLocationComponent: volume_period must be >= 2, got {self.volume_period}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(
                f"VolumeWeightedCloseLocationComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.reference = self.parameters.get("reference", "signed")
        if self.reference not in ("signed", "low", "high"):
            raise ValueError(
                "VolumeWeightedCloseLocationComponent: reference must be 'signed', 'low' or 'high', "
                f"got {self.reference!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = len(data)
        h = float(data["high"].iloc[-1])
        l = float(data["low"].iloc[-1])
        c = float(data["close"].iloc[-1])
        vol = data["volume"].astype(float).to_numpy()
        v_t = float(vol[-1])
        ex = self.exclude_current
        base = vol[n - self.volume_period - ex: n - ex]
        if np.isnan(h) or np.isnan(l) or np.isnan(c) or np.isnan(v_t) or np.isnan(base).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        den = float(np.mean(base))
        if not den > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rng = h - l
        if self.reference == "signed":
            loc = 0.0 if rng == 0 else 2.0 * (c - l) / rng - 1.0
        elif self.reference == "low":
            loc = 0.5 if rng == 0 else (c - l) / rng
        else:
            loc = 0.5 if rng == 0 else (h - c) / rng
        ratio = v_t / den
        self._raw_value = float(loc * ratio)
        self.confidence = 1.0
        self.debug_info = {"location": loc, "volume_ratio": ratio, "reference": self.reference,
                           "exclude_current": ex}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.volume_period + self.exclude_current


class VolumeWeightedCloseLocationVolatilityRatioComponent(SubStrategyComponent):
    """
    Low close on heavy volume in a volatile market, on every bar:

        loc   = (high[t] - close[t]) / (high[t] - low[t])      (0.5 when high[t] == low[t])
        vr    = volume[t] / mean(volume[t - volume_period .. t - 1])   (bar t excluded from the base)
        s(i)  = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1, j = i-vol_period+1 .. i
        volr  = s(t) / mean(s(t - vol_lookback + 1) .. s(t))
        raw_value = loc * vr * volr

    Range: 0 and up, unbounded above, never negative, with no direction. It is 0 with the close at the bar's high
    and grows as the close nears the low, as volume rises above its prior average, and as volatility rises above
    its average (volr is at most vol_lookback because the mean includes s(t)).
    Warm-up: max(volume_period + 1, vol_lookback + vol_period) rows, bar t included (80 at the defaults).
    NaN: a NaN in any high, low, close or volume read gives NaN. A close not above 0 among the closes read, a base
    mean volume not above 0, or a mean of s equal to 0 also gives NaN (never seen on real bars).
    Building the component raises for volume_period < 2, vol_period < 2 or vol_lookback < 1.

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data). These are
    high[t], low[t], volume of bars t-volume_period .. t, and closes of the last vol_lookback + vol_period rows,
    all known at bar t's close.
    """

    def __init__(self, name="VolumeWeightedCloseLocationVolatilityRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 20))
        if self.volume_period < 2:
            raise ValueError(f"volume_period must be >= 2, got {self.volume_period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"vol_period must be >= 2, got {self.vol_period}")
        self.vol_lookback = int(self.parameters.get("vol_lookback", 60))
        if self.vol_lookback < 1:
            raise ValueError(f"vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        nan = float("nan")
        h = float(data["high"].iloc[-1])
        lo = float(data["low"].iloc[-1])
        c_t = float(data["close"].iloc[-1])
        vol = data["volume"].astype(float).to_numpy()
        v_t = vol[-1]
        base = vol[-(self.volume_period + 1):-1]
        n_c = self.vol_lookback + self.vol_period
        c = data["close"].astype(float).to_numpy()[-n_c:]
        if (np.isnan(h) or np.isnan(lo) or np.isnan(c_t) or np.isnan(v_t)
                or np.isnan(base).any() or np.isnan(c).any() or (c <= 0).any()):
            self._raw_value = nan
            self.confidence = 1.0
            return
        rng = h - lo
        loc = 0.5 if rng == 0 else (h - c_t) / rng
        base_mean = float(base.mean())
        if not base_mean > 0:
            self._raw_value = nan
            self.confidence = 1.0
            return
        vr = v_t / base_mean
        r = c[1:] / c[:-1] - 1.0
        s = np.array([np.std(r[k:k + self.vol_period], ddof=1) for k in range(self.vol_lookback)])
        s_mean = float(s.mean())
        if not s_mean > 0:
            self._raw_value = nan
            self.confidence = 1.0
            return
        volr = float(s[-1]) / s_mean
        self._raw_value = float(loc * vr * volr)
        self.confidence = 1.0
        self.debug_info = {"location": loc, "volume_ratio": vr, "volatility_ratio": volr}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.volume_period + 1, self.vol_lookback + self.vol_period)


class FallVolumeVolatilityWeightedComponent(SubStrategyComponent):
    """
    One-bar fall, weighted by the bar's volume against its prior average and by recent against longer volatility:

        r(j)      = close[j] / close[j-1] - 1
        fall      = max(0, -r(t)) x 100
        vratio    = volume[t] / mean(volume[t-volume_period .. t-1])        (bar t excluded from the base)
        s_recent  = std (ddof 1) of r(j), j = t-vol_period+1 .. t
        s_base    = std (ddof 1) of r(j), j = t-base_vol_period+1 .. t
        raw_value = fall x vratio x s_recent / s_base

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 on up bars and flat bars, and grows
    with the fall, the volume ratio and the volatility ratio. Graded, and continuous in the prices and volumes.
    Warm-up: max(volume_period + 1, vol_period + 1, base_vol_period + 1) rows, bar t included (121 at the defaults).

    NaN: a NaN close among the closes read, or a NaN volume on bar t or in the base, gives NaN, whatever the move's
    sign. A close not above 0 among those read, a base mean volume not above 0, or an s_base of 0 gives NaN (never
    on real bars).
    Building the component raises for a volume_period below 1, or a vol_period or base_vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the close and volume columns of the last get_required_periods() rows of
    data, the last row being bar t; every value is known at bar t's close.
    """

    def __init__(self, name="FallVolVolWeighted", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 20))
        self.vol_period = int(self.parameters.get("vol_period", 20))
        self.base_vol_period = int(self.parameters.get("base_vol_period", 120))
        if self.volume_period < 1:
            raise ValueError(f"FallVolumeVolatilityWeightedComponent: volume_period must be >= 1, got {self.volume_period}")
        if self.vol_period < 2:
            raise ValueError(f"FallVolumeVolatilityWeightedComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.base_vol_period < 2:
            raise ValueError(
                f"FallVolumeVolatilityWeightedComponent: base_vol_period must be >= 2, got {self.base_vol_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        nc = max(self.vol_period, self.base_vol_period) + 1
        closes = data["close"].astype(float).to_numpy()[-nc:]
        vols = data["volume"].astype(float).to_numpy()
        v_t = float(vols[-1])
        base = vols[-self.volume_period - 1:-1]
        self.confidence = 1.0
        if np.isnan(closes).any() or np.isnan(base).any() or np.isnan(v_t) or not (closes > 0).all():
            self._raw_value = float("nan")
            return
        mean_base = float(np.mean(base))
        if not mean_base > 0:
            self._raw_value = float("nan")
            return
        rets = closes[1:] / closes[:-1] - 1.0
        r_t = float(rets[-1])
        s_recent = float(np.std(rets[-self.vol_period:], ddof=1))
        s_base = float(np.std(rets[-self.base_vol_period:], ddof=1))
        if not s_base > 0:
            self._raw_value = float("nan")
            return
        fall = max(0.0, -r_t) * 100.0
        vratio = v_t / mean_base
        self._raw_value = float(fall * vratio * s_recent / s_base)
        self.debug_info = {"fall_pct": fall, "volume_ratio": vratio, "s_recent": s_recent, "s_base": s_base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.volume_period + 1, self.vol_period + 1, self.base_vol_period + 1)


class FallVolumeTimesPriorDeclineComponent(SubStrategyComponent):
    """
    The day's fall in usual moves, times its volume multiple, times the decline before it:

        r(j) = close[j] / close[j-1] - 1
        s    = std (ddof 1) of r(j), j = t-vol_period+1 .. t            (bar t's return included)
        F    = max(0, -r(t)) / s                                        (0 when s = 0)
        V    = volume[t] / mean(volume[t-volume_period] .. volume[t-1])  (bar t excluded from the base)
        P    = max(0, -(close[t-1] / close[t-1-decline_period] - 1)) x 100
        raw_value = F x V x P

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 on up and flat bars, and 0 when
    close[t-1] is not below close[t-1-decline_period]. It grows with the fall in usual moves, with the volume
    multiple and with the prior decline in percent.
    Warm-up: max(vol_period + 1, volume_period + 1, decline_period + 2) rows, bar t included (22 at the defaults).

    NaN: a NaN close among the last max(vol_period + 1, decline_period + 2) rows, or a NaN volume at bar t or in
    the base, gives NaN whatever the sign of the move. A close not above 0 there gives NaN, and so does a base
    mean volume not above 0 (neither is seen on real bars). s = 0 gives 0.
    Building the component raises for vol_period < 2, volume_period < 1 or decline_period < 1.

    WHY THIS CANNOT LEAK: it reads only the close and volume columns of the last rows of data, up to and
    including bar t (the last row); the prior decline ends at bar t-1 and the volume base ends at bar t-1.
    """

    def __init__(self, name="FallVolumePriorDecline", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"FallVolumeTimesPriorDeclineComponent: vol_period must be >= 2, got {self.vol_period}")
        self.volume_period = int(self.parameters.get("volume_period", 20))
        if self.volume_period < 1:
            raise ValueError(
                f"FallVolumeTimesPriorDeclineComponent: volume_period must be >= 1, got {self.volume_period}")
        self.decline_period = int(self.parameters.get("decline_period", 20))
        if self.decline_period < 1:
            raise ValueError(
                f"FallVolumeTimesPriorDeclineComponent: decline_period must be >= 1, got {self.decline_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n_close = max(self.vol_period + 1, self.decline_period + 2)
        close = data["close"].astype(float).to_numpy()[-n_close:]
        vol = data["volume"].astype(float).to_numpy()[-(self.volume_period + 1):]
        if np.isnan(close).any() or np.isnan(vol).any() or not (close > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        vp = self.vol_period
        rets = close[-vp:] / close[-vp - 1:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        r_t = float(close[-1] / close[-2] - 1.0)
        fall = max(0.0, -r_t) / s if s > 0 else 0.0
        base_mean = float(np.mean(vol[:-1]))
        if not base_mean > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        vratio = float(vol[-1]) / base_mean
        dp = self.decline_period
        decline = max(0.0, -(float(close[-2]) / float(close[-2 - dp]) - 1.0)) * 100.0
        self._raw_value = float(fall * vratio * decline)
        self.confidence = 1.0
        self.debug_info = {"fall_in_usual_moves": fall, "volume_ratio": vratio, "prior_decline_pct": decline,
                           "std": s}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.vol_period + 1, self.volume_period + 1, self.decline_period + 2)


class CloseLocationTimesVolatilityComponent(SubStrategyComponent):
    """
    The close's location under the bar's high times the recent volatility, on every bar:

        loc = (high[t] - close[t]) / (high[t] - low[t])        (0.5 when high[t] = low[t])
        r[j] = close[j] / close[j-1] - 1,  j = t - vol_period + 1 .. t   (bar t's return included)
        s = standard deviation (ddof 1) of those vol_period returns
        raw_value = loc x s

    Range and sign: 0 and up, never negative on real bars (the close lies inside [low, high], so loc is 0 to 1).
    It has no direction. It is 0 with the close at the bar's high, and it grows as the close nears the bar's low
    and as s rises. It is at most s.
    Warm-up: vol_period + 1 rows, bar t included (21 at the default).
    NaN: a NaN high[t], low[t] or a NaN close among the last vol_period + 1 rows gives NaN. A close not above 0
    among the return bases gives NaN (never on real bars). A zero range gives loc = 0.5.
    Building the component raises for a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads high[t], low[t] and the closes of the last vol_period + 1 rows of data, bar t
    (the last row) included and nothing after it; each value is known at its bar's close.
    """

    def __init__(self, name="CloseLocationTimesVolatility", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"CloseLocationTimesVolatilityComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.vol_period
        closes = data['close'].astype(float).to_numpy()[-(n + 1):]
        h = float(data['high'].iloc[-1])
        l = float(data['low'].iloc[-1])
        c = float(closes[-1])
        if np.isnan(closes).any() or np.isnan(h) or np.isnan(l):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        bases = closes[:-1]
        if not (bases > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = closes[1:] / bases - 1.0
        s = float(np.std(rets, ddof=1))
        rng = h - l
        loc = 0.5 if rng == 0 else (h - c) / rng
        self._raw_value = float(loc * s)
        self.confidence = 1.0
        self.debug_info = {'location': loc, 'volatility': s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.vol_period + 1


class ExcessPowerReversalTimesMaDistanceComponent(SubStrategyComponent):
    """
    Excess predictive power of the nearness to the high, read as a reversal, times the trend distance:

        s(i)    = close[i] / max(close[i-high_period+1 .. i]) - 1
        y(i)    = close[i+horizon] / close[i] - 1
        w(u)    = Pearson corr of s(i) with y(i) over i = u-corr_lookback .. u-horizon
                  (0 when s or y is flat over those rows)
        wbar(t) = mean of w(t-mean_window) .. w(t-1)
        z(t)    = (s(t) - mean) / std (ddof 1) of s over bars t-z_window+1 .. t   (0 when s is flat there)
        SMA     = mean(close[t-ma_period+1 .. t])
        raw_value = max(0, -(w(t) - wbar(t)) * z(t)) * max(0, (close[t] - SMA) / SMA * 100)

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 unless (w - wbar) * z < 0 and
    close[t] > SMA. Graded: it grows continuously with both factors.
    Warm-up: max(mean_window + corr_lookback, z_window - 1) + high_period rows, at least ma_period (820 at the
    defaults), bar t included.
    NaN: a NaN close, or a close not above 0, in the last (warm-up) rows gives NaN.
    Building raises for high_period < 2, horizon < 1, corr_lookback - horizon < 2, z_window < 2,
    mean_window < 1, ma_period < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last (warm-up) rows up to and including bar t.
    The latest forward return used is y(t-horizon) = close[t] / close[t-horizon] - 1, which ends at bar t.
    """

    def __init__(self, name="ExcessPowerReversalTrend", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.high_period = int(p.get("high_period", 90))
        self.corr_lookback = int(p.get("corr_lookback", 365))
        self.horizon = int(p.get("horizon", 5))
        self.z_window = int(p.get("z_window", 365))
        self.mean_window = int(p.get("mean_window", 365))
        self.ma_period = int(p.get("ma_period", 100))
        if self.high_period < 2:
            raise ValueError(f"high_period must be >= 2, got {self.high_period}")
        if self.horizon < 1:
            raise ValueError(f"horizon must be >= 1, got {self.horizon}")
        if self.corr_lookback - self.horizon < 2:
            raise ValueError("corr_lookback - horizon must be >= 2")
        if self.z_window < 2:
            raise ValueError(f"z_window must be >= 2, got {self.z_window}")
        if self.mean_window < 1:
            raise ValueError(f"mean_window must be >= 1, got {self.mean_window}")
        if self.ma_period < 2:
            raise ValueError(f"ma_period must be >= 2, got {self.ma_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        T = len(c) - 1
        hp, L, h = self.high_period, self.corr_lookback, self.horizon
        hi = pd.Series(c).rolling(hp, min_periods=hp).max().to_numpy()
        s = c / hi - 1.0
        y = np.full(T + 1, np.nan)
        y[:T + 1 - h] = c[h:] / c[:T + 1 - h] - 1.0

        def corr(u):
            a = s[u - L:u - h + 1]
            b = y[u - L:u - h + 1]
            if a.max() == a.min() or b.max() == b.min():
                return 0.0
            da = a - a.mean()
            db = b - b.mean()
            den = np.sqrt(np.sum(da * da) * np.sum(db * db))
            if not den > 0:
                return 0.0
            return float(np.sum(da * db) / den)

        w_t = corr(T)
        wbar = float(np.mean([corr(T - k) for k in range(1, self.mean_window + 1)]))
        zw = s[T - self.z_window + 1:T + 1]
        if zw.max() == zw.min():
            z = 0.0
        else:
            sd = float(np.std(zw, ddof=1))
            z = float((s[T] - zw.mean()) / sd) if sd > 0 else 0.0
        sma = float(np.mean(c[T - self.ma_period + 1:T + 1]))
        dist = (c[T] - sma) / sma * 100.0
        rev = max(0.0, -(w_t - wbar) * z)
        trend = max(0.0, dist)
        self._raw_value = float(rev * trend)
        self.confidence = 1.0
        self.debug_info = {"w": w_t, "wbar": wbar, "z": z, "ma_distance": dist}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(max(self.mean_window + self.corr_lookback, self.z_window - 1) + self.high_period,
                   self.ma_period)


class RecentToPriorVolumeScaledReturnComponent(SubStrategyComponent):
    """
    The period-bar return in usual period-bar moves, weighted by recent volume against the volume just before it:

        R      = close[t] / close[t - period] - 1
        m      = mean over i = t-window+1 .. t of abs(close[i] / close[i - period] - 1)
        first  = R / m            (0.0 when m = 0)
        recent = mean(volume[t - period + 1 .. t])
        base   = mean(volume[t - period - base_period + 1 .. t - period])
        raw_value = first * recent / base

    Defaults: period 48, window 720, base_period 120, so the base is bars t-167 .. t-48.
    Range and sign: unbounded and signed like the period-bar return. It is 0 for a flat move. Its size grows
    with the move in usual moves, which is at most `window` because R is one of the averaged returns. It also
    grows with the volume ratio, which is above 0 and is 1 at equal means.
    Warm-up: max(window + period, period + base_period) rows (768 at the defaults), bar t included.
    NaN: a NaN close in the last window + period rows, or a NaN volume in either volume window, gives NaN.
    A close not above 0 there, or a base mean volume not above 0, also gives NaN (never on real bars).
    m = 0 gives 0.
    Building the component raises for period < 1, window < 1 or base_period < 1.

    WHY THIS CANNOT LEAK: it reads only the `close` and `volume` columns of the rows up to and including bar t
    (the last row of data). It reads at most the last max(window + period, period + base_period) rows.
    """

    def __init__(self, name="RecentToPriorVolumeScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        self.window = int(self.parameters.get("window", 720))
        self.base_period = int(self.parameters.get("base_period", 120))
        if self.period < 1:
            raise ValueError(f"RecentToPriorVolumeScaledReturnComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"RecentToPriorVolumeScaledReturnComponent: window must be >= 1, got {self.window}")
        if self.base_period < 1:
            raise ValueError(
                f"RecentToPriorVolumeScaledReturnComponent: base_period must be >= 1, got {self.base_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        P, W, B = self.period, self.window, self.base_period
        c = data['close'].astype(float).to_numpy()[-(W + P):]
        v = data['volume'].astype(float).to_numpy()
        recent = v[-P:]
        base = v[-(P + B):-P]
        if np.isnan(c).any() or not (c > 0).all() or np.isnan(recent).any() or np.isnan(base).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        base_mean = float(base.mean())
        if not base_mean > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = c[P:] / c[:W] - 1.0
        ret = float(rets[-1])
        m = float(np.abs(rets).mean())
        first = 0.0 if m == 0 else ret / m
        recent_mean = float(recent.mean())
        self._raw_value = float(first * recent_mean / base_mean)
        self.confidence = 1.0
        self.debug_info = {'return': ret, 'mean_abs_return': m, 'recent_volume': recent_mean,
                           'base_volume': base_mean}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.window + self.period, self.period + self.base_period)


class RiseTimesVolatilityCalmnessComponent(SubStrategyComponent):
    """
    A lagged rise weighted by how calm the market is now, on every bar:

        e = t - lag
        rise = max(0, close[e] / close[e - period] - 1)
        r[j] = close[j] / close[j-1] - 1
        s(i) = std (ddof 1) of r[i-vol_period+1 .. i]          (bar i's return included)
        ratio = mean(s(t-vol_lookback+1) .. s(t)) / s(t)
        raw_value = rise x ratio

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 when the period-bar return
    ending at bar t-lag is 0 or negative. It grows with that rise and as the current volatility s(t) sits
    below its mean over the lookback (ratio 1 at equal volatility).
    Units: simple return (fraction) x ratio of volatilities.
    Warm-up: max(period + lag + 1, vol_lookback + vol_period) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the rows up to and including bar t (the last
    row of data). The rise uses closes t-lag-period and t-lag, and the volatilities use the closes of bars
    t-vol_lookback-vol_period+1 .. t. A bar's close is known at that bar's close.

    NaN: a NaN close in the rows read gives NaN, and so does a close not above 0 there (never on real bars).
    s(t) = 0 gives NaN (never on real bars).
    Building the component raises for period < 1, lag < 0, vol_period < 2 or vol_lookback < 1.
    """

    def __init__(self, name="RiseTimesCalmness", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        self.lag = int(self.parameters.get("lag", 24))
        self.vol_period = int(self.parameters.get("vol_period", 720))
        self.vol_lookback = int(self.parameters.get("vol_lookback", 8760))
        if self.period < 1:
            raise ValueError(f"RiseTimesVolatilityCalmnessComponent: period must be >= 1, got {self.period}")
        if self.lag < 0:
            raise ValueError(f"RiseTimesVolatilityCalmnessComponent: lag must be >= 0, got {self.lag}")
        if self.vol_period < 2:
            raise ValueError(
                f"RiseTimesVolatilityCalmnessComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.vol_lookback < 1:
            raise ValueError(
                f"RiseTimesVolatilityCalmnessComponent: vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).iloc[-n:].reset_index(drop=True)
        if c.isna().any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        last = len(c) - 1
        base = float(c.iloc[last - self.lag - self.period])
        end = float(c.iloc[last - self.lag])
        rise = max(0.0, end / base - 1.0)
        r = c / c.shift(1) - 1.0
        s = r.rolling(self.vol_period).std(ddof=1)
        s_win = s.iloc[-self.vol_lookback:]
        s_t = float(s.iloc[-1])
        if s_win.isna().any() or not s_t > 0:
            self._raw_value = float("nan")
        else:
            ratio = float(s_win.mean()) / s_t
            self._raw_value = float(rise * ratio)
        self.confidence = 1.0
        self.debug_info = {'rise': rise, 's_t': s_t}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + self.lag + 1, self.vol_lookback + self.vol_period)


class MeanAbsScaledReturnTimesVolatilityComponent(SubStrategyComponent):
    """
    The period-bar return in usual period-bar moves (optionally capped), times the one-bar volatility:

        x = (close[t] / close[t-period] - 1) / m
        m = mean over i = t-window+1 .. t of abs(close[i] / close[i-period] - 1)   (bar t included)
        x = 0 when m = 0
        cap = None (default): x unchanged (the original output)
        cap = c > 0:          x = clip(x, -c, +c)
        s = std (ddof 1) of r[j] = close[j] / close[j-1] - 1, j = t-vol_period+1 .. t
        raw_value = x * s

    Range: unbounded, signed like the period-bar return, 0 for a flat move. abs(x) is at most window (today's
    return is one of those averaged), and at most cap when cap is set. s is 0 and up.
    Graded: linear in the scaled move (up to cap usual moves, then flat), and growing with s.
    Warm-up: max(window + period, vol_period + 1) rows, bar t included (744 at the defaults).
    NaN: a NaN close, or a close not above 0, in the last max(window + period, vol_period + 1) rows gives NaN.
    m = 0 gives x = 0 (never on real bars).
    Building raises for period < 1, window < 1, vol_period < 2, or a cap that is set and not above 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window + period, vol_period + 1)
    rows of data, the last row being bar t; no later row exists in data.
    """

    def __init__(self, name="MeanAbsScaledReturnTimesVol", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        self.window = int(self.parameters.get("window", 720))
        self.vol_period = int(self.parameters.get("vol_period", 720))
        if self.period < 1:
            raise ValueError(f"MeanAbsScaledReturnTimesVolatilityComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledReturnTimesVolatilityComponent: window must be >= 1, got {self.window}")
        if self.vol_period < 2:
            raise ValueError(
                f"MeanAbsScaledReturnTimesVolatilityComponent: vol_period must be >= 2, got {self.vol_period}")
        cap = self.parameters.get("cap", None)
        if cap is not None:
            try:
                cap = float(cap)
            except (TypeError, ValueError):
                raise ValueError(f"MeanAbsScaledReturnTimesVolatilityComponent: cap must be a number > 0, got {cap!r}")
            if not cap > 0:
                raise ValueError(f"MeanAbsScaledReturnTimesVolatilityComponent: cap must be > 0, got {cap!r}")
        self.cap = cap
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-need:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        t = len(c) - 1
        p = self.period
        idx = np.arange(t - self.window + 1, t + 1)
        rets = c[idx] / c[idx - p] - 1.0
        m = float(np.mean(np.abs(rets)))
        x = (c[t] / c[t - p] - 1.0) / m if m > 0 else 0.0
        if self.cap is not None:
            x = min(max(x, -self.cap), self.cap)
        j = np.arange(t - self.vol_period + 1, t + 1)
        r1 = c[j] / c[j - 1] - 1.0
        s = float(np.std(r1, ddof=1))
        self._raw_value = float(x * s)
        self.confidence = 1.0
        self.debug_info = {"scaled_move": float(x), "mean_abs_return": m, "vol": s, "cap": self.cap}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.window + self.period, self.vol_period + 1)


class UpCloseStreakLengthComponent(SubStrategyComponent):
    """
    Length of the current streak of closes on one side, optionally against the coin's completed streaks.

        moved(i) = close[i] > close[i-1]   (side "up", default)
        moved(i) = close[i] < close[i-1]   (side "down")
        n = number of consecutive bars i ending at t (bar t included) with moved(i), capped at max_bars;
            n = 0 when bar t did not move to the counted side.
        A completed streak is a maximal run of moved bars inside bars t-base_window+1 .. t. It counts when
        the bar before its first bar is inside that window and did not move, and the bar after its last bar
        is at or before t and did not move, so the open streak ending at t is excluded. K is the number of
        completed streaks; their lengths are uncapped.
        base "none" (default):  raw_value = n
        base "mean_streak":     raw_value = n / mean(completed lengths)
        base "rank":            raw_value = (number of completed lengths <= n) / K
        Every base gives 0 when n = 0.

    Range: "none" 0 .. max_bars, integers; "mean_streak" 0 .. max_bars; "rank" 0 .. 1. Never negative, no direction.
    side "up" with any base is the original output, unchanged. "down" is the run of lower closes.
    A flat bar ends either streak.
    Warm-up: max_bars + 1 rows with "none"; max(max_bars, base_window) + 1 rows with "mean_streak" or "rank".
    NaN: a NaN close in those rows gives NaN. With "mean_streak" or "rank", no completed streak while n > 0
    gives NaN (never on real bars).
    Building the component raises for max_bars < 1, an unknown base, base_window < 3, or a side other than
    "up" or "down".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last (warm-up) rows of data, the last row
    being bar t; no row after t exists in the data it is given.
    """

    def __init__(self, name="Close streak length", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(f"UpCloseStreakLengthComponent: max_bars must be >= 1, got {self.max_bars}")
        self.base = self.parameters.get("base", "none")
        if self.base not in ("none", "mean_streak", "rank"):
            raise ValueError(
                f"UpCloseStreakLengthComponent: base must be 'none', 'mean_streak' or 'rank', got {self.base!r}")
        self.base_window = int(self.parameters.get("base_window", 365))
        if self.base_window < 3:
            raise ValueError(f"UpCloseStreakLengthComponent: base_window must be >= 3, got {self.base_window}")
        self.side = self.parameters.get("side", "up")
        if self.side not in ("up", "down"):
            raise ValueError(f"UpCloseStreakLengthComponent: side must be 'up' or 'down', got {self.side!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        self.confidence = 1.0
        if np.isnan(c).any():
            self._raw_value = float("nan")
            return
        if self.side == "up":
            moved = c[1:] > c[:-1]
        else:
            moved = c[1:] < c[:-1]
        # moved[k] is the move of bar (k+1) of c; moved[-1] is bar t
        n = 0
        k = len(moved) - 1
        while n < self.max_bars and k >= 0 and moved[k]:
            n += 1
            k -= 1
        if self.base == "none":
            self._raw_value = float(n)
            self.debug_info = {'n': n, 'side': self.side}
            return
        if n == 0:
            self._raw_value = 0.0
            self.debug_info = {'n': 0, 'side': self.side}
            return
        w = moved[-self.base_window:]
        m = len(w)
        lengths = []
        a = 0
        while a < m:
            if w[a]:
                b = a
                while b + 1 < m and w[b + 1]:
                    b += 1
                if a >= 1 and b + 1 <= m - 1:
                    lengths.append(b - a + 1)
                a = b + 1
            else:
                a += 1
        if len(lengths) == 0:
            self._raw_value = float("nan")
            return
        lengths = np.asarray(lengths, dtype=float)
        if self.base == "mean_streak":
            self._raw_value = float(n / lengths.mean())
        else:
            self._raw_value = float(np.sum(lengths <= n) / len(lengths))
        self.debug_info = {'n': n, 'side': self.side, 'completed_streaks': int(len(lengths))}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "none":
            return self.max_bars + 1
        return max(self.max_bars, self.base_window) + 1


class VolatilityRatioWeightedScaledFallComponent(SubStrategyComponent):
    """
    The day's fall in usual base-window moves, weighted by recent over base volatility:

        r[j] = close[j] / close[j-1] - 1
        s_recent = std (ddof 1) of r[t-vol_period+1 .. t]        (bar t's return included)
        s_base   = std (ddof 1) of r[t-base_vol_period+1 .. t]   (bar t's return included)
        raw_value = max(0, -r[t]) / s_base * s_recent / s_base
        raw_value = 0.0 when s_base = 0 (every base return equal: never on real bars; the fall is then 0 too)

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 on up and flat bars. It grows with
    the fall in usual base moves and with s_recent / s_base (1 at equal volatility).
    Warm-up: max(vol_period, base_vol_period) + 1 rows, bar t included.

    NaN: a NaN close in the last max(vol_period, base_vol_period) + 1 rows gives NaN, and so does a close not
    above 0 there (never on real bars).
    Building raises for vol_period < 2 or base_vol_period < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(vol_period, base_vol_period) + 1 rows
    of data, the last row being bar t; every close is known at its bar's close.
    """

    def __init__(self, name="VolRatioScaledFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 10))
        self.base_vol_period = int(self.parameters.get("base_vol_period", 60))
        if self.vol_period < 2:
            raise ValueError(f"VolatilityRatioWeightedScaledFallComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.base_vol_period < 2:
            raise ValueError(
                f"VolatilityRatioWeightedScaledFallComponent: base_vol_period must be >= 2, got {self.base_vol_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = max(self.vol_period, self.base_vol_period)
        c = data["close"].astype(float).to_numpy()[-(n + 1):]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[1:] / c[:-1] - 1.0
        s_recent = float(np.std(r[-self.vol_period:], ddof=1))
        s_base = float(np.std(r[-self.base_vol_period:], ddof=1))
        fall = max(0.0, -float(r[-1]))
        if not s_base > 0:
            value = 0.0
        else:
            value = fall / s_base * s_recent / s_base
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"fall": fall, "s_recent": s_recent, "s_base": s_base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.vol_period, self.base_vol_period) + 1
    A return weighted by recent volatility against the volatility of an earlier stretch, on every bar:
        R       = (close[t] / close[t - period] - 1) x 100
        r[j]    = close[j] / close[j-1] - 1
        s_recent = std (ddof 1) of r[j], j = t - vol_period + 1 .. t
        s_base   = std (ddof 1) of r[j], j = t - base_lag - base_period + 1 .. t - base_lag
        raw_value = R x s_recent / s_base
    Range & sign: unbounded, signed like the period-bar return (0 when it is 0). The size grows with the move and
    with s_recent / s_base (0 and up, 1 when the two volatilities are equal). At the defaults (48, 48, 168, 48)
    the recent returns are those of bars t-47 .. t and the base those of bars t-215 .. t-48, adjacent and not
    overlapping.
    Warm-up: max(period, vol_period, base_lag + base_period) + 1 rows (217 at the defaults), bar t included.
    NaN: a NaN close, or a close not above 0, in those rows gives NaN; s_base = 0 gives NaN (never on real bars).
    Building raises for period < 1, vol_period < 2, base_period < 2, base_lag < 0.
    base_lag + base_period) + 1 rows of data, the last of which is bar t; no row after bar t is read.
                f"RecentToPriorVolatilityWeightedReturnComponent: vol_period must be >= 2, got {self.vol_period}")
                f"RecentToPriorVolatilityWeightedReturnComponent: base_period must be >= 2, got {self.base_period}")
                f"RecentToPriorVolatilityWeightedReturnComponent: base_lag must be >= 0, got {self.base_lag}")
        n = len(r)
        recent = r[n - self.vol_period:]
        base = r[n - self.base_lag - self.base_period: n - self.base_lag]
        ret = (c[-1] / c[-1 - self.period] - 1.0) * 100.0
            self._raw_value = float(ret * s_recent / s_base)
        self.debug_info = {"return_pct": float(ret), "s_recent": s_recent, "s_base": s_base}
class RiseTimesRangeMultipleComponent(SubStrategyComponent):
    A rise times the current bar's range in multiples of its average bar range, on every bar:
        R    = max(0, close[t] / close[t - rise_period] - 1) x 100
        M    = (high[t] - low[t]) / mean(high[i] - low[i], i = t - range_period + 1 .. t)   (bar t included)
        raw_value = R x M          (0.0 when the mean range is 0)
    Range and sign: 0 and up, unbounded above, never negative, no direction. The value is 0 when the
    rise_period-bar return is 0 or negative, and 0 for a zero-range bar t. M is at most range_period,
    because the mean includes bar t. The value grows with the rise and with how wide bar t is against
    its average. It is continuous in the prices.
    Warm-up: max(rise_period + 1, range_period) rows, bar t included (20 at the defaults).
    NaN: a NaN close at bar t or at bar t - rise_period, or a NaN high or low in the last range_period
    rows, gives NaN, whatever the sign of the move. A close[t - rise_period] not above 0 gives NaN
    (never on real bars). A mean range of 0 gives 0.0, because the range of bar t is then 0 too.
    Building the component raises for a rise_period below 1 or a range_period below 2.
    WHY THIS CANNOT LEAK: it reads close[t] and close[t - rise_period], and the high and low of the
    last range_period rows ending at bar t (the last row of data). All of them are known at bar t's close.
    def __init__(self, name="RiseTimesRangeMultiple", weight=1.0, parameters=None):
        self.rise_period = int(self.parameters.get("rise_period", 5))
            raise ValueError(f"RiseTimesRangeMultipleComponent: rise_period must be >= 1, got {self.rise_period}")
        self.range_period = int(self.parameters.get("range_period", 20))
        if self.range_period < 2:
            raise ValueError(f"RiseTimesRangeMultipleComponent: range_period must be >= 2, got {self.range_period}")
        c_t = close[-1]
        c_b = close[-(self.rise_period + 1)]
        h = high[-self.range_period:]
        lo = low[-self.range_period:]
        if np.isnan(c_t) or np.isnan(c_b) or np.isnan(h).any() or np.isnan(lo).any():
        if not c_b > 0:
        rise = max(0.0, c_t / c_b - 1.0) * 100.0
        ranges = h - lo
        if mean_range == 0.0:
            mult = 0.0
            mult = float(ranges[-1]) / mean_range
        self._raw_value = float(rise * mult)
        self.debug_info = {'rise_pct': rise, 'range_multiple': mult, 'mean_range': mean_range}
        return max(self.rise_period + 1, self.range_period)
