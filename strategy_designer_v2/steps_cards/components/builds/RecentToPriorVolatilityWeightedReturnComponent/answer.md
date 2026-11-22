# RecentToPriorVolatilityWeightedReturnComponent: night4_weekend_run | 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue_1h | WeekendVolatilityWeightedReturn

## attempt 1

answer: built
class: RecentToPriorVolatilityWeightedReturnComponent
settings: {"period": 48, "vol_period": 48, "base_period": 168, "base_lag": 48}
reason: No component in the catalogue gives a return weighted by the volatility of the last bars against the volatility of a separate earlier stretch. `VolatilityRatioToAverageComponent` and `VolatilityScaledReturnComponent` (`vol_lookback`) both compare against a mean of rolling stds that includes bar t, not the std of the 168 returns ending at t-48. This one class computes the wished product: the 48-bar percent return times std(last 48 returns) / std(the 168 returns ending at t-48).

table: Directional components
row: | `RecentToPriorVolatilityWeightedReturnComponent` | `period` (48), `vol_period` (48), `base_period` (168), `base_lag` (48) | (close[t] / close[t-`period`] - 1) x 100 x s_recent / s_base. s_recent = std (ddof 1) of the `vol_period` one-bar returns r[j] = close[j] / close[j-1] - 1, j = t-`vol_period`+1 .. t. s_base = std (ddof 1) of the `base_period` returns r[j], j = t-`base_lag`-`base_period`+1 .. t-`base_lag` (ending at bar t-`base_lag`, that bar's return included) | unbounded, signed like the `period`-bar return; 0 when that return is 0; its size grows with the move and with how much more volatile the recent `vol_period` bars were than the earlier base (the ratio is 0 and up, 1 when the two stds are equal) | graded | percent x volatility ratio (recent over prior) | max(`period`, `vol_period`, `base_lag` + `base_period`) + 1 (217) | closes only. A NaN close in the last 217 rows gives NaN. A close not above 0 there gives NaN (never on real bars). s_base = 0 (168 flat returns, never on real bars) gives NaN. These settings raise when the component is built: `period` < 1, `vol_period` < 2, `base_period` < 2, `base_lag` < 0 | stateless. At the defaults the recent window (returns of bars t-47 .. t) and the base (returns of bars t-215 .. t-48) are adjacent and do not overlap: on 1h bars, the last two days against the week before them. `negate` gives the fall-positive reading. No `scaling_factor`: scale it with transforms |

```python class
class RecentToPriorVolatilityWeightedReturnComponent(SubStrategyComponent):
    """
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

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, vol_period,
    base_lag + base_period) + 1 rows of data, the last of which is bar t; no row after bar t is read.
    """

    def __init__(self, name="RecentToPriorVolWeightedReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        self.vol_period = int(self.parameters.get("vol_period", 48))
        self.base_period = int(self.parameters.get("base_period", 168))
        self.base_lag = int(self.parameters.get("base_lag", 48))
        if self.period < 1:
            raise ValueError(f"RecentToPriorVolatilityWeightedReturnComponent: period must be >= 1, got {self.period}")
        if self.vol_period < 2:
            raise ValueError(
                f"RecentToPriorVolatilityWeightedReturnComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.base_period < 2:
            raise ValueError(
                f"RecentToPriorVolatilityWeightedReturnComponent: base_period must be >= 2, got {self.base_period}")
        if self.base_lag < 0:
            raise ValueError(
                f"RecentToPriorVolatilityWeightedReturnComponent: base_lag must be >= 0, got {self.base_lag}")
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
        r = c[1:] / c[:-1] - 1.0
        n = len(r)
        recent = r[n - self.vol_period:]
        base = r[n - self.base_lag - self.base_period: n - self.base_lag]
        s_recent = float(np.std(recent, ddof=1))
        s_base = float(np.std(base, ddof=1))
        ret = (c[-1] / c[-1 - self.period] - 1.0) * 100.0
        if not s_base > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(ret * s_recent / s_base)
        self.confidence = 1.0
        self.debug_info = {"return_pct": float(ret), "s_recent": s_recent, "s_base": s_base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period, self.vol_period, self.base_lag + self.base_period) + 1
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 48))
    vp = int(params.get("vol_period", 48))
    bp = int(params.get("base_period", 168))
    lag = int(params.get("base_lag", 48))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    first = t - max(p, vp, lag + bp)
    for i in range(first, t + 1):
        x = c[i]
        if x != x or not x > 0:
            return float("nan")

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def sd(xs):
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) ** 2
        return math.sqrt(ss / (len(xs) - 1))

    recent = [ret(j) for j in range(t - vp + 1, t + 1)]
    base = [ret(j) for j in range(t - lag - bp + 1, t - lag + 1)]
    s_recent = sd(recent)
    s_base = sd(base)
    if not s_base > 0:
        return float("nan")
    move = (c[t] / c[t - p] - 1.0) * 100.0
    return move * s_recent / s_base
```

checks:
RecentToPriorVolatilityWeightedReturnComponent: every check passed
the bot's suite: == 1611 passed, 16 skipped, 75 deselected, 2244 warnings in 104.20s (0:01:44) ==
