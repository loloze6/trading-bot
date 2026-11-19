# VolatilityScaledReturnComponent: slow_1h_run | 016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h | VolRatioWeightedScaledReturn

## attempt 1

answer: built
class: VolatilityScaledReturnComponent
settings: {"period": 24, "vol_period": 168, "vol_lookback": 720}
reason: The two s(t) factors cancel, so the wished value is the 24-bar return divided by sqrt(24) times the mean of s over the last 720 bars. That is `VolatilityScaledReturnComponent`'s return in usual moves measured against another base (the mean of s instead of s(t)), so it is the same measure and needs one new setting, `vol_lookback`, whose default 1 gives exactly today's output.

table: Directional components
row: | `VolatilityScaledReturnComponent` | `period` (1), `vol_period` (20), `lag` (0), `vol_lookback` (1) | (close[t-`lag`] / close[t-`lag`-`period`] - 1) / (m x sqrt(`period`)). m = mean(s(t-`lag`-`vol_lookback`+1) .. s(t-`lag`)), and s(i) is the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1 ending at bar i, that bar's included. `vol_lookback` 1 gives m = s(t-`lag`), and `lag` 0 is bar t itself | unbounded, signed; about +1 for a rise of one usual move, -2 for a fall of two; with `vol_lookback` above 1 the usual move is its average over the lookback, so the size also grows when the current volatility sits above that average | graded | usual moves | max(`period` + 1, `vol_period` + `vol_lookback`) + `lag` (21) | closes. A NaN close among the last max(`period` + 1, `vol_period` + `vol_lookback`) + `lag` rows gives NaN. m = 0 (flat return windows) gives 0. These settings raise when the component is built: `period` below 1, `vol_period` below 2, `lag` below 0, `vol_lookback` below 1 | stateless. `vol_lookback` 1 (default) is the original output, unchanged. With `period` 24, `vol_period` 168 and `vol_lookback` 720 it equals the 24-bar return in usual moves times s(t) / mean(s over the last 720 bars). It is `VolatilityScaledReturnComponent` (period 24, vol_period 168) x `VolatilityRatioToAverageComponent` (vol_period 168, vol_lookback 720). No `scaling_factor`: scale it with transforms |

```python class
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
        sds = []
        for k in range(self.vol_lookback):
            i = e - k
            w = c[i - self.vol_period:i + 1]
            r = w[1:] / w[:-1] - 1.0
            sds.append(float(np.std(r, ddof=1)))
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
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 1))
    vp = int(params.get("vol_period", 20))
    lag = int(params.get("lag", 0))
    lb = int(params.get("vol_lookback", 1))
    c = [float(x) for x in list(df["close"])]
    n = len(c)
    first = n - lag - max(p + 1, vp + lb)
    j = first
    while j <= n - 1 - lag:
        if c[j] != c[j]:
            return float("nan")
        j = j + 1
    e = n - 1 - lag
    ret = c[e] / c[e - p] - 1.0

    def std1(xs):
        mu = sum(xs) / len(xs)
        acc = 0.0
        for x in xs:
            acc = acc + (x - mu) * (x - mu)
        return math.sqrt(acc / (len(xs) - 1))

    total = 0.0
    k = 0
    while k < lb:
        i = e - k
        rets = []
        jj = i - vp + 1
        while jj <= i:
            rets.append(c[jj] / c[jj - 1] - 1.0)
            jj = jj + 1
        total = total + std1(rets)
        k = k + 1
    m = total / lb
    if not m > 0:
        return 0.0
    return ret / (m * math.sqrt(p))
```

checks:
VolatilityScaledReturnComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1559 passed, 8 skipped, 74 deselected, 2244 warnings in 60.98s (0:01:00) ===
