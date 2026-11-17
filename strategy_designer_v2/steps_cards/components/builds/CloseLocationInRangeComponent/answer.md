# CloseLocationInRangeComponent: night_run | 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.g1_falls-closing-near-low-bounce_1d | CloseLocationComponent

## attempt 1

answer: built
class: CloseLocationInRangeComponent
settings: {"reference": "high"}
reason: `CloseLocationInRangeComponent` gives (close − low) / (high − low), and the wish is 1 minus that. Under rule 1 this is the same measure. No config step gives 1 minus a value (`negate` gives the negative, and `standardise` does not centre), so the class is written again with a `reference` setting. Its default "low" keeps today's output exactly, and "high" gives (high − close) / (high − low), which differs on every real bar whose close is not at mid-range.

table: Hedges and filters
row: | `CloseLocationInRangeComponent` | `reference` ("low") | `reference` "low": (close[t] − low[t]) / (high[t] − low[t]); `reference` "high": (high[t] − close[t]) / (high[t] − low[t]); 0.5 when high[t] = low[t] (either setting) | 0 to 1, never negative; no sign. "low": 0 = close at the bar's low, 1 = at its high. "high": 0 = close at the bar's high, 1 = at its low (grows as the close nears the low). 0.5 at mid-range | graded | dimensionless (share of the bar's range) | 1 | high, low, close of bar t only. A NaN in any of the three gives NaN; a zero range gives 0.5; a missing column raises; a `reference` other than "low" or "high" raises when the component is built | stateless; the shape of the current bar only, no lookback. "high" is 1 minus "low" (no config step gives 1 minus a value, hence the setting). Bounded in [0, 1] when the close lies inside [low, high], as on real bars. Ignores the open. No `scaling_factor`: scale it with transforms |

```python class
class CloseLocationInRangeComponent(SubStrategyComponent):
    """
    Where the current bar's close sits inside the bar's own range, measured from one end:

        reference = "low" (default): raw_value = (close[t] - low[t]) / (high[t] - low[t])
        reference = "high":          raw_value = (high[t] - close[t]) / (high[t] - low[t])
        high[t] == low[t] (zero range): raw_value = 0.5 with either reference

    The default "low" is the original output: 0 when the close is at the bar's low, 1 at its high.
    Setting "high" gives 1 minus that: 0 when the close is at the bar's high, growing to 1 as the close
    nears the bar's low.
    Graded. The value lies in 0 to 1 and is never negative when the close lies inside [low, high], as it does
    on real bars. It has no sign. It is 0.5 at mid-range.
    Warm-up: 1 row (bar t only).

    WHY THIS CANNOT LEAK: it reads only the `high`, `low` and `close` values of the last row of data (bar t),
    all of which are known at bar t's close; no earlier or later row is read.

    NaN: a NaN high, low or close on bar t gives NaN. A zero range gives 0.5, because there is no range to
    place the close in. A missing column raises.
    Building the component raises for a reference other than "low" or "high".
    """

    def __init__(self, name="CloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        ref = self.parameters.get("reference", "low")
        if ref not in ("low", "high"):
            raise ValueError(
                f"CloseLocationInRangeComponent: reference must be 'low' or 'high', got {ref!r}")
        self.reference = ref
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        h = float(data['high'].iloc[-1])
        l = float(data['low'].iloc[-1])
        c = float(data['close'].iloc[-1])
        if np.isnan(h) or np.isnan(l) or np.isnan(c):
            self._raw_value = float("nan")
        else:
            rng = h - l
            if rng == 0:
                self._raw_value = 0.5
            elif self.reference == "high":
                self._raw_value = float((h - c) / rng)
            else:
                self._raw_value = float((c - l) / rng)
        self.confidence = 1.0
        self.debug_info = {'high': h, 'low': l, 'close': c, 'reference': self.reference}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1
```

```python hand
def hand(df, params):
    ref = params.get("reference", "low")
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    h = highs[len(highs) - 1]
    l = lows[len(lows) - 1]
    c = closes[len(closes) - 1]
    if h != h or l != l or c != c:
        return float("nan")
    if h == l:
        return 0.5
    if ref == "high":
        distance = h - c
    else:
        distance = c - l
    return distance / (h - l)
```

checks:
CloseLocationInRangeComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1534 passed, 8 skipped, 74 deselected, 2170 warnings in 65.68s (0:01:05) ===
