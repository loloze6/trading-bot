# CappedScaledRiseTimesDepthBelowHighComponent: night8_fallingagitated_run | 058-01.g2.b1.d2.b1.d2_rises-deep-in-decline-fade_1d | CappedScaledRiseTimesDepthBelowHigh

## attempt 1

answer: built
class: CappedScaledRiseTimesDepthBelowHighComponent
settings: {"vol_period": 30, "period": 20, "cap": 1.0}
reason: No component of the catalogue multiplies bar t's rise in usual one-bar moves, capped, by the close's percent depth below its own closing high. `LowProximityScaledRiseComponent` weights the rise by nearness to the low, `UpStreakGainTimesDepthBelowAverageComponent` uses an up-streak and an SMA, and no config step multiplies two components or caps a factor before a product, so one new class computes this combined measure.

table: Directional components
row: | `CappedScaledRiseTimesDepthBelowHighComponent` | `vol_period` (30), `period` (20), `cap` (1.0) | min(max(0, (close[t] / close[t-1] − 1) / s), `cap`) x max(0, (H − close[t]) / H x 100). s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included. H = the highest of the last `period` closes, bar t included. The first factor is 0 when s = 0 | 0 to below `cap` x 100, never negative; no direction. It is 0 on down and flat bars and 0 with the close at its `period`-bar closing high. It grows with bar t's rise in usual one-bar moves up to `cap` of them, then stays flat in the rise. It grows linearly with the percent depth below the high | graded | usual one-bar moves (capped at `cap`) x percent of the high | max(`vol_period` + 1, `period`) (31) | closes only. A NaN close in the last max(`vol_period` + 1, `period`) rows gives NaN, and so does a close not above 0 there (never on real bars). s = 0 (a flat return window, never on real bars) gives 0. These settings raise when the component is built: `vol_period` < 2, `period` < 2, `cap` not above 0 | stateless. The first factor is `VolatilityScaledReturnComponent` (`period` 1, `vol_period`) clipped to [0, `cap`]. The second factor is −`DistanceFromHighComponent` (`period`, `source` "close", `exclude_current` 0, `form` "percent"). A `clip` on the output is not this, because it would clip the product rather than the rise. The value is continuous in the closes and exactly 0 on every bar that did not close up. On 1d bars the defaults give the day's rise in usual 30-day moves, capped at one, times the percent depth below the 20-day closing high. It is one-sided, a rise-deep-in-a-decline reading. No `scaling_factor`: scale it with transforms |

```python class
class CappedScaledRiseTimesDepthBelowHighComponent(SubStrategyComponent):
    """
    Bar t's rise in usual one-bar moves, capped, times the close's percent depth below its closing high:

        r(j) = close[j] / close[j-1] - 1
        s    = std (ddof 1) of r(j), j = t-vol_period+1 .. t (bar t's return included)
        x    = min(max(0, r(t) / s), cap)        (x = 0 when s = 0)
        H    = max(close[t-period+1 .. t])       (bar t included)
        D    = max(0, (H - close[t]) / H x 100)
        raw_value = x * D

    Range and sign: 0 to below cap x 100, never negative, no direction. It is 0 on down and flat bars and 0 at the
    closing high. It grows with the rise up to cap usual moves and linearly with the depth below the high.
    Warm-up: max(vol_period + 1, period) rows, bar t included (31 at the defaults).
    NaN: a NaN close in the last max(vol_period + 1, period) rows gives NaN; a close not above 0 there gives NaN
    (never on real bars). s = 0 gives 0. Building the component raises for vol_period < 2, period < 2, or a cap
    that is not above 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(vol_period + 1, period) rows of data,
    the last of which is bar t; a close is known at its bar's close.
    """

    def __init__(self, name="CappedScaledRiseDepthBelowHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 30))
        if self.vol_period < 2:
            raise ValueError(f"CappedScaledRiseTimesDepthBelowHighComponent: vol_period must be >= 2, got {self.vol_period}")
        self.period = int(self.parameters.get("period", 20))
        if self.period < 2:
            raise ValueError(f"CappedScaledRiseTimesDepthBelowHighComponent: period must be >= 2, got {self.period}")
        try:
            self.cap = float(self.parameters.get("cap", 1.0))
        except (TypeError, ValueError):
            raise ValueError("CappedScaledRiseTimesDepthBelowHighComponent: cap must be a number above 0")
        if not self.cap > 0:
            raise ValueError(f"CappedScaledRiseTimesDepthBelowHighComponent: cap must be above 0, got {self.cap}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or (c <= 0).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        vp = self.vol_period
        rets = c[-vp:] / c[-vp - 1:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        r = float(rets[-1])
        if s > 0:
            x = min(max(0.0, r / s), self.cap)
        else:
            x = 0.0
        h = float(np.max(c[-self.period:]))
        d = max(0.0, (h - float(c[-1])) / h * 100.0)
        self._raw_value = float(x * d)
        self.confidence = 1.0
        self.debug_info = {"scaled_rise_capped": x, "std": s, "high": h, "depth_pct": d}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.vol_period + 1, self.period)
```

```python hand
def hand(df, params):
    vp = int(params.get("vol_period", 30))
    p = int(params.get("period", 20))
    cap = float(params.get("cap", 1.0))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(vp + 1, p)
    for k in range(need):
        v = c[t - k]
        if v != v or not v > 0:
            return float("nan")
    # one-bar returns j = t-vp+1 .. t
    rets = []
    for j in range(t - vp + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    total = 0.0
    for v in rets:
        total += v
    mean = total / len(rets)
    ss = 0.0
    for v in rets:
        ss += (v - mean) * (v - mean)
    s = (ss / (len(rets) - 1)) ** 0.5
    rise = c[t] / c[t - 1] - 1.0
    if s > 0:
        x = rise / s
        if x < 0:
            x = 0.0
        if x > cap:
            x = cap
    else:
        x = 0.0
    h = c[t]
    for k in range(p):
        if c[t - k] > h:
            h = c[t - k]
    depth = (h - c[t]) / h * 100.0
    if depth < 0:
        depth = 0.0
    return x * depth
```

checks:
CappedScaledRiseTimesDepthBelowHighComponent: every check passed
the bot's suite: == 1669 passed, 16 skipped, 75 deselected, 2244 warnings in 132.74s (0:02:12) ==
