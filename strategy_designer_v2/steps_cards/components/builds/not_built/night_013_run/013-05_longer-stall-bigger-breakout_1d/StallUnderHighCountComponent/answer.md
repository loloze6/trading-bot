# not built: night_013_run | 013-05_longer-stall-bigger-breakout_1d | StallUnderHighCountComponent

## attempt 1

answer: built
class: NearHighCountComponent
settings: {"window": 60, "period": 365, "band_pct": 10.0}
reason: No catalogue component counts the bars whose close sat below the highest of the prior closes and within a percent band of it. `DistanceFromHighComponent` and `ConvexHighProximityComponent` read only bar t's distance from the high, not how many recent bars held near it. A new class computes this count from closes only.

table: Regime measures
row: | `NearHighCountComponent` | `window` (60), `period` (365), `band_pct` (10.0) | number of bars i in t-`window`+1 .. t with close[i] < H(i) and (H(i) - close[i]) / H(i) x 100 <= `band_pct`, H(i) being the highest of the `period` closes i-`period` .. i-1 (bar i excluded) | 0 to `window`, integers, never negative; no direction; grows by one for each further bar spent just under the prior high | graded | bars | `window` + `period` (425) | closes only. A NaN close anywhere in the last `window` + `period` rows gives NaN, and so does an H(i) not above 0. These settings raise when the component is built: `window` < 1, `period` < 2, `band_pct` not in (0, 100] | stateless; a bar that closes at or above its prior high (a breakout) is not counted, and neither is a bar that sits deeper than the band below it. How long price has stalled under its high, not a breakout event. No `scaling_factor`: scale it with transforms |

```python class
class NearHighCountComponent(SubStrategyComponent):
    """
    How many of the recent bars closed just under the prior high, on every bar:

        H(i) = max(close[i - period] .. close[i - 1])                (bar i excluded)
        near(i) = close[i] < H(i) and (H(i) - close[i]) / H(i) x 100 <= band_pct
        raw_value = number of bars i in t - window + 1 .. t with near(i)

    Graded: an integer from 0 to window, never negative, no direction. It grows by one for each further bar that
    closes below its prior high and within band_pct percent of it. A bar closing at or above its prior high, or
    deeper than the band below it, is not counted.
    Warm-up: window + period rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data, up to and
    including bar t (the last row). Each H(i) uses closes strictly before bar i <= t.

    NaN: a NaN close anywhere in the last window + period rows gives NaN, and so does an H(i) not above 0.
    Building the component raises for a window below 1, a period below 2, or a band_pct not in (0, 100].
    """

    def __init__(self, name="NearHighCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 60))
        if self.window < 1:
            raise ValueError(f"NearHighCountComponent: window must be >= 1, got {self.window}")
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"NearHighCountComponent: period must be >= 2, got {self.period}")
        self.band_pct = float(self.parameters.get("band_pct", 10.0))
        if not (self.band_pct > 0.0 and self.band_pct <= 100.0):
            raise ValueError(f"NearHighCountComponent: band_pct must be in (0, 100], got {self.band_pct}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.window + self.period
        c = data['close'].astype(float).iloc[-n:].to_numpy()
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        count = 0
        for j in range(self.window):
            i = self.period + j
            h = float(np.max(c[j:i]))
            if not h > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            x = float(c[i])
            if x < h and (h - x) / h * 100.0 <= self.band_pct:
                count += 1
        self._raw_value = float(count)
        self.confidence = 1.0
        self.debug_info = {'near_high_count': count}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period
```

```python hand
def hand(df, params):
    w = int(params.get("window", 60))
    p = int(params.get("period", 365))
    b = float(params.get("band_pct", 10.0))
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    for k in range(last - w - p + 1, last + 1):
        if closes[k] != closes[k]:
            return float("nan")
    count = 0
    for i in range(last - w + 1, last + 1):
        high = closes[i - p]
        for k in range(i - p, i):
            if closes[k] > high:
                high = closes[k]
        if not high > 0:
            return float("nan")
        below = closes[i] < high
        depth = (high - closes[i]) / high * 100.0
        if below and depth <= b:
            count = count + 1
    return float(count)
```

checks:
the standard checks:
FAIL warm-up {}: not ready with 425 rows = get_required_periods()
FAIL warm-up {'window': 60, 'period': 365, 'band_pct': 10.0}: not ready with 425 rows = get_required_periods()
NearHighCountComponent: 2 failure(s)

## attempt 2

answer: built
class: NearHighCountComponent
settings: {"window": 60, "period": 365, "band_pct": 10.0}
reason: No catalogue component counts the bars in a recent window whose close sat below, but within a percent band of, the highest of the prior `period` closes. `DistanceFromHighComponent` gives that distance on one bar only, never a count. This new class computes it from closes only, and it is ready with exactly `window + period` rows.

table: Regime measures
row: | `NearHighCountComponent` | `window` (60), `period` (365), `band_pct` (10.0) | the number of bars i in t-`window`+1 .. t with 0 < D(i) <= `band_pct`, where D(i) = (H(i) - close[i]) / H(i) x 100 and H(i) is the highest of the `period` closes i-`period` .. i-1 (bar i excluded) | 0 to `window`, integers, never negative; no direction; larger the longer the close has stalled just under its prior high | regime measure | bars | `window` + `period` (425) | closes only. A NaN close anywhere in the last `window` + `period` rows gives NaN, and so does an H(i) not above 0. These settings raise when the component is built: `window` < 1, `period` < 1, `band_pct` not above 0 | stateless. A close at or above its prior high (a breakout) is not counted, and neither is a close deeper than `band_pct` below the high. It is graded in steps of one bar. No `scaling_factor`: scale it with transforms |

```python class
class NearHighCountComponent(SubStrategyComponent):
    """
    How many recent bars closed just under their prior high:

        H(i) = max(close[i - period .. i - 1])            (bar i excluded)
        D(i) = (H(i) - close[i]) / H(i) x 100
        raw_value = number of bars i in t - window + 1 .. t with 0 < D(i) <= band_pct

    Range: integers 0 to window, never negative, no direction. A larger value means the close has stalled under
    its prior high for longer. A close at or above H(i) is not counted, and neither is one more than band_pct
    below it.
    Warm-up: window + period rows, bar t included.

    NaN: a NaN close anywhere in the last window + period rows gives NaN, and so does an H(i) not above 0.
    Building the component raises for window < 1, period < 1, or band_pct not above 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data, which are
    rows t - window - period + 1 .. t (bar t being the last row). Each H(i) uses only rows before bar i.
    """

    def __init__(self, name="Near high count", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 60))
        if self.window < 1:
            raise ValueError(f"NearHighCountComponent: window must be >= 1, got {self.window}")
        self.period = int(self.parameters.get("period", 365))
        if self.period < 1:
            raise ValueError(f"NearHighCountComponent: period must be >= 1, got {self.period}")
        self.band_pct = float(self.parameters.get("band_pct", 10.0))
        if not self.band_pct > 0:
            raise ValueError(f"NearHighCountComponent: band_pct must be above 0, got {self.band_pct}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.window + self.period
        c = data['close'].astype(float).to_numpy()[-n:]
        if len(c) < n or np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        count = 0
        for j in range(self.window):
            i = self.period + j
            h = float(np.max(c[i - self.period:i]))
            if not h > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            d = (h - float(c[i])) / h * 100.0
            if d > 0 and d <= self.band_pct:
                count += 1
        self._raw_value = float(count)
        self.confidence = 1.0
        self.debug_info = {'count': count}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period
```

```python hand
def hand(df, params):
    w = int(params.get("window", 60))
    p = int(params.get("period", 365))
    b = float(params.get("band_pct", 10.0))
    closes = [float(x) for x in list(df["close"])]
    m = len(closes)
    if m < w + p:
        return float("nan")
    for x in closes[m - w - p:]:
        if x != x:
            return float("nan")
    count = 0
    for i in range(m - w, m):
        h = closes[i - p]
        for k in range(i - p, i):
            if closes[k] > h:
                h = closes[k]
        if not h > 0:
            return float("nan")
        d = (h - closes[i]) / h * 100.0
        if d > 0 and d <= b:
            count = count + 1
    return float(count)
```

checks:
the standard checks:
FAIL warm-up {}: not ready with 425 rows = get_required_periods()
FAIL warm-up {'window': 60, 'period': 365, 'band_pct': 10.0}: not ready with 425 rows = get_required_periods()
FAIL hand computation {} at bar 399: class 0.0, hand nan
FAIL hand computation {'window': 60, 'period': 365, 'band_pct': 10.0} at bar 399: class 0.0, hand nan
NearHighCountComponent: 4 failure(s)

## attempt 3

answer: built
class: NearHighCountComponent
settings: {"window": 60, "period": 365, "band_pct": 10.0}
reason: No catalogue component counts bars: `ConvexHighProximityComponent` and `DistanceFromHighComponent` give the distance from the high on bar t only, not how many of the last 60 bars sat close under the prior 365-close high. This new class computes that count, which rises from 0 to `window` the longer the close stays just under its high.

table: Regime measures
row: | `NearHighCountComponent` | `window` (60), `period` (365), `band_pct` (10.0) | number of bars i in t-`window`+1 .. t with close[i] < H(i) and (H(i) - close[i]) / H(i) x 100 <= `band_pct`, H(i) being the highest of the `period` closes before bar i (bars i-`period` .. i-1, bar i excluded) | 0 to `window`, integers, never negative; no direction; larger the longer the close has stalled just under its prior high | graded | bars | `window` + `period` (425) | closes only. A NaN close anywhere in the last `window` + `period` rows gives NaN, and so does an H(i) not above 0. These settings raise when the component is built: `window` < 1, `period` < 1, `band_pct` not above 0 | stateless. A bar that closes at or above its prior high (a new high) is not counted, and neither is a bar more than `band_pct` percent below it. Use it in a regime rule ("stalled under the high for at least 40 of the last 60 bars") or as a forecast source after transforms. No `scaling_factor` |

```python class
class NearHighCountComponent(SubStrategyComponent):
    """
    How many recent bars closed just under their prior high:

        H(i) = max(close[i - period .. i - 1])                 (the period closes before bar i, bar i excluded)
        near(i) = 1 if close[i] < H(i) and (H(i) - close[i]) / H(i) x 100 <= band_pct, else 0
        raw_value = sum of near(i) for i = t - window + 1 .. t

    Range 0 to window, integers, never negative. No direction: it grows by one for each further bar of the
    window that sits under its prior high and within band_pct percent of it. A bar at or above its prior high
    is not counted, and neither is a bar further below it than band_pct percent.
    Warm-up: window + period rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data, all at or
    before bar t (the last row); each H(i) uses closes strictly before bar i, and i <= t.

    NaN: a NaN close anywhere in the last window + period rows, or an H(i) not above 0, gives NaN.
    Building the component raises for a window below 1, a period below 1 or a band_pct not above 0.
    """

    def __init__(self, name="NearHighCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 60))
        if self.window < 1:
            raise ValueError(f"NearHighCountComponent: window must be >= 1, got {self.window}")
        self.period = int(self.parameters.get("period", 365))
        if self.period < 1:
            raise ValueError(f"NearHighCountComponent: period must be >= 1, got {self.period}")
        self.band_pct = float(self.parameters.get("band_pct", 10.0))
        if not self.band_pct > 0:
            raise ValueError(f"NearHighCountComponent: band_pct must be above 0, got {self.band_pct}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        count = 0
        for k in range(self.window):
            i = self.period + k
            h = float(np.max(c[i - self.period:i]))
            if not h > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            x = float(c[i])
            if x < h and (h - x) / h * 100.0 <= self.band_pct:
                count += 1
        self._raw_value = float(count)
        self.confidence = 1.0
        self.debug_info = {'near_high_count': count}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period
```

```python hand
def hand(df, params):
    w = int(params.get("window", 60))
    p = int(params.get("period", 365))
    b = float(params.get("band_pct", 10.0))
    c = [float(x) for x in list(df["close"])]
    if len(c) < w + p:
        return float("nan")
    last = c[len(c) - w - p:]
    for x in last:
        if x != x:
            return float("nan")
    t = len(c) - 1
    count = 0
    for i in range(t - w + 1, t + 1):
        h = c[i - p]
        for j in range(i - p, i):
            if c[j] > h:
                h = c[j]
        if not h > 0:
            return float("nan")
        if c[i] < h and (h - c[i]) / h * 100.0 <= b:
            count = count + 1
    return float(count)
```

checks:
the standard checks:
FAIL warm-up {}: not ready with 425 rows = get_required_periods()
FAIL warm-up {'window': 60, 'period': 365, 'band_pct': 10.0}: not ready with 425 rows = get_required_periods()
FAIL hand computation {} at bar 399: class 0.0, hand nan
FAIL hand computation {'window': 60, 'period': 365, 'band_pct': 10.0} at bar 399: class 0.0, hand nan
NearHighCountComponent: 4 failure(s)
