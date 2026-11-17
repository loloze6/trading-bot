# VolatilityRankedFallComponent: night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.g1_next-day-rebound-after-sharp-falls.g1_rebound-grows-with-volatility_1d | VolRankedFallRebound

## attempt 1

answer: built
class: VolatilityRankedFallComponent
settings: {"vol_period": 20, "lookback": 120}
reason: No component in the catalogue computes this product. `VolatilityScaledReturnComponent` (`period` 1) gives the scaled one-bar move. `VolatilityPercentileRegimeComponent` ranks a different standard deviation (returns divided by the current close) and then smooths it. So a new class computes the one-sided fall, measured in usual moves, times the rank of today's 20-bar volatility against its last 120 values.

table: Directional components
row: | `VolatilityRankedFallComponent` | `vol_period` (20), `lookback` (120) | max(0, -(close[t] / close[t-1] - 1) / s(t)) x (number of i in t-`lookback`+1 .. t with s(i) <= s(t)) / `lookback`, s(i) being the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1 ending at bar i | 0 and up, unbounded above, never negative; 0 on up bars (and flat bars); grows with the depth of today's fall in usual moves and with the rank of today's volatility (the rank is above 0, up to 1) | graded | usual moves x share of bars | `lookback` + `vol_period` (140) | closes only. A NaN close in the last 140 rows gives NaN; a current std s(t) of 0 (20 equal returns, never seen on real bars) gives NaN. A `vol_period` below 2 or a `lookback` below 1 raises when the component is built | stateless. The first factor equals `VolatilityScaledReturnComponent` (`period` 1) negated and clipped at 0. The rank counts s(t) itself and is unsmoothed. One-sided (a long-only rebound reading); no `scaling_factor`: scale it with transforms |

```python class
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
        stds = []
        for k in range(self.lookback):
            end = self.vol_period + k
            stds.append(float(np.std(r[end - self.vol_period:end], ddof=1)))
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
```

```python hand
def hand(df, params):
    import math
    m = int(params.get("vol_period", 20))
    L = int(params.get("lookback", 120))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    first = t - L - m + 1
    i = first
    while i <= t:
        if c[i] != c[i]:
            return float("nan")
        i = i + 1

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def sd(i):
        xs = []
        j = i - m + 1
        while j <= i:
            xs.append(ret(j))
            j = j + 1
        mean = 0.0
        for x in xs:
            mean = mean + x
        mean = mean / m
        ss = 0.0
        for x in xs:
            ss = ss + (x - mean) * (x - mean)
        return math.sqrt(ss / (m - 1))

    s_now = sd(t)
    if not s_now > 0:
        return float("nan")
    count = 0
    i = t - L + 1
    while i <= t:
        if sd(i) <= s_now:
            count = count + 1
        i = i + 1
    rank = count / L
    z = -ret(t) / s_now
    if z < 0:
        z = 0.0
    return z * rank
```

checks:
VolatilityRankedFallComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1533 passed, 8 skipped, 74 deselected, 2170 warnings in 73.57s (0:01:13) ===
