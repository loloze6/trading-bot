# RiseTimesVolatilityCalmnessComponent: retest_weekend_run | 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d1_saturday-continuation-in-calm-markets.d2_calm-up-saturday-continues-higher_1h | LaggedRiseTimesCalmness

## attempt 1

answer: built
class: RiseTimesVolatilityCalmnessComponent
settings: {"period": 24, "lag": 24, "vol_period": 720, "vol_lookback": 8760}
reason: No component multiplies a clipped, lagged rise by the inverse ratio of current volatility to its average. `VolatilityScaledReturnComponent` divides the return by the mean volatility, and `HighProximityVolatilityRatioComponent` pairs that inverse ratio with high-proximity, not a rise. This product is one new measure computed from closes only, so it is a new class.

table: Directional components
row: | `RiseTimesVolatilityCalmnessComponent` | `period` (24), `lag` (24), `vol_period` (720), `vol_lookback` (8760) | max(0, close[t-`lag`] / close[t-`lag`-`period`] - 1) x mean(s(t-`vol_lookback`+1) .. s(t)) / s(t), s(i) being the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1 ending at bar i, that bar's included | 0 and up, unbounded above, never negative; no direction; 0 when the `period`-bar return ending at bar t-`lag` is 0 or negative; grows with that rise and as s(t) sits below its mean over the lookback (the ratio is 1 at equal volatility) | graded | simple return (fraction) x volatility ratio (mean over current) | max(`period` + `lag` + 1, `vol_lookback` + `vol_period`) (9480) | closes only. A NaN close in the last max(`period` + `lag` + 1, `vol_lookback` + `vol_period`) rows gives NaN, and so does a close not above 0 there (never on real bars). s(t) = 0 (a flat return window, never on real bars) gives NaN. These settings raise when the component is built: `period` < 1, `lag` < 0, `vol_period` < 2, `vol_lookback` < 1 | stateless. The volatility ratio is the R factor of `HighProximityVolatilityRatioComponent` and the inverse of `VolatilityRatioToAverageComponent` (`vol_period`, `vol_lookback`). The rise ends at bar t-`lag` and the volatility ends at bar t. On 1h bars the wished settings give the 24h rise that ended 24h ago times the 30-day volatility's past-year mean over its current value. It is continuous in the closes and exactly 0 after a flat or falling stretch. One-sided. No `scaling_factor`: scale it with transforms |

```python class
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
```

```python hand
def hand(df, params):
    import math
    period = int(params.get("period", 24))
    lag = int(params.get("lag", 24))
    vp = int(params.get("vol_period", 720))
    vl = int(params.get("vol_lookback", 8760))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(period + lag + 1, vl + vp)
    rows = c[t - need + 1:]
    for x in rows:
        if x != x or not x > 0:
            return float("nan")

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def std_at(i):
        xs = [ret(j) for j in range(i - vp + 1, i + 1)]
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (len(xs) - 1))

    rise = c[t - lag] / c[t - lag - period] - 1.0
    if rise < 0:
        rise = 0.0
    total = 0.0
    for i in range(t - vl + 1, t + 1):
        total += std_at(i)
    mean_s = total / vl
    s_t = std_at(t)
    if not s_t > 0:
        return float("nan")
    return rise * mean_s / s_t
```

checks:
RiseTimesVolatilityCalmnessComponent: every check passed
the bot's suite: == 1636 passed, 16 skipped, 75 deselected, 2244 warnings in 95.36s (0:01:35) ===
