# DistanceFromHighComponent: night_006_run | 006-05_downside-squeeze-break-continuation_1d | DistanceBelowPriorLow

## attempt 1

answer: built
class: DistanceFromHighComponent
settings: {"period": 20, "source": "low", "exclude_current": 1, "extreme": "min"}
reason: The wish is the percent distance of the close from a rolling extreme of the bars before t. `DistanceFromHighComponent` already computes that measure, but only against the highest value (and of `close` or `high` only), so the same measure against the lowest `low` is a new setting. A new `extreme` setting (default "max", which keeps today's output) and a `source` "low" give (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100.

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `extreme` ("max") | `form` "percent": (close[t] - E) / E x 100; `form` "proximity": (1 / (1 + D))^`power`, where D = max(0, (E - close[t]) / E x 100) with `extreme` "max" (the depth below the extreme) or D = max(0, (close[t] - E) / E x 100) with `extreme` "min" (the height above it). E is the highest (`extreme` "max") or lowest (`extreme` "min") `source` value (the `close`, `high` or `low` column), taken over the last `period` bars with bar t included (`exclude_current` 0) or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1). With `period` 20, `source` "low", `exclude_current` 1 and `extreme` "min": (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100 | "percent": -100 and up. With "max", `source` "close" or "high" and `exclude_current` 0 it is 0 to -100 and never positive. With "min", `source` "close" or "low" and `exclude_current` 0 it is 0 and up and never negative. With `exclude_current` 1 it is signed: with "min" it is negative and grows in size as the close falls further below the prior low, and positive above it. "proximity": above 0, up to 1, and 1 at or beyond the extreme | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus the `source` column. A NaN in the window, a NaN close[t], or an E not above 0 gives NaN. These settings raise when the component is built: `period` below 2, `source` other than "close", "high" or "low", `exclude_current` not 0 or 1, `form` other than "percent" or "proximity", `power` not above 0, `extreme` other than "max" or "min" | stateless. `extreme` "max" (the default) is the original output, unchanged. `period` 20, `source` "low", `exclude_current` 1, `extreme` "min" gives the distance of the close below the prior 20-bar low (a `clip` with `max` 0 keeps only the break). No `scaling_factor`: scale it with transforms. |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    Percent distance of the close from a rolling extreme of a bar column, on every bar:

        window = src[t - period + 1 .. t]    (exclude_current 0, default: bar t included)
        window = src[t - period .. t - 1]    (exclude_current 1: bar t excluded)
        src = the `source` column: "close" (default), "high" or "low"
        E = max(window)  (extreme "max", default)   or   min(window)  (extreme "min")
        form "percent" (default):  raw_value = (close[t] - E) / E x 100
        form "proximity":          raw_value = (1 / (1 + D)) ** power, with
                                   D = max(0, (E - close[t]) / E x 100)  for extreme "max"
                                   D = max(0, (close[t] - E) / E x 100)  for extreme "min"

    The defaults (extreme "max") give the original output, unchanged. With period 20, source "low",
    exclude_current 1 and extreme "min" the value is (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100:
    negative and growing in size as the close falls further below the prior 20-bar low, positive above it.

    Range and sign: "percent" is -100 and up. With "max" and exclude_current 0 (source close or high) it is
    0 to -100, never positive. With "min" and exclude_current 0 (source close or low) it is 0 and up.
    With exclude_current 1 it is signed. "proximity" is above 0, up to 1: it equals 1 at or beyond the extreme
    and gets smaller the further the close is from it. Graded.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column and the `source` column of the last
    period + exclude_current rows of data, the last row being bar t. Every value it reads is known at bar t's close.

    NaN: a NaN in the window or a NaN close[t] gives NaN, and so does an E that is not above 0.
    Building the component raises for: a period below 2; a source other than "close", "high" or "low";
    an exclude_current other than 0 or 1; a form other than "percent" or "proximity"; a power that is not above 0;
    an extreme other than "max" or "min".
    """

    def __init__(self, name="DistanceFromHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 60))
        if self.period < 2:
            raise ValueError(f"DistanceFromHighComponent: period must be >= 2, got {self.period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high", "low"):
            raise ValueError(f"DistanceFromHighComponent: source must be 'close', 'high' or 'low', got {self.source!r}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"DistanceFromHighComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.form = self.parameters.get("form", "percent")
        if self.form not in ("percent", "proximity"):
            raise ValueError(f"DistanceFromHighComponent: form must be 'percent' or 'proximity', got {self.form!r}")
        self.power = float(self.parameters.get("power", 1.0))
        if not self.power > 0:
            raise ValueError(f"DistanceFromHighComponent: power must be > 0, got {self.power}")
        self.extreme = self.parameters.get("extreme", "max")
        if self.extreme not in ("max", "min"):
            raise ValueError(f"DistanceFromHighComponent: extreme must be 'max' or 'min', got {self.extreme!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float)
        src = data[self.source].astype(float)
        c = float(close.iloc[-1])
        if self.exclude_current:
            window = src.iloc[-(self.period + 1):-1]
        else:
            window = src.iloc[-self.period:]
        if window.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        e = float(window.max()) if self.extreme == "max" else float(window.min())
        if not e > 0:
            self._raw_value = float("nan")
        elif self.form == "percent":
            self._raw_value = float((c - e) / e * 100.0)
        else:
            if self.extreme == "max":
                d = max(0.0, (e - c) / e * 100.0)
            else:
                d = max(0.0, (c - e) / e * 100.0)
            self._raw_value = float((1.0 / (1.0 + d)) ** self.power)
        self.confidence = 1.0
        self.debug_info = {'extreme_value': e, 'extreme': self.extreme, 'source': self.source}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    n = int(params.get("period", 60))
    source = params.get("source", "close")
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "percent")
    power = float(params.get("power", 1.0))
    extreme = params.get("extreme", "max")
    closes = [float(x) for x in list(df["close"])]
    vals = [float(x) for x in list(df[source])]
    last = len(closes) - 1
    c = closes[last]
    if ex == 1:
        start = last - n
        stop = last - 1
    else:
        start = last - n + 1
        stop = last
    window = []
    i = start
    while i <= stop:
        window.append(vals[i])
        i = i + 1
    if c != c:
        return float("nan")
    for x in window:
        if x != x:
            return float("nan")
    e = window[0]
    for x in window:
        if extreme == "max":
            if x > e:
                e = x
        else:
            if x < e:
                e = x
    if not e > 0:
        return float("nan")
    if form == "percent":
        return (c - e) / e * 100.0
    if extreme == "max":
        d = (e - c) / e * 100.0
    else:
        d = (c - e) / e * 100.0
    if d < 0:
        d = 0.0
    return (1.0 / (1.0 + d)) ** power
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 261, in <module>
    main()
    ~~~~^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 251, in main
    fails += check_new_setting(old, cls, spec.SETTINGS[-1], old_params(old_text, spec.CLASS))
             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 196, in check_new_setting
    a, b = values_on(old_cls, base, d), values_on(new_cls, params, d)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 152, in values_on
    c = cls(parameters=dict(params))
  File "old_strategy_components.py", line 1888, in __init__
ValueError: DistanceFromHighComponent: source must be 'close' or 'high', got 'low'

## attempt 2

answer: built
class: DistanceFromHighComponent
settings: {"period": 20, "source": "high", "exclude_current": 1, "form": "percent", "extreme": "low"}
reason: The percent distance of the close from the lowest low of the prior 20 bars is the measure `DistanceFromHighComponent` already computes, taken against the window's minimum instead of its maximum. The class lacks only that choice, so I rebuilt it with one new setting, `extreme` ("high" by default, which keeps today's output exactly; "low" uses the lowest value, and `source` "high" then reads the bar's own extreme on that side, the `low` column). Every setting the old class knows still takes a value it accepts.

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `extreme` ("high") | R = the highest (`extreme` "high") or lowest (`extreme` "low") value over the last `period` bars with bar t included (`exclude_current` 0), or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1). The values are those of `source`: "close" reads the close; "high" reads the bar's extreme on the `extreme` side (the `high` column for "high", the `low` column for "low"). `form` "percent": (close[t] - R) / R x 100. `form` "proximity": (1 / (1 + D))^`power`, where D = max(0, (R - close[t]) / R x 100) for "high" and max(0, (close[t] - R) / R x 100) for "low", the distance from the extreme in percent. With `period` 20, `source` "high", `exclude_current` 1 and `extreme` "low", the output is (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100 | "high", "percent": `exclude_current` 0 gives 0 to -100, never positive; 1 gives -100 and up, signed. "low", "percent": `exclude_current` 0 gives 0 and up, never negative; 1 gives -100 and up, signed: negative and larger in size the further the close sits below the prior low, positive above it. "proximity": above 0, up to 1 (1 at the extreme or beyond it) | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus `high` (or `low` with `extreme` "low") when `source` is "high". A NaN in the window, a NaN close[t], or an R not above 0 gives NaN. These settings raise when the component is built: `period` below 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `form` other than "percent" or "proximity", `power` not above 0, `extreme` other than "high" or "low" | stateless. `extreme` "high" (default) is the original output, unchanged. `extreme` "low" with `period` 20, `source` "high" and `exclude_current` 1 gives the distance of the close below the prior 20-bar low; a `clip` with `max` 0 keeps only the break. No `scaling_factor`: scale it with transforms |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    The close's percent distance from the extreme of a recent window, on every bar:

        W = the last `period` rows, bar t included (exclude_current 0),
            or rows t-period .. t-1, bar t excluded (exclude_current 1)
        column: "close" with source "close"; with source "high", the bar's extreme on the
                `extreme` side: the `high` column (extreme "high") or the `low` column (extreme "low")
        R = max(column over W) with extreme "high" (default), min(column over W) with extreme "low"
        form "percent" (default):  raw_value = (close[t] - R) / R x 100
        form "proximity":          raw_value = (1 / (1 + D)) ** power,
                                   D = max(0, (R - close[t]) / R x 100)  (extreme "high")
                                   D = max(0, (close[t] - R) / R x 100)  (extreme "low")

    The defaults (extreme "high") give the original output, unchanged. With period 20, source "high",
    exclude_current 1 and extreme "low", the output is
    (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100.

    Range and sign: graded. "high", "percent": 0 to -100 with exclude_current 0; -100 and up, signed,
    with exclude_current 1. "low", "percent": 0 and up with exclude_current 0 (the close is never below
    its own bar's low); -100 and up, signed, with exclude_current 1: negative and larger in size the
    further the close falls below the prior low. "proximity": above 0, up to 1.
    Warm-up: period + exclude_current rows, bar t included.

    NaN: a NaN in the window, a NaN close[t], or an R not above 0 gives NaN. Building the component
    raises for a period below 2, a source other than "close" or "high", an exclude_current other than
    0 or 1, a form other than "percent" or "proximity", a power not above 0, or an extreme other than
    "high" or "low".

    WHY THIS CANNOT LEAK: it reads only the close of the last row (bar t) and the close, high or low of
    the last period + exclude_current rows, all known at bar t's close; no later row is read.
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
        if ex not in (0, 1):
            raise ValueError(f"DistanceFromHighComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.form = self.parameters.get("form", "percent")
        if self.form not in ("percent", "proximity"):
            raise ValueError(f"DistanceFromHighComponent: form must be 'percent' or 'proximity', got {self.form!r}")
        self.power = float(self.parameters.get("power", 1.0))
        if not self.power > 0:
            raise ValueError(f"DistanceFromHighComponent: power must be above 0, got {self.power}")
        self.extreme = self.parameters.get("extreme", "high")
        if self.extreme not in ("high", "low"):
            raise ValueError(f"DistanceFromHighComponent: extreme must be 'high' or 'low', got {self.extreme!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        col = "close" if self.source == "close" else self.extreme
        values = data[col].astype(float)
        if self.exclude_current:
            win = values.iloc[-(self.period + 1):-1]
        else:
            win = values.iloc[-self.period:]
        c = float(data["close"].astype(float).iloc[-1])
        if win.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        ref = float(win.max()) if self.extreme == "high" else float(win.min())
        if not ref > 0:
            self._raw_value = float("nan")
        elif self.form == "percent":
            self._raw_value = float((c - ref) / ref * 100.0)
        else:
            if self.extreme == "high":
                d = max(0.0, (ref - c) / ref * 100.0)
            else:
                d = max(0.0, (c - ref) / ref * 100.0)
            self._raw_value = float((1.0 / (1.0 + d)) ** self.power)
        self.confidence = 1.0
        self.debug_info = {'reference': ref, 'extreme': self.extreme, 'column': col}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    n = int(params.get("period", 60))
    source = params.get("source", "close")
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "percent")
    power = float(params.get("power", 1.0))
    extreme = params.get("extreme", "high")
    closes = [float(x) for x in list(df["close"])]
    if source == "close":
        vals = closes
    elif extreme == "low":
        vals = [float(x) for x in list(df["low"])]
    else:
        vals = [float(x) for x in list(df["high"])]
    last = len(closes) - 1
    if ex == 1:
        first, stop = last - n, last - 1
    else:
        first, stop = last - n + 1, last
    window = []
    i = first
    while i <= stop:
        window.append(vals[i])
        i = i + 1
    c = closes[last]
    if c != c:
        return float("nan")
    for x in window:
        if x != x:
            return float("nan")
    ref = window[0]
    for x in window:
        if extreme == "low":
            if x < ref:
                ref = x
        else:
            if x > ref:
                ref = x
    if not ref > 0:
        return float("nan")
    if form == "percent":
        return (c - ref) / ref * 100.0
    if extreme == "low":
        dist = (c - ref) / ref * 100.0
    else:
        dist = (ref - c) / ref * 100.0
    if dist < 0:
        dist = 0.0
    return (1.0 / (1.0 + dist)) ** power
```

checks:
DistanceFromHighComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1536 passed, 8 skipped, 74 deselected, 2170 warnings in 56.76s ========
