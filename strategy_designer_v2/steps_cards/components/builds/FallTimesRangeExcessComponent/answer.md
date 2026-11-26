# FallTimesRangeExcessComponent: night7_steadydecline_run | 037-02_fall-range-beyond-loss-rebound_1d | FallTimesRangeExcessComponent

## attempt 1

answer: built
class: FallTimesRangeExcessComponent
settings: {}
reason: No catalogue component multiplies the day's close-to-close fall by the part of the bar's range that lies beyond that loss. The nearest is `RiseTimesRangeMultipleComponent` "down", and it multiplies the fall by the range over its mean, not by the excess range in percent of the prior close. This is one new measure computed from the coin's own close, high and low.

table: Directional components
row: | `FallTimesRangeExcessComponent` | none | F x E, F = max(0, close[t-1] − close[t]) / close[t-1] x 100, E = max(0, (high[t] − low[t]) − max(0, close[t-1] − close[t])) / close[t-1] x 100 | 0 and up, unbounded above, never negative; no direction. It is 0 on up days and flat days, and 0 when the bar's range does not exceed the closing loss (as after a gap down). It grows with the fall and with the range travelled beyond it | graded | percent x percent (fall in percent of the prior close x excess range in percent of the prior close) | 2 | close (bars t and t-1), high and low (bar t). A NaN in any value read gives NaN, whatever the sign of the move. A close[t-1] not above 0 gives NaN (never on real bars) | stateless. It is continuous in the prices and exactly 0 on every bar that did not close down. A gap down whose fall exceeds bar t's range reads 0. It ignores the open and the volume. One-sided, a fall-with-wide-range (rebound) reading. No `scaling_factor`: scale it with transforms |

```python class
class FallTimesRangeExcessComponent(SubStrategyComponent):
    """
    The day's closing loss times the range the bar travelled beyond that loss, both in percent of the prior close:

        L = max(0, close[t-1] - close[t])
        F = L / close[t-1] x 100
        E = max(0, (high[t] - low[t]) - L) / close[t-1] x 100
        raw_value = F x E

    Range and sign: 0 and up, unbounded above, never negative; no direction. It is 0 on up bars and flat bars,
    and 0 when the bar's range does not exceed the closing loss (a gap down). It grows with the fall and with the
    excess range. Continuous in the prices.
    Warm-up: 2 rows (bars t-1 and t).
    NaN: a NaN close[t], close[t-1], high[t] or low[t] gives NaN, whatever the sign of the move. A close[t-1] not
    above 0 gives NaN (never on real bars).

    WHY THIS CANNOT LEAK: it reads only close of the last two rows (bars t-1 and t) and high and low of the last
    row (bar t) of data; all are known at bar t's close.
    """

    def __init__(self, name="FallTimesRangeExcess", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c_prev = float(data["close"].iloc[-2])
        c_now = float(data["close"].iloc[-1])
        h = float(data["high"].iloc[-1])
        lo = float(data["low"].iloc[-1])
        if np.isnan(c_prev) or np.isnan(c_now) or np.isnan(h) or np.isnan(lo) or not c_prev > 0:
            self._raw_value = float("nan")
        else:
            loss = max(0.0, c_prev - c_now)
            fall_pct = loss / c_prev * 100.0
            excess_pct = max(0.0, (h - lo) - loss) / c_prev * 100.0
            self._raw_value = float(fall_pct * excess_pct)
            self.debug_info = {"fall_pct": fall_pct, "excess_range_pct": excess_pct}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return 2
```

```python hand
def hand(df, params):
    closes = [float(x) for x in list(df["close"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    prev = closes[t - 1]
    now = closes[t]
    hi = highs[t]
    lo = lows[t]
    for x in (prev, now, hi, lo):
        if x != x:
            return float("nan")
    if not prev > 0:
        return float("nan")
    drop = prev - now
    if drop < 0:
        drop = 0.0
    fall = drop / prev * 100.0
    beyond = (hi - lo) - drop
    if beyond < 0:
        beyond = 0.0
    beyond_pct = beyond / prev * 100.0
    return fall * beyond_pct
```

checks:
FallTimesRangeExcessComponent: every check passed
the bot's suite: == 1658 passed, 16 skipped, 75 deselected, 2244 warnings in 122.10s (0:02:02) ==
