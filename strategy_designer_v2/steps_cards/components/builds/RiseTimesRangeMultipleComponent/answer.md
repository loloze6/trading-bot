# RiseTimesRangeMultipleComponent: night6_indecision_run | 031-01.b1.b2_wide-day-extends-strong-run_1d | RiseTimesRangeMultiple

## attempt 1

answer: built
class: RiseTimesRangeMultipleComponent
settings: {"rise_period": 5, "range_period": 20}
reason: No catalogue component multiplies a clipped rise by bar t's range in multiples of its mean bar range. `FallGatedRangeMultipleComponent` and `ScaledFallRangeMultipleComponent` gate on falls and use multi-bar stretches, and `MeanBarRangeRatioComponent` with `short_period` 1 is the inverse ratio with no rise factor. This product is its own measure, so one new class computes it.

table: Directional components
row: | `RiseTimesRangeMultipleComponent` | `rise_period` (5), `range_period` (20) | max(0, close[t] / close[t-`rise_period`] − 1) x 100 x (high[t] − low[t]) / mean(high[i] − low[i], i = t-`range_period`+1 .. t), bar t included in the mean; 0.0 when that mean is 0 | 0 and up, unbounded above, never negative; no direction. It is 0 when the `rise_period`-bar return is 0 or negative, and 0 for a zero-range bar t. It grows with the rise in percent and with bar t's range against its average. The range multiple is at most `range_period`, because the mean includes bar t | graded | percent x range multiple (bar range over mean bar range) | max(`rise_period` + 1, `range_period`) (20) | close (bars t and t-`rise_period`), high and low (last `range_period` rows). A NaN in any value read gives NaN, whatever the sign of the move. A close[t-`rise_period`] not above 0 gives NaN (never on real bars). A mean range of 0 gives 0.0, because the bar t range is then 0 too (never on real bars). These settings raise when the component is built: `rise_period` < 1, `range_period` < 2 | stateless. It is continuous in the prices and exactly 0 after a flat or falling stretch. On 1d bars the defaults give the 5-day rise in percent times the day's range over its 20-day mean range. It is one-sided, a wide-day-in-a-run reading. No `scaling_factor`: scale it with transforms |

```python class
class RiseTimesRangeMultipleComponent(SubStrategyComponent):
    """
    A rise times the current bar's range in multiples of its average bar range, on every bar:

        R    = max(0, close[t] / close[t - rise_period] - 1) x 100
        M    = (high[t] - low[t]) / mean(high[i] - low[i], i = t - range_period + 1 .. t)   (bar t included)
        raw_value = R x M          (0.0 when the mean range is 0)

    Range and sign: 0 and up, unbounded above, never negative, no direction. The value is 0 when the
    rise_period-bar return is 0 or negative, and 0 for a zero-range bar t. M is at most range_period,
    because the mean includes bar t. The value grows with the rise and with how wide bar t is against
    its average. It is continuous in the prices.
    Warm-up: max(rise_period + 1, range_period) rows, bar t included (20 at the defaults).
    NaN: a NaN close at bar t or at bar t - rise_period, or a NaN high or low in the last range_period
    rows, gives NaN, whatever the sign of the move. A close[t - rise_period] not above 0 gives NaN
    (never on real bars). A mean range of 0 gives 0.0, because the range of bar t is then 0 too.
    Building the component raises for a rise_period below 1 or a range_period below 2.

    WHY THIS CANNOT LEAK: it reads close[t] and close[t - rise_period], and the high and low of the
    last range_period rows ending at bar t (the last row of data). All of them are known at bar t's close.
    """

    def __init__(self, name="RiseTimesRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.rise_period = int(self.parameters.get("rise_period", 5))
        if self.rise_period < 1:
            raise ValueError(f"RiseTimesRangeMultipleComponent: rise_period must be >= 1, got {self.rise_period}")
        self.range_period = int(self.parameters.get("range_period", 20))
        if self.range_period < 2:
            raise ValueError(f"RiseTimesRangeMultipleComponent: range_period must be >= 2, got {self.range_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float).to_numpy()
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        c_t = close[-1]
        c_b = close[-(self.rise_period + 1)]
        h = high[-self.range_period:]
        lo = low[-self.range_period:]
        if np.isnan(c_t) or np.isnan(c_b) or np.isnan(h).any() or np.isnan(lo).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if not c_b > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rise = max(0.0, c_t / c_b - 1.0) * 100.0
        ranges = h - lo
        mean_range = float(ranges.mean())
        if mean_range == 0.0:
            mult = 0.0
        else:
            mult = float(ranges[-1]) / mean_range
        self._raw_value = float(rise * mult)
        self.confidence = 1.0
        self.debug_info = {'rise_pct': rise, 'range_multiple': mult, 'mean_range': mean_range}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.rise_period + 1, self.range_period)
```

```python hand
def hand(df, params):
    p = int(params.get("rise_period", 5))
    n = int(params.get("range_period", 20))
    c = [float(x) for x in list(df["close"])]
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    now = c[t]
    base = c[t - p]
    widths = []
    for k in range(n):
        i = t - k
        if hi[i] != hi[i] or lo[i] != lo[i]:
            return float("nan")
        widths.append(hi[i] - lo[i])
    if now != now or base != base:
        return float("nan")
    if not base > 0:
        return float("nan")
    ret = now / base - 1.0
    if ret < 0.0:
        ret = 0.0
    total = 0.0
    for w in widths:
        total = total + w
    avg = total / n
    if avg == 0.0:
        return 0.0
    today = hi[t] - lo[t]
    return ret * 100.0 * today / avg
```

checks:
RiseTimesRangeMultipleComponent: every check passed
the bot's suite: == 1653 passed, 16 skipped, 75 deselected, 2244 warnings in 154.36s (0:02:34) ==
