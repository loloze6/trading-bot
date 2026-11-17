# OpenToLowDropComponent: night_012_run | 012-04_flush-depth-retracement-size_1d | OpenToLowDropComponent

## attempt 1

answer: built
class: OpenToLowDropComponent
settings: {}
reason: No component measures the fall from the bar's open to its low. `LowerWickPercentComponent` measures from min(open, close) and divides by the close, so it differs from (open − low) / open × 100 whenever the bar closes below its open. This is a new single-bar measure, computed from `open` and `low` of bar t only.

table: Hedges and filters
row: | `OpenToLowDropComponent` | none | (open[t] − low[t]) / open[t] x 100 | 0 to 100, never negative on real bars (low <= open); no direction; 0 = the bar never traded below its open, larger the deeper the intrabar fall below the open | graded | percent of the open | 1 | open, low of bar t only. A NaN in either gives NaN; an open that is not above 0 gives NaN; a missing column raises | stateless; the shape of the current bar only, no lookback. Not `LowerWickPercentComponent` ((min(open, close) − low) / close x 100): this measures from the open whatever the close, so a bar that falls and stays down reads its whole drop. For a regime rule ("the bar fell more than 5 percent below its open") or as a forecast source after transforms; no `scaling_factor` |

```python class
class OpenToLowDropComponent(SubStrategyComponent):
    """
    The depth of the bar's intrabar fall below its open, on every bar:

        raw_value = (open[t] - low[t]) / open[t] x 100

    Graded and non-negative on real bars (low <= open): 0 when the bar never traded below its open, larger the
    deeper the fall from the open to the low, at most 100. It carries no direction. The unit is percent of the open.
    Warm-up: 1 row (bar t only).

    WHY THIS CANNOT LEAK: it reads only the `open` and `low` columns of the last row of data, which is bar t. Both
    are known at that bar's close.

    NaN: a NaN open or low at bar t gives NaN. An open that is not above 0, which never happens on real bars, also
    gives NaN. A missing column raises.
    """

    def __init__(self, name="OpenToLowDrop", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        o = float(data['open'].iloc[-1])
        lo = float(data['low'].iloc[-1])
        if np.isnan(o) or np.isnan(lo) or not o > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float((o - lo) / o * 100.0)
        self.confidence = 1.0
        self.debug_info = {'open': o, 'low': lo}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1
```

```python hand
def hand(df, params):
    opens = [float(x) for x in list(df["open"])]
    lows = [float(x) for x in list(df["low"])]
    o = opens[-1]
    lo = lows[-1]
    if o != o or lo != lo or not o > 0:
        return float("nan")
    drop = o - lo
    return drop / o * 100.0
```

checks:
OpenToLowDropComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1524 passed, 8 skipped, 74 deselected, 2170 warnings in 53.28s ========
