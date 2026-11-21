# NarrowRangeBreakoutRangeRatioComponent: night3_4h_run | 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h | QuietWeekNarrowRangeBreakoutComponent

## attempt 1

answer: built
class: NarrowRangeBreakoutRangeRatioComponent
settings: {"period": 12, "base_period": 180, "ratio_long_period": 360, "ratio_short_period": 42}
reason: No component computes the product of `NarrowRangeBreakoutComponent`'s reading and the ratio of the long mean bar range to the short one. No component computes that range ratio either: `RangeCompressionRatioComponent` puts a max-min stretch over its base, not a mean bar range. So one new class computes the combined measure.

table: Directional components
row: | `NarrowRangeBreakoutRangeRatioComponent` | `period` (12), `base_period` (180), `ratio_long_period` (360), `ratio_short_period` (42) | max(0, close[t] − H) / close[t] x 100 x B / S x L / Q, where H = max(high[t-`period`..t-1]), S = H − min(low[t-`period`..t-1]), and B, L, Q = mean(high[i] − low[i]) over the last `base_period`, `ratio_long_period` and `ratio_short_period` bars, bar t included. It is 0.0 when S = 0 or Q = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 when the close is at or below the prior high. It grows with the size of the breakout, with how narrow the stretch is against the average bar range, and with how quiet the recent bars are against the long average (L / Q above 1 when recent bars are smaller) | graded | percent of close x (mean bar ranges per stretch range) x (ratio of mean bar ranges) | max(`base_period`, `period` + 1, `ratio_long_period`) (360) | close, high, low. A NaN high or low in the stretch or in the last max(`base_period`, `ratio_long_period`) rows, or a NaN close[t], gives NaN. A close[t] not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `base_period` < 1, `ratio_short_period` < 1, `ratio_short_period` >= `ratio_long_period` | stateless. Equals `NarrowRangeBreakoutComponent` (same `period`, `base_period`) x mean bar range over `ratio_long_period` / mean bar range over `ratio_short_period`. The stretch excludes bar t; B, L and Q include it. Q = 0 needs `ratio_short_period` zero-range bars in a row and reads 0.0. One-sided (an upward-breakout reading). No `scaling_factor`: scale it with transforms |

```python class
class NarrowRangeBreakoutRangeRatioComponent(SubStrategyComponent):
    """
    A narrow-range upward breakout, weighted by how quiet the recent bars are against the long average bar range:

        H = max(high[t-period .. t-1])                  (the stretch, bar t excluded)
        S = H - min(low[t-period .. t-1])
        B = mean(high[i] - low[i]) over the last base_period bars, bar t included
        L = mean(high[i] - low[i]) over the last ratio_long_period bars, bar t included
        Q = mean(high[i] - low[i]) over the last ratio_short_period bars, bar t included
        raw_value = max(0, close[t] - H) / close[t] x 100 x B / S x L / Q
        raw_value = 0.0 when S = 0 or Q = 0

    This equals NarrowRangeBreakoutComponent(period, base_period) x L / Q.
    Range and sign: 0 and up, unbounded above, never negative, no direction. It is 0 when the close is at or below
    the prior high. It grows with the size of the break, the narrowness of the stretch, and the quietness of the
    last ratio_short_period bars against the last ratio_long_period bars.
    Graded: continuous in the close at the prior high.
    Warm-up: max(base_period, period + 1, ratio_long_period) rows, bar t included (360 at the defaults).

    NaN: a NaN high or low in any row read, or a NaN close[t], gives NaN. A close[t] not above 0 gives NaN.
    Building the component raises for a period, base_period or ratio_short_period below 1, and for a
    ratio_short_period at or above ratio_long_period.

    WHY THIS CANNOT LEAK: it reads only the high, low and close columns of the last
    max(base_period, period + 1, ratio_long_period) rows of data, bar t (the last row) included. The stretch uses
    rows t-period .. t-1. Every value it reads is known at bar t's close.
    """

    def __init__(self, name="NarrowRangeBreakoutRangeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 12))
        self.base_period = int(self.parameters.get("base_period", 180))
        self.ratio_long_period = int(self.parameters.get("ratio_long_period", 360))
        self.ratio_short_period = int(self.parameters.get("ratio_short_period", 42))
        if self.period < 1:
            raise ValueError(f"NarrowRangeBreakoutRangeRatioComponent: period must be >= 1, got {self.period}")
        if self.base_period < 1:
            raise ValueError(
                f"NarrowRangeBreakoutRangeRatioComponent: base_period must be >= 1, got {self.base_period}")
        if self.ratio_short_period < 1:
            raise ValueError(
                f"NarrowRangeBreakoutRangeRatioComponent: ratio_short_period must be >= 1, "
                f"got {self.ratio_short_period}")
        if self.ratio_short_period >= self.ratio_long_period:
            raise ValueError(
                f"NarrowRangeBreakoutRangeRatioComponent: ratio_short_period must be below ratio_long_period, "
                f"got {self.ratio_short_period} and {self.ratio_long_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data["high"].astype(float).to_numpy()
        low = data["low"].astype(float).to_numpy()
        close_t = float(data["close"].astype(float).to_numpy()[-1])
        p = self.period
        st_h = high[-(p + 1):-1]
        st_l = low[-(p + 1):-1]
        rng = high - low
        b_win = rng[-self.base_period:]
        l_win = rng[-self.ratio_long_period:]
        q_win = rng[-self.ratio_short_period:]
        if (np.isnan(close_t) or np.isnan(st_h).any() or np.isnan(st_l).any()
                or np.isnan(b_win).any() or np.isnan(l_win).any() or np.isnan(q_win).any()):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if not close_t > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(np.max(st_h))
        S = H - float(np.min(st_l))
        B = float(np.mean(b_win))
        L = float(np.mean(l_win))
        Q = float(np.mean(q_win))
        brk = max(0.0, close_t - H)
        if S <= 0 or Q <= 0:
            value = 0.0
        else:
            value = brk / close_t * 100.0 * B / S * L / Q
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"prior_high": H, "stretch_range": S, "base_mean_range": B,
                           "long_mean_range": L, "short_mean_range": Q}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.base_period, self.period + 1, self.ratio_long_period)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    lp = int(params.get("ratio_long_period", 360))
    sp = int(params.get("ratio_short_period", 42))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    c = closes[last]
    if c != c:
        return float("nan")

    stretch_h = []
    stretch_l = []
    i = last - p
    while i <= last - 1:
        stretch_h.append(highs[i])
        stretch_l.append(lows[i])
        i = i + 1

    def mean_range(n):
        total = 0.0
        j = last - n + 1
        while j <= last:
            r = highs[j] - lows[j]
            if r != r:
                return float("nan")
            total = total + r
            j = j + 1
        return total / n

    for x in stretch_h + stretch_l:
        if x != x:
            return float("nan")
    B = mean_range(bp)
    L = mean_range(lp)
    Q = mean_range(sp)
    if B != B or L != L or Q != Q:
        return float("nan")
    if not c > 0:
        return float("nan")

    H = stretch_h[0]
    for x in stretch_h:
        if x > H:
            H = x
    lo = stretch_l[0]
    for x in stretch_l:
        if x < lo:
            lo = x
    S = H - lo
    if S <= 0 or Q <= 0:
        return 0.0
    brk = c - H
    if brk < 0:
        brk = 0.0
    return brk / c * 100.0 * (B / S) * (L / Q)
```

checks:
NarrowRangeBreakoutRangeRatioComponent: every check passed
the bot's suite: ======= 1588 passed, 16 skipped, 75 deselected, 2244 warnings in 41.57s ========
