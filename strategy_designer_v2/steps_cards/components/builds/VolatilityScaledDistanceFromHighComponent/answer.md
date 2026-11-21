# VolatilityScaledDistanceFromHighComponent: night3_levels_run | 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d | VolatilityScaledHighBreakComponent

## attempt 1

answer: built
class: VolatilityScaledDistanceFromHighComponent
settings: {"period": 20, "vol_period": 20}
reason: `DistanceFromHighComponent` with `exclude_current` 1 gives the percent distance from the prior 20-close high, but no component divides that distance by the 20-bar standard deviation of one-bar returns. This measure combines the two, so one new class computes it, named by what it measures and not by the breakout idea.

table: Directional components
row: | `VolatilityScaledDistanceFromHighComponent` | `period` (20), `vol_period` (20) | (close[t] - H) / H / s. H = the highest close of bars t-`period` .. t-1 (bar t excluded). s = the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1, j = t-`vol_period`+1 .. t, bar t's included. The output is 0 when s = 0 | unbounded, signed; 0 when the close equals the prior high, positive above it, negative below it; its size is the distance from the prior high counted in usual one-bar moves | graded | usual moves | max(`period`, `vol_period`) + 1 (21) | closes only. A NaN close in the last max(`period`, `vol_period`) + 1 rows gives NaN. An H or a return base close not above 0 gives NaN (never on real bars). A flat return window (s = 0, never on real bars) gives 0. These settings raise when the component is built: `period` < 1, `vol_period` < 2 | stateless. Bar t's close cannot raise H, so the value measures the clearance over the high that stood before bar t. Equals `DistanceFromHighComponent` (`period` 20, `exclude_current` 1) / 100 / s. A `clip` with `min` 0 keeps only the break side. No `scaling_factor`: scale it with transforms |

```python class
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
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 20))
    vp = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(p, vp) + 1
    i = last - need + 1
    while i <= last:
        if c[i] != c[i]:
            return float("nan")
        i = i + 1
    h = c[last - p]
    i = last - p
    while i <= last - 1:
        if c[i] > h:
            h = c[i]
        i = i + 1
    if not h > 0:
        return float("nan")
    rets = []
    j = last - vp + 1
    while j <= last:
        if not c[j - 1] > 0:
            return float("nan")
        rets.append(c[j] / c[j - 1] - 1.0)
        j = j + 1
    total = 0.0
    for r in rets:
        total = total + r
    mean = total / len(rets)
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean) * (r - mean)
    s = math.sqrt(ss / (len(rets) - 1))
    if s == 0:
        return 0.0
    return (c[last] - h) / h / s
```

checks:
VolatilityScaledDistanceFromHighComponent: every check passed
the bot's suite: ======= 1584 passed, 16 skipped, 75 deselected, 2244 warnings in 56.99s ========
