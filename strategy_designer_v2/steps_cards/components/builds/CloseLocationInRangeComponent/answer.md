# CloseLocationInRangeComponent: night9_chopmonth_run | 077-03_agitated-high-close-later-rise_1d | LaggedCloseLocationInRangeComponent

## attempt 1

answer: built
class: CloseLocationInRangeComponent
settings: {"reference": "low", "lag": 1}
reason: `CloseLocationInRangeComponent` (`reference` "low") computes this measure, but only on bar t. No config step delays a value, so the class is written again with a `lag` setting whose default 0 keeps today's output exactly.

table: Hedges and filters
row: | `CloseLocationInRangeComponent` | `reference` ("low"), `lag` (0) | with e = t − `lag`: `reference` "low": (close[e] − low[e]) / (high[e] − low[e]); `reference` "high": (high[e] − close[e]) / (high[e] − low[e]); 0.5 when high[e] = low[e] (either setting). With `lag` 1 and "low": (close[t-1] − low[t-1]) / (high[t-1] − low[t-1]) | 0 to 1, never negative; no sign. "low": 0 = close at bar e's low, 1 = at its high. "high": 0 = close at bar e's high, 1 = at its low. 0.5 at mid-range | graded | dimensionless (share of the bar's range) | `lag` + 1 (1) | high, low, close of bar e = t − `lag` only. A NaN in any of the three gives NaN; a zero range gives 0.5; a missing column raises. These settings raise when the component is built: `reference` other than "low" or "high", `lag` not an integer >= 0 | stateless; the shape of one bar only, no lookback. `lag` 0 (default) is the original output, unchanged. With `lag` above 0, bars after t − `lag` are not read, so the value at t is the `lag` 0 value at bar t − `lag`. No config step delays a value, hence the setting. "high" is 1 minus "low" (no config step gives 1 minus a value, hence that setting). Bounded in [0, 1] when the close lies inside [low, high], as on real bars. Ignores the open. No `scaling_factor`: scale it with transforms |

```python class
class CloseLocationInRangeComponent(SubStrategyComponent):
    """
    Where the close of one bar sits inside that bar's range, read lag bars back:

        e = t - lag                  (lag 0, the default: e = t, bar t itself)
        reference = "low" (default): raw_value = (close[e] - low[e]) / (high[e] - low[e])
        reference = "high":          raw_value = (high[e] - close[e]) / (high[e] - low[e])
        raw_value = 0.5 when high[e] == low[e] (either reference)

    With lag 1 and reference "low": (close[t-1] - low[t-1]) / (high[t-1] - low[t-1]), the prior bar's
    close location. lag 0 with either reference is the original output, unchanged.
    Range and sign: 0 to 1 when the close lies inside [low, high] (always on real bars), never negative,
    no direction. "low": 0 at the bar's low, 1 at its high. "high": 0 at the bar's high, 1 at its low.
    Graded and continuous in the close, high and low while the range is above 0.
    Warm-up: lag + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the high, low and close of the single row e = t - lag of the data
    (the row lag rows before the last one, the last one being bar t); no later row is read, and a bar's
    high, low and close are known at that bar's close.

    NaN: a NaN high, low or close on bar e gives NaN. A missing column raises.
    Building the component raises for a reference other than "low" or "high", or a lag that is not an
    integer >= 0.
    """

    def __init__(self, name="CloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        ref = self.parameters.get("reference", "low")
        if ref not in ("low", "high"):
            raise ValueError(f"CloseLocationInRangeComponent: reference must be 'low' or 'high', got {ref!r}")
        self.reference = ref
        lag = self.parameters.get("lag", 0)
        if isinstance(lag, bool):
            raise ValueError(f"CloseLocationInRangeComponent: lag must be an integer >= 0, got {lag!r}")
        try:
            lag_int = int(lag)
        except (TypeError, ValueError):
            raise ValueError(f"CloseLocationInRangeComponent: lag must be an integer >= 0, got {lag!r}")
        if lag_int != lag or lag_int < 0:
            raise ValueError(f"CloseLocationInRangeComponent: lag must be an integer >= 0, got {lag!r}")
        self.lag = lag_int
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        idx = len(data) - 1 - self.lag
        h = float(data['high'].iloc[idx])
        l = float(data['low'].iloc[idx])
        c = float(data['close'].iloc[idx])
        if np.isnan(h) or np.isnan(l) or np.isnan(c):
            value = float("nan")
        else:
            rng = h - l
            if rng == 0:
                value = 0.5
            elif self.reference == "high":
                value = (h - c) / rng
            else:
                value = (c - l) / rng
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'high': h, 'low': l, 'close': c, 'lag': self.lag, 'reference': self.reference}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.lag + 1
```

```python hand
def hand(df, params):
    ref = params.get("reference", "low")
    lag = int(params.get("lag", 0))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    e = t - lag
    h = highs[e]
    l = lows[e]
    c = closes[e]
    if h != h or l != l or c != c:
        return float("nan")
    width = h - l
    if width == 0:
        return 0.5
    if ref == "high":
        return (h - c) / width
    return (c - l) / width
```

checks:
CloseLocationInRangeComponent: every check passed
the bot's suite: == 1677 passed, 16 skipped, 75 deselected, 2244 warnings in 135.46s (0:02:15) ==
