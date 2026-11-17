# not built: night_012_run | 012-03_lower-wick-flush-recovery_1d | LowerWickShareComponent

## attempt 1

answer: built
class: CloseLocationComponent
settings: {}
reason: No catalogue component measures where the current bar's close sits inside that bar's own high-low range. `DonchianBreakoutComponent` uses closes over a window, and `KeltnerBreakoutComponent` uses the distance from an EMA. The new class is named for what it measures, the close's location in the bar's range: the wished formula reads the close against the low, not the size of the lower wick.

table: Regime measures
row: | `CloseLocationComponent` | none | (close[t] - low[t]) / (high[t] - low[t]) of the current bar; 0.5 when high[t] = low[t] | 0 to 1, never negative; 0 when the close is at the bar's low, 1 at its high; no direction | regime measure (graded) | dimensionless (share of the bar's range) | 1 | high, low, close of bar t only. A NaN in any of the three gives NaN; a zero range gives 0.5 | stateless; reads one bar. A bar that flushed down and closed near its high reads near 1. Centre it (minus 0.5) with transforms for a signed forecast |

```python class
class CloseLocationComponent(SubStrategyComponent):
    """
    Where the current bar's close sits inside that bar's own range, on every bar:

        raw_value = (close[t] - low[t]) / (high[t] - low[t])      (0.5 when high[t] == low[t])

    Range: 0 to 1, never negative. It is 0 when the close is at the bar's low, 1 at its high, and grows continuously
    as the close sits further above the low. It has no direction: it describes the bar's shape (a bar that dipped and
    recovered closes high in its range).
    Warm-up: 1 bar (bar t alone).
    NaN: a NaN high, low or close on bar t gives NaN, never a fabricated reading. A zero range (high == low, all
    finite) gives 0.5, the middle of a range that has no extent.

    WHY THIS CANNOT LEAK: it reads only the high, low and close of the last row (bar t), all known at bar t's close.
    """

    def __init__(self, name="Close location", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = float(data['high'].iloc[-1])
        low = float(data['low'].iloc[-1])
        close = float(data['close'].iloc[-1])
        if np.isnan(high) or np.isnan(low) or np.isnan(close):
            value = float("nan")
        else:
            rng = high - low
            value = 0.5 if rng == 0 else (close - low) / rng
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'high': high, 'low': low, 'close': close}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1
```

```python hand
def hand(df, params):
    h = list(df["high"])[-1]
    l = list(df["low"])[-1]
    c = list(df["close"])[-1]
    if h != h or l != l or c != c:
        return float("nan")
    if h == l:
        return 0.5
    return (c - l) / (h - l)
```

checks:
the standard checks:
FAIL engine {}: no finite forecast at row 21 ({'not_ready_component': 'c'})
CloseLocationComponent: 1 failure(s)

## attempt 2

answer: built
class: CloseLocationComponent
settings: {}
reason: No component in the catalogue measures where the current bar's close sits inside that same bar's high-low range. `DonchianBreakoutComponent` measures the close's position among many bars' closes, not within one bar. This new class computes (close - low) / (high - low) of bar t and needs only that one row. It is named by what it measures, the close's location in the bar, not by the "lower wick" idea that asked for it.

table: Regime measures
row: | `CloseLocationComponent` | none | (close[t] - low[t]) / (high[t] - low[t]) of the current bar; 0.5 when high[t] = low[t] | 0 to 1, never negative; 0 = close at the bar's low, 1 = close at the bar's high, 0.5 = mid-bar or a zero range | regime measure | dimensionless (share of the bar's range) | 1 | high, low, close of bar t only. A NaN in any of the three gives NaN | stateless; graded, bounded, on every bar; a high close location after a deep low is the "lower wick" share of the bar's range |

```python class
class CloseLocationComponent(SubStrategyComponent):
    """
    Where the current bar's close sits inside that same bar's high-low range:

        raw_value = (close[t] - low[t]) / (high[t] - low[t])     (0.5 when high[t] == low[t])

    Range 0 to 1, never negative, no direction: 0 when the bar closes at its low, 1 when it closes at its high.
    The value grows continuously as the close sits further above the bar's low (a long lower wick with a high
    close gives a value near 1). A zero range (high == low) gives 0.5, the middle.
    Warm-up: 1 bar (bar t alone).

    NaN: a NaN high, low or close on bar t gives NaN; there is no fabricated value.

    WHY THIS CANNOT LEAK: it reads only the `high`, `low` and `close` of the last row of the data (bar t). All
    three are known at bar t's close.
    """

    def __init__(self, name="CloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.data = None
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        last = data.iloc[-1]
        high = float(last['high'])
        low = float(last['low'])
        close = float(last['close'])
        if np.isnan(high) or np.isnan(low) or np.isnan(close):
            value = float("nan")
        else:
            rng = high - low
            value = 0.5 if rng == 0 else (close - low) / rng
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'high': high, 'low': low, 'close': close}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1
```

```python hand
def hand(df, params):
    h = list(df["high"])[-1]
    l = list(df["low"])[-1]
    c = list(df["close"])[-1]
    if h != h or l != l or c != c:
        return float("nan")
    if h == l:
        return 0.5
    return (c - l) / (h - l)
```

checks:
the standard checks:
FAIL engine {}: no finite forecast at row 21 ({'not_ready_component': 'c'})
CloseLocationComponent: 1 failure(s)

## attempt 3

answer: built
class: CloseLocationComponent
settings: {}
reason: No catalogue component measures where bar t's close sits inside bar t's own high-low range. `DonchianBreakoutComponent` uses closes over a window, not the bar's high and low, so one new stateless class computes it. It is ready from a single row, so the engine finds a finite value on every bar once the strategy is warm.

table: Regime measures
row: | `CloseLocationComponent` | none | (close[t] - low[t]) / (high[t] - low[t]) of the current bar; 0.5 when high[t] = low[t] | 0 to 1, never negative; no direction; 1 when the close is the bar's high, 0 when it is the bar's low | regime measure (graded) | dimensionless (share of the bar's range) | 1 | high, low, close of bar t only. A NaN high, low or close on bar t gives NaN; a zero range gives 0.5 | stateless; no lag; the share of the bar's range lying below the close (the lower-wick-plus-body share). Use it in regime rules, or as a forecast source after transforms |

```python class
class CloseLocationComponent(SubStrategyComponent):
    """
    Where the current bar's close sits inside that bar's own high-low range, on every bar:

        raw_value = (close[t] - low[t]) / (high[t] - low[t])     (0.5 when high[t] == low[t])

    Range is 0 to 1, never negative, with no direction. It is 1 when the close is at the bar's high and 0 when it is
    at the bar's low. It grows continuously as the close sits further above the bar's low. The warm-up is 1 bar
    (bar t alone). There is no lag.

    NaN: a NaN high, low or close on bar t gives NaN, never a fabricated reading. A zero range (high equal to low) is
    real data and gives 0.5, the middle of the bar.

    WHY THIS CANNOT LEAK: it reads only the `high`, `low` and `close` of the last row of the data it is given (bar t),
    all known at bar t's close; no earlier or later row is read.
    """

    def __init__(self, name="CloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        last = data.iloc[-1]
        high = float(last['high'])
        low = float(last['low'])
        close = float(last['close'])
        if np.isnan(high) or np.isnan(low) or np.isnan(close):
            value = float("nan")
        elif high == low:
            value = 0.5
        else:
            value = (close - low) / (high - low)
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'high': high, 'low': low, 'close': close}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1
```

```python hand
def hand(df, params):
    h = list(df["high"])[-1]
    l = list(df["low"])[-1]
    c = list(df["close"])[-1]
    if h != h or l != l or c != c:
        return float("nan")
    if h == l:
        return 0.5
    return (c - l) / (h - l)
```

checks:
the standard checks:
FAIL engine {}: no finite forecast at row 21 ({'not_ready_component': 'c'})
CloseLocationComponent: 1 failure(s)
