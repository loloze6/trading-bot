# FailedBreakoutDepthInUsualMovesComponent: short_1d_run | 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d | FailedBreakoutVolScaledDepth

## attempt 1

answer: built
class: FailedBreakoutDepthInUsualMovesComponent
settings: {"period": 20, "fail_window": 3, "vol_period": 20, "exclude_current": 0, "lag": 0}
reason: `FailedBreakoutDepthInUsualMovesComponent` has the measure but not the wished window or delay. It searches for the breakout in t-`fail_window` .. t-1, which excludes bar t and has no `lag`, so its output differs on real bars wherever bar e breaks out or a breakout sits at bar e-`fail_window`. The class is rewritten with `exclude_current` (default 1, today's window) and `lag` (default 0, today's output), the same settings and meaning as `FailedBreakoutDepthComponent`. The plan sets `lag`; 0 is shown here.

table: Directional components
row: | `FailedBreakoutDepthInUsualMovesComponent` | `period` (20), `fail_window` (3), `vol_period` (20), `exclude_current` (1), `lag` (0) | max(0, H(j) − close[e]) / H(j) / s(e), with e = t − `lag`. j is the most recent bar with close[j] > H(j), searched in e-`fail_window` .. e-1 (`exclude_current` 1, bar e excluded) or in e-`fail_window`+1 .. e (`exclude_current` 0, bar e included). H(j) = max(close[j-`period`] .. close[j-1]). s(e) = std (ddof 1) of the `vol_period` one-bar returns close[i] / close[i-1] − 1, i = e-`vol_period`+1 .. e. The output is 0 when no bar of that window broke out, or when s(e) = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 when no breakout lies in the window, or when close[e] is at or above H(j). With `exclude_current` 0 it is also 0 when bar e itself breaks out. It grows linearly as close[e] sinks under the old high and as the recent volatility falls | graded | usual one-bar moves | max(`period` + `fail_window` + `exclude_current`, `vol_period` + 1) + `lag` (24) | closes only. A NaN close in bars t-(warmup)+1 .. t-`lag` gives NaN, and so does a close not above 0 there (never on real bars). s = 0 (flat return window, never on real bars) gives 0. Bars after t-`lag` are not read. These settings raise when the component is built: `period` < 1, `fail_window` < 1, `vol_period` < 2, `exclude_current` not 0 or 1, `lag` not an integer >= 0 | stateless. `exclude_current` 1 with `lag` 0 (the defaults) is the original output, unchanged. `exclude_current` 0 searches the breakout in e-`fail_window`+1 .. e, the window of `FailedBreakoutDepthComponent` `exclude_current` 0, so a breakout on bar e hides earlier ones and reads 0. `lag` delays the whole reading: the value at t is the `lag` 0 value at bar t-`lag`. No config step delays a value, hence the setting. It equals `FailedBreakoutDepthComponent` (`period`, `fail_window`, `source` "close", `reference` "prior_high", same `exclude_current`, `lag`) / 100 / s(e). A breakout needs a strictly higher close, and only the most recent breakout counts. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class FailedBreakoutDepthInUsualMovesComponent(SubStrategyComponent):
    """
    Depth of a failed breakout's re-entry close under the old closing high, in usual one-bar moves:

        e = t - lag
        j = the most recent bar with close[j] > H(j), searched in
            exclude_current = 1 (default): e - fail_window .. e - 1   (bar e excluded)
            exclude_current = 0:           e - fail_window + 1 .. e   (bar e included)
        H(j) = max(close[j - period] .. close[j - 1])
        s(e) = std (ddof 1) of the vol_period returns close[i] / close[i-1] - 1, i = e - vol_period + 1 .. e
        raw_value = max(0, H(j) - close[e]) / H(j) / s(e)
        raw_value = 0 when no bar of the window broke out, or when s(e) = 0

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 when close[e] >= H(j), and so 0
    when bar e itself breaks out with exclude_current 0. It grows linearly as close[e] sinks below the old high.
    exclude_current 1 with lag 0 (the defaults) is the original output, unchanged.
    Warm-up: max(period + fail_window + exclude_current, vol_period + 1) + lag rows, bar t included.

    NaN: a NaN close, or a close not above 0, among rows t - warmup + 1 .. e gives NaN.
    s(e) = 0 gives 0 (never on real bars).
    Building raises for period < 1, fail_window < 1, vol_period < 2, exclude_current not 0 or 1,
    or lag not an integer >= 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of rows t - warmup + 1 .. t - lag, all at or before
    bar t (the last row of data); no row after bar t - lag is read.
    """

    def __init__(self, name="FailedBreakoutDepthInUsualMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutDepthInUsualMovesComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutDepthInUsualMovesComponent: fail_window must be >= 1, got {self.fail_window}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"FailedBreakoutDepthInUsualMovesComponent: vol_period must be >= 2, got {self.vol_period}")
        ex = self.parameters.get("exclude_current", 1)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(
                f"FailedBreakoutDepthInUsualMovesComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        lag = self.parameters.get("lag", 0)
        if isinstance(lag, bool):
            raise ValueError(f"FailedBreakoutDepthInUsualMovesComponent: lag must be an integer >= 0, got {lag!r}")
        try:
            lag_int = int(lag)
        except (TypeError, ValueError):
            raise ValueError(f"FailedBreakoutDepthInUsualMovesComponent: lag must be an integer >= 0, got {lag!r}")
        if lag_int != lag or lag_int < 0:
            raise ValueError(f"FailedBreakoutDepthInUsualMovesComponent: lag must be an integer >= 0, got {lag!r}")
        self.lag = lag_int
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()
        n = len(c)
        e = n - 1 - self.lag
        req = self.get_required_periods()
        seg = c[n - req:e + 1]
        if np.isnan(seg).any() or (seg <= 0).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        x = self.exclude_current
        j_found = None
        h_found = None
        for j in range(e - x, e - x - self.fail_window, -1):
            h = float(np.max(c[j - self.period:j]))
            if c[j] > h:
                j_found = j
                h_found = h
                break
        rets = c[e - self.vol_period + 1:e + 1] / c[e - self.vol_period:e] - 1.0
        s = float(np.std(rets, ddof=1))
        if j_found is None or not s > 0:
            value = 0.0
        else:
            value = max(0.0, h_found - float(c[e])) / h_found / s
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'breakout_bar_offset': None if j_found is None else int(n - 1 - j_found),
                           'old_high': h_found, 'std': s, 'lag': self.lag,
                           'exclude_current': self.exclude_current}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period + self.fail_window + self.exclude_current, self.vol_period + 1) + self.lag
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    vp = int(params.get("vol_period", 20))
    ex = int(params.get("exclude_current", 1))
    lag = int(params.get("lag", 0))
    c = [float(v) for v in list(df["close"])]
    t = len(c) - 1
    e = t - lag
    need = max(p + fw + ex, vp + 1) + lag
    first = t - need + 1
    for i in range(first, e + 1):
        v = c[i]
        if v != v or not v > 0:
            return float("nan")
    # candidate breakout bars, newest first
    if ex == 1:
        cands = list(range(e - 1, e - fw - 1, -1))
    else:
        cands = list(range(e, e - fw, -1))
    old_high = None
    for j in cands:
        hi = c[j - 1]
        for k in range(j - p, j):
            if c[k] > hi:
                hi = c[k]
        if c[j] > hi:
            old_high = hi
            break
    # std (ddof 1) of the vp one-bar returns ending at e
    rets = []
    for i in range(e - vp + 1, e + 1):
        rets.append(c[i] / c[i - 1] - 1.0)
    mu = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var += (r - mu) * (r - mu)
    var = var / (len(rets) - 1)
    s = math.sqrt(var)
    if old_high is None or not s > 0:
        return 0.0
    depth = old_high - c[e]
    if depth < 0:
        depth = 0.0
    return depth / old_high / s
```

checks:
FailedBreakoutDepthInUsualMovesComponent: every check passed
the bot's suite: == 1631 passed, 16 skipped, 75 deselected, 2244 warnings in 79.13s (0:01:19) ===
