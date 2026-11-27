# VolatilityScaledDistanceFromHighComponent: pilot_a4_auto_run | 060-02_falling-calm-low-to-close-fade_1d | CloseAboveLowInUsualMoves

## attempt 1

answer: built
class: VolatilityScaledDistanceFromHighComponent
settings: {"period": 1, "vol_period": 30, "source": "high", "exclude_current": 0, "base": "close", "extreme": "low"}
reason: The wish is the close's distance from a bar extreme, divided by close[t], in usual one-bar moves. `VolatilityScaledDistanceFromHighComponent` computes this measure from the high only, and no config step gives the distance from the low (`negate` of the high reading is not it; `RangeInReturnStdComponent` x `CloseLocationInRangeComponent` "low" would need a product of two components). So the class is written again with an `extreme` setting, as `DistanceFromHighComponent` has, and its default "high" keeps today's output exactly.

table: Directional components
row: | `VolatilityScaledDistanceFromHighComponent` | `period` (20), `vol_period` (20), `source` ("close"), `exclude_current` (1), `base` ("level"), `extreme` ("high") | (close[t] − R) / D / s. R = the highest (`extreme` "high") or lowest (`extreme` "low") value of `source` over bars t-`period` .. t-1 (`exclude_current` 1, bar t excluded) or t-`period`+1 .. t (`exclude_current` 0, bar t included). The value is the close with `source` "close", or with "high" the bar's extreme on the `extreme` side (the `high` column for "high", the `low` column for "low"). D = R (`base` "level") or close[t] (`base` "close"). s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included. 0 when s = 0. With `period` 1, `vol_period` 30, `source` "high", `exclude_current` 0, `base` "close", `extreme` "low": (close[t] − low[t]) / close[t] / s30 | unbounded, signed. 0 when the close equals R, positive above it, negative below it. "high", `exclude_current` 0: never positive on real bars (close <= R). "low", `exclude_current` 0: never negative on real bars (close >= R); 0 with the close at the low, growing linearly as it stands above it. "low", `exclude_current` 1: negative below the prior low, positive above it. Its size is the distance from the extreme in usual one-bar moves | graded | usual moves | max(`period` + `exclude_current`, `vol_period` + 1) (21; 31 at the wished settings) | closes (last `vol_period` + 1 rows and the window with "close"); high (or low with `extreme` "low") over the window rows with "high". A NaN in any value read gives NaN. An R, a return base close, or (with `base` "close") a close[t] not above 0 gives NaN (never on real bars). s = 0 (flat return window, never on real bars) gives 0. These settings raise when the component is built: `period` < 1, `vol_period` < 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `base` other than "level" or "close", `extreme` other than "high" or "low" | stateless. The defaults (`source` "close", `exclude_current` 1, `base` "level", `extreme` "high") are the original output, unchanged, and so are all earlier settings with `extreme` "high". `extreme` "low" measures from the window's low. No config step gives it, because `negate` of a distance from the high is not it, hence the setting. On 1d bars the wished settings give the close's height above the day's low in percent of the close, in usual 30-day moves. That equals `RangeInReturnStdComponent` (30) x `CloseLocationInRangeComponent` ("low"). Continuous in the prices. Ignores the open and the volume. No `scaling_factor`: scale it with transforms |

```python class
class VolatilityScaledDistanceFromHighComponent(SubStrategyComponent):
    """
    Distance of the close from a window extreme, in usual one-bar moves, on every bar:

        window = bars t-period .. t-1        (exclude_current 1, default: bar t excluded)
                 bars t-period+1 .. t        (exclude_current 0: bar t included)
        source "close" (default): the values are the closes of the window
        source "high":            the values are the bar's extreme on the `extreme` side
                                  (the `high` column for extreme "high", the `low` column for extreme "low")
        extreme "high" (default): R = max(values)
        extreme "low":            R = min(values)
        D = R (base "level", default) or close[t] (base "close")
        s = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1, j = t-vol_period+1 .. t
        raw_value = (close[t] - R) / D / s,   0.0 when s = 0

    With period 1, vol_period 30, source "high", exclude_current 0, base "close", extreme "low":
    (close[t] - low[t]) / close[t] / s30.
    Range and sign: unbounded, signed; 0 at R, positive above it, negative below it. With exclude_current 0,
    "high" is never positive and "low" is never negative on real bars. Graded, in usual one-bar moves.
    The defaults (and every setting with extreme "high") are the original output, unchanged.
    Warm-up: max(period + exclude_current, vol_period + 1) rows, bar t included.

    NaN: a NaN in any value read (window values, close[t], the vol_period + 1 closes) gives NaN. An R, a
    return base close, or (base "close") a close[t] not above 0 gives NaN (never on real bars). s = 0 gives 0.0.
    Building the component raises for period < 1, vol_period < 2, an unknown source, exclude_current not 0 or 1,
    an unknown base, or an extreme other than "high" or "low".

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data): the window
    rows ending at t or t-1, the last vol_period + 1 closes, and close[t], all known at bar t's close.
    """

    def __init__(self, name="VolScaledDistanceFromHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"VolatilityScaledDistanceFromHighComponent: period must be >= 1, got {self.period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: vol_period must be >= 2, got {self.vol_period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high"):
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: source must be 'close' or 'high', got {self.source!r}")
        ex = self.parameters.get("exclude_current", 1)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.base = self.parameters.get("base", "level")
        if self.base not in ("level", "close"):
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: base must be 'level' or 'close', got {self.base!r}")
        self.extreme = self.parameters.get("extreme", "high")
        if self.extreme not in ("high", "low"):
            raise ValueError(
                f"VolatilityScaledDistanceFromHighComponent: extreme must be 'high' or 'low', got {self.extreme!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        nan = float("nan")
        close = data["close"].astype(float).to_numpy()
        n = len(close)
        stop = n - self.exclude_current
        start = stop - self.period
        if self.source == "close":
            vals = close[start:stop]
        else:
            col = "high" if self.extreme == "high" else "low"
            vals = data[col].astype(float).to_numpy()[start:stop]
        c = float(close[-1])
        rc = close[n - self.vol_period - 1:]
        self.confidence = 1.0
        if np.isnan(vals).any() or np.isnan(c) or np.isnan(rc).any():
            self._raw_value = nan
            return
        if not (rc[:-1] > 0).all():
            self._raw_value = nan
            return
        R = float(vals.max()) if self.extreme == "high" else float(vals.min())
        if not R > 0:
            self._raw_value = nan
            return
        if self.base == "close" and not c > 0:
            self._raw_value = nan
            return
        rets = rc[1:] / rc[:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        D = R if self.base == "level" else c
        if s == 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float((c - R) / D / s)
        self.debug_info = {"extreme_value": R, "divisor": D, "return_std": s, "extreme": self.extreme}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
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
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    if source == "close":
        col = closes
    elif extreme == "high":
        col = [float(x) for x in list(df["high"])]
    else:
        col = [float(x) for x in list(df["low"])]
    # window: bars t-ex-period+1 .. t-ex
    vals = []
    for k in range(period):
        vals.append(col[t - ex - k])
    c = closes[t]
    rc = []
    for j in range(t - vp, t + 1):
        rc.append(closes[j])
    for x in vals + [c] + rc:
        if x != x:
            return float("nan")
    for x in rc[:-1]:
        if not x > 0:
            return float("nan")
    R = vals[0]
    for x in vals:
        if extreme == "high":
            if x > R:
                R = x
        else:
            if x < R:
                R = x
    if not R > 0:
        return float("nan")
    if base == "close" and not c > 0:
        return float("nan")
    rets = []
    for i in range(1, len(rc)):
        rets.append(rc[i] / rc[i - 1] - 1.0)
    m = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var += (r - m) * (r - m)
    s = math.sqrt(var / (len(rets) - 1))
    if s == 0:
        return 0.0
    D = R if base == "level" else c
    return (c - R) / D / s
```

checks:
VolatilityScaledDistanceFromHighComponent: every check passed
the bot's suite: = 1685 passed, 16 skipped, 75 deselected, 95636 warnings in 154.75s (0:02:34) ==
