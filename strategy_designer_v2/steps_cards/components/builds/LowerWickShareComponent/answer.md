# LowerWickShareComponent: night_012_run | 012-04_flush-depth-retracement-size_1d | LowerWickShareComponent

## attempt 1

answer: built
class: LowerWickShareComponent
settings: {}
reason: No catalogue component reads the bar's `open` or measures where the low sits against the bar's body. The share of the bar's range taken by its lower wick is a new measure, so one new class without settings computes it.

table: Hedges and filters
row: | `LowerWickShareComponent` | none | (min(open[t], close[t]) − low[t]) / (high[t] − low[t]); 0.0 when high[t] = low[t] | 0 to 1, never negative; no direction; 0 = no lower wick (the body's bottom is the low), 1 = the whole range is lower wick (open and close at the high) | graded | dimensionless (share of the bar's range) | 1 | open, high, low, close of bar t only. A NaN in any of the four gives NaN; a zero range (high = low) gives 0.0 (no wick); a missing column raises | stateless; the shape of the current bar only, no lookback. Bounded in [0, 1] when open and close lie inside [low, high], as they do on real bars. Use it in a regime rule ("a long lower wick: share above 0.6") or as a forecast source after transforms |

```python class
class LowerWickShareComponent(SubStrategyComponent):
    """
    The share of the current bar's range that is lower wick, on every bar:

        raw_value = (min(open[t], close[t]) - low[t]) / (high[t] - low[t])
        raw_value = 0.0 when high[t] == low[t]  (a zero range has no wick)

    Graded, from 0 to 1, never negative, no direction. It is 0 when the bottom of the body is the bar's low (no lower
    wick). It is 1 when the open and the close both sit at the high and the whole range lies below the body. It grows
    continuously as the low sits further below the body. On real bars open and close lie in [low, high], so the value
    stays in [0, 1].

    Warm-up: 1 bar (bar t itself).

    NaN: a NaN open, high, low or close on bar t gives NaN; it is never turned into a number. A missing column raises.

    WHY THIS CANNOT LEAK: it reads only the `open`, `high`, `low` and `close` of the last row of the data (bar t). All
    four are known at bar t's close. No earlier or later row is used.
    """

    def __init__(self, name="LowerWickShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        row = data.iloc[-1]
        o = float(row['open'])
        h = float(row['high'])
        l = float(row['low'])
        c = float(row['close'])
        if np.isnan(o) or np.isnan(h) or np.isnan(l) or np.isnan(c):
            value = float("nan")
        else:
            rng = h - l
            value = (min(o, c) - l) / rng if rng > 0 else 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'open': o, 'high': h, 'low': l, 'close': c}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1
```

```python hand
def hand(df, params):
    o = list(df["open"])[-1]
    h = list(df["high"])[-1]
    l = list(df["low"])[-1]
    c = list(df["close"])[-1]
    if o != o or h != h or l != l or c != c:
        return float("nan")
    body_bottom = o if o < c else c
    wick = body_bottom - l
    full_range = h - l
    if full_range == 0:
        return 0.0
    return wick / full_range
```

checks:
LowerWickShareComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1521 passed, 8 skipped, 74 deselected, 2170 warnings in 50.15s ========
