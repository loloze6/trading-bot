# FailedBreakoutVolumeRatioComponent: short_1d_run | 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d | FailedBreakoutThinVolumeComponent

## attempt 1

answer: built
class: FailedBreakoutVolumeRatioComponent
settings: {"period": 20, "fail_window": 3, "source": "close", "volume_period": 20, "form": "thin"}
reason: `FailedBreakoutVolumeRatioComponent` already computes r = volume[j] / mean(volume[j-19..j]) on exactly this failed breakout, but the wish wants max(0, 1 − r) on a failure and 0 otherwise. No config step gives 1 minus a value (and 1 − r would also read 1, not 0, where there is no failure), so the class is written again with a `form` setting whose default "ratio" keeps today's output.

table: Directional components
row: | `FailedBreakoutVolumeRatioComponent` | `period` (20), `fail_window` (3), `source` ("close"), `volume_period` (20), `form` ("ratio") | r = volume[j] / mean(volume[j-`volume_period`+1 .. j]). j is the most recent bar in t-`fail_window`+1 .. t (bar t included) with close[j] > H(j). H(j) = max(close[j-`period`] .. close[j-1]) (`source` "close") or max(high[j-`period`] .. high[j-1]) (`source` "high"). The output is computed only when close[t] < H(j), the breakout failed. `form` "ratio": r. `form` "thin": max(0, 1 − r). Both are 0 when no bar of the window broke out, or when close[t] >= H(j) for that most recent breakout (so 0 when bar t itself breaks out) | "ratio": 0, or above 0 up to `volume_period` (the mean includes volume[j]); 1 when the breakout bar's volume equals its average, larger the heavier it is. "thin": 0 to below 1; 0 when the breakout bar's volume is at or above its average, growing toward 1 as it thins. Never negative; no direction | graded | dimensionless ("ratio": ratio of volumes; "thin": 1 minus that ratio, clipped at 0) | max(`period` + `fail_window`, `volume_period` + `fail_window` − 1) (23) | "close": closes (last `period` + `fail_window` rows). "high": high (bars t-`period`-`fail_window`+1 .. t-1) and close (bars t-`fail_window`+1 .. t). A NaN in any of those gives NaN. Volume is read only for a failed breakout, over bars j-`volume_period`+1 .. j. A NaN there gives NaN, and so does a mean not above 0 (never on real bars). These settings raise when the component is built: `period` < 1, `fail_window` < 1, `volume_period` < 2, `source` other than "close" or "high", `form` other than "ratio" or "thin" | stateless. `form` "ratio" (default) is the original output, unchanged. "thin" is the thinness of the breakout bar's volume against its average. No config step gives 1 minus a value, hence the setting. The breakout bar j and the failure test are those of `FailedBreakoutDepthComponent` (same `period`, `fail_window`, `source`). A breakout needs a strictly higher close, and only the most recent breakout of the window counts. The value is continuous in the volumes. It jumps between 0 and its reading where close[t] crosses H(j), and drops to 0 when the breakout leaves the window. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class FailedBreakoutVolumeRatioComponent(SubStrategyComponent):
    """
    The volume of a failed breakout bar against its own average, on bar t:

        j = the most recent bar in t-fail_window+1 .. t (bar t included) with close[j] > H(j)
            source = "close" (default): H(j) = max(close[j-period] .. close[j-1])
            source = "high":            H(j) = max(high[j-period] .. high[j-1])
        failed breakout: such a j exists and close[t] < H(j)
        r = volume[j] / mean(volume[j-volume_period+1 .. j])
        form = "ratio" (default): raw_value = r
        form = "thin":            raw_value = max(0, 1 - r)
        raw_value = 0.0 when no bar of the window broke out, or when close[t] >= H(j)
        (so 0.0 when bar t itself breaks out).

    Range: "ratio" is 0, or above 0 up to volume_period (the mean includes volume[j]). "thin" is 0 to below 1:
    it is 0 when the breakout bar's volume is at or above its average and grows toward 1 as that volume thins.
    Both are never negative and have no direction. They are graded and continuous in the volumes.
    form "ratio" is the original output, unchanged.
    Warm-up: max(period + fail_window, volume_period + fail_window - 1) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only rows up to and including bar t (the last row of data). The closes
    (and highs) of bars t-period-fail_window+1 .. t and the volumes of bars j-volume_period+1 .. j are read,
    with j <= t. Each is known at its bar's close.

    NaN: a NaN close in the rows read (or a NaN high, with source "high") gives NaN. For a failed breakout,
    a NaN volume in bars j-volume_period+1 .. j, or a mean volume not above 0 (never on real bars), gives NaN.
    Building the component raises for period < 1, fail_window < 1, volume_period < 2, a source other than
    "close" or "high", or a form other than "ratio" or "thin".
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
        self.form = self.parameters.get("form", "ratio")
        if self.form not in ("ratio", "thin"):
            raise ValueError(
                f"FailedBreakoutVolumeRatioComponent: form must be 'ratio' or 'thin', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float).to_numpy()
        n = len(close)
        t = n - 1
        p = self.period
        fw = self.fail_window
        if self.source == "close":
            ref = close
            if np.isnan(close[n - p - fw:]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        else:
            ref = data['high'].astype(float).to_numpy()
            if np.isnan(ref[t - p - fw + 1:t]).any() or np.isnan(close[t - fw + 1:]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        j = None
        h_j = None
        for cand in range(t, t - fw, -1):
            h = float(np.max(ref[cand - p:cand]))
            if close[cand] > h:
                j = cand
                h_j = h
                break
        if j is None or not close[t] < h_j:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {'breakout_bar': j, 'prior_high': h_j}
            return
        vol = data['volume'].astype(float).to_numpy()
        win = vol[j - self.volume_period + 1:j + 1]
        if np.isnan(win).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        m = float(np.mean(win))
        if not m > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = float(vol[j] / m)
        if self.form == "thin":
            self._raw_value = float(max(0.0, 1.0 - r))
        else:
            self._raw_value = r
        self.confidence = 1.0
        self.debug_info = {'breakout_bar': j, 'prior_high': h_j, 'volume_ratio': r, 'form': self.form}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period + self.fail_window, self.volume_period + self.fail_window - 1)
```

```python hand
def hand(df, params):
    period = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    vp = int(params.get("volume_period", 20))
    source = params.get("source", "close")
    form = params.get("form", "ratio")
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    if source == "high":
        hi = [float(x) for x in list(df["high"])]
        read = [hi[i] for i in range(t - period - fw + 1, t)] + [c[i] for i in range(t - fw + 1, t + 1)]
        ref = hi
    else:
        read = [c[i] for i in range(t - period - fw + 1, t + 1)]
        ref = c
    for x in read:
        if x != x:
            return float("nan")
    # most recent breakout bar: newest first
    j = -1
    H = None
    k = t
    while k >= t - fw + 1:
        top = ref[k - period]
        for i in range(k - period, k):
            if ref[i] > top:
                top = ref[i]
        if c[k] > top:
            j = k
            H = top
            break
        k = k - 1
    if j < 0:
        return 0.0
    if c[t] >= H:
        return 0.0
    total = 0.0
    for i in range(j - vp + 1, j + 1):
        if v[i] != v[i]:
            return float("nan")
        total = total + v[i]
    mean_v = total / vp
    if not mean_v > 0:
        return float("nan")
    ratio = v[j] / mean_v
    if form == "thin":
        thin = 1.0 - ratio
        return thin if thin > 0.0 else 0.0
    return ratio
```

checks:
FailedBreakoutVolumeRatioComponent: every check passed
the bot's suite: == 1631 passed, 16 skipped, 75 deselected, 2244 warnings in 80.46s (0:01:20) ===
