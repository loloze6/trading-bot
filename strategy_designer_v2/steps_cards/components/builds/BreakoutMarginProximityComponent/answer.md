# BreakoutMarginProximityComponent: night7c_rangefail_run | 032-02.b1.e1.e1.e1.e3_first-break-short-follow-through_1d | BreakoutMarginProximityComponent

## attempt 1

answer: built
class: DistanceFromHighComponent
settings: {"period": 60, "source": "close", "exclude_current": 1, "form": "break_proximity"}
reason: The wished quantity is the close's percent margin over the prior 60-bar closing high, which `DistanceFromHighComponent` (`period` 60, `exclude_current` 1, `form` "percent") already measures. No config step turns that into the gated proximity G x 1 / (1 + margin): its "proximity" form reads 1 on every bar above the high, and `standardise` gives no 1 / (1 + x). So this is a new value, "break_proximity", of the `form` setting, which already chooses how the distance is expressed (as `DonchianBreakoutComponent` "below_proximity" did); the default "percent" and the other forms are unchanged.

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `extreme` ("high") | R = the highest (`extreme` "high") or lowest (`extreme` "low") value over the last `period` bars with bar t included (`exclude_current` 0), or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1). The values are those of `source`: "close" reads the close; "high" reads the bar's extreme on the `extreme` side (the `high` column for "high", the `low` column for "low"). `form` "percent": (close[t] - R) / R x 100. `form` "proximity": (1 / (1 + D))^`power`, where D = max(0, (R - close[t]) / R x 100) for "high" and max(0, (close[t] - R) / R x 100) for "low", the distance from the extreme in percent. `form` "break_proximity": G x (1 / (1 + M))^`power`. For "high", G = 1 when close[t] > R, else 0, and M = (close[t] - R) / R x 100. For "low", G = 1 when close[t] < R, else 0, and M = (R - close[t]) / R x 100. M is the margin beyond the extreme in percent. With `period` 60, `source` "close", `exclude_current` 1 and "break_proximity", the output is 1 / (1 + (close[t] - H) / H x 100) when close[t] > H = max(close[t-60..t-1]), else 0 | "high", "percent": `exclude_current` 0 gives 0 to -100, never positive; 1 gives -100 and up, signed. "low", "percent": `exclude_current` 0 gives 0 and up, never negative; 1 gives -100 and up, signed. "proximity": above 0, up to 1 (1 at the extreme or beyond it). "break_proximity": 0, or above 0 and below 1, never negative, no direction. It is 0 when the close does not break beyond R (always 0 with `exclude_current` 0, since R then includes bar t). It nears 1 as the margin beyond R shrinks toward 0 and shrinks smoothly toward 0 as the margin grows | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus `high` (or `low` with `extreme` "low") when `source` is "high". A NaN in the window, a NaN close[t], or an R not above 0 gives NaN. These settings raise when the component is built: `period` below 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `form` other than "percent", "proximity" or "break_proximity", `power` not above 0, `extreme` other than "high" or "low" | stateless. `form` "percent" (default) and "proximity" are the original outputs, unchanged. "break_proximity" is the nearness of a close beyond the prior extreme to that extreme: it measures how small the break's margin is, not a break event. No config step gives it, hence the setting. It jumps from 0 to near 1 where the close crosses R and is continuous in the close beyond it. `extreme` "low" with `period` 20, `source` "high" and `exclude_current` 1 gives the distance of the close below the prior 20-bar low; a `clip` with `max` 0 keeps only the break. No `scaling_factor`: scale it with transforms |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    The close's distance from the extreme of a window, on every bar:

        W = the last `period` bars, bar t included (exclude_current 0),
            or bars t-period .. t-1, bar t excluded (exclude_current 1)
        values: source "close" -> close; source "high" -> high (extreme "high") or low (extreme "low")
        R = max(values over W) (extreme "high") or min(values over W) (extreme "low")
        form "percent" (default): (close[t] - R) / R x 100
        form "proximity":         (1 / (1 + D)) ** power,
                                  D = max(0, (R - close[t]) / R x 100) for "high",
                                      max(0, (close[t] - R) / R x 100) for "low"
        form "break_proximity":   G x (1 / (1 + M)) ** power,
                                  "high": G = 1 if close[t] > R else 0, M = (close[t] - R) / R x 100
                                  "low":  G = 1 if close[t] < R else 0, M = (R - close[t]) / R x 100

    Range and sign: "high"/"percent" is 0 to -100 with exclude_current 0, and -100 and up with 1.
    "low"/"percent" is 0 and up with exclude_current 0, and -100 and up with 1. "proximity" is above 0, up to 1.
    "break_proximity" is 0, or above 0 and below 1. It is 0 off a break and nears 1 as the break's margin
    shrinks to 0. It always reads 0 with exclude_current 0, because R then includes bar t.
    The defaults (form "percent") and form "proximity" are the original outputs, unchanged.
    Warm-up: period + exclude_current rows, bar t included.
    NaN: a NaN in the window, a NaN close[t], or an R not above 0 gives NaN.
    Building raises for period < 2, source not "close"/"high", exclude_current not 0/1,
    form not "percent"/"proximity"/"break_proximity", power not above 0, extreme not "high"/"low".

    WHY THIS CANNOT LEAK: it reads only the close (and the high or low with source "high") of the last
    period + exclude_current rows of data, which end at bar t, the last row; nothing after bar t is read.
    """

    def __init__(self, name="DistanceFromHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 60))
        if self.period < 2:
            raise ValueError(f"DistanceFromHighComponent: period must be >= 2, got {self.period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high"):
            raise ValueError(f"DistanceFromHighComponent: source must be 'close' or 'high', got {self.source!r}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"DistanceFromHighComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.form = self.parameters.get("form", "percent")
        if self.form not in ("percent", "proximity", "break_proximity"):
            raise ValueError(
                f"DistanceFromHighComponent: form must be 'percent', 'proximity' or 'break_proximity', "
                f"got {self.form!r}")
        self.power = float(self.parameters.get("power", 1.0))
        if not self.power > 0:
            raise ValueError(f"DistanceFromHighComponent: power must be above 0, got {self.power}")
        self.extreme = self.parameters.get("extreme", "high")
        if self.extreme not in ("high", "low"):
            raise ValueError(f"DistanceFromHighComponent: extreme must be 'high' or 'low', got {self.extreme!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        if self.source == "close":
            col = "close"
        else:
            col = "high" if self.extreme == "high" else "low"
        vals = data[col].astype(float).to_numpy()
        n = len(vals)
        ex = self.exclude_current
        window = vals[n - self.period - ex: n - ex]
        c = float(data["close"].astype(float).iloc[-1])
        if np.isnan(window).any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        R = float(window.max()) if self.extreme == "high" else float(window.min())
        if not R > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.form == "percent":
            value = (c - R) / R * 100.0
        elif self.form == "proximity":
            if self.extreme == "high":
                D = max(0.0, (R - c) / R * 100.0)
            else:
                D = max(0.0, (c - R) / R * 100.0)
            value = (1.0 / (1.0 + D)) ** self.power
        else:
            if self.extreme == "high":
                broke = c > R
                M = (c - R) / R * 100.0
            else:
                broke = c < R
                M = (R - c) / R * 100.0
            value = (1.0 / (1.0 + M)) ** self.power if broke else 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"reference": R, "close": c, "form": self.form, "extreme": self.extreme}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    period = int(params.get("period", 60))
    source = params.get("source", "close")
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "percent")
    power = float(params.get("power", 1.0))
    extreme = params.get("extreme", "high")
    closes = [float(x) for x in list(df["close"])]
    if source == "close":
        series = closes
    elif extreme == "high":
        series = [float(x) for x in list(df["high"])]
    else:
        series = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    # window: bars t-period+1 .. t (ex 0) or t-period .. t-1 (ex 1)
    last = t - ex
    vals = []
    i = last - period + 1
    while i <= last:
        vals.append(series[i])
        i += 1
    c = closes[t]
    for v in vals + [c]:
        if v != v:
            return float("nan")
    R = vals[0]
    for v in vals:
        if extreme == "high" and v > R:
            R = v
        if extreme == "low" and v < R:
            R = v
    if not R > 0:
        return float("nan")
    if form == "percent":
        return (c - R) / R * 100.0
    if form == "proximity":
        if extreme == "high":
            d = (R - c) / R * 100.0
        else:
            d = (c - R) / R * 100.0
        if d < 0:
            d = 0.0
        return (1.0 / (1.0 + d)) ** power
    # break_proximity: 0 unless the close is beyond the prior extreme
    if extreme == "high":
        if not c > R:
            return 0.0
        margin = (c - R) / R * 100.0
    else:
        if not c < R:
            return 0.0
        margin = (R - c) / R * 100.0
    return (1.0 / (1.0 + margin)) ** power
```

checks:
the bot's suite fails:
cludes implicit conversion of bare integers (e.g. `+ 1`).Please use a specific unit instead.
    ts = ts[:gap_point] + [t + pd.Timedelta(hours=gap_hours) for t in ts[gap_point:]]

tests/test_build_core_block_adjusted_significance.py::test_block_adjusted_pvalue_gap_aware_with_a_real_gap
  /home/user/trading-bot/trading-bot/tests/test_build_core_block_adjusted_significance.py:136: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. `+ 1`).Please use a specific unit instead.
    expected_step = pd.Timedelta(seconds=candle_interval_seconds)

tests/test_build_core_ic_horizons.py: 52 warnings
  /home/user/trading-bot/trading-bot/reporting/run_artifact.py:92: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. `+ 1`).Please use a specific unit instead.
    span_ok = (ts.shift(-horizon) - ts) == pd.Timedelta(seconds=candle_interval_seconds * horizon)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_built_components.py::test_standard_checks[RankWeightedScaledMoveComponent]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
=== 1 failed, 210 passed, 1 skipped, 75 deselected, 1808 warnings in 39.03s ====


## attempt 2

answer: built
class: BreakoutMarginProximityComponent
settings: {"period": 60}
reason: No component gives the nearness of a fresh break to the prior closing high. `DistanceFromHighComponent` "proximity" is 1 at or above the high and decays below it, and `VolScaledBreakAboveHighComponent` and `BreakoutRunUpDiscountComponent` measure other things. So one new class computes this measure. The failed check named `RankWeightedScaledMoveComponent`, an existing class, not this one; this class is unchanged in substance and resubmitted.

table: Directional components
row: | `BreakoutMarginProximityComponent` | `period` (60) | G x 1 / (1 + (close[t] − H) / H x 100), H = max(close[t-`period`] .. close[t-1]) (bar t excluded), G = 1 when close[t] > H, else 0 | 0 to 1, never negative; no direction. It is 0 when the close is at or below the prior high. It is above 0 and below 1 on a break, nearing 1 as the margin above H nears 0, and shrinking smoothly as the margin grows | graded | dimensionless (proximity, 0 to 1) | `period` + 1 (61) | closes only (last `period` + 1 rows). A NaN close among them gives NaN; an H not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1 | stateless. A break needs a strictly higher close than every prior close of the window; a tie is not a break. Bar t's close cannot raise H. The value jumps from 0 to near 1 where close[t] crosses H, and is continuous in the close while bar t breaks out. One-sided, a first-break (shallow-margin) reading. No `scaling_factor`: scale it with transforms |

```python class
class BreakoutMarginProximityComponent(SubStrategyComponent):
    """
    Nearness of a breaking close to the prior closing high, on every bar:

        H = max(close[t-period] .. close[t-1])          (bar t excluded)
        G = 1 if close[t] > H else 0
        raw_value = G x 1 / (1 + (close[t] - H) / H x 100)

    Range: 0 to 1, never negative, no direction. It is 0 when close[t] <= H (no break; a tie is not a
    break). On a break it is in (0, 1): near 1 for a tiny margin above H, shrinking smoothly as the
    margin (in percent of H) grows.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN close in the last period + 1 rows gives NaN; an H not above 0 gives NaN (never on real bars).
    Building raises for a period below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bars
    t-period .. t, bar t being the last row; each close is known at its bar's close.
    """

    def __init__(self, name="BreakoutMarginProximity", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 60))
        if self.period < 1:
            raise ValueError(f"BreakoutMarginProximityComponent: period must be >= 1, got {self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        closes = data['close'].astype(float).to_numpy()[-(p + 1):]
        if np.isnan(closes).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        c = float(closes[-1])
        h = float(np.max(closes[:-1]))
        if not h > 0:
            value = float("nan")
        elif c > h:
            value = 1.0 / (1.0 + (c - h) / h * 100.0)
        else:
            value = 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'prior_high': h, 'close': c}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    p = int(params.get("period", 60))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    window = [closes[t - k] for k in range(0, p + 1)]
    for x in window:
        if x != x:
            return float("nan")
    c = closes[t]
    h = closes[t - 1]
    for k in range(1, p + 1):
        if closes[t - k] > h:
            h = closes[t - k]
    if not h > 0:
        return float("nan")
    if not c > h:
        return 0.0
    margin = (c - h) / h * 100.0
    return 1.0 / (1.0 + margin)
```

checks:
BreakoutMarginProximityComponent: every check passed
the bot's suite: == 1660 passed, 16 skipped, 75 deselected, 2244 warnings in 97.99s (0:01:37) ===
