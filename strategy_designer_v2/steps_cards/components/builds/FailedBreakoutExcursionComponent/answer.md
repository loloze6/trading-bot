# FailedBreakoutExcursionComponent: short_1d_run | 029-04_breakout-extension-failure-decline_1d | failed-breakout excursion

## attempt 1

answer: built
class: FailedBreakoutExcursionComponent
settings: {"period": 20, "fail_window": 4}
reason: No component of the catalogue measures how far a failed breakout pushed above the old high. `FailedBreakoutDepthComponent` uses the same breakout bar but measures the close's depth below the level, and `FailedBreakoutVolumeRatioComponent` measures the breakout bar's volume. The excursion above H is a different measure, so it gets a new class.

table: Directional components
row: | `FailedBreakoutExcursionComponent` | `period` (20), `fail_window` (4) | (P − H(j)) / H(j) x 100 when close[t] < H(j), else 0. j is the most recent bar in t-`fail_window`+1 .. t (bar t included) with close[j] > H(j), where H(j) = max(close[j-`period`] .. close[j-1]). P = max(high[j .. t]), the highest high from the breakout bar to bar t. The output is 0 when no bar of the window broke out, or when close[t] >= H(j) for that most recent breakout (so 0 when bar t itself breaks out) | 0, or above 0 and unbounded above; never negative; no direction. When non-zero it is at least (close[j] − H(j)) / H(j) x 100 > 0, because high[j] >= close[j]. It grows with the size of the push above the old high before the close fell back under it | graded | percent of the old high | `period` + `fail_window` (24) | close (last `period` + `fail_window` rows), high (bars j .. t, read only for a failed breakout). A NaN close in those rows, or a NaN high in bars j .. t, gives NaN. An H(j) not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `fail_window` < 1 | stateless. The breakout bar j and the failure test are those of `FailedBreakoutDepthComponent` (`period`, `fail_window`, `source` "close"). Because j >= t-`fail_window`+1, the high window j .. t is always within j .. j+`fail_window`-1. A breakout needs a strictly higher close, and only the most recent breakout counts. The value is continuous in the highs. It jumps between 0 and the excursion where close[t] crosses H(j), and drops to 0 when the breakout leaves the window. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class FailedBreakoutExcursionComponent(SubStrategyComponent):
    """
    How far a recent breakout pushed above the old closing high before failing back under it:

        j = the most recent bar in t-fail_window+1 .. t (bar t included) with close[j] > H(j),
            H(j) = max(close[j-period] .. close[j-1])
        P = max(high[j .. t])
        raw_value = (P - H(j)) / H(j) x 100   when close[t] < H(j)
        raw_value = 0.0                        when no bar of the window broke out, or close[t] >= H(j)

    Range: 0, or above 0 and unbounded above. It is never negative and has no direction. When non-zero it is
    at least (close[j] - H(j)) / H(j) x 100 > 0, because high[j] >= close[j].
    Units: percent of the old high. Graded: it grows with the size of the failed push above the old high.
    Warm-up: period + fail_window rows, bar t included.

    NaN: a NaN close in the last period + fail_window rows gives NaN. For a failed breakout, a NaN high in
    bars j .. t gives NaN, and so does an H(j) not above 0 (never on real bars).
    Building the component raises for a period below 1 or a fail_window below 1.

    WHY THIS CANNOT LEAK: it reads only the close of the last period + fail_window rows and the high of
    bars j .. t, all at or before bar t (the last row of data); bar t's high and close are known at its close.
    """

    def __init__(self, name="FailedBreakoutExcursion", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutExcursionComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 4))
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutExcursionComponent: fail_window must be >= 1, got {self.fail_window}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n_rows = self.get_required_periods()
        close = data["close"].astype(float).to_numpy()[-n_rows:]
        high_all = data["high"].astype(float).to_numpy()[-n_rows:]
        self.confidence = 1.0
        if np.isnan(close).any():
            self._raw_value = float("nan")
            return
        t = n_rows - 1
        j = None
        h_level = None
        for cand in range(t, t - self.fail_window, -1):
            h = float(np.max(close[cand - self.period:cand]))
            if close[cand] > h:
                j = cand
                h_level = h
                break
        if j is None:
            self.debug_info = {"breakout": False}
            return
        if not close[t] < h_level:
            self.debug_info = {"breakout": True, "failed": False, "H": h_level}
            return
        highs = high_all[j:t + 1]
        if np.isnan(highs).any() or not h_level > 0:
            self._raw_value = float("nan")
            return
        p = float(np.max(highs))
        self._raw_value = float((p - h_level) / h_level * 100.0)
        self.debug_info = {"breakout": True, "failed": True, "H": h_level, "P": p,
                           "bars_since_breakout": t - j}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + self.fail_window
```

```python hand
def hand(df, params):
    period = int(params.get("period", 20))
    fw = int(params.get("fail_window", 4))
    c = [float(x) for x in list(df["close"])]
    hi = [float(x) for x in list(df["high"])]
    t = len(c) - 1
    # every close that can be read: bars t-fw+1-period .. t
    for i in range(t - fw + 1 - period, t + 1):
        if c[i] != c[i]:
            return float("nan")
    # most recent breakout bar, searched from bar t backwards
    found = None
    level = None
    for b in range(t, t - fw, -1):
        prior = c[b - period]
        for i in range(b - period, b):
            if c[i] > prior:
                prior = c[i]
        if c[b] > prior:
            found = b
            level = prior
            break
    if found is None:
        return 0.0
    if c[t] >= level:
        return 0.0
    peak = None
    for i in range(found, t + 1):
        if hi[i] != hi[i]:
            return float("nan")
        if peak is None or hi[i] > peak:
            peak = hi[i]
    if not level > 0:
        return float("nan")
    return (peak - level) / level * 100.0
```

checks:
FailedBreakoutExcursionComponent: every check passed
the bot's suite: == 1630 passed, 16 skipped, 75 deselected, 2244 warnings in 79.45s (0:01:19) ===
