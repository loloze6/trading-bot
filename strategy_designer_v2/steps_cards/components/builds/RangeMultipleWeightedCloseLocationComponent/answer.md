# RangeMultipleWeightedCloseLocationComponent: night7c_panic_run | 032-02.b2.g1.d1_close-location-on-wide-days_1d | RangeMultipleWeightedCloseLocation

## attempt 1

answer: built
class: RangeMultipleWeightedCloseLocationComponent
settings: {"period": 20}
reason: No component multiplies the signed close location in bar t's range by bar t's range over its prior mean range. `VolumeWeightedCloseLocationComponent` weights the location by volume, and `RiseTimesRangeMultipleComponent` weights a rise by a range multiple whose mean includes bar t. So one new class computes this measure, with the base window as a setting.

table: Directional components
row: | `RangeMultipleWeightedCloseLocationComponent` | `period` (20) | loc x (high[t] − low[t]) / M. loc = 2 x (close[t] − low[t]) / (high[t] − low[t]) − 1, and loc = 0 when high[t] = low[t]. M = mean(high[i] − low[i]) over i = t-`period` .. t-1 (bar t excluded). On real bars this equals (2 x close[t] − high[t] − low[t]) / M | unbounded, signed. Positive when the close is in the upper half of bar t, negative in the lower half, 0 at mid-range or for a zero-range bar. On real bars its size is at most the range multiple (high[t] − low[t]) / M, which is unbounded above because bar t is excluded from its base. It grows as the close nears an extreme and as the day's range widens against the prior mean | graded | dimensionless (signed share of the bar's range x range multiple; equivalently 2 x (close − mid) in prior mean bar ranges) | `period` + 1 (21) | high, low (bars t-`period` .. t), close (bar t). A NaN in any value read gives NaN. M not above 0 gives NaN (`period` zero-range bars in a row, never seen on real bars). These settings raise when the component is built: `period` < 1 | stateless. The base excludes bar t, so bar t's own range cannot raise its base. Continuous in the prices while the range is above 0. Ignores the open and the volume. `negate` gives the reversal reading. Not `VolumeWeightedCloseLocationComponent` (a volume weight) and not `RiseTimesRangeMultipleComponent` (a rise, with bar t in the mean). No `scaling_factor`: scale it with transforms |

```python class
class RangeMultipleWeightedCloseLocationComponent(SubStrategyComponent):
    """
    Signed close location in bar t's range, weighted by bar t's range against the mean range of the prior bars:

        rng   = high[t] - low[t]
        loc   = 2 x (close[t] - low[t]) / rng - 1        (0 when rng = 0)
        M     = mean(high[i] - low[i]), i = t-period .. t-1   (bar t excluded)
        raw_value = loc x rng / M

    On real bars (low <= close <= high) this equals (2 x close[t] - high[t] - low[t]) / M.

    Range & sign: unbounded and signed. It is positive when the close is in the upper half of bar t, negative in
    the lower half, and 0 at mid-range or for a zero-range bar. Its size is at most rng / M on real bars. It grows
    as the close nears an extreme of the bar and as the day's range widens against the prior mean range.
    Graded, continuous in the prices while rng > 0.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN high, low or close among the values read gives NaN. An M not above 0 gives NaN (period zero-range
    bars in a row, never seen on real bars).
    Building the component raises for a period below 1.

    WHY THIS CANNOT LEAK: it reads high and low of bars t-period .. t and the close of bar t only, the last
    period + 1 rows of data, all known at bar t's close.
    """

    def __init__(self, name="RangeMultipleWeightedCloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(
                f"RangeMultipleWeightedCloseLocationComponent: period must be >= 1, got {self.period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        h = data["high"].astype(float).to_numpy()[-(p + 1):]
        l = data["low"].astype(float).to_numpy()[-(p + 1):]
        ct = float(data["close"].astype(float).iloc[-1])
        ht = float(h[-1])
        lt = float(l[-1])
        prior = h[:-1] - l[:-1]
        if np.isnan(ct) or np.isnan(ht) or np.isnan(lt) or np.isnan(prior).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        m = float(np.mean(prior))
        if not m > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rng = ht - lt
        loc = 2.0 * (ct - lt) / rng - 1.0 if rng > 0 else 0.0
        self._raw_value = float(loc * rng / m)
        self.confidence = 1.0
        self.debug_info = {"location": loc, "range": rng, "prior_mean_range": m}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    p = int(params.get("period", 20))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    c = closes[t]
    h = highs[t]
    lo = lows[t]
    if c != c or h != h or lo != lo:
        return float("nan")
    total = 0.0
    for i in range(t - p, t):
        hi_i = highs[i]
        lo_i = lows[i]
        if hi_i != hi_i or lo_i != lo_i:
            return float("nan")
        total = total + (hi_i - lo_i)
    mean_range = total / p
    if not mean_range > 0:
        return float("nan")
    width = h - lo
    if width > 0:
        location = 2.0 * (c - lo) / width - 1.0
    else:
        location = 0.0
    return location * (width / mean_range)
```

checks:
RangeMultipleWeightedCloseLocationComponent: every check passed
the bot's suite: == 1658 passed, 16 skipped, 75 deselected, 2244 warnings in 94.94s (0:01:34) ===
