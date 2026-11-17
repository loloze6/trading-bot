# ConvexHighProximityComponent: night_013_run | 013-01_nearness-to-high-predicts-gains.d1_gain-concentrated-at-the-high_1d | ConvexHighProximityComponent

## attempt 1

answer: built
class: HighProximityComponent
settings: {"period": 365, "power": 2.0}
reason: No component computes this measure. `DistanceFromHighComponent` gives the depth below the high, but no transform op computes `(1 / (1 + depth)) ^ power`. One new class computes it, with the window length and the exponent as settings. The wish only says the exponent is "above 1", so 2.0 is my choice of value.

table: Directional components
row: | `HighProximityComponent` | `period` (365), `power` (2.0) | (1 / (1 + d)) ^ `power`, where d = (H[t] − close[t]) / H[t] x 100 and H[t] is the highest of the last `period` closes, bar t included | above 0, up to 1; never negative, no direction; 1 at a new high, smaller the deeper the close sits below the high (at least 1/101^`power`) | graded | dimensionless | `period` (365) | closes only. A window holding a NaN close, or a high not above 0, gives NaN; a `period` below 2 or a `power` not above 0 raises when the engine starts | stateless; a convex function of `DistanceFromHighComponent` (d = −its output). With `power` > 1 the value falls steeply in the first percents below the high and flattens deeper down. No `scaling_factor`: scale it with transforms |

```python class
class HighProximityComponent(SubStrategyComponent):
    """
    How near the close is to its recent closing high, on a convex scale, on every bar:

        H[t]      = max(close[t - period + 1 .. t])                (bar t included)
        d[t]      = (H[t] - close[t]) / H[t] * 100                 (percent below the high, >= 0)
        raw_value = (1 / (1 + d[t])) ** power

    Range: above 0, up to 1; never negative, no direction. It is 1 at a new closing high and smaller the deeper the
    close sits below the high (at least 1 / 101 ** power, since d < 100 for positive closes). With power > 1 the value
    changes fastest just below the high. Graded: it is continuous in the close.
    Warm-up: `period` rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last `period` rows of data, bar t (the last row)
    included; each close is known at its bar's close.

    NaN: a NaN close anywhere in the window gives NaN, and so does a high that is not above 0. A missing `close`
    column raises. A `period` below 2, or a `power` not above 0, raises when the component is built.
    """

    def __init__(self, name="HighProximity", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"HighProximityComponent: period must be >= 2, got {self.period}")
        self.power = float(self.parameters.get("power", 2.0))
        if not self.power > 0:
            raise ValueError(f"HighProximityComponent: power must be > 0, got {self.power}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = data['close'].astype(float).iloc[-self.period:]
        if closes.isna().any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        c = float(closes.iloc[-1])
        h = float(closes.max())
        if not h > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        depth = (h - c) / h * 100.0
        self._raw_value = float((1.0 / (1.0 + depth)) ** self.power)
        self.confidence = 1.0
        self.debug_info = {'close': c, 'high': h, 'depth_pct': depth}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period
```

```python hand
def hand(df, params):
    n = int(params.get("period", 365))
    p = float(params.get("power", 2.0))
    closes = [float(x) for x in list(df["close"])]
    window = closes[-n:]
    for x in window:
        if x != x:
            return float("nan")
    high = window[0]
    for x in window:
        if x > high:
            high = x
    if not high > 0:
        return float("nan")
    cur = window[-1]
    depth = (high - cur) / high * 100.0
    closeness = 1.0 / (1.0 + depth)
    return closeness ** p
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 34, in <module>
    import strategies.strategy_components as SC  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/strategies/strategy_components.py", line 2418
    self._raw_value = float((1.0 / (1.0 + depth))  self.power)
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?

## attempt 2

answer: built
class: ConvexHighProximityComponent
settings: {"period": 365, "power": 2.0}
reason: `DistanceFromHighComponent` gives only the signed depth below the recent closing high, and no component gives the convex closeness (1 / (1 + depth)) ** power. One new class computes it; the earlier attempt failed only because the `**` operator was missing, which is fixed here.

table: Directional components
row: | `ConvexHighProximityComponent` | `period` (365), `power` (2.0) | (1 / (1 + d)) ** `power`, d = (H[t] - close[t]) / H[t] x 100, H[t] being the highest of the last `period` closes, bar t included | above 0, up to 1; never negative; 1 at a new closing high, falling towards 0 the deeper the close sits below it; no direction | graded | dimensionless | `period` (365) | closes. A window holding a NaN close gives NaN; a `period` below 2 or a `power` not above 0 raises when the engine starts | stateless. Convex in nearness: with `power` above 1 it rises fastest as the close nears the high (d 0 gives 1, d 1 gives 0.25, d 10 gives about 0.008 at `power` 2). It is the closeness to the high, not a bet on direction. No `scaling_factor`: scale it with transforms |

```python class
class ConvexHighProximityComponent(SubStrategyComponent):
    """
    Convex closeness of the close to its recent closing high, on every bar:

        H[t]      = max(close[t - period + 1 .. t])               (bar t included)
        d[t]      = (H[t] - close[t]) / H[t] x 100                (percent below the high, >= 0)
        raw_value = (1 / (1 + d[t])) ** power

    Graded, above 0 and up to 1, never negative, no direction. It is 1 on a bar whose close is the highest of the
    window, and it falls towards 0 as the close sits deeper below that high. With power above 1 it rises faster the
    nearer the close is to the high. Warm-up: `period` rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last `period` rows of data, which are the bars up
    to and including bar t (the last row). A close is known at its bar's close.

    NaN: a NaN close anywhere in the last `period` rows gives NaN. A `period` below 2, or a `power` not above 0,
    raises when the component is built.
    """

    def __init__(self, name="ConvexHighProximity", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"ConvexHighProximityComponent: period must be >= 2, got {self.period}")
        self.power = float(self.parameters.get("power", 2.0))
        if not self.power > 0:
            raise ValueError(f"ConvexHighProximityComponent: power must be > 0, got {self.power}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        window = data['close'].astype(float).iloc[-self.period:]
        if window.isna().any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        close = float(window.iloc[-1])
        high = float(window.max())
        if not high > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        depth = (high - close) / high * 100.0
        base = 1.0 / (1.0 + depth)
        self._raw_value = float(base ** self.power)
        self.confidence = 1.0
        self.debug_info = {'close': close, 'high': high, 'depth_pct': depth}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period
```

```python hand
def hand(df, params):
    n = int(params.get("period", 365))
    p = float(params.get("power", 2.0))
    c = [float(x) for x in list(df["close"])]
    w = c[-n:]
    for x in w:
        if x != x:
            return float("nan")
    h = w[0]
    for x in w:
        if x > h:
            h = x
    if not h > 0:
        return float("nan")
    cur = w[-1]
    d = (h - cur) / h * 100.0
    return math_pow(1.0 / (1.0 + d), p)


def math_pow(b, e):
    return b ** e
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 34, in <module>
    import strategies.strategy_components as SC  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/strategies/strategy_components.py", line 2418
    self._raw_value = float(base  self.power)
                            ^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?

## attempt 3

answer: built
class: ConvexHighProximityComponent
settings: {"period": 365, "power": 2.0}
reason: No catalogue component gives a convex closeness to the high. `DistanceFromHighComponent` gives the linear percent depth below the high, not (1 / (1 + depth)) raised to a power. A new class computes this one measure from the closes. The earlier failure was a lost `**` operator; this version uses `np.power` and `pow`.

table: Directional components
row: | `ConvexHighProximityComponent` | `period` (365), `power` (2.0) | (1 / (1 + D))^`power`, D = (H[t] - close[t]) / H[t] x 100, H[t] being the highest of the last `period` closes, bar t included | above 0, up to 1; never negative; 1 at a new high, smaller the deeper below it (at least 101^-`power` for positive closes); no direction | graded | dimensionless | `period` (365) | closes. A window holding a NaN close gives NaN; a highest close not above 0 gives NaN; a `period` below 2 or a `power` not above 0 raises when the engine starts | stateless; with `power` above 1 the value rises faster the nearer the close is to the high (convex near the high); `power` 1 gives the plain 1 / (1 + D). No `scaling_factor`: scale it with transforms |

```python class
class ConvexHighProximityComponent(SubStrategyComponent):
    """
    How close the close is to its recent high, made convex by a power, on every bar:

        H[t] = max(close[t - period + 1 .. t])                  (bar t included)
        D[t] = (H[t] - close[t]) / H[t] x 100                   (percent depth below the high, >= 0)
        raw_value = (1 / (1 + D[t])) ^ power

    Range: above 0, up to 1, never negative. It is 1 at a new high and smaller the deeper the close sits
    below the high. For positive closes D <= 100, so the value is at least 101^(-power). There is no direction.
    With power > 1 the value climbs faster the nearer the close is to the high.
    Graded: the value moves continuously with the depth.
    Warm-up: `period` rows, bar t included.

    NaN: a NaN close anywhere in the last `period` rows gives NaN. A highest close not above 0 also gives NaN.
    A missing `close` column raises. A `period` below 2, or a `power` not above 0, raises when the component
    is built.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last `period` rows of data, the last row
    being bar t; every close used is known at bar t's close.
    """

    def __init__(self, name="ConvexHighProximity", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"ConvexHighProximityComponent: period must be >= 2, got {self.period}")
        self.power = float(self.parameters.get("power", 2.0))
        if not np.isfinite(self.power) or self.power <= 0:
            raise ValueError(f"ConvexHighProximityComponent: power must be > 0, got {self.power}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        window = data['close'].astype(float).iloc[-self.period:]
        if window.isna().any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        high = float(window.max())
        close = float(window.iloc[-1])
        if not high > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        depth = (high - close) / high * 100.0
        base = 1.0 / (1.0 + depth)
        self._raw_value = float(np.power(base, self.power))
        self.confidence = 1.0
        self.debug_info = {'high': high, 'close': close, 'depth_pct': depth}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period
```

```python hand
def hand(df, params):
    n = int(params.get("period", 365))
    p = float(params.get("power", 2.0))
    closes = [float(x) for x in list(df["close"])]
    window = closes[-n:]
    for x in window:
        if x != x:
            return float("nan")
    h = window[0]
    for x in window:
        if x > h:
            h = x
    if not h > 0:
        return float("nan")
    c = window[-1]
    depth = (h - c) / h * 100.0
    closeness = 1.0 / (1.0 + depth)
    return pow(closeness, p)
```

checks:
ConvexHighProximityComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1525 passed, 8 skipped, 74 deselected, 2170 warnings in 54.98s ========
