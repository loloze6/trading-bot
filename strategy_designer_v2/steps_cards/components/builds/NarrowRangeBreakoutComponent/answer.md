# NarrowRangeBreakoutComponent: night3_4h_run | 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins.b1_quiet-breakdown-in-downtrend_4h | NarrowRangeBreakdownComponent

## attempt 1

answer: built
class: NarrowRangeBreakoutComponent
settings: {"period": 12, "base_period": 180, "side": "below"}
reason: The wished value is the downward mirror of `NarrowRangeBreakoutComponent`. It is the break of the close below the prior 12-bar low, in percent of the close, times B / S. That is not the negative of the upward break, and no config step gives it, so it is the same measure with a new `side` setting whose default "above" keeps today's output exactly. `BreakoutInMeanRangesComponent` "below" is not it: that reads H − close against the prior high and divides only by B.

table: Directional components
row: | `NarrowRangeBreakoutComponent` | `period` (12), `base_period` (180), `side` ("above") | `side` "above": max(0, close[t] − H) / close[t] x 100 x B / S. `side` "below": max(0, L − close[t]) / close[t] x 100 x B / S. H = max(high[t-`period`..t-1]), L = min(low[t-`period`..t-1]), S = H − L, and B = mean(high[i] − low[i]) over the last `base_period` bars, bar t included. It is 0.0 when S = 0 | 0 and up, unbounded above, never negative; no direction. "above" is 0 when the close is at or below the prior high. "below" is 0 when the close is at or above the prior low. Both grow with the size of the break and with how narrow the stretch is against the average bar range | graded | percent of close x (mean bar ranges per stretch range) | max(`base_period`, `period` + 1) (180) | close, high, low. A NaN high or low in the last `base_period` rows or in the stretch, or a NaN close[t], gives NaN. A close[t] not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `base_period` < 1, `side` other than "above" or "below" | stateless. `side` "above" (default) is the original output, unchanged. "below" is the downward breakdown below the prior low; no config step gives it (negate of the upward break is not it), hence the setting. Use `negate` on "below" for a short-side forecast. The stretch excludes bar t, so bar t's own move cannot widen it. B includes bar t. S = 0 needs `period` identical flat bars and reads 0.0. Continuous in the close at the prior extreme. Not `BreakoutInMeanRangesComponent` "below", which is H − close in mean bar ranges. No `scaling_factor`: scale it with transforms |

```python class
class NarrowRangeBreakoutComponent(SubStrategyComponent):
    """
    A break out of a narrow stretch, scaled by how narrow the stretch is, on every bar:

        stretch = bars t-period .. t-1                      (bar t excluded)
        H = max(high over the stretch), L = min(low over the stretch), S = H - L
        B = mean(high[i] - low[i]) over the last base_period bars, bar t included
        side = "above" (default): brk = max(0, close[t] - H)
        side = "below":           brk = max(0, L - close[t])
        raw_value = brk / close[t] x 100 x B / S            (0.0 when S = 0)

    Range & sign: 0 and up, unbounded above, never negative; no direction. "above" is 0 when the close is at or
    below the prior high. "below" is 0 when the close is at or above the prior low. Both grow with the size of
    the break and with how narrow the stretch is against the average bar range. side "above" is the original
    output, unchanged; use `negate` on "below" for a short-side forecast.
    Warm-up: max(base_period, period + 1) rows, bar t included.
    NaN: a NaN high or low in the stretch or in the last base_period rows, or a NaN close[t], gives NaN. A
    close[t] not above 0 gives NaN (never on real bars). S = 0 (period identical flat bars) gives 0.0.
    Building the component raises for a period below 1, a base_period below 1, or a side other than "above"
    or "below".

    WHY THIS CANNOT LEAK: it reads only the high, low and close of the rows up to and including bar t (the last
    row of data): highs and lows of the last max(base_period, period + 1) rows and the close of bar t, all known
    at bar t's close.
    """

    def __init__(self, name="NarrowRangeBreakout", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 12))
        if self.period < 1:
            raise ValueError(f"NarrowRangeBreakoutComponent: period must be >= 1, got {self.period}")
        self.base_period = int(self.parameters.get("base_period", 180))
        if self.base_period < 1:
            raise ValueError(f"NarrowRangeBreakoutComponent: base_period must be >= 1, got {self.base_period}")
        side = self.parameters.get("side", "above")
        if side not in ("above", "below"):
            raise ValueError(f"NarrowRangeBreakoutComponent: side must be 'above' or 'below', got {side!r}")
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
        close_t = float(data['close'].astype(float).to_numpy()[-1])
        sh = high[-(self.period + 1):-1]
        sl = low[-(self.period + 1):-1]
        bh = high[-self.base_period:]
        bl = low[-self.base_period:]
        if (np.isnan(sh).any() or np.isnan(sl).any() or np.isnan(bh).any() or np.isnan(bl).any()
                or np.isnan(close_t)):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if not close_t > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        hi = float(np.max(sh))
        lo = float(np.min(sl))
        s = hi - lo
        b = float(np.mean(bh - bl))
        if s == 0:
            value = 0.0
            brk = 0.0
        else:
            if self.side == "below":
                brk = max(0.0, lo - close_t)
            else:
                brk = max(0.0, close_t - hi)
            value = brk / close_t * 100.0 * b / s
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'prior_high': hi, 'prior_low': lo, 'stretch_range': s,
                           'mean_bar_range': b, 'break': brk, 'side': self.side}

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
    hs = [float(x) for x in list(df["high"])]
    ls = [float(x) for x in list(df["low"])]
    cs = [float(x) for x in list(df["close"])]
    t = len(cs) - 1
    c = cs[t]
    # the stretch: bars t-p .. t-1
    st_h = []
    st_l = []
    i = t - p
    while i <= t - 1:
        st_h.append(hs[i])
        st_l.append(ls[i])
        i = i + 1
    # the base: bars t-bp+1 .. t
    ranges = []
    nan_seen = False
    i = t - bp + 1
    while i <= t:
        if hs[i] != hs[i] or ls[i] != ls[i]:
            nan_seen = True
        ranges.append(hs[i] - ls[i])
        i = i + 1
    for x in st_h + st_l:
        if x != x:
            nan_seen = True
    if c != c:
        nan_seen = True
    if nan_seen:
        return float("nan")
    if not c > 0:
        return float("nan")
    top = st_h[0]
    for x in st_h:
        if x > top:
            top = x
    bottom = st_l[0]
    for x in st_l:
        if x < bottom:
            bottom = x
    s = top - bottom
    if s == 0:
        return 0.0
    total = 0.0
    for r in ranges:
        total = total + r
    b = total / len(ranges)
    if side == "below":
        depth = bottom - c
    else:
        depth = c - top
    if depth < 0:
        depth = 0.0
    return depth / c * 100.0 * b / s
```

checks:
NarrowRangeBreakoutComponent: every check passed
the bot's suite: ======= 1588 passed, 16 skipped, 75 deselected, 2244 warnings in 41.86s ========
