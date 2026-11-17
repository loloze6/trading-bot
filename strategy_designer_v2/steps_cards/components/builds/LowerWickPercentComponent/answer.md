# LowerWickPercentComponent: night_012_run | 012-01_liquidation-flush-rebound_1d | LowerWickComponent

## attempt 1

answer: built
class: LowerWickPercentComponent
settings: {}
reason: `LowerWickShareComponent` divides the lower wick by the bar's range (high − low), which is a different measure. No component divides the lower wick by the close to give a percent of price, so a new class computes (min(open, close) − low) / close × 100 from bar t's own open, low and close.

table: Hedges and filters
row: | `LowerWickPercentComponent` | none | (min(open[t], close[t]) − low[t]) / close[t] x 100 | 0 and up, unbounded, never negative on real bars; no direction; 0 = no lower wick, larger as the wick below the body lengthens | graded | percent of price | 1 | open, low, close of bar t only. A NaN in any of the three gives NaN; a missing column raises | stateless; the shape of the current bar only, no lookback. Unlike `LowerWickShareComponent` (wick / range), this is the wick against the price level, so a long wick on a narrow-range day still reads small. For a regime rule ("a lower wick of more than 3 percent") or as a forecast source after transforms; no `scaling_factor` |

```python class
class LowerWickPercentComponent(SubStrategyComponent):
    """
    The current bar's lower wick as a percent of its close, on every bar:

        raw_value = (min(open[t], close[t]) - low[t]) / close[t] x 100

    Graded and non-negative on real bars (the low is at or below both the open and the close): 0 when the body's
    bottom is the bar's low (no lower wick), growing continuously as the wick below the body lengthens; unbounded
    above (in practice below 100). No direction. Warm-up: 1 bar (bar t only).

    WHY THIS CANNOT LEAK: it reads only the `open`, `low` and `close` of the last row (bar t), all known at bar t's
    close; no earlier or later row is used.

    NaN: a NaN open, low or close on bar t gives NaN (propagated, never turned into 0). A missing column raises.
    Real closes are positive, so the division is always defined on real data.
    """

    def __init__(self, name="LowerWickPercent", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        o = float(data['open'].iloc[-1])
        l = float(data['low'].iloc[-1])
        c = float(data['close'].iloc[-1])
        if np.isnan(o) or np.isnan(l) or np.isnan(c) or c == 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float((min(o, c) - l) / c * 100.0)
        self.confidence = 1.0
        self.debug_info = {'open': o, 'low': l, 'close': c}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1
```

```python hand
def hand(df, params):
    import math
    o = list(df["open"])[-1]
    l = list(df["low"])[-1]
    c = list(df["close"])[-1]
    if any(isinstance(x, float) and math.isnan(x) for x in (o, l, c)) or c == 0:
        return float("nan")
    body_bottom = o if o < c else c
    return (body_bottom - l) / c * 100.0
```

checks:
LowerWickPercentComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1522 passed, 8 skipped, 74 deselected, 2170 warnings in 52.68s ========
