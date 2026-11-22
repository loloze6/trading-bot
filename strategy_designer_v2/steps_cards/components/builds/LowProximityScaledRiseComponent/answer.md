# LowProximityScaledRiseComponent: night4_fallingbounce_run | 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d | LowProximityScaledRiseComponent

## attempt 1

answer: built
class: LowProximityScaledRiseComponent
settings: {"vol_period": 20, "period": 90}
reason: No component computes this product. `VolatilityScaledReturnComponent` (`period` 1, `vol_period` 20) clipped at 0 gives the first factor, and `DistanceFromHighComponent` (`extreme` "low", `form` "proximity", `period` 90) gives the second. No config step multiplies two components, so one new class computes the whole measure.

table: Directional components
row: | `LowProximityScaledRiseComponent` | `vol_period` (20), `period` (90) | max(0, (close[t] / close[t-1] - 1) / s) x 1 / (1 + D). s is the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1, j = t-`vol_period`+1 .. t, bar t's included. D = (close[t] - Lo) / Lo x 100, Lo being the lowest of the last `period` closes, bar t included. The first factor is 0 when s = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 on down bars and flat bars. It grows with the size of today's rise in usual moves and with the nearness of the close to its `period`-bar closing low. The weight is above 0, up to 1, and is 1 at the low | graded | usual moves x proximity (0 to 1) | max(`vol_period` + 1, `period`) (90) | closes only. A NaN close in the last max(`vol_period` + 1, `period`) rows gives NaN. A Lo or a return base close not above 0 gives NaN (never on real bars). A flat return window (s = 0, never on real bars) gives 0. These settings raise when the component is built: `vol_period` < 2, `period` < 2 | stateless. Equals `VolatilityScaledReturnComponent` (`period` 1, `vol_period` 20) clipped at 0, times `DistanceFromHighComponent` (`period` 90, `extreme` "low", `form` "proximity"). One-sided, a bounce-near-lows reading. Continuous in the closes. No `scaling_factor`: scale it with transforms |

```python class
class LowProximityScaledRiseComponent(SubStrategyComponent):
    """
    Today's rise in usual one-bar moves, weighted by the nearness of the close to its recent closing low:

        r(j)  = close[j] / close[j-1] - 1
        s     = std (ddof 1) of r(j), j = t-vol_period+1 .. t        (bar t's return included)
        Lo    = min(close[t-period+1 .. t])                          (bar t included)
        D     = (close[t] - Lo) / Lo x 100                           (>= 0, since Lo includes close[t])
        raw_value = max(0, r(t) / s) x 1 / (1 + D)                   (first factor 0 when s = 0)

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 on down and flat bars and grows with
    the size of the rise in usual moves and with the nearness of the close to its low. The weight is in (0, 1] and
    equals 1 at the low.
    Warm-up: max(vol_period + 1, period) rows, bar t included.
    NaN: a NaN close in the last max(vol_period + 1, period) rows gives NaN. A Lo or a return base close not above
    0 gives NaN (never on real bars). s = 0 gives 0.
    Building raises for vol_period < 2 or period < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(vol_period + 1, period) rows of data,
    the last of which is bar t; no later row exists in what it is given.
    """

    def __init__(self, name="LowProximityScaledRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"LowProximityScaledRiseComponent: vol_period must be >= 2, got {self.vol_period}")
        self.period = int(self.parameters.get("period", 90))
        if self.period < 2:
            raise ValueError(f"LowProximityScaledRiseComponent: period must be >= 2, got {self.period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rc = c[-(self.vol_period + 1):]
        bases = rc[:-1]
        if not (bases > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = rc[1:] / bases - 1.0
        s = float(np.std(rets, ddof=1))
        lo = float(np.min(c[-self.period:]))
        if not lo > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        d = (float(c[-1]) - lo) / lo * 100.0
        w = 1.0 / (1.0 + d)
        first = max(0.0, float(rets[-1]) / s) if s > 0 else 0.0
        self._raw_value = float(first * w)
        self.confidence = 1.0
        self.debug_info = {"ret": float(rets[-1]), "std": s, "low": lo, "D": d, "weight": w}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.vol_period + 1, self.period)
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("vol_period", 20))
    p = int(params.get("period", 90))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(vp + 1, p)
    for i in range(last - need + 1, last + 1):
        if c[i] != c[i]:
            return float("nan")
    rets = []
    for j in range(last - vp + 1, last + 1):
        if not c[j - 1] > 0:
            return float("nan")
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var = var + (r - mean) * (r - mean)
    var = var / (len(rets) - 1)
    s = math.sqrt(var)
    lo = c[last]
    for i in range(last - p + 1, last + 1):
        if c[i] < lo:
            lo = c[i]
    if not lo > 0:
        return float("nan")
    d = (c[last] - lo) / lo * 100.0
    weight = 1.0 / (1.0 + d)
    today = c[last] / c[last - 1] - 1.0
    if s > 0:
        first = today / s
        if first < 0:
            first = 0.0
    else:
        first = 0.0
    return first * weight
```

checks:
LowProximityScaledRiseComponent: every check passed
the bot's suite: == 1610 passed, 16 skipped, 75 deselected, 2244 warnings in 96.92s (0:01:36) ===
