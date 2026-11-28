# VolatilityScaledDistanceFromHighComponent: night10_fallcalmshort_run | 060-02_falling-calm-low-to-close-fade_1d | CloseAboveLowInUsualMovesComponent

## attempt 1

answer: built
class: VolatilityScaledDistanceFromHighComponent
settings: {"period": 1, "vol_period": 30, "source": "high", "exclude_current": 0, "base": "close", "extreme": "low"}
reason: `VolatilityScaledDistanceFromHighComponent` already computes the close's distance from a window extreme in usual one-bar moves, but only from the high, and `negate` of that is (high − close) / close / s, not this measure. The class is rewritten with an `extreme` setting, "high" by default so today's output is unchanged; "low" measures from the window's low, as `DistanceFromHighComponent` does.

table: Directional components
row: | `VolatilityScaledDistanceFromHighComponent` | `period` (20), `vol_period` (20), `source` ("close"), `exclude_current` (1), `base` ("level"), `extreme` ("high") | (close[t] − R) / D / s. R = the highest (`extreme` "high") or lowest (`extreme` "low") value of `source` over bars t-`period` .. t-1 (`exclude_current` 1, bar t excluded) or t-`period`+1 .. t (`exclude_current` 0, bar t included). The value is the close with `source` "close". With "high" it is the bar's extreme on the `extreme` side: the `high` column for "high", the `low` column for "low". D = R (`base` "level") or close[t] (`base` "close"). s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included. 0 when s = 0. With `period` 1, `vol_period` 30, `source` "high", `exclude_current` 0, `base` "close" and `extreme` "low": (close[t] − low[t]) / close[t] / s30 | unbounded, signed. 0 when the close equals R, positive above it, negative below it. "high" with `exclude_current` 0 is never positive on real bars. "low" with `exclude_current` 0 is never negative on real bars: 0 with the close at the low, growing linearly as the close stands above it. Its size is the distance from the extreme in usual one-bar moves | graded | usual moves | max(`period` + `exclude_current`, `vol_period` + 1) (21; 31 at the wished settings) | closes (last `vol_period` + 1 rows and the window with "close"); high (or low with `extreme` "low") over the window rows with `source` "high". A NaN in any value read gives NaN. An R, a return base close, or (with `base` "close") a close[t] not above 0 gives NaN (never on real bars). s = 0 (flat return window, never on real bars) gives 0. These settings raise when the component is built: `period` < 1, `vol_period` < 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `base` other than "level" or "close", `extreme` other than "high" or "low" | stateless. The defaults (`source` "close", `exclude_current` 1, `base` "level", `extreme` "high") are the original output, unchanged, and so are all earlier settings with `extreme` "high". `extreme` "low" measures from the window's low; no config step gives it (`negate` of the distance from the high is not it), hence the setting. On 1d bars the wished settings give the close's height above the day's low in percent of the close, in usual 30-day moves. It equals `CloseLocationInRangeComponent` (`reference` "low") x `RangeInReturnStdComponent` (`vol_period` 30). Continuous in the prices. No `scaling_factor`: scale it with transforms |

```python class
class VolatilityScaledDistanceFromHighComponent(SubStrategyComponent):
    """
    Distance of the close from a window extreme, in usual one-bar moves, on every bar:

        window = bars t-period .. t-1          (exclude_current 1, default: bar t excluded)
                 bars t-period+1 .. t          (exclude_current 0: bar t included)
        values = close                         (source "close", default)
                 high column / low column      (source "high": the bar's extreme on the `extreme` side)
        R = max(values over window)            (extreme "high", default)
            min(values over window)            (extreme "low")
        D = R (base "level", default) or close[t] (base "close")
        s = std (ddof 1) of close[j] / close[j-1] - 1, j = t-vol_period+1 .. t (bar t's return included)
        raw_value = (close[t] - R) / D / s,    0.0 when s = 0

    With period 1, vol_period 30, source "high", exclude_current 0, base "close", extreme "low":
    (close[t] - low[t]) / close[t] / s30, which is 0 with the close at the day's low and grows linearly as the
    close stands above it.
    Range and sign: unbounded, signed; 0 at R, positive above it, negative below it. With exclude_current 0 the
    extreme "high" reading is never positive and the extreme "low" reading is never negative on real bars.
    Graded. The defaults (extreme "high") are the original output, unchanged.
    Warm-up: max(period + exclude_current, vol_period + 1) rows, bar t included.
    NaN: a NaN in any value read gives NaN. An R, a return base close, or (base "close") a close[t] that is not
    above 0 gives NaN. s = 0 gives 0.0.
    Building raises for period < 1, vol_period < 2, source other than "close"/"high", exclude_current not 0/1,
    base other than "level"/"close", and extreme other than "high"/"low".

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data): the closes of
    the last vol_period + 1 rows, and the close/high/low values of the window rows, which end at bar t at the latest.
    """

    def __init__(self, name="VolScaledDistFromExtreme", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.period = int(p.get("period", 20))
        if self.period < 1:
            raise ValueError(f"VolatilityScaledDistanceFromHighComponent: period must be >= 1, got {self.period}")
        self.vol_period = int(p.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: vol_period must be >= 2, got {self.vol_period}")
        self.source = p.get("source", "close")
        if self.source not in ("close", "high"):
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: source must be 'close' or 'high', got {self.source!r}")
        ex = p.get("exclude_current", 1)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.base = p.get("base", "level")
        if self.base not in ("level", "close"):
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: base must be 'level' or 'close', got {self.base!r}")
        self.extreme = p.get("extreme", "high")
        if self.extreme not in ("high", "low"):
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: extreme must be 'high' or 'low', got {self.extreme!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float).to_numpy()
        n = len(close)
        t = n - 1
        if self.exclude_current == 1:
            lo, hi = t - self.period, t
        else:
            lo, hi = t - self.period + 1, t + 1
        if self.source == "close":
            col = close
        else:
            col = data["high" if self.extreme == "high" else "low"].astype(float).to_numpy()
        win = col[lo:hi]
        rc = close[n - self.vol_period - 1:]
        c = close[t]
        if np.isnan(win).any() or np.isnan(rc).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        R = float(win.max()) if self.extreme == "high" else float(win.min())
        bases = rc[:-1]
        if not R > 0 or not (bases > 0).all() or (self.base == "close" and not c > 0):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        D = R if self.base == "level" else float(c)
        rets = rc[1:] / rc[:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        if not s > 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float((c - R) / D / s)
        self.confidence = 1.0
        self.debug_info = {"extreme_value": R, "divisor": D, "return_std": s, "extreme": self.extreme}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + self.exclude_current, self.vol_period + 1)
```

```python hand
def hand(df, params):
    import math
    period = int(params.get("period", 20))
    vp = int(params.get("vol_period", 20))
    source = params.get("source", "close")
    ex = int(params.get("exclude_current", 1))
    base = params.get("base", "level")
    extreme = params.get("extreme", "high")
    close = [float(x) for x in list(df["close"])]
    t = len(close) - 1
    if source == "close":
        vals = close
    else:
        vals = [float(x) for x in list(df["high" if extreme == "high" else "low"])]
    # window bars
    if ex == 1:
        idx = [t - k for k in range(1, period + 1)]
    else:
        idx = [t - k for k in range(0, period)]
    win = [vals[i] for i in idx]
    closes_used = [close[t - k] for k in range(0, vp + 1)]
    for x in win + closes_used:
        if x != x:
            return float("nan")
    R = win[0]
    for x in win:
        if extreme == "high":
            if x > R:
                R = x
        else:
            if x < R:
                R = x
    if not R > 0:
        return float("nan")
    # returns j = t-vp+1 .. t
    rets = []
    for j in range(t - vp + 1, t + 1):
        if not close[j - 1] > 0:
            return float("nan")
        rets.append(close[j] / close[j - 1] - 1.0)
    c = close[t]
    if base == "close" and not c > 0:
        return float("nan")
    D = R if base == "level" else c
    m = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - m) * (r - m)
    s = math.sqrt(ss / (len(rets) - 1))
    if not s > 0:
        return 0.0
    return (c - R) / D / s
```

checks:
VolatilityScaledDistanceFromHighComponent: every check passed
the bot's suite: = 1686 passed, 16 skipped, 75 deselected, 95636 warnings in 175.14s (0:02:55) ==
