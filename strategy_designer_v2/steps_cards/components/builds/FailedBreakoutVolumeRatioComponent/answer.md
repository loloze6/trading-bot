# FailedBreakoutVolumeRatioComponent: short_1d_run | 029-02_breakout-volume-trapped-decline_1d | FailedBreakoutVolumeRatio

## attempt 1

answer: built
class: FailedBreakoutVolumeRatioComponent
settings: {"period": 20, "fail_window": 3, "source": "high", "volume_period": 20}
reason: No component of the catalogue reads the volume of an event-selected bar. `FailedBreakoutDepthComponent` finds the same breakout bar j but measures price depth, and `VolumeRatioComponent` lags its windows by a fixed number of bars, not to the breakout bar. This new class takes the breakout bar j of `FailedBreakoutDepthComponent` and returns volume[j] / mean(volume[j-19 .. j]) while that breakout has failed.

table: Directional components
row: | `FailedBreakoutVolumeRatioComponent` | `period` (20), `fail_window` (3), `source` ("close"), `volume_period` (20) | volume[j] / mean(volume[j-`volume_period`+1 .. j]). j is the most recent bar in t-`fail_window`+1 .. t (bar t included) with close[j] > H(j). H(j) = max(close[j-`period`] .. close[j-1]) (`source` "close") or max(high[j-`period`] .. high[j-1]) (`source` "high"). The output is computed only when close[t] < H(j), the breakout failed. It is 0 when no bar of the window broke out, or when close[t] >= H(j) for that most recent breakout (so 0 when bar t itself breaks out) | 0, or above 0 up to `volume_period` (the mean includes volume[j]); never negative; no direction; 1 when the breakout bar's volume equals its `volume_period`-bar average, larger the heavier the breakout bar's volume | graded | dimensionless (ratio of volumes) | max(`period` + `fail_window`, `volume_period` + `fail_window` − 1) (23) | "close": closes (last `period` + `fail_window` rows). "high": high (bars t-`period`-`fail_window`+1 .. t-1) and close (bars t-`fail_window`+1 .. t). A NaN in any of those gives NaN. Volume is read only for a failed breakout, over bars j-`volume_period`+1 .. j: a NaN there gives NaN, and so does a mean not above 0 (never on real bars). These settings raise when the component is built: `period` < 1, `fail_window` < 1, `volume_period` < 2, `source` other than "close" or "high" | stateless. The breakout bar j and the failure test are those of `FailedBreakoutDepthComponent` (same `period`, `fail_window`, `source`): this component is non-zero exactly where that one is above 0. A breakout needs a strictly higher close, and only the most recent breakout of the window counts. The value is continuous in the volumes. It jumps between 0 and the ratio where close[t] crosses H(j), and drops to 0 when the breakout leaves the window. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class FailedBreakoutVolumeRatioComponent(SubStrategyComponent):
    """
    Volume of the most recent failed breakout bar against its own average:

        j = the most recent bar in t-fail_window+1 .. t (bar t included) with close[j] > H(j)
        H(j) = max(close[j-period] .. close[j-1])   (source "close", default)
             = max(high[j-period] .. high[j-1])     (source "high")
        failed: close[t] < H(j)
        raw_value = volume[j] / mean(volume[j-volume_period+1 .. j])   when a breakout exists and failed
        raw_value = 0.0                                                otherwise (no breakout in the window,
                                                                       or close[t] >= H(j), e.g. bar t breaks out)

    Range: 0, or above 0 up to volume_period (the mean includes volume[j]); never negative; no direction.
    It is 1 when the breakout bar's volume equals its volume_period-bar average and grows with that volume.
    Graded in the volumes. It jumps between 0 and the ratio where close[t] crosses H(j).
    Warm-up: max(period + fail_window, volume_period + fail_window - 1) rows, bar t included (23 at the defaults).

    NaN: "close": a NaN close in the last period + fail_window rows gives NaN. "high": a NaN high in bars
    t-period-fail_window+1 .. t-1, or a NaN close in bars t-fail_window+1 .. t, gives NaN. For a failed breakout,
    a NaN volume in bars j-volume_period+1 .. j, or a mean volume not above 0, gives NaN.
    Building raises for period < 1, fail_window < 1, volume_period < 2, or a source other than "close" or "high".

    WHY THIS CANNOT LEAK: it reads only the close, high and volume of rows up to and including bar t (the last row
    of data). Every bar j tested is at or before t, its H(j) uses bars before j, and its volume window ends at j.
    """

    def __init__(self, name="FailedBreakoutVolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutVolumeRatioComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutVolumeRatioComponent: fail_window must be >= 1, got {self.fail_window}")
        self.volume_period = int(self.parameters.get("volume_period", 20))
        if self.volume_period < 2:
            raise ValueError(
                f"FailedBreakoutVolumeRatioComponent: volume_period must be >= 2, got {self.volume_period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high"):
            raise ValueError(
                f"FailedBreakoutVolumeRatioComponent: source must be 'close' or 'high', got {self.source!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data["close"].astype(float).to_numpy()
        n = len(c)
        t = n - 1
        P, F, VP = self.period, self.fail_window, self.volume_period
        if self.source == "high":
            ref = data["high"].astype(float).to_numpy()
            if np.isnan(ref[n - P - F:n - 1]).any() or np.isnan(c[n - F:]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        else:
            ref = c
            if np.isnan(c[n - P - F:]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        j_found = None
        h_old = None
        for j in range(t, t - F, -1):
            hj = float(np.max(ref[j - P:j]))
            if c[j] > hj:
                j_found = j
                h_old = hj
                break
        if j_found is None or not (c[t] < h_old):
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {"breakout_bar": j_found, "old_high": h_old}
            return
        v = data["volume"].astype(float).to_numpy()
        w = v[j_found - VP + 1:j_found + 1]
        if np.isnan(w).any():
            self._raw_value = float("nan")
        else:
            m = float(np.mean(w))
            self._raw_value = float(v[j_found] / m) if m > 0 else float("nan")
        self.confidence = 1.0
        self.debug_info = {"breakout_bar": j_found, "old_high": h_old, "bars_ago": t - j_found}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + self.fail_window, self.volume_period + self.fail_window - 1)
```

```python hand
def hand(df, params):
    period = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    vp = int(params.get("volume_period", 20))
    source = params.get("source", "close")
    close = [float(x) for x in list(df["close"])]
    vol = [float(x) for x in list(df["volume"])]
    if source == "high":
        ref = [float(x) for x in list(df["high"])]
    else:
        ref = close
    t = len(close) - 1

    def isnan(x):
        return x != x

    # rows needed for the breakout tests
    if source == "high":
        for i in range(t - period - fw + 1, t):
            if isnan(ref[i]):
                return float("nan")
        for i in range(t - fw + 1, t + 1):
            if isnan(close[i]):
                return float("nan")
    else:
        for i in range(t - period - fw + 1, t + 1):
            if isnan(close[i]):
                return float("nan")

    # the most recent breakout bar of the window
    found = -1
    old_high = None
    k = 0
    while k < fw:
        j = t - k
        hi = ref[j - period]
        for i in range(j - period, j):
            if ref[i] > hi:
                hi = ref[i]
        if close[j] > hi:
            found = j
            old_high = hi
            break
        k = k + 1
    if found < 0:
        return 0.0
    if not (close[t] < old_high):
        return 0.0

    # volume of the breakout bar against its own vp-bar mean
    total = 0.0
    for i in range(found - vp + 1, found + 1):
        if isnan(vol[i]):
            return float("nan")
        total = total + vol[i]
    mean_v = total / vp
    if not mean_v > 0:
        return float("nan")
    return vol[found] / mean_v
```

checks:
FailedBreakoutVolumeRatioComponent: every check passed
the bot's suite: == 1629 passed, 16 skipped, 75 deselected, 2244 warnings in 78.49s (0:01:18) ===
