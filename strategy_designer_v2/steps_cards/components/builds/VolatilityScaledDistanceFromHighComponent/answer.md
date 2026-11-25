# VolatilityScaledDistanceFromHighComponent: night7_steadydecline_run | 035-02_swing-wide-low-close-rebounds_1d | LowCloseRangeInUsualMovesComponent

## attempt 1

answer: built
class: VolatilityScaledDistanceFromHighComponent
settings: {"period": 1, "vol_period": 20, "source": "high", "exclude_current": 0, "base": "close"}
reason: The wish is the distance of the close from a high, divided by the close and counted in usual one-bar moves. That is the measure of `VolatilityScaledDistanceFromHighComponent`, here taken against bar t's own high and divided by close[t]. The class lacks the high source, the window that includes bar t and the close divisor, so it is written again with `source`, `exclude_current` and `base` (the defaults keep today's output). Its value at these settings is (close[t] − high[t]) / close[t] / s, and `negate` gives exactly the wished (high[t] − close[t]) / close[t] / s.

table: Directional components
row: | `VolatilityScaledDistanceFromHighComponent` | `period` (20), `vol_period` (20), `source` ("close"), `exclude_current` (1), `base` ("level") | (close[t] − H) / D / s. H = the highest value of `source` over bars t-`period` .. t-1 (`exclude_current` 1, bar t excluded) or t-`period`+1 .. t (`exclude_current` 0, bar t included). The value is the close with `source` "close" and the bar's high with "high". D = H (`base` "level") or close[t] (`base` "close"). s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included. 0 when s = 0. With `period` 1, `source` "high", `exclude_current` 0 and `base` "close": (close[t] − high[t]) / close[t] / s | unbounded, signed. 0 when the close equals H, positive above it, negative below it. With `exclude_current` 0 it is never positive on real bars (close <= H). Its size is the distance from the high in usual one-bar moves | graded | usual moves | max(`period` + `exclude_current`, `vol_period` + 1) (21) | closes (last `vol_period` + 1 rows and the window with "close"); high (window rows) with "high". A NaN in any value read gives NaN. An H, a return base close, or (with `base` "close") a close[t] not above 0 gives NaN (never on real bars). s = 0 (flat return window, never on real bars) gives 0. These settings raise when the component is built: `period` < 1, `vol_period` < 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `base` other than "level" or "close" | stateless. The defaults (`source` "close", `exclude_current` 1, `base` "level") are the original output, unchanged. On 1d bars `period` 1, `source` "high", `exclude_current` 0 and `base` "close" give minus the close's drop under the day's high in percent of the close, in usual 20-day moves. `negate` gives the low-close reading, which equals (high − low) / close / s x (high − close) / (high − low). A `clip` with `min` 0 keeps only the break side at the defaults. No `scaling_factor`: scale it with transforms |

```python class
class VolatilityScaledDistanceFromHighComponent(SubStrategyComponent):
    """
    Distance of the close from a recent high, counted in usual one-bar moves:

        H = max of `source` values over bars t-period .. t-1   (exclude_current = 1, default; bar t excluded)
            or over bars t-period+1 .. t                       (exclude_current = 0; bar t included)
            source = "close" (default): the closes; source = "high": the highs
        D = H (base = "level", default) or close[t] (base = "close")
        s = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1, j = t-vol_period+1 .. t
        raw_value = (close[t] - H) / D / s       (0.0 when s = 0)

    The defaults are the original output, unchanged: (close[t] - max(close[t-20..t-1])) / H / s20.
    With period 1, source "high", exclude_current 0 and base "close" it is (close[t] - high[t]) / close[t] / s:
    never positive on real bars. `negate` gives the low-close reading (high[t] - close[t]) / close[t] / s.
    Range: unbounded, signed; 0 at H, positive above it, negative below it (never positive with exclude_current 0).
    Warm-up: max(period + exclude_current, vol_period + 1) rows, bar t included.
    NaN: a NaN in any value read gives NaN; an H, a return base close or (base "close") a close[t] not above 0
    gives NaN (never on real bars); a flat return window (s = 0) gives 0.0.
    Building the component raises for period < 1, vol_period < 2, a source other than "close" or "high", an
    exclude_current other than 0 or 1, or a base other than "level" or "close".

    WHY THIS CANNOT LEAK: it reads the `close` column (and `high` with source "high") of the last
    max(period + exclude_current, vol_period + 1) rows of data only, the last of them being bar t; every value read
    is known at bar t's close.
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
        vals = close if self.source == "close" else data["high"].astype(float).to_numpy()
        ex = self.exclude_current
        win = vals[t - self.period + 1 - ex: t + 1 - ex]
        rc = close[t - self.vol_period: t + 1]
        c = close[t]
        if np.isnan(win).any() or np.isnan(rc).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(np.max(win))
        if not H > 0 or not (rc[:-1] > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.base == "close" and not c > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = rc[1:] / rc[:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        D = H if self.base == "level" else float(c)
        if s == 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float((c - H) / D / s)
        self.confidence = 1.0
        self.debug_info = {"H": H, "divisor": D, "s": s, "source": self.source,
                           "exclude_current": ex, "base": self.base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + self.exclude_current, self.vol_period + 1)
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 20))
    vp = int(params.get("vol_period", 20))
    source = params.get("source", "close")
    ex = int(params.get("exclude_current", 1))
    base = params.get("base", "level")
    c = [float(x) for x in list(df["close"])]
    src = c if source == "close" else [float(x) for x in list(df["high"])]
    t = len(c) - 1
    # window of the high: bars t-p-ex+1 .. t-ex
    win = []
    for k in range(p):
        win.append(src[t - ex - k])
    # closes for the returns: bars t-vp .. t
    closes = []
    for k in range(vp + 1):
        closes.append(c[t - vp + k])
    for x in win + closes:
        if x != x:
            return float("nan")
    H = win[0]
    for x in win:
        if x > H:
            H = x
    if not H > 0:
        return float("nan")
    for x in closes[:-1]:
        if not x > 0:
            return float("nan")
    ct = c[t]
    if base == "close" and not ct > 0:
        return float("nan")
    rets = []
    for k in range(1, len(closes)):
        rets.append(closes[k] / closes[k - 1] - 1.0)
    mean = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean) ** 2
    s = math.sqrt(ss / (len(rets) - 1))
    if s == 0:
        return 0.0
    D = H if base == "level" else ct
    return (ct - H) / D / s
```

checks:
VolatilityScaledDistanceFromHighComponent: every check passed
the bot's suite: == 1657 passed, 16 skipped, 75 deselected, 2244 warnings in 122.48s (0:02:02) ==
