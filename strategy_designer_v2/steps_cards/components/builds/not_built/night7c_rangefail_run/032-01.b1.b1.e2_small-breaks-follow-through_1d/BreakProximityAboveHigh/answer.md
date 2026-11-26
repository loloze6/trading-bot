# not built: night7c_rangefail_run | 032-01.b1.b1.e2_small-breaks-follow-through_1d | BreakProximityAboveHigh

## attempt 1

answer: built
class: DistanceFromHighComponent
settings: {"period": 60, "source": "close", "exclude_current": 1, "form": "break_proximity", "power": 1.0}
reason: `DistanceFromHighComponent` already measures the close's distance from its prior closing high R = max(close[t-60 .. t-1]) (`exclude_current` 1). None of its forms gives the wished bounded break reading: "proximity" reads 1 at or above the high, and no config step gives 1 / (1 + D) or zeroes the side below it. So the class is written again with a new `form` value "break_proximity", and its default keeps today's output unchanged.

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `extreme` ("high") | R = the highest (`extreme` "high") or lowest (`extreme` "low") value over the last `period` bars with bar t included (`exclude_current` 0), or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1). The values are those of `source`: "close" reads the close; "high" reads the bar's extreme on the `extreme` side (the `high` column for "high", the `low` column for "low"). `form` "percent": (close[t] - R) / R x 100. `form` "proximity": (1 / (1 + D))^`power`, D = max(0, (R - close[t]) / R x 100) for "high", max(0, (close[t] - R) / R x 100) for "low". `form` "break_proximity": (1 / (1 + B))^`power` when the close is beyond the extreme, else 0. Beyond means close[t] > R for "high", with B = (close[t] - R) / R x 100. It means close[t] < R for "low", with B = (R - close[t]) / R x 100. With `period` 60 and `exclude_current` 1 the output is (1 / (1 + (close[t] - H) / H x 100))^`power` for close[t] > H = max(close[t-60 .. t-1]), else 0 | "high", "percent": `exclude_current` 0 gives 0 to -100, never positive; 1 gives -100 and up, signed. "low", "percent": `exclude_current` 0 gives 0 and up; 1 gives -100 and up, signed. "proximity": above 0, up to 1 (1 at the extreme or beyond it). "break_proximity": 0, or above 0 and below 1. It is never negative and has no direction. It is 0 at or inside the extreme and nears 1 for a break of near-zero size. It falls smoothly toward 0 as the break grows. It jumps from 0 to near 1 where the close crosses R | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus `high` (or `low` with `extreme` "low") when `source` is "high". A NaN in the window, a NaN close[t], or an R not above 0 gives NaN. These settings raise when the component is built: `period` below 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `form` other than "percent", "proximity" or "break_proximity", `power` not above 0, `extreme` other than "high" or "low" | stateless. `form` "percent" (default) and "proximity" are the original outputs, unchanged. "break_proximity" is the nearness of a close beyond the prior extreme to that extreme, rising as the break gets smaller. No config step gives it, hence the setting. With `exclude_current` 0 the close can never pass R, so "break_proximity" is 0 on every bar: use `exclude_current` 1. No `scaling_factor`: scale it with transforms |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    The close's distance from the extreme of a window, on every bar:

        W = bars t-period+1 .. t (exclude_current 0) or bars t-period .. t-1 (exclude_current 1)
        values = close (source "close") or the bar's extreme on the extreme side
                 (source "high": the high column for extreme "high", the low column for extreme "low")
        R = max(values over W) (extreme "high") or min(values over W) (extreme "low")
        form "percent" (default): (close[t] - R) / R x 100
        form "proximity":         (1 / (1 + D))^power,
                                  D = max(0, (R - close[t]) / R x 100) for "high",
                                  D = max(0, (close[t] - R) / R x 100) for "low"
        form "break_proximity":   "high": (1 / (1 + B))^power with B = (close[t] - R) / R x 100 when close[t] > R,
                                          else 0
                                  "low":  (1 / (1 + B))^power with B = (R - close[t]) / R x 100 when close[t] < R,
                                          else 0

    Range and sign: "percent" with "high" is 0 to -100 (exclude_current 0) or -100 and up (1). With "low" it is
    0 and up (exclude_current 0) or -100 and up (1). "proximity" is above 0, up to 1. "break_proximity" is 0, or
    above 0 and below 1, never negative and with no direction. It is 0 at or inside the extreme, nears 1 for a
    tiny break, and falls smoothly toward 0 as the break grows. With exclude_current 0 the close cannot pass R,
    so it is 0 on every bar.
    Warm-up: period + exclude_current rows, bar t included.
    NaN: a NaN value in the window, a NaN close[t], or an R not above 0 gives NaN.
    Building raises for period < 2, source not "close"/"high", exclude_current not 0/1,
    form not "percent"/"proximity"/"break_proximity", power not above 0, extreme not "high"/"low".

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data): the close of
    bar t and the close (or high/low) of the last period + exclude_current rows.
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
        close = data["close"].astype(float)
        if self.source == "close":
            col = close
        else:
            col = data["high" if self.extreme == "high" else "low"].astype(float)
        n = len(data)
        stop = n - self.exclude_current
        start = stop - self.period
        win = col.iloc[start:stop]
        c = float(close.iloc[-1])
        if win.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        R = float(win.max()) if self.extreme == "high" else float(win.min())
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
                if c > R:
                    B = (c - R) / R * 100.0
                    value = (1.0 / (1.0 + B)) ** self.power
                else:
                    value = 0.0
            else:
                if c < R:
                    B = (R - c) / R * 100.0
                    value = (1.0 / (1.0 + B)) ** self.power
                else:
                    value = 0.0
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
        vals = closes
    elif extreme == "high":
        vals = [float(x) for x in list(df["high"])]
    else:
        vals = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    c = closes[t]
    # window: bars t-ex-period+1 .. t-ex
    window = []
    for k in range(period):
        window.append(vals[t - ex - k])
    for x in window:
        if x != x:
            return float("nan")
    if c != c:
        return float("nan")
    R = window[0]
    for x in window:
        if extreme == "high" and x > R:
            R = x
        if extreme == "low" and x < R:
            R = x
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
    # break_proximity: nearness of a close beyond the extreme to that extreme
    if extreme == "high":
        if not c > R:
            return 0.0
        b = (c - R) / R * 100.0
    else:
        if not c < R:
            return 0.0
        b = (R - c) / R * 100.0
    return (1.0 / (1.0 + b)) ** power
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
=== 1 failed, 210 passed, 1 skipped, 75 deselected, 1808 warnings in 39.00s ====


## attempt 2

answer: built
class: DistanceFromHighComponent
settings: {"period": 60, "source": "close", "exclude_current": 1, "form": "break_proximity"}
reason: `DistanceFromHighComponent` (`period` 60, `source` "close", `exclude_current` 1) already measures the close's percent distance from the prior 60-close high, but its "proximity" form is the nearness from below and reads 1 above the high. No config step gives the bounded nearness of a break above it that reads 0 below, so the class is rewritten with a new `form` value, "break_proximity", and its defaults keep today's output (the failing check named `RankWeightedScaledMoveComponent`, not this class).

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `extreme` ("high") | R = the highest (`extreme` "high") or lowest (`extreme` "low") value over the last `period` bars with bar t included (`exclude_current` 0), or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1). The values are those of `source`: "close" reads the close; "high" reads the bar's extreme on the `extreme` side (the `high` column for "high", the `low` column for "low"). `form` "percent": (close[t] - R) / R x 100. `form` "proximity": (1 / (1 + D))^`power`, where D = max(0, (R - close[t]) / R x 100) for "high" and max(0, (close[t] - R) / R x 100) for "low". `form` "break_proximity": (1 / (1 + B))^`power` when B > 0, else 0, where B = (close[t] - R) / R x 100 for "high" and (R - close[t]) / R x 100 for "low", the size of the break beyond the prior extreme in percent. With `period` 60, `source` "close", `exclude_current` 1 and "break_proximity": (1 / (1 + (close[t] - H) / H x 100))^`power` when close[t] > H = max(close[t-60 .. t-1]), else 0 | "high", "percent": `exclude_current` 0 gives 0 to -100, never positive; 1 gives -100 and up, signed. "low", "percent": `exclude_current` 0 gives 0 and up, never negative; 1 gives -100 and up, signed. "proximity": above 0, up to 1 (1 at the extreme or beyond it). "break_proximity": 0 to below 1, never negative, no direction; 0 at or inside the prior extreme, near 1 for a tiny break, falling smoothly toward 0 as the break grows; it jumps from near 1 to 0 where the close crosses back to R | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus `high` (or `low` with `extreme` "low") when `source` is "high". A NaN in the window, a NaN close[t], or an R not above 0 gives NaN. These settings raise when the component is built: `period` below 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `form` other than "percent", "proximity" or "break_proximity", `power` not above 0, `extreme` other than "high" or "low", and `form` "break_proximity" with `exclude_current` 0 (R then contains bar t's own value, so the output would be 0 on every bar) | stateless. `extreme` "high" and `form` "percent" (default) are the original output, unchanged. "break_proximity" is the nearness of a small break beyond the prior extreme, 0 without a break. It rises as the break gets smaller, and no config step gives this bounded form, hence the setting. With `extreme` "low" it is the nearness of a small break below the prior low. No `scaling_factor`: scale it with transforms |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    Distance of the close from the extreme of a window, on every bar.

        R = max (extreme "high") or min (extreme "low") of the source values over
            bars t-period+1 .. t (exclude_current 0) or t-period .. t-1 (exclude_current 1).
            source "close": the close; source "high": the high column (extreme "high")
            or the low column (extreme "low").
        form "percent" (default):  (close[t] - R) / R x 100
        form "proximity":          (1 / (1 + D))^power,
                                   D = max(0, (R - close[t]) / R x 100) for "high",
                                   D = max(0, (close[t] - R) / R x 100) for "low"
        form "break_proximity":    (1 / (1 + B))^power when B > 0, else 0,
                                   B = (close[t] - R) / R x 100 for "high",
                                   B = (R - close[t]) / R x 100 for "low"

    Range: "percent" with "high": 0 to -100 (exclude_current 0), -100 and up (1);
    with "low": 0 and up (0), -100 and up (1). "proximity": above 0, up to 1.
    "break_proximity": 0 to below 1, never negative, no direction. It is 0 at or inside the prior
    extreme, near 1 for a tiny break, and falls toward 0 as the break grows.
    Warm-up: period + exclude_current rows, bar t included.
    NaN: a NaN in the window, a NaN close[t], or an R not above 0 gives NaN.
    The defaults (form "percent", extreme "high") are the original output, unchanged.

    WHY THIS CANNOT LEAK: it reads only the close of bar t and the source column over the last
    period + exclude_current rows of data (bar t the last row); no later row is read.
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
        if self.form == "break_proximity" and self.exclude_current == 0:
            raise ValueError(
                "DistanceFromHighComponent: form 'break_proximity' needs exclude_current 1 "
                "(with bar t in the window there is never a break)")
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
        close_t = float(data["close"].astype(float).to_numpy()[-1])
        n = len(vals)
        stop = n - self.exclude_current
        window = vals[stop - self.period:stop]
        if np.isnan(window).any() or np.isnan(close_t):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        R = float(window.max()) if self.extreme == "high" else float(window.min())
        if not R > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.form == "percent":
            value = (close_t - R) / R * 100.0
        elif self.form == "proximity":
            if self.extreme == "high":
                D = max(0.0, (R - close_t) / R * 100.0)
            else:
                D = max(0.0, (close_t - R) / R * 100.0)
            value = (1.0 / (1.0 + D)) ** self.power
        else:
            if self.extreme == "high":
                B = (close_t - R) / R * 100.0
            else:
                B = (R - close_t) / R * 100.0
            value = (1.0 / (1.0 + B)) ** self.power if B > 0 else 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"reference": R, "close": close_t, "form": self.form, "extreme": self.extreme}

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
        src = closes
    elif extreme == "high":
        src = [float(x) for x in list(df["high"])]
    else:
        src = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    c = closes[t]
    if c != c:
        return float("nan")
    # window: bars t-period+1-ex .. t-ex
    win = []
    for k in range(period):
        x = src[t - ex - k]
        if x != x:
            return float("nan")
        win.append(x)
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
    # break_proximity: size of the break beyond the prior extreme
    if extreme == "high":
        b = (c - R) / R * 100.0
    else:
        b = (R - c) / R * 100.0
    if b <= 0:
        return 0.0
    return (1.0 / (1.0 + b)) ** power
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
=== 1 failed, 210 passed, 1 skipped, 75 deselected, 1808 warnings in 40.48s ====


## attempt 3

answer: built
class: DistanceFromHighComponent
settings: {"period": 60, "source": "close", "exclude_current": 1, "form": "break_proximity", "power": 1.0, "extreme": "high"}
reason: `DistanceFromHighComponent` already measures the close against the prior 60-close high, but no form turns the size of a break above that high into a proximity that is 0 without a break, so this adds a new value of its `form` setting, "break_proximity"; every default output is unchanged. The earlier failing check was `RankWeightedScaledMoveComponent`'s test, not this class.

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `extreme` ("high") | R = the highest (`extreme` "high") or lowest (`extreme` "low") value over the last `period` bars with bar t included (`exclude_current` 0), or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1). The values are those of `source`: "close" reads the close; "high" reads the bar's extreme on the `extreme` side (the `high` column for "high", the `low` column for "low"). `form` "percent": (close[t] - R) / R x 100. `form` "proximity": (1 / (1 + D))^`power`, where D = max(0, (R - close[t]) / R x 100) for "high" and max(0, (close[t] - R) / R x 100) for "low", the distance from the extreme in percent. `form` "break_proximity": (1 / (1 + D))^`power` when the close lies beyond R (close[t] > R for "high", close[t] < R for "low"), with D = (close[t] - R) / R x 100 for "high" and (R - close[t]) / R x 100 for "low", the size of the break in percent; 0 otherwise | "high", "percent": `exclude_current` 0 gives 0 to -100, never positive; 1 gives -100 and up, signed. "low", "percent": `exclude_current` 0 gives 0 and up, never negative; 1 gives -100 and up, signed. "proximity": above 0, up to 1 (1 at the extreme or beyond it). "break_proximity": 0 to 1, never negative, no direction; 0 when the close is not beyond R, near 1 for a tiny break, falling smoothly toward 0 as the break grows; it jumps from 0 to near 1 where the close crosses R. With `exclude_current` 0 it is 0 on every bar, because the close cannot lie beyond a window that includes bar t | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus `high` (or `low` with `extreme` "low") when `source` is "high". A NaN in the window, a NaN close[t], or an R not above 0 gives NaN. These settings raise when the component is built: `period` below 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `form` other than "percent", "proximity" or "break_proximity", `power` not above 0, `extreme` other than "high" or "low" | stateless. `form` "percent" and "proximity" and `extreme` "high" (the defaults) are the original outputs, unchanged. "break_proximity" with `period` 60, `exclude_current` 1 rates how small a fresh break above the prior 60-close high is: 1 at a break of zero size. No config step gives it (it is 0 off the break and decreasing in the break size), hence the setting. No `scaling_factor`: scale it with transforms |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    Distance of the close from the extreme of a window, on bar t:

        R = max (extreme "high") or min (extreme "low") of the source values over
            bars t-period+1 .. t (exclude_current 0) or t-period .. t-1 (exclude_current 1).
            source "close": closes; source "high": the high column (extreme "high") or the low column
            (extreme "low").
        form "percent":          (close[t] - R) / R x 100
        form "proximity":        (1 / (1 + D))^power,
                                 D = max(0, (R - close[t]) / R x 100) ("high"),
                                     max(0, (close[t] - R) / R x 100) ("low")
        form "break_proximity":  (1 / (1 + D))^power when the close is beyond R
                                 (close[t] > R for "high", close[t] < R for "low"),
                                 D = (close[t] - R) / R x 100 ("high"), (R - close[t]) / R x 100 ("low");
                                 0 otherwise.

    Range: "percent" signed (see the catalogue). "proximity" in (0, 1]. "break_proximity" in [0, 1],
    never negative: 0 without a break, near 1 for a tiny break, falling toward 0 as the break grows.
    With exclude_current 0, "break_proximity" is 0 on every bar.
    Warm-up: period + exclude_current rows, bar t included.
    NaN: a NaN in the window, a NaN close[t], or an R not above 0 gives NaN.

    WHY THIS CANNOT LEAK: it reads only the last period + exclude_current rows of data (bar t the last),
    the close of bar t and the source column of the window; nothing after bar t.
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
        n = len(data)
        ex = self.exclude_current
        if self.source == "close":
            col = "close"
        else:
            col = "high" if self.extreme == "high" else "low"
        vals = data[col].astype(float).iloc[n - self.period - ex:n - ex]
        c = float(data["close"].astype(float).iloc[-1])
        if vals.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        R = float(vals.max()) if self.extreme == "high" else float(vals.min())
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
                if c > R:
                    D = (c - R) / R * 100.0
                    value = (1.0 / (1.0 + D)) ** self.power
                else:
                    value = 0.0
            else:
                if c < R:
                    D = (R - c) / R * 100.0
                    value = (1.0 / (1.0 + D)) ** self.power
                else:
                    value = 0.0
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
        col = closes
    else:
        col = [float(x) for x in list(df["high" if extreme == "high" else "low"])]
    t = len(closes) - 1
    window = []
    for k in range(period):
        window.append(col[t - ex - k])
    c = closes[t]
    for x in window + [c]:
        if x != x:
            return float("nan")
    R = window[0]
    for x in window:
        if extreme == "high":
            if x > R:
                R = x
        else:
            if x < R:
                R = x
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
    # break_proximity
    if extreme == "high":
        if c > R:
            d = (c - R) / R * 100.0
            return (1.0 / (1.0 + d)) ** power
        return 0.0
    if c < R:
        d = (R - c) / R * 100.0
        return (1.0 / (1.0 + d)) ** power
    return 0.0
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
=== 1 failed, 210 passed, 1 skipped, 75 deselected, 1808 warnings in 39.25s ====

