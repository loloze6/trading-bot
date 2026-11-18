# not built: night_006_run | 006-05_downside-squeeze-break-continuation_1d | DistanceBelowPriorLow

## attempt 1

answer: built
class: DistanceFromHighComponent
settings: {"period": 20, "source": "low", "exclude_current": 1, "form": "percent", "extreme": "low"}
reason: The wish is the percent distance of the close from an extreme of a past window. `DistanceFromHighComponent` already computes this measure, but only against the highest value of a `close` or `high` window. Taking the lowest `low` instead is the same measure on another base and statistic. So this is that whole class again with a new value "low" for `source` and a new setting `extreme` ("high" default, "low"), and the defaults keep today's output exactly.
table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `extreme` ("high") | E is the highest (`extreme` "high") or lowest (`extreme` "low") `source` value (the `close`, `high` or `low` column) over the last `period` bars with bar t included (`exclude_current` 0), or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1). `form` "percent": (close[t] - E) / E x 100. `form` "proximity": (1 / (1 + D))^`power`, where D is the distance from E toward the inside of the range in percent: D = max(0, (E - close[t]) / E x 100) for "high" and D = max(0, (close[t] - E) / E x 100) for "low". With `period` 20, `source` "low", `exclude_current` 1 and `extreme` "low": (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100 | "percent", "high", `exclude_current` 0: 0 to -100, never positive. "percent", "high", `exclude_current` 1: -100 and up, signed. "percent", "low", `exclude_current` 0 with `source` "close" or "low": 0 and up, never negative. "percent", "low", `exclude_current` 1: -100 and up, signed; negative and growing in size as the close falls further below the prior low, positive above it. "proximity": above 0, up to 1, with 1 at or beyond the extreme | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus `high` or `low` per `source`. A NaN in the window or a NaN close[t] gives NaN, and so does an E not above 0. These settings raise when the component is built: `period` below 2, `source` other than "close", "high" or "low", `exclude_current` not 0 or 1, `form` other than "percent" or "proximity", `power` not above 0, `extreme` other than "high" or "low" | stateless. `extreme` "high" (the default) is the original output, unchanged. With `period` 20, `source` "low", `exclude_current` 1 and `extreme` "low" it is the distance of the close below the prior 20-bar low; a `clip` with `max` 0 keeps only the break. No `scaling_factor`: scale it with transforms. |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    The close's percent distance from an extreme of a window, on every bar:

        exclude_current = 0 (default): W = source[t - period + 1 .. t]   (bar t included)
        exclude_current = 1:           W = source[t - period .. t - 1]   (bar t excluded)
        extreme = "high" (default): E = max(W);   extreme = "low": E = min(W)
        form = "percent" (default):  raw_value = (close[t] - E) / E x 100
        form = "proximity":          raw_value = (1 / (1 + D)) ** power,
            D = max(0, (E - close[t]) / E x 100)  for extreme "high"
            D = max(0, (close[t] - E) / E x 100)  for extreme "low"

    source is the column of W: "close" (default), "high" or "low". The defaults (extreme "high") give the original
    output, unchanged. With period 20, source "low", exclude_current 1, extreme "low": the percent distance of the
    close from the lowest low of the prior 20 bars, negative and growing in size the further the close falls below it.
    Graded. Range: "percent" with "high" and exclude_current 0 is 0 to -100. With "low", exclude_current 0 and a
    source of "close" or "low" it is 0 and up. With exclude_current 1 it is -100 and up, signed. "proximity" is above
    0, up to 1.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only `close` of bar t (the last row) and the `source` column of at most the last
    period + exclude_current rows, all ending at bar t; every value is known at bar t's close.

    NaN: a NaN in the window or a NaN close[t] gives NaN; an E not above 0 gives NaN.
    Building the component raises for a period below 2, a source other than "close", "high" or "low", an
    exclude_current other than 0 or 1, a form other than "percent" or "proximity", a power not above 0, or an extreme
    other than "high" or "low".
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
        src = data[self.source].astype(float)
        if self.exclude_current:
            window = src.iloc[-(self.period + 1):-1]
        else:
            window = src.iloc[-self.period:]
        close_t = float(data['close'].astype(float).iloc[-1])
        if window.isna().any() or np.isnan(close_t):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        ref = float(window.max()) if self.extreme == "high" else float(window.min())
        if not ref > 0:
            self._raw_value = float("nan")
        elif self.form == "percent":
            self._raw_value = float((close_t - ref) / ref * 100.0)
        else:
            if self.extreme == "high":
                depth = (ref - close_t) / ref * 100.0
            else:
                depth = (close_t - ref) / ref * 100.0
            d = max(0.0, depth)
            self._raw_value = float((1.0 / (1.0 + d)) ** self.power)
        self.confidence = 1.0
        self.debug_info = {'extreme_value': ref, 'close': close_t, 'extreme': self.extreme}

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
    col = [float(x) for x in list(df[source])]
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    c = closes[last]
    if ex == 1:
        first, end = last - n, last - 1
    else:
        first, end = last - n + 1, last
    vals = []
    i = first
    while i <= end:
        vals.append(col[i])
        i = i + 1
    for x in vals:
        if x != x:
            return float("nan")
    if c != c:
        return float("nan")
    ref = vals[0]
    for x in vals:
        if extreme == "high":
            if x > ref:
                ref = x
        else:
            if x < ref:
                ref = x
    if not ref > 0:
        return float("nan")
    if form == "percent":
        return (c - ref) / ref * 100.0
    if extreme == "high":
        depth = (ref - c) / ref * 100.0
    else:
        depth = (c - ref) / ref * 100.0
    if depth < 0:
        depth = 0.0
    return (1.0 / (1.0 + depth)) ** power
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 36, in <module>
    import strategies.strategy_components as SC  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/strategies/strategy_components.py", line 1927
    self._raw_value = float((1.0 / (1.0 + d))  self.power)
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?

## attempt 2

answer: built
class: DistanceFromHighComponent
settings: {"period": 20, "source": "low", "exclude_current": 1, "extreme": "low"}
reason: The wished quantity is the measure `DistanceFromHighComponent` already computes, the percent distance of the close from a recent price extreme, but measured against the lowest low instead of the highest high, so by rule 1 it is the same component with the extreme as a setting. That class has no setting for it. It is rewritten whole with a new `extreme` setting (default "high", which keeps today's output exactly) and a third `source` value, "low".

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `extreme` ("high") | E is the highest (`extreme` "high") or lowest (`extreme` "low") `source` value (the `close`, `high` or `low` column) over the last `period` bars with bar t included (`exclude_current` 0), or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1). `form` "percent": (close[t] - E) / E x 100. `form` "proximity": (1 / (1 + D))^`power`, D being the percent distance of the close beyond E on the side away from the extreme: max(0, (E - close[t]) / E x 100) for "high", max(0, (close[t] - E) / E x 100) for "low". With `period` 20, `source` "low", `exclude_current` 1, `extreme` "low": (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100 | "percent", "high", `exclude_current` 0: 0 to -100, never positive. "high", `exclude_current` 1: -100 and up, signed, positive above the prior high. "low", `exclude_current` 0 with `source` "close": 0 and up, never negative. "low", `exclude_current` 1: -100 and up, signed, negative and growing in size as the close falls further below the prior low. "proximity": above 0, up to 1 (1 at or beyond the extreme) | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus `high` or `low` with that `source`. A NaN in the window or a NaN close[t] gives NaN, and so does an E not above 0. These settings raise when the component is built: `period` below 2, `source` other than "close", "high" or "low", `exclude_current` not 0 or 1, `form` other than "percent" or "proximity", `power` not above 0, `extreme` other than "high" or "low" | stateless. `extreme` "high" (the default) is the original output, unchanged. With `period` 20, `source` "low", `exclude_current` 1 and `extreme` "low" it is the distance of the close below the prior 20-bar low (a `clip` with `max` 0 keeps only the break). `form` "proximity" with `period` 365 and `power` 2.0 is the convex nearness to the yearly high. No `scaling_factor`: scale it with transforms. |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    Distance of the close from a recent price extreme, on every bar:

        W = source[t - period + 1 .. t]   (exclude_current 0, bar t included)
        W = source[t - period .. t - 1]   (exclude_current 1, bar t excluded)
        E = max(W) (extreme "high", default) or min(W) (extreme "low")
        form "percent" (default):  raw_value = (close[t] - E) / E x 100
        form "proximity":          raw_value = (1 / (1 + D)) to the power `power`, where
                                   D = max(0, (E - close[t]) / E x 100) for extreme "high",
                                   D = max(0, (close[t] - E) / E x 100) for extreme "low"

    source is the `close`, `high` or `low` column. The default extreme "high" gives the original output, unchanged.
    With period 20, source "low", exclude_current 1 and extreme "low" the value is
    (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100: negative and growing in size as the close falls
    further below the prior 20-bar low.
    Range: "percent" with extreme "high" and exclude_current 0: 0 to -100, never positive. With exclude_current 1:
    -100 and up, signed. "percent" with extreme "low": 0 and up when the close is in the window (source "close",
    exclude_current 0); -100 and up, signed, with exclude_current 1. "proximity": above 0, up to 1. Graded.
    Warm-up: period + exclude_current rows, bar t included.

    NaN: a NaN in the window or a NaN close[t] gives NaN; an E not above 0 gives NaN. A missing column raises.
    Building the component raises for a period below 2, a source other than "close", "high" or "low", an
    exclude_current other than 0 or 1, a form other than "percent" or "proximity", a power not above 0, or an
    extreme other than "high" or "low".

    WHY THIS CANNOT LEAK: it reads only the `close` column of bar t and the `source` column of at most the last
    period + exclude_current rows of data, all at or before bar t (the last row); each is known at that bar's close.
    """

    def __init__(self, name="DistanceFromHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 60))
        if self.period < 2:
            raise ValueError(f"DistanceFromHighComponent: period must be >= 2, got {self.period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high", "low"):
            raise ValueError(
                f"DistanceFromHighComponent: source must be 'close', 'high' or 'low', got {self.source!r}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"DistanceFromHighComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.form = self.parameters.get("form", "percent")
        if self.form not in ("percent", "proximity"):
            raise ValueError(
                f"DistanceFromHighComponent: form must be 'percent' or 'proximity', got {self.form!r}")
        self.power = float(self.parameters.get("power", 1.0))
        if not self.power > 0:
            raise ValueError(f"DistanceFromHighComponent: power must be above 0, got {self.power}")
        self.extreme = self.parameters.get("extreme", "high")
        if self.extreme not in ("high", "low"):
            raise ValueError(
                f"DistanceFromHighComponent: extreme must be 'high' or 'low', got {self.extreme!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        src = data[self.source].astype(float)
        if self.exclude_current:
            win = src.iloc[-(self.period + 1):-1]
        else:
            win = src.iloc[-self.period:]
        c = float(data['close'].astype(float).iloc[-1])
        if win.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.extreme == "high":
            ref = float(win.max())
        else:
            ref = float(win.min())
        if not ref > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.form == "percent":
            self._raw_value = float((c - ref) / ref * 100.0)
        else:
            if self.extreme == "high":
                d = max(0.0, (ref - c) / ref * 100.0)
            else:
                d = max(0.0, (c - ref) / ref * 100.0)
            self._raw_value = float(np.power(1.0 / (1.0 + d), self.power))
        self.confidence = 1.0
        self.debug_info = {'extreme_value': ref, 'close': c, 'extreme': self.extreme}

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
    p = float(params.get("power", 1.0))
    extreme = params.get("extreme", "high")
    col = [float(x) for x in list(df[source])]
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    c = closes[last]
    if ex == 1:
        first = last - n
        end = last - 1
    else:
        first = last - n + 1
        end = last
    window = []
    i = first
    while i <= end:
        window.append(col[i])
        i = i + 1
    if c != c:
        return float("nan")
    for x in window:
        if x != x:
            return float("nan")
    ref = window[0]
    for x in window:
        if extreme == "high":
            if x > ref:
                ref = x
        else:
            if x < ref:
                ref = x
    if not ref > 0:
        return float("nan")
    if form == "percent":
        return (c - ref) / ref * 100.0
    if extreme == "high":
        depth = (ref - c) / ref * 100.0
    else:
        depth = (c - ref) / ref * 100.0
    if depth < 0.0:
        depth = 0.0
    return pow(1.0 / (1.0 + depth), p)
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

## attempt 3

answer: built
class: DistanceFromHighComponent
settings: {"period": 20, "source": "high", "exclude_current": 1, "form": "percent", "side": "low"}
reason: The wish is the distance of the close from the extreme of the prior 20 bars. `DistanceFromHighComponent` already measures this distance, but only against the highest value, and it accepts only the `close` and `high` columns. Passing `source` "low" fails on today's class, as the checks showed. So the class is rewritten with one new setting, `side`, which picks the highest (default, today's output unchanged) or the lowest of the window. With `side` "low", `source` "high" reads the bar's extreme on that side, which is the `low` column.

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0), `form` ("percent"), `power` (1.0), `side` ("high") | `form` "percent": (close[t] - H) / H x 100; `form` "proximity": (1 / (1 + D))^`power`, where D is the distance of the close from H in percent on the far side of H: max(0, (H - close[t]) / H x 100) for `side` "high" and max(0, (close[t] - H) / H x 100) for `side` "low". H is the extreme of the last `period` bars, bar t included (`exclude_current` 0), or of bars t-`period` .. t-1, bar t excluded (`exclude_current` 1). With `side` "high", H is the highest value of the `close` column (`source` "close") or of the `high` column (`source` "high"). With `side` "low", H is the lowest value of the `close` column (`source` "close") or of the `low` column (`source` "high": the bar's extreme on that side). With `period` 20, `source` "high", `exclude_current` 1 and `side` "low", the output is (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100 | "percent", `side` "high": `exclude_current` 0 gives 0 to -100, never positive; `exclude_current` 1 gives -100 and up, signed. "percent", `side` "low": `exclude_current` 0 gives 0 and up, never negative; `exclude_current` 1 gives -100 and up, signed, negative and growing in size as the close falls further below the prior low. "proximity": above 0, up to 1 (1 at or beyond the extreme) | graded | percent, or a proximity 0 to 1 | `period` + `exclude_current` (60) | `close`, plus `high` (`side` "high") or `low` (`side` "low") with `source` "high". A NaN in the window or a NaN close[t] gives NaN, and so does an H not above 0. These settings raise when the engine starts: `period` below 2, `source` other than "close" or "high", `exclude_current` not 0 or 1, `form` other than "percent" or "proximity", `power` not above 0, `side` other than "high" or "low" | stateless. `side` "high" (default) is the original output, unchanged. With `side` "low", `source` "high" means the bar's low (the bar's extreme on the chosen side), not the high column. `period` 20, `source` "high", `exclude_current` 1, `side` "low" gives the distance of the close below the prior 20-bar low (a `clip` with `max` 0 keeps only the break). No `scaling_factor`: scale it with transforms. |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    Percent distance of the close from the extreme of a recent window, on every bar:

        side = "high" (default): H = highest of the window
        side = "low":            H = lowest of the window
        the window is the column read over bars t-period+1 .. t (exclude_current 0)
        or bars t-period .. t-1 (exclude_current 1)
        column: source "close" -> close; source "high" -> the bar's extreme on the side:
                high for side "high", low for side "low"
        form = "percent" (default): raw_value = (close[t] - H) / H x 100
        form = "proximity":         raw_value = (1 / (1 + D)) ** power,
                                    D = max(0, (H - close[t]) / H x 100) for side "high",
                                    D = max(0, (close[t] - H) / H x 100) for side "low"

    side "high" is the original output, unchanged. With period 20, source "high", exclude_current 1
    and side "low" the output is (close[t] - min(low[t-20..t-1])) / min(low[t-20..t-1]) x 100: negative
    and growing in size as the close falls further below the prior 20-bar low.

    Range and sign: "percent", side "high": 0 to -100 (exclude_current 0), -100 and up (exclude_current 1).
    "percent", side "low": 0 and up (exclude_current 0), -100 and up, signed (exclude_current 1).
    "proximity": above 0, up to 1. Graded.
    Warm-up: period + exclude_current rows, bar t included.

    NaN: a NaN in the window or a NaN close[t] gives NaN, and so does an H not above 0.
    Building it raises for period < 2, source not "close"/"high", exclude_current not 0/1,
    form not "percent"/"proximity", power not above 0, side not "high"/"low".

    WHY THIS CANNOT LEAK: it reads only the close of bar t and the close, high or low of the last
    period + exclude_current rows, all at or before bar t (the last row of data).
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
        self.side = self.parameters.get("side", "high")
        if self.side not in ("high", "low"):
            raise ValueError(f"DistanceFromHighComponent: side must be 'high' or 'low', got {self.side!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float)
        if self.source == "close":
            col = close
        else:
            col = data['high' if self.side == "high" else 'low'].astype(float)
        n = self.period
        if self.exclude_current:
            w = col.iloc[-(n + 1):-1]
        else:
            w = col.iloc[-n:]
        c = float(close.iloc[-1])
        if w.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
        else:
            H = float(w.max()) if self.side == "high" else float(w.min())
            if not H > 0:
                self._raw_value = float("nan")
            elif self.form == "percent":
                self._raw_value = float((c - H) / H * 100.0)
            else:
                if self.side == "high":
                    D = max(0.0, (H - c) / H * 100.0)
                else:
                    D = max(0.0, (c - H) / H * 100.0)
                self._raw_value = float((1.0 / (1.0 + D)) ** self.power)
            self.debug_info = {'extreme': H, 'side': self.side}
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    n = int(params.get("period", 60))
    src = params.get("source", "close")
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "percent")
    power = float(params.get("power", 1.0))
    side = params.get("side", "high")
    closes = [float(x) for x in list(df["close"])]
    if src == "close":
        vals = closes
    elif side == "high":
        vals = [float(x) for x in list(df["high"])]
    else:
        vals = [float(x) for x in list(df["low"])]
    last = len(closes) - 1
    if ex == 1:
        lo, hi = last - n, last - 1
    else:
        lo, hi = last - n + 1, last
    window = []
    i = lo
    while i <= hi:
        window.append(vals[i])
        i = i + 1
    c = closes[last]
    if c != c:
        return float("nan")
    for x in window:
        if x != x:
            return float("nan")
    H = window[0]
    for x in window:
        if side == "high":
            if x > H:
                H = x
        else:
            if x < H:
                H = x
    if not H > 0:
        return float("nan")
    if form == "percent":
        return (c - H) / H * 100.0
    if side == "high":
        d = (H - c) / H * 100.0
    else:
        d = (c - H) / H * 100.0
    if d < 0:
        d = 0.0
    return (1.0 / (1.0 + d)) ** power
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 36, in <module>
    import strategies.strategy_components as SC  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/strategies/strategy_components.py", line 1933
    self._raw_value = float((1.0 / (1.0 + D))  self.power)
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?
