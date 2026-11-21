# MeanBarRangeRatioComponent: night3_4h_run | 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b2_breakout-graded-by-quiet-week_4h | MeanBarRangeRatioComponent

## attempt 1

answer: built
class: MeanBarRangeRatioComponent
settings: {"long_period": 360, "short_period": 42}
reason: No component outputs a ratio of two mean bar ranges on its own. `NarrowRangeBreakoutRangeRatioComponent` contains L / Q only as one factor of a breakout product, and `RangeCompressionRatioComponent` puts the stretch max(high) − min(low) in its numerator, not a mean bar range. So a new class computes L / Q, the mean bar range over the long window divided by the mean bar range over the short window, both including bar t.

table: Regime measures
row: | `MeanBarRangeRatioComponent` | `long_period` (360), `short_period` (42) | L / Q, where L = mean(high[i] − low[i]) over the last `long_period` bars and Q = the same mean over the last `short_period` bars, bar t included in both | `short_period`/`long_period` (0.117 at the defaults) and up, unbounded above, never negative; no direction; 1 when the recent bars are as wide as the long average, above 1 as the recent bars get quieter, below 1 as they get wider | regime measure | dimensionless (ratio of mean bar ranges) | `long_period` (360) | high, low. A NaN high or low in the last `long_period` rows gives NaN. Q = 0 (`short_period` zero-range bars in a row, never seen on real bars) gives NaN. These settings raise when the component is built: `short_period` < 1, `short_period` >= `long_period` | stateless; graded and continuous in the highs and lows. It is the L / Q factor of `NarrowRangeBreakoutRangeRatioComponent` (`ratio_long_period`, `ratio_short_period`) on its own. The short window lies inside the long one, so the ratio is at least `short_period`/`long_period`. No `scaling_factor`: scale it with transforms |

```python class
class MeanBarRangeRatioComponent(SubStrategyComponent):
    """
    Long-run average bar range against the recent average bar range, on every bar:

        L = mean(high[i] - low[i]) for i = t - long_period + 1 .. t     (bar t included)
        Q = mean(high[i] - low[i]) for i = t - short_period + 1 .. t    (bar t included)
        raw_value = L / Q

    Range and sign: short_period / long_period and up, unbounded above, never negative, no direction. The short
    window lies inside the long one, so L >= Q x short_period / long_period. The value is 1 when the recent bars are
    as wide as the long average, grows as the recent bars get quieter, and falls below 1 as they get wider. Graded:
    continuous in the highs and lows.
    Warm-up: long_period rows, bar t included.

    NaN: a NaN high or low in the last long_period rows gives NaN. Q = 0 needs short_period zero-range bars in a
    row (never seen on real bars) and gives NaN. A missing column raises.
    Building the component raises for a short_period below 1 or a short_period at or above long_period.

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the last long_period rows of data, the last
    of which is bar t; a bar's high and low are known at that bar's close.
    """

    def __init__(self, name="MeanBarRangeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.long_period = int(self.parameters.get("long_period", 360))
        self.short_period = int(self.parameters.get("short_period", 42))
        if self.short_period < 1:
            raise ValueError(f"MeanBarRangeRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"MeanBarRangeRatioComponent: short_period must be below long_period, got "
                f"{self.short_period} >= {self.long_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).iloc[-self.long_period:].to_numpy()
        low = data['low'].astype(float).iloc[-self.long_period:].to_numpy()
        rng = high - low
        if np.isnan(rng).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        long_mean = float(rng.mean())
        short_mean = float(rng[-self.short_period:].mean())
        if not short_mean > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(long_mean / short_mean)
        self.confidence = 1.0
        self.debug_info = {'long_mean_range': long_mean, 'short_mean_range': short_mean}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.long_period
```

```python hand
def hand(df, params):
    lp = int(params.get("long_period", 360))
    sp = int(params.get("short_period", 42))
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    last = len(h) - 1
    long_sum = 0.0
    i = last - lp + 1
    while i <= last:
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
        long_sum = long_sum + (h[i] - l[i])
        i = i + 1
    short_sum = 0.0
    i = last - sp + 1
    while i <= last:
        short_sum = short_sum + (h[i] - l[i])
        i = i + 1
    L = long_sum / lp
    Q = short_sum / sp
    if not Q > 0:
        return float("nan")
    return L / Q
```

checks:
MeanBarRangeRatioComponent: every check passed
the bot's suite: ======= 1589 passed, 16 skipped, 75 deselected, 2244 warnings in 44.98s ========
