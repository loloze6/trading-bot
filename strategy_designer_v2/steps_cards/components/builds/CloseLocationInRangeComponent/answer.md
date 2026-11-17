# CloseLocationInRangeComponent: night_012_run | 012-03_lower-wick-flush-recovery_1d | LowerWickShareComponent

## attempt 1

answer: built
class: CloseLocationInRangeComponent
settings: {}
reason: The wish measures where bar t's close sits in its own high-low range, (close - low) / (high - low). `LowerWickShareComponent` measures something else: (min(open, close) - low) / (high - low), the wick below the body. No catalogue class computes the close's position in its own bar, so a new class named by that measure is written; it needs no setting.

table: Hedges and filters
row: | `CloseLocationInRangeComponent` | none | (close[t] − low[t]) / (high[t] − low[t]); 0.5 when high[t] = low[t] | 0 to 1, never negative; 0 = close at the bar's low, 1 = close at the bar's high, 0.5 at mid-range; no sign, but higher means a stronger close | graded | dimensionless (share of the bar's range) | 1 | high, low, close of bar t only. A NaN in any of the three gives NaN; a zero range (high = low) gives 0.5 (no range to place the close in); a missing column raises | stateless; the shape of the current bar only, no lookback. Bounded in [0, 1] when the close lies inside [low, high], as it does on real bars. Not `LowerWickShareComponent` (which uses min(open, close), the body's bottom): this ignores the open. For a regime rule ("closed in the top quarter of its range: above 0.75") or as a forecast source after transforms; no `scaling_factor` |

```python class
class CloseLocationInRangeComponent(SubStrategyComponent):
    """
    Where the current bar's close sits inside that bar's own high-low range, on every bar:

        raw_value = (close[t] - low[t]) / (high[t] - low[t])      (0.5 when high[t] == low[t])

    Range: 0 to 1 on real bars (the close lies between the low and the high). It is never negative. 0 means the bar
    closed at its low, 1 means it closed at its high, and 0.5 means mid-range. It has no sign; a larger value is a
    stronger close. It is graded: it moves continuously with the distance of the close above the low. Warm-up: 1 bar
    (bar t alone).

    NaN: a NaN high, low or close on bar t gives NaN, never a fabricated reading. A zero range (high == low, a flat
    bar) gives 0.5: there is no range to place the close in, so the close is neither high nor low in it. A missing
    column raises.

    WHY THIS CANNOT LEAK: it reads only the `high`, `low` and `close` of the last row of `data`, which is bar t. All
    three are known at bar t's close. It reads no other row.
    """

    def __init__(self, name="CloseLocationInRange", weight=1.0, parameters=None):
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
CloseLocationInRangeComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1523 passed, 8 skipped, 74 deselected, 2170 warnings in 53.69s ========
