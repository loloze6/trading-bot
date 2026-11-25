# DonchianBreakoutComponent: night7_rangefail_run | 033-01.b2_beyond-range-close-drift_1d | PriorRangePositionComponent

## attempt 1

answer: built
class: DonchianBreakoutComponent
settings: {"period": 20, "scaling_factor": 1.0, "source": "high_low", "form": "position", "exclude_current": 1}
reason: `DonchianBreakoutComponent` (`source` "high_low", `form` "position", `sf` 1) already computes this measure, the close's position in the window's high-low range, but its window always includes bar t, so the value stays between −1 and +1. The wish needs the prior window, bars t-20 .. t-1. That is the same measure on another window, so it becomes a new `exclude_current` setting whose default 0 keeps today's output unchanged.

table: Directional components
row: | `DonchianBreakoutComponent` | `period` (48), `scaling_factor` (20.0), `source` ("close"), `form` ("position"), `exclude_current` (0) | H, L over bars t-`period`+1 .. t (`exclude_current` 0, bar t included) or t-`period` .. t-1 (`exclude_current` 1, bar t excluded). `source` "close": H, L = highest and lowest close. `source` "high_low": H = max(high), L = min(low). `form` "position": (2 x pos − 1) x `sf`, pos = (close[t] − L) / (H − L), pos = 0.5 when H = L. `form` "below_proximity": mid = (H + L) / 2, D = (mid − close[t]) / mid x 100; 1 / (1 + D) when close[t] < mid, 0 when close[t] >= mid (`sf` not used). With `period` 20, `sf` 1, `source` "high_low", `exclude_current` 1: 2 x (close[t] − min(low[t-20..t-1])) / (max(high[t-20..t-1]) − min(low[t-20..t-1])) − 1 | "position", `exclude_current` 0: −`sf` to +`sf`, signed, positive above the window's middle, 0 at the middle or for a zero range. "position", `exclude_current` 1: unbounded, signed; −`sf` at the prior low, +`sf` at the prior high, beyond +`sf` above it and below −`sf` under it, 0 at the middle or for a zero range. "below_proximity": 0 to below 1, never negative, no direction; 0 at or above the middle (and for a zero range), rising toward 1 as a close below the middle climbs back to it; it jumps from near 1 to 0 where the close crosses the middle | graded | "position": forecast units (x `sf`). "below_proximity": dimensionless (0 to 1) | `period` + `exclude_current` (48) | "close": closes only (window rows and close[t]). "high_low": high and low (the window rows) and close[t]. A NaN in any value read gives NaN. With "below_proximity", a mid not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `source` other than "close" or "high_low", `form` other than "position" or "below_proximity", `exclude_current` not 0 or 1 | stateless. `form` "position" with `exclude_current` 0 (the defaults) is the original output, unchanged. `exclude_current` 1 reads the channel that stood before bar t, so bar t's own high, low or close cannot widen it. The position then keeps growing past ±`sf` as the close moves beyond the prior range. It is not a breakout event. No config step gives the bounded "below_proximity" form, hence that setting. |

```python class
class DonchianBreakoutComponent(SubStrategyComponent):
    """
    Where the close sits in a channel of the last `period` bars, on every bar.

        exclude_current = 0 (default): window = bars t-period+1 .. t   (bar t included)
        exclude_current = 1:           window = bars t-period .. t-1   (bar t excluded)
        source = "close" (default): H, L = highest and lowest close of the window
        source = "high_low":        H = max(high), L = min(low) over the window
        form = "position" (default):
            pos = (close[t] - L) / (H - L), pos = 0.5 when H = L
            raw_value = (2 x pos - 1) x scaling_factor
        form = "below_proximity":
            mid = (H + L) / 2, D = (mid - close[t]) / mid x 100
            raw_value = 1 / (1 + D) when close[t] < mid, else 0   (scaling_factor not used)

    Range and sign: "position" with exclude_current 0 runs from -sf to +sf. It is signed, positive above the
    window's middle and 0 at the middle or for a zero range. With exclude_current 1 it is unbounded and signed:
    -sf at the prior low, +sf at the prior high, beyond them outside the prior range.
    "below_proximity" runs from 0 to below 1, never negative.
    The defaults (exclude_current 0, form "position") are the original output, unchanged.
    Warm-up: period + exclude_current rows, bar t included.

    NaN: a NaN in any value read (the window's closes, or highs and lows, and close[t]) gives NaN. With
    "below_proximity", a mid not above 0 gives NaN (never on real bars).
    Building raises for period < 1, a source other than "close" or "high_low", a form other than "position"
    or "below_proximity", or an exclude_current other than 0 or 1.

    WHY THIS CANNOT LEAK: it reads only the last period + exclude_current rows of data (the last row is bar t):
    the window's closes or highs and lows (ending at bar t, or at bar t-1 with exclude_current 1) and close[t],
    all known at bar t's close.
    """

    def __init__(self, name="DonchianBreakout", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        if self.period < 1:
            raise ValueError(f"DonchianBreakoutComponent: period must be >= 1, got {self.period}")
        self.scaling_factor = float(self.parameters.get("scaling_factor", 20.0))
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high_low"):
            raise ValueError(f"DonchianBreakoutComponent: source must be 'close' or 'high_low', got {self.source!r}")
        self.form = self.parameters.get("form", "position")
        if self.form not in ("position", "below_proximity"):
            raise ValueError(
                f"DonchianBreakoutComponent: form must be 'position' or 'below_proximity', got {self.form!r}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"DonchianBreakoutComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = len(data)
        stop = n - self.exclude_current
        start = stop - self.period
        close_t = float(data["close"].astype(float).iloc[-1])
        if self.source == "close":
            win = data["close"].astype(float).iloc[start:stop]
            hi_vals = win
            lo_vals = win
        else:
            hi_vals = data["high"].astype(float).iloc[start:stop]
            lo_vals = data["low"].astype(float).iloc[start:stop]
        if np.isnan(close_t) or hi_vals.isna().any() or lo_vals.isna().any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(hi_vals.max())
        L = float(lo_vals.min())
        if self.form == "position":
            rng = H - L
            pos = 0.5 if rng == 0 else (close_t - L) / rng
            value = (2.0 * pos - 1.0) * self.scaling_factor
        else:
            mid = (H + L) / 2.0
            if not mid > 0:
                value = float("nan")
            elif close_t < mid:
                D = (mid - close_t) / mid * 100.0
                value = 1.0 / (1.0 + D)
            else:
                value = 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"high": H, "low": L, "close": close_t, "exclude_current": self.exclude_current}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    p = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    source = params.get("source", "close")
    form = params.get("form", "position")
    ex = int(params.get("exclude_current", 0))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    # window: bars t-ex-p+1 .. t-ex
    idx = [t - ex - k for k in range(p)]
    if source == "close":
        his = [closes[i] for i in idx]
        los = [closes[i] for i in idx]
    else:
        highs = [float(x) for x in list(df["high"])]
        lows = [float(x) for x in list(df["low"])]
        his = [highs[i] for i in idx]
        los = [lows[i] for i in idx]
    c = closes[t]
    for x in his + los + [c]:
        if x != x:
            return float("nan")
    H = his[0]
    for x in his:
        if x > H:
            H = x
    L = los[0]
    for x in los:
        if x < L:
            L = x
    if form == "position":
        if H - L == 0:
            pos = 0.5
        else:
            pos = (c - L) / (H - L)
        return (2.0 * pos - 1.0) * sf
    mid = (H + L) / 2.0
    if not mid > 0:
        return float("nan")
    if c < mid:
        D = (mid - c) / mid * 100.0
        return 1.0 / (1.0 + D)
    return 0.0
```

checks:
DonchianBreakoutComponent: every check passed
the bot's suite: == 1657 passed, 16 skipped, 75 deselected, 2244 warnings in 121.94s (0:02:01) ==
