# FlatnessWeightedRangePositionComponent: night4_range_run | 023-03_flatter-range-stronger-reversion_1d | FlatnessWeightedRangeReversion

## attempt 1

answer: built
class: FlatnessWeightedRangePositionComponent
settings: {"period": 30}
reason: No component multiplies the close's position in its closing range by the window's flatness (1 minus the net move over the closing range). `DonchianBreakoutComponent` gives only the first factor, and `NetMoveToRangeRatioComponent` uses the high–low range, not the closes. The class gives (2 x pos − 1) x flatness; the wished reversion reading is its negative, which `negate` gives exactly.

table: Directional components
row: | `FlatnessWeightedRangePositionComponent` | `period` (30) | (2 x pos − 1) x (1 − abs(close[t] − close[t-`period`]) / (H − L)), H and L being the highest and lowest of closes t-`period`+1 .. t, pos = (close[t] − L) / (H − L); 0.0 when H = L | unbounded below, at most 1 in size while abs(close[t] − close[t-`period`]) <= H − L. It is at most 1 in size whenever close[t-`period`] lies inside [L, H]. It is signed: positive above the window's middle, negative below it, 0 at the middle or for a zero range. Its size grows with the distance from the middle and with the flatness. The flatness factor turns negative when close[t-`period`] lies outside [L, H] by more than the range allows (a strong one-way move), which flips the sign. `negate` gives the wished reversion reading | graded | dimensionless (position x flatness) | `period` + 1 (31) | closes only (last `period` + 1 rows). A NaN close there gives NaN; a zero range gives 0.0. `period` < 2 raises when the component is built | stateless; equals `DonchianBreakoutComponent` (`period`, `sf` 1) x (1 − net move / closing range), and the range excludes bar t-`period`, as in `NetMoveToRangeRatioComponent`. No `scaling_factor`: scale it with transforms |

```python class
class FlatnessWeightedRangePositionComponent(SubStrategyComponent):
    """
    Where the close sits in its closing range, weighted by how flat the window is:

        H = max(close[t-period+1 .. t]), L = min(close[t-period+1 .. t])     (bar t included)
        pos = (close[t] - L) / (H - L)
        F   = 1 - abs(close[t] - close[t-period]) / (H - L)
        raw_value = (2 x pos - 1) x F,   0.0 when H = L

    Range & sign: signed; positive above the window's middle, negative below it, 0 at the middle or for a
    zero range. Its size is at most 1 while abs(close[t] - close[t-period]) <= H - L (always so when
    close[t-period] lies inside [L, H]). Otherwise F is negative, which flips the sign, and the value is
    unbounded below in F. Graded: continuous in the closes while H > L. `negate` gives the reversion reading
    -(2 x pos - 1) x F.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN close among the last period + 1 rows gives NaN. A zero range gives 0.0.
    Building the component raises for a period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t (the
    last row) and the period rows before it; a close is known at its bar's close.
    """

    def __init__(self, name="FlatnessWeightedRangePosition", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(
                f"FlatnessWeightedRangePositionComponent: period must be >= 2, got {self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).iloc[-(self.period + 1):].to_numpy()
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        win = c[1:]
        hi = float(np.max(win))
        lo = float(np.min(win))
        rng = hi - lo
        if not rng > 0:
            self._raw_value = 0.0
        else:
            pos = (c[-1] - lo) / rng
            flat = 1.0 - abs(c[-1] - c[0]) / rng
            self._raw_value = float((2.0 * pos - 1.0) * flat)
        self.confidence = 1.0
        self.debug_info = {'high': hi, 'low': lo, 'base_close': float(c[0])}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 30))
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    used = []
    i = last - n
    while i <= last:
        used.append(closes[i])
        i = i + 1
    for x in used:
        if x != x:
            return float("nan")
    base = closes[last - n]
    now = closes[last]
    hi = closes[last - n + 1]
    lo = closes[last - n + 1]
    i = last - n + 1
    while i <= last:
        if closes[i] > hi:
            hi = closes[i]
        if closes[i] < lo:
            lo = closes[i]
        i = i + 1
    width = hi - lo
    if width <= 0:
        return 0.0
    position = (now - lo) / width
    move = now - base
    if move < 0:
        move = -move
    flatness = 1.0 - move / width
    return (2.0 * position - 1.0) * flatness
```

checks:
FlatnessWeightedRangePositionComponent: every check passed
the bot's suite: == 1612 passed, 16 skipped, 75 deselected, 2244 warnings in 101.65s (0:01:41) ==
