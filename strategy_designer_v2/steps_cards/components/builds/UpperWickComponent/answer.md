# UpperWickComponent: night10_fallagishort_run | 086-01_upper-shadow-further-fall_1d | UpperWickInMeanRangesComponent

## attempt 1

answer: built
class: LowerWickComponent
settings: {"side": "upper", "relative_to": "mean_range", "base_period": 30, "exclude_current": 0}
reason: `LowerWickComponent` already measures a bar's wick against a base, but it has no upper shadow and no mean-bar-range base. The upper wick is that measure's mirror, which no config step gives, so it becomes a `side` setting. The mean bar range is a new value of the existing `relative_to` setting, with `base_period` and `exclude_current` for its window. The defaults keep today's output exactly.

table: Hedges and filters
row: | `LowerWickComponent` | `relative_to` ("range"), `side` ("lower"), `base_period` (30), `exclude_current` (0) | W = min(open[t], close[t]) − low[t] (`side` "lower") or high[t] − max(open[t], close[t]) (`side` "upper"). `relative_to` "range": W / (high[t] − low[t]), 0 when the range is 0. "close": W / close[t] x 100. "mean_range": W / B, where B = mean(high[i] − low[i]) over i = t-`base_period`+1 .. t (`exclude_current` 0, bar t included) or i = t-`base_period` .. t-1 (`exclude_current` 1); 0.0 when B = 0. With `side` "upper", "mean_range", `base_period` 30, `exclude_current` 0: (high[t] − max(open[t], close[t])) / mean(high[i] − low[i], i = t-29 .. t) | "range": 0 to 1. "close": 0 and up. "mean_range": 0 and up; at most `base_period` with `exclude_current` 0 (the mean includes bar t's range), unbounded with 1. Never negative; no direction. 0 for no shadow on the chosen side, growing linearly as it lengthens | graded | "range": share of the bar's range. "close": percent. "mean_range": mean bar ranges | 1 with "range" or "close"; `base_period` + `exclude_current` with "mean_range" (30 at the wished settings) | open, high, low, close of bar t; with "mean_range" also high and low of the base rows. A NaN in any value read gives NaN. A close not above 0 with "close" gives NaN (never on real bars). B = 0 gives 0.0 (never on real bars). These settings raise when the component is built: `relative_to` other than "range", "close" or "mean_range"; `side` other than "lower" or "upper"; `base_period` not an integer >= 1; `exclude_current` not 0 or 1 | stateless. `side` "lower" with `relative_to` "range" or "close" is the original output, unchanged. "upper" is the upper shadow, the mirror, which no config step gives, hence the setting. `base_period` and `exclude_current` are read only by "mean_range". On 1d bars the wished settings give the day's upper shadow in 30-day mean daily ranges. Continuous in the prices. No `scaling_factor`: scale it with transforms |

```python class
class LowerWickComponent(SubStrategyComponent):
    """
    The length of one of bar t's wicks, against a base, on every bar:

        side = "lower" (default): W = min(open[t], close[t]) - low[t]
        side = "upper":           W = high[t] - max(open[t], close[t])
        relative_to = "range" (default): raw_value = W / (high[t] - low[t]), 0.0 when high[t] = low[t]
        relative_to = "close":           raw_value = W / close[t] x 100
        relative_to = "mean_range":      raw_value = W / B, B = mean(high[i] - low[i]) over
                                         i = t-base_period+1 .. t   (exclude_current 0, bar t included)
                                         i = t-base_period .. t-1   (exclude_current 1, bar t excluded)
                                         0.0 when B = 0

    side "lower" with relative_to "range" or "close" is the original output, unchanged.
    Range: never negative, no direction. "range" is 0 to 1. "close" is 0 and up. "mean_range" is 0 and up,
    at most base_period with exclude_current 0, unbounded with 1. It is 0 for no wick on the chosen side and
    grows linearly with the wick.
    Warm-up: 1 row with "range" or "close"; base_period + exclude_current rows with "mean_range".

    WHY THIS CANNOT LEAK: it reads open, high, low and close of the last row (bar t) and, with "mean_range",
    the high and low of at most the last base_period + exclude_current rows, all up to and including bar t.

    NaN: a NaN in any value read gives NaN. A close not above 0 with "close" gives NaN (never on real bars).
    B = 0 gives 0.0 (never on real bars).
    Building the component raises for a relative_to other than "range", "close" or "mean_range", a side other
    than "lower" or "upper", a base_period that is not an integer >= 1, or an exclude_current other than 0 or 1.
    """

    def __init__(self, name="LowerWick", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.relative_to = self.parameters.get("relative_to", "range")
        if self.relative_to not in ("range", "close", "mean_range"):
            raise ValueError(
                f"LowerWickComponent: relative_to must be 'range', 'close' or 'mean_range', got {self.relative_to!r}")
        self.side = self.parameters.get("side", "lower")
        if self.side not in ("lower", "upper"):
            raise ValueError(f"LowerWickComponent: side must be 'lower' or 'upper', got {self.side!r}")
        bp = self.parameters.get("base_period", 30)
        if isinstance(bp, bool):
            raise ValueError(f"LowerWickComponent: base_period must be an integer >= 1, got {bp!r}")
        try:
            bp_int = int(bp)
        except (TypeError, ValueError):
            raise ValueError(f"LowerWickComponent: base_period must be an integer >= 1, got {bp!r}")
        if bp_int != bp or bp_int < 1:
            raise ValueError(f"LowerWickComponent: base_period must be an integer >= 1, got {bp!r}")
        self.base_period = bp_int
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"LowerWickComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        o = float(data['open'].iloc[-1])
        h = float(data['high'].iloc[-1])
        l = float(data['low'].iloc[-1])
        c = float(data['close'].iloc[-1])
        if np.isnan(o) or np.isnan(h) or np.isnan(l) or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.side == "upper":
            wick = h - max(o, c)
        else:
            wick = min(o, c) - l
        base = float("nan")
        if self.relative_to == "range":
            rng = h - l
            value = 0.0 if rng == 0 else wick / rng
            base = rng
        elif self.relative_to == "close":
            value = wick / c * 100.0 if c > 0 else float("nan")
            base = c
        else:
            n = len(data)
            stop = n - self.exclude_current
            start = stop - self.base_period
            hi = data['high'].iloc[start:stop].astype(float)
            lo = data['low'].iloc[start:stop].astype(float)
            if hi.isna().any() or lo.isna().any():
                value = float("nan")
            else:
                base = float((hi - lo).mean())
                value = 0.0 if base == 0 else wick / base
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'wick': wick, 'base': base, 'side': self.side, 'relative_to': self.relative_to}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.relative_to == "mean_range":
            return self.base_period + self.exclude_current
        return 1
```

```python hand
def hand(df, params):
    rel = params.get("relative_to", "range")
    side = params.get("side", "lower")
    bp = int(params.get("base_period", 30))
    ex = int(params.get("exclude_current", 0))
    opens = [float(x) for x in list(df["open"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    o, h, l, c = opens[t], highs[t], lows[t], closes[t]
    for x in (o, h, l, c):
        if x != x:
            return float("nan")
    # the shadow above the body, or below it
    if side == "upper":
        body_top = o if o > c else c
        wick = h - body_top
    else:
        body_bottom = o if o < c else c
        wick = body_bottom - l
    if rel == "range":
        rng = h - l
        if rng == 0:
            return 0.0
        return wick / rng
    if rel == "close":
        if not c > 0:
            return float("nan")
        return wick / c * 100.0
    # mean bar range over bars t-ex-bp+1 .. t-ex
    total = 0.0
    for k in range(bp):
        i = t - ex - k
        hi = highs[i]
        lo = lows[i]
        if hi != hi or lo != lo:
            return float("nan")
        total = total + (hi - lo)
    mean_range = total / bp
    if mean_range == 0:
        return 0.0
    return wick / mean_range
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 275, in <module>
    main()
    ~~~~^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 265, in main
    fails += check_new_setting(old, cls, spec.SETTINGS[-1], old_params(old_text, spec.CLASS))
             ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 210, in check_new_setting
    a, b = values_on(old_cls, base, d), values_on(new_cls, params, d)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 166, in values_on
    c = cls(parameters=dict(params))
  File "old_strategy_components.py", line 2497, in __init__
ValueError: LowerWickComponent: relative_to must be 'range' or 'close', got 'mean_range'

## attempt 2

answer: built
class: UpperWickComponent
settings: {"relative_to": "mean_range", "base_period": 30, "exclude_current": 0}
reason: No component measures the upper shadow, high[t] − max(open[t], close[t]). `LowerWickComponent` measures the other shadow, which is neither the negative of this one nor 1 minus it, so a new class computes it. Its base ("range", "close", or the mean bar range over `base_period` bars with bar t included or excluded) is one setting, `relative_to`.

table: Hedges and filters
row: | `UpperWickComponent` | `relative_to` ("range"), `base_period` (30), `exclude_current` (0) | W = high[t] − max(open[t], close[t]). "range": W / (high[t] − low[t]), 0.0 when high[t] = low[t]. "close": W / close[t] x 100. "mean_range": W / B, B = mean(high[i] − low[i]) over i = t-`exclude_current`-`base_period`+1 .. t-`exclude_current` (`exclude_current` 0: bar t included; 1: bars t-`base_period` .. t-1), 0.0 when B = 0. With "mean_range", `base_period` 30, `exclude_current` 0: (high[t] − max(open[t], close[t])) / mean(high[i] − low[i], i = t-29 .. t) | "range": 0 to 1. "close": 0 and up. "mean_range": 0 and up, at most `base_period` with `exclude_current` 0 (the mean includes bar t's range), unbounded above with 1. Never negative on real bars; no direction; 0 when the bar has no upper shadow, growing linearly as the shadow lengthens | graded | "range": share of the bar's range. "close": percent of the close. "mean_range": mean bar ranges | 1 with "range" or "close"; `base_period` + `exclude_current` with "mean_range" (30 at the wished settings) | open, high, low, close of bar t; with "mean_range" also high and low of the base rows. A NaN in any value read gives NaN. With "close", a close[t] not above 0 gives NaN (never on real bars). A zero range ("range") or B = 0 ("mean_range", never on real bars) reads 0.0. These settings raise when the component is built: `relative_to` other than "range", "close" or "mean_range", `base_period` < 1, `exclude_current` not 0 or 1 | stateless. The shadow above the body, the counterpart of `LowerWickComponent`, which measures the shadow below. With `exclude_current` 1 bar t's own range cannot raise its base. Continuous in the prices. On 1d bars the wished settings give the day's upper shadow in 30-day mean daily ranges. No `scaling_factor`: scale it with transforms |

```python class
class UpperWickComponent(SubStrategyComponent):
    """
    The upper shadow of bar t, the part of the bar above its body:

        W = high[t] - max(open[t], close[t])
        relative_to = "range" (default): raw_value = W / (high[t] - low[t]), 0.0 when high[t] = low[t]
        relative_to = "close":           raw_value = W / close[t] x 100
        relative_to = "mean_range":      raw_value = W / B,
            B = mean(high[i] - low[i]) over i = t - exclude_current - base_period + 1 .. t - exclude_current
            (exclude_current 0: bar t included; 1: bars t-base_period .. t-1), 0.0 when B = 0

    Range and sign: never negative on real bars, no direction. 0 when the bar has no upper shadow, growing
    linearly as the shadow lengthens. "range" is 0 to 1. "close" is 0 and up. "mean_range" is 0 to base_period
    with exclude_current 0 (the mean includes bar t's range) and unbounded above with exclude_current 1.
    Warm-up: 1 row with "range" or "close"; base_period + exclude_current rows with "mean_range".
    NaN: a NaN open, high, low or close of bar t, or a NaN high or low in the base rows ("mean_range"), gives NaN.
    With "close", a close[t] not above 0 gives NaN (never on real bars).
    Building the component raises for a relative_to other than "range", "close" or "mean_range", a base_period
    below 1, or an exclude_current other than 0 or 1.

    WHY THIS CANNOT LEAK: it reads only bar t's open, high, low and close and, with "mean_range", the high and low
    of at most the last base_period + exclude_current rows of data, all ending at bar t (the last row).
    """

    def __init__(self, name="UpperWick", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.relative_to = self.parameters.get("relative_to", "range")
        if self.relative_to not in ("range", "close", "mean_range"):
            raise ValueError(
                f"UpperWickComponent: relative_to must be 'range', 'close' or 'mean_range', got {self.relative_to!r}")
        self.base_period = int(self.parameters.get("base_period", 30))
        if self.base_period < 1:
            raise ValueError(f"UpperWickComponent: base_period must be >= 1, got {self.base_period}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"UpperWickComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        o = float(data["open"].iloc[-1])
        h = float(data["high"].iloc[-1])
        l = float(data["low"].iloc[-1])
        c = float(data["close"].iloc[-1])
        if np.isnan(o) or np.isnan(h) or np.isnan(l) or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        w = h - max(o, c)
        if self.relative_to == "range":
            r = h - l
            value = w / r if r > 0 else 0.0
            base = r
        elif self.relative_to == "close":
            value = w / c * 100.0 if c > 0 else float("nan")
            base = c
        else:
            n = len(data)
            stop = n - self.exclude_current
            start = stop - self.base_period
            hi = data["high"].astype(float).to_numpy()[start:stop]
            lo = data["low"].astype(float).to_numpy()[start:stop]
            rng = hi - lo
            if np.isnan(rng).any():
                value = float("nan")
                base = float("nan")
            else:
                base = float(np.mean(rng))
                value = w / base if base > 0 else 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"upper_wick": w, "base": base, "relative_to": self.relative_to}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.relative_to == "mean_range":
            return self.base_period + self.exclude_current
        return 1
```

```python hand
def hand(df, params):
    rel = params.get("relative_to", "range")
    bp = int(params.get("base_period", 30))
    ex = int(params.get("exclude_current", 0))
    opens = [float(x) for x in list(df["open"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    o, h, l, c = opens[t], highs[t], lows[t], closes[t]
    for x in (o, h, l, c):
        if x != x:
            return float("nan")
    top_of_body = o if o > c else c
    shadow = h - top_of_body
    if rel == "range":
        if h - l > 0:
            return shadow / (h - l)
        return 0.0
    if rel == "close":
        if not c > 0:
            return float("nan")
        return shadow / c * 100.0
    # mean_range: bars t-ex-bp+1 .. t-ex
    total = 0.0
    for k in range(bp):
        i = t - ex - k
        hi = highs[i]
        lo = lows[i]
        if hi != hi or lo != lo:
            return float("nan")
        total = total + (hi - lo)
    mean_range = total / bp
    if not mean_range > 0:
        return 0.0
    return shadow / mean_range
```

checks:
UpperWickComponent: every check passed
the bot's suite: = 1686 passed, 16 skipped, 75 deselected, 95636 warnings in 142.69s (0:02:22) ==
