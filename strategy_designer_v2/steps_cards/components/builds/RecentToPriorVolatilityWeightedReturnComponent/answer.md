# RecentToPriorVolatilityWeightedReturnComponent: night6_longreversal_run | 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d | VolatilityRatioWeightedScaledReturn

## attempt 1

answer: built
class: RecentToPriorVolatilityWeightedReturnComponent
settings: {"period": 1, "vol_period": 5, "base_period": 30, "base_lag": 0, "return_scale": "base_std"}
reason: `RecentToPriorVolatilityWeightedReturnComponent` (period 1, vol_period 5, base_period 30, base_lag 0) already gives the day's return weighted by s5 / s30, but it counts the return in percent (x 100), not in s30 units. The wished quantity is the same return against another base, so it is a new value of a setting on that class: `return_scale` "base_std" divides the return by s_base. Its default, "percent", keeps today's output.

table: Directional components
row: | `RecentToPriorVolatilityWeightedReturnComponent` | `period` (48), `vol_period` (48), `base_period` (168), `base_lag` (48), `return_scale` ("percent") | R x K x s_recent / s_base, R = close[t] / close[t-`period`] - 1. s_recent = std (ddof 1) of the `vol_period` one-bar returns r[j] = close[j] / close[j-1] - 1, j = t-`vol_period`+1 .. t. s_base = std (ddof 1) of the `base_period` returns r[j], j = t-`base_lag`-`base_period`+1 .. t-`base_lag` (ending at bar t-`base_lag`, that bar's return included). `return_scale` "percent": K = 100. `return_scale` "base_std": K = 1 / s_base, so the output is R / s_base x s_recent / s_base. With `period` 1, `vol_period` 5, `base_period` 30, `base_lag` 0 and "base_std": (close[t] / close[t-1] - 1) / s30 x s5 / s30 | unbounded, signed like the `period`-bar return; 0 when that return is 0. Its size grows with the move ("percent": in percent; "base_std": in usual one-bar moves of the base window, with no sqrt(`period`) scaling) and with how much more volatile the recent `vol_period` bars were than the base (the ratio is 0 and up, 1 when the two stds are equal) | graded | "percent": percent x volatility ratio (recent over prior). "base_std": base-window one-bar stds x volatility ratio | max(`period`, `vol_period`, `base_lag` + `base_period`) + 1 (217; 31 at the wished settings) | closes only. A NaN close in the last (warmup) rows gives NaN. A close not above 0 there gives NaN (never on real bars). s_base = 0 (flat base returns, never on real bars) gives NaN. These settings raise when the component is built: `period` < 1, `vol_period` < 2, `base_period` < 2, `base_lag` < 0, `return_scale` other than "percent" or "base_std" | stateless. `return_scale` "percent" (default) is the original output, unchanged. "base_std" counts the move in base-window one-bar stds; no config step divides by a window's std, hence the setting. With `base_lag` 0 the base window contains the recent one. At the wished settings on 1d bars: the day's return in usual 30-day moves times the 5-day over the 30-day volatility. `negate` gives the fade reading. No `scaling_factor`: scale it with transforms |

```python class
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
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 48))
    vp = int(params.get("vol_period", 48))
    bp = int(params.get("base_period", 168))
    lag = int(params.get("base_lag", 48))
    scale = params.get("return_scale", "percent")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(p, vp, lag + bp) + 1
    for k in range(need):
        x = c[t - k]
        if x != x or not x > 0:
            return float("nan")

    def ret1(j):
        return c[j] / c[j - 1] - 1.0

    def std1(xs):
        n = len(xs)
        m = 0.0
        for x in xs:
            m += x
        m /= n
        ss = 0.0
        for x in xs:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (n - 1))

    recent = [ret1(j) for j in range(t - vp + 1, t + 1)]
    base = [ret1(j) for j in range(t - lag - bp + 1, t - lag + 1)]
    s_recent = std1(recent)
    s_base = std1(base)
    if not s_base > 0:
        return float("nan")
    R = c[t] / c[t - p] - 1.0
    if scale == "base_std":
        return R / s_base * (s_recent / s_base)
    return R * 100.0 * (s_recent / s_base)
```

checks:
RecentToPriorVolatilityWeightedReturnComponent: every check passed
the bot's suite: == 1652 passed, 16 skipped, 75 deselected, 2244 warnings in 130.90s (0:02:10) ==
