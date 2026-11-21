# HighProximityScaledReturnComponent: night3_1h_run | 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h | ProximityWeightedSurgeComponent

## attempt 1

answer: built
class: HighProximityScaledReturnComponent
settings: {"period": 720, "return_period": 24, "window": 720, "power": 2.0}
reason: No component computes this measure. `HighProximityMomentumComponent` weights the return in percent of the base close. `MeanAbsReturnComponent` gives the usual move but multiplies nothing, and no config step divides one component by another. This measure is the product of a convex high-proximity weight and the 24-bar return in usual 24-bar moves, so one new class computes it.

table: Directional components
row: | `HighProximityScaledReturnComponent` | `period` (720), `return_period` (24), `window` (720), `power` (2.0) | W x (close[t] / close[t-`return_period`] - 1) / m. W = (1 / (1 + D))^`power`, where D = max(0, (H - close[t]) / H x 100) and H is the highest of the last `period` closes, bar t included. m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`return_period`] - 1), the overlapping `return_period`-bar returns ending at each of the last `window` bars, bar t included. The output is 0 when m = 0 | unbounded in practice, signed like the `return_period`-bar return. Its size is at most `window` (today's return is one of the `window` returns averaged in m). It equals the return in usual moves at a new high and shrinks towards 0 the deeper the close sits below the high | graded | usual `return_period`-bar moves (proximity-weighted) | max(`period`, `window` + `return_period`) (744) | closes only. A NaN close in the last max(`period`, `window` + `return_period`) rows gives NaN, and so does a close not above 0 there (never on real bars). m = 0 gives 0 (never on real bars; the return is then 0 too). These settings raise when the component is built: `period` < 2, `return_period` < 1, `window` < 1, `power` not above 0 | stateless. It equals `ConvexHighProximityComponent`-style weight W (as in `HighProximityMomentumComponent` "convex") x the `return_period`-bar return / `MeanAbsReturnComponent` (`period` = `return_period`, `window`). On 1h bars the defaults give the 24h surge in usual daily moves, weighted by the nearness to the 30-day closing high. No `scaling_factor`: scale it with transforms |

```python class
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
```

```python hand
def hand(df, params):
    period = int(params.get("period", 720))
    rp = int(params.get("return_period", 24))
    window = int(params.get("window", 720))
    power = float(params.get("power", 2.0))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(period, window + rp)
    i = last - need + 1
    while i <= last:
        x = c[i]
        if x != x or not x > 0:
            return float("nan")
        i = i + 1
    high = c[last]
    i = last - period + 1
    while i <= last:
        if c[i] > high:
            high = c[i]
        i = i + 1
    d = (high - c[last]) / high * 100.0
    if d < 0:
        d = 0.0
    w = (1.0 / (1.0 + d)) ** power
    total = 0.0
    i = last - window + 1
    while i <= last:
        r = c[i] / c[i - rp] - 1.0
        total = total + (r if r >= 0 else -r)
        i = i + 1
    m = total / window
    if m == 0:
        return 0.0
    ret = c[last] / c[last - rp] - 1.0
    return w * ret / m
```

checks:
HighProximityScaledReturnComponent: every check passed
the bot's suite: ======= 1582 passed, 16 skipped, 75 deselected, 2244 warnings in 56.96s ========
