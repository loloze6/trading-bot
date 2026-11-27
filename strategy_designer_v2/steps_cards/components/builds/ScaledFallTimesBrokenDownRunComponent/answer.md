# ScaledFallTimesBrokenDownRunComponent: night9_fallcalmfade_run | 070-01.g1.d1_deep-slide-calm-run-break-fade_1d | RunBreakDepthComponent

## attempt 1

answer: built
class: ScaledFallTimesBrokenDownRunComponent
settings: {"period": 20, "vol_period": 20, "max_bars": 30}
reason: No component multiplies the 20-bar fall in usual moves by the length of a down run that bar t's up close breaks. `VolatilityScaledReturnComponent` gives the fall and `PriorDownRunOnUpCloseComponent` "beyond_first" gives n − 1, but no config step multiplies two components, so one new class computes the product. Read from closes only as the wish requires, the run is strictly falling. Its low is therefore close[t−1] itself, and the tiebreak d is computed but equals 0 on every bar.

table: Directional components
row: | `ScaledFallTimesBrokenDownRunComponent` | `period` (20), `vol_period` (20), `max_bars` (30) | F x (n − 1 + d) when close[t] > close[t-1], else 0. n = the number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1], capped at `max_bars`. d = (close[t-1] − min(close[t-n .. t-1])) / (max(close[t-n .. t-1]) − min(close[t-n .. t-1])), 0 when that range is 0. F = max(0, −(close[t] / close[t-`period`] − 1) / (s x sqrt(`period`))), s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included; F = 0 when s = 0. The output is 0 when n = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 on down and flat bars, on an up bar after an up or flat bar, after a single down bar (n = 1), and when close[t] is not below close[t-`period`]. The multiplier is at most `max_bars` − 1 | graded | usual `period`-bar moves x bars | max(`max_bars` + 2, `period` + 1, `vol_period` + 1) (32) | closes only. A NaN close in the last (warmup) rows gives NaN, whatever the gate, and so does a close not above 0 there (never on real bars). s = 0 (never on real bars) gives 0. These settings raise when the component is built: `period` < 1, `vol_period` < 2, `max_bars` < 1 | stateless. The run of lower closes is strictly falling, so its lowest close is close[t-1] and d is 0 on every bar: on closes, the wished tiebreak adds nothing, and the multiplier is the whole number n − 1. Equals max(0, −`VolatilityScaledReturnComponent` (`period`, `vol_period`)) x `PriorDownRunOnUpCloseComponent` (`max_bars`, `form` "beyond_first"). The value is nonzero only on the bar that breaks a run, so it jumps from 0 there; it is continuous in the closes through F. The cap binds only on a run longer than `max_bars` bars, which real 1d bars do not show. One-sided, a rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class ScaledFallTimesBrokenDownRunComponent(SubStrategyComponent):
    """
    The slide in usual moves times the length of the down run that bar t's up close breaks:

        gate: close[t] > close[t-1], else the output is 0
        n = number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1],
            capped at max_bars; the output is 0 when n = 0
        run = close[t-n .. t-1];  d = (close[t-1] - min(run)) / (max(run) - min(run)), 0 when max = min
        s = std (ddof 1) of the vol_period one-bar returns close[j]/close[j-1] - 1, j = t-vol_period+1 .. t
        F = max(0, -(close[t]/close[t-period] - 1) / (s * sqrt(period))),  F = 0 when s = 0
        raw_value = F * (n - 1 + d)

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 on down and flat bars, on an up
    bar that follows an up or flat bar, after a single down bar, and when close[t] >= close[t-period].
    The run of lower closes is strictly falling, so min(run) = close[t-1] and d is 0 on every bar.
    Warm-up: max(max_bars + 2, period + 1, vol_period + 1) rows, bar t included (32 at the defaults).
    NaN: a NaN close, or a close not above 0, in the warm-up rows gives NaN, whatever the gate.
    s = 0 gives 0. Building raises for period < 1, vol_period < 2, max_bars < 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last get_required_periods() rows of data,
    the last of which is bar t; no later row exists in data.
    """

    def __init__(self, name="ScaledFallTimesBrokenDownRun", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"ScaledFallTimesBrokenDownRunComponent: period must be >= 1, got {self.period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"ScaledFallTimesBrokenDownRunComponent: vol_period must be >= 2, got {self.vol_period}")
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(
                f"ScaledFallTimesBrokenDownRunComponent: max_bars must be >= 1, got {self.max_bars}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        w = data['close'].astype(float).to_numpy()[-need:]
        if np.isnan(w).any() or not (w > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        t = len(w) - 1
        value = 0.0
        n = 0
        d = 0.0
        fall = 0.0
        if w[t] > w[t - 1]:
            i = t - 1
            while n < self.max_bars and w[i] < w[i - 1]:
                n += 1
                i -= 1
            if n > 0:
                run = w[t - n:t]
                hi = float(run.max())
                lo = float(run.min())
                d = (w[t - 1] - lo) / (hi - lo) if hi > lo else 0.0
                rets = w[t - self.vol_period + 1:t + 1] / w[t - self.vol_period:t] - 1.0
                s = float(np.std(rets, ddof=1))
                if s > 0:
                    r = w[t] / w[t - self.period] - 1.0
                    fall = max(0.0, -r / (s * np.sqrt(self.period)))
                value = fall * (n - 1 + d)
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'run_length': n, 'tiebreak': d, 'scaled_fall': fall}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.max_bars + 2, self.period + 1, self.vol_period + 1)
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 20))
    vp = int(params.get("vol_period", 20))
    mb = int(params.get("max_bars", 30))
    need = max(mb + 2, p + 1, vp + 1)
    c = [float(x) for x in list(df["close"])][-need:]
    for x in c:
        if x != x or not x > 0:
            return float("nan")
    t = len(c) - 1
    if not c[t] > c[t - 1]:
        return 0.0
    # length of the run of lower closes ending at bar t-1
    n = 0
    i = t - 1
    while n < mb and c[i] < c[i - 1]:
        n = n + 1
        i = i - 1
    if n == 0:
        return 0.0
    run = [c[k] for k in range(t - n, t)]
    hi = max(run)
    lo = min(run)
    d = (c[t - 1] - lo) / (hi - lo) if hi > lo else 0.0
    # std (ddof 1) of the vp one-bar returns ending at bar t
    rets = []
    for j in range(t - vp + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var = var + (r - mean) * (r - mean)
    s = math.sqrt(var / (len(rets) - 1))
    if not s > 0:
        return 0.0
    ret = c[t] / c[t - p] - 1.0
    fall = -ret / (s * math.sqrt(p))
    if fall < 0:
        fall = 0.0
    return fall * (n - 1 + d)
```

checks:
ScaledFallTimesBrokenDownRunComponent: every check passed
the bot's suite: == 1679 passed, 16 skipped, 75 deselected, 2244 warnings in 143.71s (0:02:23) ==
