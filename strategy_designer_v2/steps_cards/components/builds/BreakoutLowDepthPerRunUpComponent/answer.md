# BreakoutLowDepthPerRunUpComponent: short_1d_run | 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d | QuietBaseFailedBreakoutDepth

## attempt 1

answer: built
class: BreakoutLowDepthPerRunUpComponent
settings: {"period": 20, "fail_window": 3, "rise_period": 20}
reason: `FailedBreakoutDepthComponent` (`source` "high", `reference` "breakout_low") gives the depth of the close under the breakout bar's low, but no component divides that depth by 1 plus the 20-bar rise into bar j. That product of the depth and a run-up discount is a measure of its own, so one new class computes it.

table: Directional components
row: | `BreakoutLowDepthPerRunUpComponent` | `period` (20), `fail_window` (3), `rise_period` (20) | max(0, low[j] − close[t]) / low[j] x 100 / (1 + max(0, close[j] / close[j-`rise_period`] − 1) x 100). j is the most recent bar in t-`fail_window`+1 .. t (bar t included) with close[j] > H(j), where H(j) = max(high[j-`period`] .. high[j-1]). The output is 0 when no bar of the window broke out | 0 to below 100, never negative; no direction. It is 0 when no breakout lies in the window, or when close[t] is at or above low[j] (so 0 when bar t itself is the breakout). It grows linearly as the close sinks under the breakout bar's low, and grows as the rise into bar j shrinks (the divisor is 1 for a flat or falling run-up) | graded | percent of the breakout bar's low per (1 + run-up in percent) | max(`period`, `rise_period`) + `fail_window` (23) | high (bars t-`fail_window`-`period`+1 .. t-1), close (bars t-`fail_window`+1 .. t, and close[j-`rise_period`] of the chosen bar), low (low[j] of the chosen bar). A NaN in any of those gives NaN. A low[j] or close[j-`rise_period`] not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `fail_window` < 1, `rise_period` < 1 | stateless. The breakout bar j is that of `FailedBreakoutDepthComponent` (`period`, `fail_window`, `source` "high", `exclude_current` 0). The first factor is that component with `reference` "breakout_low". A breakout needs a strictly higher close than the prior highs, and only the most recent breakout counts. Continuous in close[t] while the same breakout stays the most recent. It jumps when that breakout leaves the window or a newer one appears. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class BreakoutLowDepthPerRunUpComponent(SubStrategyComponent):
    """
    Depth of the close under the low of the most recent breakout bar, discounted by the rise into that bar:

        H(j) = max(high[j - period] .. high[j - 1])              (bar j excluded)
        j    = the most recent bar in t - fail_window + 1 .. t with close[j] > H(j)
        D    = max(0, low[j] - close[t]) / low[j] x 100
        U    = max(0, close[j] / close[j - rise_period] - 1) x 100
        raw_value = D / (1 + U)
        raw_value = 0.0 when no bar of the window broke out.

    Range: 0 to below 100, never negative, no direction. It is 0 with no breakout in the window, or when
    close[t] >= low[j] (so 0 when bar t itself breaks out). It grows as the close sinks below the breakout
    bar's low and as the run-up into bar j shrinks (U = 0 for a flat or falling run-up). Graded.
    Warm-up: max(period, rise_period) + fail_window rows, bar t included.

    NaN: a NaN high in bars t-fail_window-period+1 .. t-1, a NaN close in bars t-fail_window+1 .. t, or a
    NaN low[j] or close[j - rise_period] for the chosen bar gives NaN. A low[j] or close[j - rise_period]
    not above 0 gives NaN (never on real bars).
    Building the component raises for period < 1, fail_window < 1 or rise_period < 1.

    WHY THIS CANNOT LEAK: it reads only high, low and close of rows up to and including bar t (the last row
    of data): highs of bars t-fail_window-period+1 .. t-1, closes of bars t-fail_window+1 .. t, and low[j],
    close[j - rise_period] with j <= t; every value is known at its bar's close.
    """

    def __init__(self, name="BreakoutLowDepthPerRunUp", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"BreakoutLowDepthPerRunUpComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(
                f"BreakoutLowDepthPerRunUpComponent: fail_window must be >= 1, got {self.fail_window}")
        self.rise_period = int(self.parameters.get("rise_period", 20))
        if self.rise_period < 1:
            raise ValueError(
                f"BreakoutLowDepthPerRunUpComponent: rise_period must be >= 1, got {self.rise_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].to_numpy(dtype=float)
        low = data['low'].to_numpy(dtype=float)
        close = data['close'].to_numpy(dtype=float)
        t = len(close) - 1
        p, fw, rp = self.period, self.fail_window, self.rise_period
        hs = high[t - fw - p + 1:t]
        cs = close[t - fw + 1:t + 1]
        self.confidence = 1.0
        if np.isnan(hs).any() or np.isnan(cs).any():
            self._raw_value = float("nan")
            return
        j = None
        for cand in range(t, t - fw, -1):
            h_prior = float(np.max(high[cand - p:cand]))
            if close[cand] > h_prior:
                j = cand
                break
        if j is None:
            self._raw_value = 0.0
            self.debug_info = {'breakout_bar': None}
            return
        lj = float(low[j])
        base = float(close[j - rp])
        if np.isnan(lj) or np.isnan(base) or not lj > 0 or not base > 0:
            self._raw_value = float("nan")
            return
        depth = max(0.0, lj - float(close[t])) / lj * 100.0
        rise = max(0.0, float(close[j]) / base - 1.0) * 100.0
        self._raw_value = float(depth / (1.0 + rise))
        self.debug_info = {'breakout_bar_offset': t - j, 'breakout_low': lj, 'depth_pct': depth,
                           'run_up_pct': rise}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.rise_period) + self.fail_window
```

```python hand
def hand(df, params):
    p = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    rp = int(params.get("rise_period", 20))
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1

    def isnan(x):
        return x != x

    # every high that can enter a prior-high window, every close that can be a breakout close
    for i in range(t - fw - p + 1, t):
        if isnan(hi[i]):
            return float("nan")
    for i in range(t - fw + 1, t + 1):
        if isnan(cl[i]):
            return float("nan")

    # most recent breakout bar, scanning back from bar t
    j = -1
    k = 0
    while k < fw:
        b = t - k
        prior = hi[b - p]
        for i in range(b - p, b):
            if hi[i] > prior:
                prior = hi[i]
        if cl[b] > prior:
            j = b
            break
        k = k + 1
    if j < 0:
        return 0.0

    level = lo[j]
    start = cl[j - rp]
    if isnan(level) or isnan(start) or not level > 0 or not start > 0:
        return float("nan")
    gap = level - cl[t]
    if gap < 0:
        gap = 0.0
    depth = gap / level * 100.0
    run = cl[j] / start - 1.0
    if run < 0:
        run = 0.0
    run = run * 100.0
    return depth / (1.0 + run)
```

checks:
BreakoutLowDepthPerRunUpComponent: every check passed
the bot's suite: == 1632 passed, 16 skipped, 75 deselected, 2244 warnings in 81.36s (0:01:21) ===
