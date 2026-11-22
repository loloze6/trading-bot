# FlatnessWeightedRangePositionComponent: night4_range_run | 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.d1_reversion-only-near-zero-net-move_1d | FlatnessWeightedRangePositionHighLow

## attempt 1

answer: built
class: FlatnessWeightedRangePositionComponent
settings: {"period": 30, "source": "high_low"}
reason: `FlatnessWeightedRangePositionComponent` computes this measure, but it takes H and L from the closes only, and a range from the bars' highs and lows changes its output on real data. So the whole class is written again with a `source` setting whose default "close" keeps today's output exactly. "high_low" takes H = max(high) and L = min(low) over the last `period` bars.

table: Directional components
row: | `FlatnessWeightedRangePositionComponent` | `period` (30), `source` ("close") | (2 x pos − 1) x (1 − abs(close[t] − close[t-`period`]) / (H − L)), pos = (close[t] − L) / (H − L), over bars t-`period`+1 .. t. `source` "close": H, L = highest and lowest close. `source` "high_low": H = max(high), L = min(low). 0.0 when H = L | unbounded below. It is at most 1 in size whenever close[t-`period`] lies inside [L, H], which holds more often with "high_low" because the range is wider. Signed: positive above the window's middle, negative below it, 0 at the middle or for a zero range. Its size grows with the distance from the middle and with the flatness. The flatness factor turns negative when close[t-`period`] lies outside [L, H] by more than the range allows, which flips the sign | graded | dimensionless (position x flatness) | `period` + 1 (31) | "close": closes only (last `period` + 1 rows). "high_low": high and low (last `period` rows), close[t] and close[t-`period`]. A NaN in any value read gives NaN. A zero range gives 0.0. These settings raise when the component is built: `period` < 2, `source` other than "close" or "high_low" | stateless. `source` "close" (default) is the original output, unchanged. "high_low" equals `DonchianBreakoutComponent` (`period`, `sf` 1, `source` "high_low") x (1 − `NetMoveToRangeRatioComponent` (`period`, `source` "high_low")). The range excludes bar t-`period`, whose close is the base of the net move. `negate` gives the reversion reading. No `scaling_factor`: scale it with transforms |

```python class
class FlatnessWeightedRangePositionComponent(SubStrategyComponent):
    """
    Where the close sits in its recent range, weighted by how flat the window's net move is:

        p = period, window = bars t-p+1 .. t (bar t included)
        source = "close" (default): H = max(close[window]), L = min(close[window])
        source = "high_low":        H = max(high[window]),  L = min(low[window])
        pos  = (close[t] - L) / (H - L)
        flat = 1 - abs(close[t] - close[t-p]) / (H - L)
        raw_value = (2 x pos - 1) x flat          (0.0 when H = L)

    The default source "close" is the original output, unchanged. "high_low" measures the position and the
    flatness against the window's full high-low range (the Donchian channel proper).
    Range & sign: signed. It is positive above the window's middle, negative below it, and 0 at the middle or
    for a zero range. It is at most 1 in size whenever close[t-p] lies inside [L, H]. It is unbounded below,
    because flat turns negative when close[t-p] lies outside [L, H] by more than the range allows.
    Graded and continuous in the prices while the range is above 0.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN in any value read gives NaN. For "close" that is the last period + 1 closes. For "high_low"
    that is the high and low of the last period rows, close[t] and close[t-p]. A zero range gives 0.0.
    Building the component raises for a period below 2 or a source other than "close" or "high_low".

    WHY THIS CANNOT LEAK: it reads only the last period + 1 rows of data (bar t is the last row): the close of
    bar t-p, and the close (or high and low) of bars t-p+1 .. t, all known at bar t's close.
    """

    def __init__(self, name="FlatnessWeightedRangePosition", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(f"FlatnessWeightedRangePositionComponent: period must be >= 2, got {self.period}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high_low"):
            raise ValueError(
                f"FlatnessWeightedRangePositionComponent: source must be 'close' or 'high_low', got {self.source!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        close = data["close"].astype(float).to_numpy()
        c_t = float(close[-1])
        c_b = float(close[-(p + 1)])
        if self.source == "close":
            win = close[-p:]
            if np.isnan(win).any() or np.isnan(c_b):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            H = float(win.max())
            L = float(win.min())
        else:
            hi = data["high"].astype(float).to_numpy()[-p:]
            lo = data["low"].astype(float).to_numpy()[-p:]
            if np.isnan(hi).any() or np.isnan(lo).any() or np.isnan(c_t) or np.isnan(c_b):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            H = float(hi.max())
            L = float(lo.min())
        rng = H - L
        if rng == 0:
            value = 0.0
        else:
            pos = (c_t - L) / rng
            flat = 1.0 - abs(c_t - c_b) / rng
            value = (2.0 * pos - 1.0) * flat
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"H": H, "L": L, "source": self.source}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    p = int(params.get("period", 30))
    source = params.get("source", "close")
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    c_t = c[last]
    c_b = c[last - p]
    if source == "high_low":
        h = [float(x) for x in list(df["high"])]
        l = [float(x) for x in list(df["low"])]
        tops = []
        bottoms = []
        i = last - p + 1
        while i <= last:
            tops.append(h[i])
            bottoms.append(l[i])
            i = i + 1
        for x in tops + bottoms + [c_t, c_b]:
            if x != x:
                return float("nan")
    else:
        tops = []
        i = last - p + 1
        while i <= last:
            tops.append(c[i])
            i = i + 1
        bottoms = list(tops)
        for x in tops + [c_b]:
            if x != x:
                return float("nan")
    H = tops[0]
    for x in tops:
        if x > H:
            H = x
    L = bottoms[0]
    for x in bottoms:
        if x < L:
            L = x
    width = H - L
    if width == 0:
        return 0.0
    position = (c_t - L) / width
    net = c_t - c_b
    if net < 0:
        net = -net
    flatness = 1.0 - net / width
    return (2.0 * position - 1.0) * flatness
```

checks:
FlatnessWeightedRangePositionComponent: every check passed
the bot's suite: == 1613 passed, 16 skipped, 75 deselected, 2244 warnings in 101.67s (0:01:41) ==
