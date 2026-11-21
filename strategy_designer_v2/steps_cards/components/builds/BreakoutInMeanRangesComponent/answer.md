# BreakoutInMeanRangesComponent: night3_4h_run | 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h | BreakoutInMeanRangesComponent

## attempt 1

answer: built
class: BreakoutInMeanRangesComponent
settings: {"period": 12, "base_period": 180}
reason: No component measures how far the close breaks above the prior `period`-bar high in units of the average bar range. `NarrowRangeBreakoutComponent` measures a different quantity: the break in percent of the close, multiplied by B / S. `DistanceFromHighComponent` gives the break only in percent of the prior high. One new class therefore computes this measure.

table: Directional components
row: | `BreakoutInMeanRangesComponent` | `period` (12), `base_period` (180) | max(0, close[t] − H) / B, where H = max(high[t-`period`..t-1]) and B = mean(high[i] − low[i]) over the last `base_period` bars, bar t included; 0.0 when B = 0 | 0 and up, unbounded above, never negative; no direction; 0 when the close is at or below the prior high; grows linearly with the size of the break in average bar ranges | graded | mean bar ranges | max(`base_period`, `period` + 1) (180) | close, high, low. A NaN high in the stretch, a NaN high or low in the last `base_period` rows, or a NaN close[t] gives NaN. These settings raise when the component is built: `period` < 1, `base_period` < 1 | stateless. The stretch excludes bar t, so bar t's own move cannot raise H. B includes bar t. B = 0 needs `base_period` zero-range bars in a row and reads 0.0. Continuous in the close at the prior high. One-sided (an upward-breakout reading). Not `NarrowRangeBreakoutComponent`, which is the break in percent of the close x B / S. No `scaling_factor`: scale it with transforms |

```python class
class BreakoutInMeanRangesComponent(SubStrategyComponent):
    """
    The size of the close's break above the prior high, counted in average bar ranges, on every bar:

        H = max(high[t - period .. t - 1])                        (bar t excluded)
        B = mean(high[i] - low[i]) for i = t - base_period + 1 .. t  (bar t included)
        raw_value = max(0, close[t] - H) / B                      (0.0 when B = 0)

    Range & sign: 0 and up, unbounded above, never negative; no direction. It is 0 when the close is at or
    below the prior high, and it grows linearly with the break measured in average bar ranges.
    Warm-up: max(base_period, period + 1) rows, bar t included.

    NaN: a NaN high in the stretch, a NaN high or low in the last base_period rows, or a NaN close[t] gives
    NaN. B = 0 (base_period zero-range bars in a row) reads 0.0.
    Building the component raises for a period below 1 or a base_period below 1.

    WHY THIS CANNOT LEAK: it reads only the high, low and close columns of the rows up to and including bar t
    (the last row of data): the highs of rows t-period .. t-1, the highs and lows of the last base_period
    rows, and close[t]. All of these are known at bar t's close.
    """

    def __init__(self, name="BreakoutInMeanRanges", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 12))
        if self.period < 1:
            raise ValueError(f"BreakoutInMeanRangesComponent: period must be >= 1, got {self.period}")
        self.base_period = int(self.parameters.get("base_period", 180))
        if self.base_period < 1:
            raise ValueError(
                f"BreakoutInMeanRangesComponent: base_period must be >= 1, got {self.base_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        stretch_high = high[-(self.period + 1):-1]
        base_high = high[-self.base_period:]
        base_low = low[-self.base_period:]
        c = float(close[-1])
        if (np.isnan(stretch_high).any() or np.isnan(base_high).any() or np.isnan(base_low).any()
                or np.isnan(c)):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        prior_high = float(np.max(stretch_high))
        mean_range = float(np.mean(base_high - base_low))
        brk = max(0.0, c - prior_high)
        if mean_range > 0:
            self._raw_value = float(brk / mean_range)
        else:
            self._raw_value = 0.0
        self.confidence = 1.0
        self.debug_info = {'prior_high': prior_high, 'mean_bar_range': mean_range, 'break': brk}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.base_period, self.period + 1)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1
    c = cl[t]
    if c != c:
        return float("nan")
    # prior high over bars t-p .. t-1
    prior = None
    j = t - p
    while j <= t - 1:
        x = hi[j]
        if x != x:
            return float("nan")
        if prior is None or x > prior:
            prior = x
        j = j + 1
    # mean bar range over bars t-bp+1 .. t
    total = 0.0
    j = t - bp + 1
    while j <= t:
        a = hi[j]
        b = lo[j]
        if a != a or b != b:
            return float("nan")
        total = total + (a - b)
        j = j + 1
    mean_range = total / bp
    brk = c - prior
    if brk < 0:
        brk = 0.0
    if not mean_range > 0:
        return 0.0
    return brk / mean_range
```

checks:
BreakoutInMeanRangesComponent: every check passed
the bot's suite: ======= 1587 passed, 16 skipped, 75 deselected, 2244 warnings in 42.48s ========
