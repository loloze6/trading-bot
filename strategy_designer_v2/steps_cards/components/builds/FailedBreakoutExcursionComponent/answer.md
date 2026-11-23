# FailedBreakoutExcursionComponent: short_1d_run | 029-05_failed-breakout-multiday-drift.d2_strong-breakout-failures-recover_1d | FailedBreakoutCloseExcursionComponent

## attempt 1

answer: built
class: FailedBreakoutExcursionComponent
settings: {"period": 20, "fail_window": 4, "peak_source": "close"}
reason: `FailedBreakoutExcursionComponent` already finds the same breakout bar j in t-3..t with H(j) = max(close[j-20..j-1]) and applies the same failure test, but its peak is always max(high[j..t]), never max(close[j..t]). A new setting `peak_source` adds the closing peak, which differs from the high peak on almost every real bar. Its default "high" keeps today's output unchanged.

table: Directional components
row: | `FailedBreakoutExcursionComponent` | `period` (20), `fail_window` (4), `peak_source` ("high") | (P − H(j)) / H(j) x 100 when close[t] < H(j), else 0. j is the most recent bar in t-`fail_window`+1 .. t (bar t included) with close[j] > H(j), where H(j) = max(close[j-`period`] .. close[j-1]). P = max(high[j .. t]) (`peak_source` "high") or max(close[j .. t]) (`peak_source` "close"). The output is 0 when no bar of the window broke out, or when close[t] >= H(j) for that most recent breakout (so 0 when bar t itself breaks out) | 0, or above 0 and unbounded above; never negative; no direction. When non-zero it is at least (close[j] − H(j)) / H(j) x 100 > 0, because P >= close[j]. It grows with the size of the push above the old high (intrabar with "high", on closes with "close") before the close fell back under it | graded | percent of the old high | `period` + `fail_window` (24) | close (last `period` + `fail_window` rows); with "high", also high (bars j .. t, read only for a failed breakout). A NaN close in those rows, or (with "high") a NaN high in bars j .. t, gives NaN. An H(j) not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `fail_window` < 1, `peak_source` other than "high" or "close" | stateless. `peak_source` "high" (default) is the original output, unchanged. "close" measures the breakout's highest close above the old high and reads closes only; no config step gives it, hence the setting. The breakout bar j and the failure test are those of `FailedBreakoutDepthComponent` (`period`, `fail_window`, `source` "close"). Because j >= t-`fail_window`+1, the peak window j .. t is always within j .. j+`fail_window`-1. A breakout needs a strictly higher close, and only the most recent breakout counts. The value is continuous in the highs (or the closes of j .. t). It jumps between 0 and the excursion where close[t] crosses H(j), and drops to 0 when the breakout leaves the window. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class FailedBreakoutExcursionComponent(SubStrategyComponent):
    """
    How far a breakout pushed above the old high before the close fell back under it:

        j = the most recent bar in t-fail_window+1 .. t (bar t included) with close[j] > H(j),
            H(j) = max(close[j-period] .. close[j-1])
        peak_source = "high" (default): P = max(high[j .. t])
        peak_source = "close":          P = max(close[j .. t])
        raw_value = (P - H(j)) / H(j) x 100   when close[t] < H(j)
        raw_value = 0                          when no bar of the window broke out, or close[t] >= H(j)

    Range: 0, or above 0 and unbounded above (at least (close[j] - H(j)) / H(j) x 100 when non-zero,
    since P >= close[j]); never negative; no direction. Graded: it grows linearly with the peak's
    distance above the old high. peak_source "high" is the original output, unchanged.
    Warm-up: period + fail_window rows, bar t included.

    NaN: a NaN close in the last period + fail_window rows gives NaN; with peak_source "high", a NaN
    high in bars j .. t (read only for a failed breakout) gives NaN; an H(j) not above 0 gives NaN
    (never on real bars). Building raises for period < 1, fail_window < 1, or a peak_source other
    than "high" or "close".

    WHY THIS CANNOT LEAK: it reads only the close of the last period + fail_window rows up to and
    including bar t (the last row of data), and with peak_source "high" the high of bars j .. t;
    every one of these is known at bar t's close.
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
        self.peak_source = self.parameters.get("peak_source", "high")
        if self.peak_source not in ("high", "close"):
            raise ValueError(
                f"FailedBreakoutExcursionComponent: peak_source must be 'high' or 'close', got {self.peak_source!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        close = data['close'].astype(float).to_numpy()[-n:]
        self.confidence = 1.0
        if np.isnan(close).any():
            self._raw_value = float("nan")
            return
        t = n - 1
        j = None
        h = None
        for jj in range(t, t - self.fail_window, -1):
            hj = float(np.max(close[jj - self.period:jj]))
            if close[jj] > hj:
                j = jj
                h = hj
                break
        if j is None:
            self._raw_value = 0.0
            return
        if not h > 0:
            self._raw_value = float("nan")
            return
        if close[t] >= h:
            self._raw_value = 0.0
            return
        if self.peak_source == "high":
            highs = data['high'].astype(float).to_numpy()[-n:][j:]
            if np.isnan(highs).any():
                self._raw_value = float("nan")
                return
            p = float(np.max(highs))
        else:
            p = float(np.max(close[j:]))
        self._raw_value = float((p - h) / h * 100.0)
        self.debug_info = {'breakout_offset': t - j, 'old_high': h, 'peak': p,
                           'peak_source': self.peak_source}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.fail_window
```

```python hand
def hand(df, params):
    period = int(params.get("period", 20))
    fw = int(params.get("fail_window", 4))
    src = params.get("peak_source", "high")
    c = [float(x) for x in list(df["close"])]
    hi = [float(x) for x in list(df["high"])]
    t = len(c) - 1
    # every close read: bars t-fw+1-period .. t
    for i in range(t - fw + 1 - period, t + 1):
        if c[i] != c[i]:
            return float("nan")
    j = -1
    old = 0.0
    for d in range(fw):
        cand = t - d
        best = c[cand - 1]
        for i in range(cand - period, cand):
            if c[i] > best:
                best = c[i]
        if c[cand] > best:
            j = cand
            old = best
            break
    if j < 0:
        return 0.0
    if not old > 0:
        return float("nan")
    if not c[t] < old:
        return 0.0
    peak = None
    for i in range(j, t + 1):
        v = hi[i] if src == "high" else c[i]
        if v != v:
            return float("nan")
        if peak is None or v > peak:
            peak = v
    return (peak - old) / old * 100.0
```

checks:
FailedBreakoutExcursionComponent: every check passed
the bot's suite: == 1634 passed, 16 skipped, 75 deselected, 2244 warnings in 77.01s (0:01:17) ===
