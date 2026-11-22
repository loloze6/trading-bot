# FallGatedRangeMultipleVolatilityRatioComponent: night4_panic_run | 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h | FallGatedRangeMultipleTimesVolRatio

## attempt 1

answer: built
class: FallGatedRangeMultipleVolatilityRatioComponent
settings: {"period": 6, "base_period": 180, "fall_period": 6, "vol_period": 42, "vol_lookback": 360}
reason: No component computes this product. It is `FallGatedRangeMultipleComponent` (period 6, base_period 180, fall_period 6) times `VolatilityRatioToAverageComponent` (vol_period 42, vol_lookback 360), and no config step multiplies two components, so one new class computes it.

table: Regime measures
row: | `FallGatedRangeMultipleVolatilityRatioComponent` | `period` (6), `base_period` (180), `fall_period` (6), `vol_period` (42), `vol_lookback` (360) | G x S(t) / mean(S(t-`base_period`+1) .. S(t)) x s(t) / mean(s(t-`vol_lookback`+1) .. s(t)). S(i) = max(high[i-`period`+1 .. i]) − min(low[i-`period`+1 .. i]). s(i) = the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1 ending at bar i, that bar's included. G = 1 when close[t] < close[t-`fall_period`], else 0. The range factor is 0.0 when its mean is 0 | 0 and up, at most `base_period` x `vol_lookback` (each mean includes its current value), never negative; no direction. It is 0 when the close is not below its value `fall_period` bars ago. While the gate is on it grows with the range multiple and with the volatility ratio | regime measure | dimensionless (multiples of the mean `period`-bar range x ratio of volatilities) | max(`base_period` + `period` − 1, `fall_period` + 1, `vol_lookback` + `vol_period`) (402) | high, low (last `base_period` + `period` − 1 rows), close (last `vol_lookback` + `vol_period` rows and bar t-`fall_period`). A NaN in any of those rows gives NaN, whatever the gate. A close not above 0 among them gives NaN, and so does a mean of s equal to 0 (neither is ever seen on real bars). A mean range of 0 gives a range factor of 0.0, because S(t) is then 0 too. These settings raise when the component is built: `period` < 1, `base_period` < 1, `fall_period` < 1, `vol_period` < 2, `vol_lookback` < 1 | stateless. Equals `FallGatedRangeMultipleComponent` (`period`, `base_period`, `fall_period`) x `VolatilityRatioToAverageComponent` (`vol_period`, `vol_lookback`). It is continuous in the prices while the gate is on, and it drops to 0 where close[t] crosses close[t-`fall_period`] upward. On 4h bars the defaults give the 24h range in multiples of its 30-day mean, times the 7-day volatility over its 60-day mean, during a 24h fall. No `scaling_factor`: scale it with transforms |

```python class
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
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 6))
    b = int(params.get("base_period", 180))
    f = int(params.get("fall_period", 6))
    v = int(params.get("vol_period", 42))
    L = int(params.get("vol_lookback", 360))
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    nan = float("nan")

    def isnan(x):
        return x != x

    # rows read
    for i in range(t - b - p + 2, t + 1):
        if isnan(h[i]) or isnan(lo[i]):
            return nan
    for i in range(t - L - v + 1, t + 1):
        if isnan(c[i]):
            return nan
        if not c[i] > 0:
            return nan
    if isnan(c[t - f]):
        return nan

    # range multiple
    def stretch_range(i):
        top = h[i - p + 1]
        bottom = lo[i - p + 1]
        for j in range(i - p + 1, i + 1):
            if h[j] > top:
                top = h[j]
            if lo[j] < bottom:
                bottom = lo[j]
        return top - bottom

    total = 0.0
    for i in range(t - b + 1, t + 1):
        total = total + stretch_range(i)
    mean_s = total / b
    if mean_s == 0:
        rm = 0.0
    else:
        rm = stretch_range(t) / mean_s

    # volatility ratio
    def sd(i):
        rets = []
        for j in range(i - v + 1, i + 1):
            rets.append(c[j] / c[j - 1] - 1.0)
        m = sum(rets) / len(rets)
        acc = 0.0
        for r in rets:
            acc = acc + (r - m) * (r - m)
        return math.sqrt(acc / (len(rets) - 1))

    total = 0.0
    for i in range(t - L + 1, t + 1):
        total = total + sd(i)
    mean_sd = total / L
    if not mean_sd > 0:
        return nan
    vr = sd(t) / mean_sd

    g = 1.0 if c[t] < c[t - f] else 0.0
    return g * rm * vr
```

checks:
FallGatedRangeMultipleVolatilityRatioComponent: every check passed
the bot's suite: == 1612 passed, 16 skipped, 75 deselected, 2244 warnings in 93.67s (0:01:33) ===
