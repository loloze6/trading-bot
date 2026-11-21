# NarrowRangeBreakoutComponent: night3_4h_run | 019-03_upward-breakout-quiet-continuation_4h | NarrowRangeBreakoutComponent

## attempt 1

answer: built
class: NarrowRangeBreakoutComponent
settings: {"period": 12, "base_period": 180}
reason: No component gives the close's rise above the prior 12-bar high (in percent of close[t]) times the mean bar range over the 12-bar stretch's range. `DistanceFromHighComponent` divides by the high, not the close, and `RangeCompressionRatioComponent` gives the inverse factor with both windows sharing one end. This product of two measures is one new measure, so one new class computes it.

table: Directional components
row: | `NarrowRangeBreakoutComponent` | `period` (12), `base_period` (180) | max(0, close[t] − H) / close[t] x 100 x B / S, where H = max(high[t-`period`..t-1]), S = H − min(low[t-`period`..t-1]) and B = mean(high[i] − low[i]) over the last `base_period` bars, bar t included; 0.0 when S = 0 | 0 and up, unbounded above, never negative; no direction; 0 when the close is at or below the prior high; grows with the size of the breakout and with how narrow the stretch is against the average bar range | graded | percent of close x (mean bar ranges per stretch range) | max(`base_period`, `period` + 1) (180) | close, high, low. A NaN high or low in the last `base_period` rows or in the stretch, or a NaN close[t], gives NaN; a close[t] not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `base_period` < 1 | stateless. The stretch excludes bar t, so bar t's own move cannot widen it. B includes bar t. S = 0 needs `period` identical flat bars, and reads 0.0. Continuous in the close at the prior high. One-sided (an upward-breakout reading). No `scaling_factor`: scale it with transforms |

```python class
class NarrowRangeBreakoutComponent(SubStrategyComponent):
    """
    The close's breakout above a narrow prior stretch, on every bar:

        H = max(high[t-period .. t-1])                 (bar t excluded)
        S = H - min(low[t-period .. t-1])              (the stretch's range)
        B = mean(high[i] - low[i]), i = t-base_period+1 .. t   (bar t included)
        raw_value = max(0, close[t] - H) / close[t] x 100 x B / S
        raw_value = 0.0 when S = 0 (period identical flat bars)

    Range & sign: 0 and up, unbounded above, never negative, no direction. It is 0 when close[t] <= H, and it grows
    continuously with the breakout's size (percent of close[t]) and with the stretch's narrowness (average bar
    ranges per stretch range).
    Warm-up: max(base_period, period + 1) rows, bar t included (180 at the defaults).
    NaN: a NaN high or low in the stretch or in the last base_period rows, or a NaN close[t], gives NaN.
    A close[t] not above 0 also gives NaN (never on real bars).
    Building the component raises for a period below 1 or a base_period below 1.

    WHY THIS CANNOT LEAK: it reads only the high, low and close columns of the rows up to and including bar t (the
    last row of data): close[t], high and low of bars t-period .. t-1, and high and low of the last base_period
    rows. All of them are known at bar t's close.
    """

    def __init__(self, name="NarrowRangeBreakout", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 12))
        if self.period < 1:
            raise ValueError(f"NarrowRangeBreakoutComponent: period must be >= 1, got {self.period}")
        self.base_period = int(self.parameters.get("base_period", 180))
        if self.base_period < 1:
            raise ValueError(f"NarrowRangeBreakoutComponent: base_period must be >= 1, got {self.base_period}")
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
        p = self.period
        bp = self.base_period
        sh = high[-(p + 1):-1]
        sl = low[-(p + 1):-1]
        bh = high[-bp:]
        bl = low[-bp:]
        c = float(close[-1])
        if (np.isnan(sh).any() or np.isnan(sl).any() or np.isnan(bh).any() or np.isnan(bl).any()
                or np.isnan(c) or not c > 0):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        h_max = float(np.max(sh))
        s = h_max - float(np.min(sl))
        b = float(np.mean(bh - bl))
        brk = max(0.0, c - h_max) / c * 100.0
        if not s > 0:
            value = 0.0
        else:
            value = brk * b / s
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'prior_high': h_max, 'stretch_range': s, 'mean_bar_range': b, 'breakout_pct': brk}

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
    # prior stretch t-p .. t-1
    top = None
    bottom = None
    j = t - p
    while j <= t - 1:
        if hi[j] != hi[j] or lo[j] != lo[j]:
            return float("nan")
        if top is None or hi[j] > top:
            top = hi[j]
        if bottom is None or lo[j] < bottom:
            bottom = lo[j]
        j = j + 1
    # mean bar range over the last bp bars, bar t included
    total = 0.0
    j = t - bp + 1
    while j <= t:
        if hi[j] != hi[j] or lo[j] != lo[j]:
            return float("nan")
        total = total + (hi[j] - lo[j])
        j = j + 1
    mean_range = total / bp
    if not c > 0:
        return float("nan")
    stretch = top - bottom
    if not stretch > 0:
        return 0.0
    rise = c - top
    if rise < 0:
        rise = 0.0
    return rise / c * 100.0 * (mean_range / stretch)
```

checks:
NarrowRangeBreakoutComponent: every check passed
the bot's suite: ======= 1586 passed, 16 skipped, 75 deselected, 2244 warnings in 41.32s ========
