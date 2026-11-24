# VolatilityRatioWeightedScaledFallComponent: night6_streak_run | 031-02.b1.d2_rebound-graded-by-turbulence_1d | VolatilityRatioWeightedScaledFall

## attempt 1

answer: built
class: VolatilityRatioWeightedScaledFallComponent
settings: {"vol_period": 10, "base_vol_period": 60}
reason: No component of the catalogue gives this measure. It is the day's fall in usual base moves, max(0, −r_t) / s60, times the recent-over-base volatility ratio s10 / s60. `FallVolumeVolatilityWeightedComponent` uses this ratio but also carries a volume factor and a fall in percent. `VolatilityRankedFallComponent` weights by a rank, and `VolatilityScaledReturnComponent` (`vol_lookback`) uses a mean of stds over one window. The measure is a product of two existing measures, so one new class computes it.

table: Directional components
row: | `VolatilityRatioWeightedScaledFallComponent` | `vol_period` (10), `base_vol_period` (60) | max(0, −(close[t] / close[t-1] − 1)) / s_base x s_recent / s_base. s_recent and s_base are the std (ddof 1) of the last `vol_period` and `base_vol_period` one-bar returns close[j] / close[j-1] − 1, both ending at bar t, bar t's return included. 0.0 when s_base = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 on up bars and flat bars. It grows with the size of today's fall in usual base-window moves and with the recent volatility against the base one (1 at equal volatility) | graded | usual one-bar moves x ratio of volatilities (recent over base) | max(`vol_period`, `base_vol_period`) + 1 (61) | closes only. A NaN close in the last max(`vol_period`, `base_vol_period`) + 1 rows gives NaN, and so does a close not above 0 there (never on real bars). s_base = 0 gives 0.0 (never on real bars; the fall is then 0 too). These settings raise when the component is built: `vol_period` < 2, `base_vol_period` < 2 | stateless. Equals max(0, −`VolatilityScaledReturnComponent` (`period` 1, `vol_period` = `base_vol_period`)) x `RecentToPriorVolatilityRatioComponent` (`vol_period`, `base_period` = `base_vol_period`, `base_lag` 0). The base window contains the recent one. It is continuous in the closes and exactly 0 on every bar that did not close down. On 1d bars the defaults give the day's fall in usual 60-day moves times the 10-day over the 60-day volatility. One-sided, a rebound reading. No `scaling_factor`: scale it with transforms |

```python class
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
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("vol_period", 10))
    bp = int(params.get("base_vol_period", 60))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    n = max(vp, bp)
    used = closes[t - n: t + 1]
    for x in used:
        if x != x or not x > 0:
            return float("nan")

    def ret(j):
        return closes[j] / closes[j - 1] - 1.0

    def std_ddof1(xs):
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (len(xs) - 1))

    recent = [ret(j) for j in range(t - vp + 1, t + 1)]
    base = [ret(j) for j in range(t - bp + 1, t + 1)]
    s_recent = std_ddof1(recent)
    s_base = std_ddof1(base)
    fall = -ret(t)
    if fall < 0:
        fall = 0.0
    if not s_base > 0:
        return 0.0
    return (fall / s_base) * (s_recent / s_base)
```

checks:
VolatilityRatioWeightedScaledFallComponent: every check passed
the bot's suite: == 1654 passed, 16 skipped, 75 deselected, 2244 warnings in 122.20s (0:02:02) ==
