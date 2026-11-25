# RangeInReturnStdComponent: night7_panic_run | 037-01_falling-market-wide-day-decline_1d | RangeInReturnStdComponent

## attempt 1

answer: built
class: RangeInReturnStdComponent
settings: {"vol_period": 30}
reason: No component divides bar t's range by the std of the one-bar returns. `CloseLocationTimesVolatilityComponent` multiplies a location by that std, and `RiseTimesRangeMultipleComponent` scales the range by the mean bar range, so a new class is needed for the bar's range as a share of the close, counted in usual one-bar return swings.

table: Hedges and filters
row: | `RangeInReturnStdComponent` | `vol_period` (30) | (high[t] − low[t]) / close[t] / s, s being the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included; 0.0 when s = 0 | 0 and up, unbounded above, never negative on real bars; no direction; 0 for a zero-range bar, grows as the day's range widens against the usual one-bar return swing | graded | usual one-bar moves (bar range as a fraction of the close, over the std of simple returns) | `vol_period` + 1 (31) | high, low of bar t; closes (last `vol_period` + 1 rows). A NaN in any value read gives NaN; a close not above 0 among those read gives NaN (never on real bars). s = 0 (a flat return window, never on real bars) gives 0.0. These settings raise when the component is built: `vol_period` < 2 | stateless. Continuous in the highs, lows and closes. Ignores the open and the volume. It is the bar's range in percent of the close divided by 100 x s, so it is not `RiseTimesRangeMultipleComponent`, whose base is the mean bar range. No `scaling_factor`: scale it with transforms |

```python class
class RangeInReturnStdComponent(SubStrategyComponent):
    """
    The current bar's range, as a share of its close, counted in usual one-bar return swings:

        r[j] = close[j] / close[j-1] - 1,   j = t - vol_period + 1 .. t   (bar t's return included)
        s    = std (ddof 1) of those vol_period returns
        raw_value = (high[t] - low[t]) / close[t] / s        (0.0 when s = 0)

    Range & sign: 0 and up, unbounded above, never negative on real bars (high >= low, close > 0); no direction.
    It is 0 for a zero-range bar and grows as the bar's range widens against the recent return swing.
    Warm-up: vol_period + 1 rows, bar t included (31 at the default).
    NaN: a NaN high or low on bar t, or a NaN close in the last vol_period + 1 rows, gives NaN; a close not above 0
    among those rows gives NaN (never on real bars). s = 0 (a flat return window, never on real bars) gives 0.0.
    Building the component raises for a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads high and low of bar t (the last row of data) and the closes of the last
    vol_period + 1 rows, all known at bar t's close; no later row exists in data.
    """

    def __init__(self, name="RangeInReturnStd", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 30))
        if self.vol_period < 2:
            raise ValueError(f"RangeInReturnStdComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.vol_period
        closes = data["close"].astype(float).to_numpy()[-(n + 1):]
        high_t = float(data["high"].iloc[-1])
        low_t = float(data["low"].iloc[-1])
        if np.isnan(closes).any() or np.isnan(high_t) or np.isnan(low_t):
            self._raw_value = float("nan")
        elif not (closes > 0).all():
            self._raw_value = float("nan")
        else:
            rets = closes[1:] / closes[:-1] - 1.0
            s = float(np.std(rets, ddof=1))
            if s == 0.0:
                self._raw_value = 0.0
            else:
                self._raw_value = float((high_t - low_t) / closes[-1] / s)
            self.debug_info = {"range_frac": (high_t - low_t) / closes[-1], "ret_std": s}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.vol_period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("vol_period", 30))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    hi = h[t]
    lo = l[t]
    if hi != hi or lo != lo:
        return float("nan")
    used = c[t - n:t + 1]
    for x in used:
        if x != x:
            return float("nan")
        if not x > 0:
            return float("nan")
    rets = []
    for j in range(t - n + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - mean) * (r - mean)
    s = math.sqrt(ss / (len(rets) - 1))
    if s == 0.0:
        return 0.0
    return (hi - lo) / c[t] / s
```

checks:
RangeInReturnStdComponent: every check passed
the bot's suite: == 1658 passed, 16 skipped, 75 deselected, 2244 warnings in 114.58s (0:01:54) ==
