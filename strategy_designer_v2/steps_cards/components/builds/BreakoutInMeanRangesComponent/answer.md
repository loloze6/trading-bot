# BreakoutInMeanRangesComponent: night3_4h_run | 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e2_pullback-inside-rising-week_4h | PullbackInMeanRangesComponent

## attempt 1

answer: built
class: BreakoutInMeanRangesComponent
settings: {"period": 12, "base_period": 180, "side": "below"}
reason: The wish is the same measure as `BreakoutInMeanRangesComponent`, the close's distance from the prior 12-bar high in mean bar ranges, read on the side below the high instead of above it. No config step gives it: `negate` of max(0, close − H) is −max(0, close − H), and the part below the high has already been zeroed. So the whole class is written again with a `side` setting, and its default "above" keeps today's output exactly.

table: Directional components
row: | `BreakoutInMeanRangesComponent` | `period` (12), `base_period` (180), `side` ("above") | `side` "above": max(0, close[t] − H) / B. `side` "below": max(0, H − close[t]) / B. H = max(high[t-`period`..t-1]) and B = mean(high[i] − low[i]) over the last `base_period` bars, bar t included; 0.0 when B = 0 | 0 and up, unbounded above, never negative; no direction. "above": 0 when the close is at or below the prior high, growing linearly with the size of the break. "below": 0 when the close is at or above the prior high, growing linearly as the close sits deeper below it | graded | mean bar ranges | max(`base_period`, `period` + 1) (180) | close, high, low. A NaN high in the stretch, a NaN high or low in the last `base_period` rows, or a NaN close[t] gives NaN. These settings raise when the component is built: `period` < 1, `base_period` < 1, `side` other than "above" or "below" | stateless. `side` "above" (default) is the original output, unchanged. "below" is the pullback under the prior high, and no config step gives it (negate of the clipped break is not it), hence the setting. The stretch excludes bar t, so bar t's own move cannot change H. B includes bar t. B = 0 needs `base_period` zero-range bars in a row and reads 0.0. Continuous in the close at the prior high. Not `NarrowRangeBreakoutComponent`, which is the break in percent of the close x B / S. No `scaling_factor`: scale it with transforms |

```python class
class BreakoutInMeanRangesComponent(SubStrategyComponent):
    """
    The close's distance from the prior stretch's highest high, in average bar ranges, on one side of it:

        H = max(high[t - period .. t - 1])                     (bar t excluded)
        B = mean(high[i] - low[i]) for i = t - base_period + 1 .. t   (bar t included)
        side = "above" (default): raw_value = max(0, close[t] - H) / B
        side = "below":           raw_value = max(0, H - close[t]) / B
        raw_value = 0.0 when B = 0

    Range and sign: 0 and up, unbounded above, never negative; no direction. "above" is 0 when the close is at or
    below the prior high and grows linearly with the size of the break. "below" is 0 when the close is at or above
    the prior high and grows linearly as the close sits deeper below it. Units: mean bar ranges. Graded and
    continuous in the close at H. The default "above" is the original output, unchanged.
    Warm-up: max(base_period, period + 1) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads the `high` column of rows t-period .. t-1, the `high` and `low` columns of the
    last base_period rows (up to and including bar t, the last row of data), and close[t]. All of these are known at
    bar t's close.

    NaN: a NaN high in the stretch, a NaN high or low in the last base_period rows, or a NaN close[t] gives NaN.
    Building the component raises for a period below 1, a base_period below 1, or a side other than "above" or
    "below".
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
        side = self.parameters.get("side", "above")
        if side not in ("above", "below"):
            raise ValueError(f"BreakoutInMeanRangesComponent: side must be 'above' or 'below', got {side!r}")
        self.side = side
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
        stretch = high[-(self.period + 1):-1]
        base_h = high[-self.base_period:]
        base_l = low[-self.base_period:]
        c = float(close[-1])
        if np.isnan(stretch).any() or np.isnan(base_h).any() or np.isnan(base_l).any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        h = float(stretch.max())
        b = float(np.mean(base_h - base_l))
        gap = (c - h) if self.side == "above" else (h - c)
        if b == 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float(max(0.0, gap) / b)
        self.confidence = 1.0
        self.debug_info = {'prior_high': h, 'mean_bar_range': b, 'side': self.side}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.base_period, self.period + 1)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    last = len(cl) - 1
    c = cl[last]
    if c != c:
        return float("nan")
    prior_high = None
    i = last - p
    while i <= last - 1:
        if hi[i] != hi[i]:
            return float("nan")
        if prior_high is None or hi[i] > prior_high:
            prior_high = hi[i]
        i = i + 1
    total = 0.0
    i = last - bp + 1
    while i <= last:
        if hi[i] != hi[i] or lo[i] != lo[i]:
            return float("nan")
        total = total + (hi[i] - lo[i])
        i = i + 1
    mean_range = total / bp
    if mean_range == 0:
        return 0.0
    if side == "below":
        dist = prior_high - c
    else:
        dist = c - prior_high
    if dist < 0:
        dist = 0.0
    return dist / mean_range
```

checks:
BreakoutInMeanRangesComponent: every check passed
the bot's suite: ======= 1588 passed, 16 skipped, 75 deselected, 2244 warnings in 43.47s ========
