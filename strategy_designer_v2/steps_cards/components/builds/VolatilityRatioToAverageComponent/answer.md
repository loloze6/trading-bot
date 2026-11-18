# VolatilityRatioToAverageComponent: night_run | 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways.g1_high-volatility-daily-move-reversal.g1_high-vol-down-day-rebound_1d | VolatilityRatioToAverageComponent

## attempt 1

answer: built
class: VolatilityRatioToAverageComponent
settings: {"vol_period": 20, "vol_lookback": 60}
reason: No component gives the current 20-bar return volatility divided by its own 60-bar mean. `HighProximityVolatilityRatioComponent` computes the inverse of this ratio, mean(s)/s(t), and only as a product with a proximity to the high. The inverse is neither the negative nor 1 minus the ratio, so it is not a mirror. `VolatilityPercentileRegimeComponent` is a smoothed rank, not a ratio to the mean. A new class therefore computes s(t) / mean(s(t-59) .. s(t)).

table: Regime measures
row: | `VolatilityRatioToAverageComponent` | `vol_period` (20), `vol_lookback` (60) | s(t) / mean(s(t-`vol_lookback`+1) .. s(t)), s(i) being the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1 ending at bar i, that bar's included | 0 and up, at most `vol_lookback` (the mean includes s(t)), never negative; no direction; 1 when today's volatility equals its mean over the lookback, above 1 when higher, below 1 when lower | regime measure | dimensionless (ratio of volatilities) | `vol_lookback` + `vol_period` (80) | closes only. A NaN close in the last `vol_lookback` + `vol_period` rows gives NaN; a mean of s equal to 0 (every return window flat, never seen on real bars) gives NaN. These settings raise when the component is built: `vol_period` < 2, `vol_lookback` < 1 | stateless; graded, growing continuously as the current volatility rises above its average. It is the inverse of the R factor of `HighProximityVolatilityRatioComponent`. No `scaling_factor`: scale it with transforms |

```python class
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
        m = len(r)
        stds = []
        for k in range(self.vol_lookback):
            end = m - k
            stds.append(float(np.std(r[end - self.vol_period:end], ddof=1)))
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
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("vol_period", 20))
    L = int(params.get("vol_lookback", 60))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    i = last - (L + p) + 1
    while i <= last:
        if c[i] != c[i]:
            return float("nan")
        i = i + 1

    def sd(bar):
        rets = []
        j = bar - p + 1
        while j <= bar:
            rets.append(c[j] / c[j - 1] - 1.0)
            j = j + 1
        mu = sum(rets) / p
        acc = 0.0
        for x in rets:
            acc = acc + (x - mu) * (x - mu)
        return math.sqrt(acc / (p - 1))

    vals = []
    b = last - L + 1
    while b <= last:
        vals.append(sd(b))
        b = b + 1
    avg = sum(vals) / L
    if not avg > 0:
        return float("nan")
    return sd(last) / avg
```

checks:
VolatilityRatioToAverageComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1537 passed, 8 skipped, 74 deselected, 2170 warnings in 55.97s ========
