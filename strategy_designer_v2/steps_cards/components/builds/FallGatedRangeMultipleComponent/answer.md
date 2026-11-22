# FallGatedRangeMultipleComponent: night4_panic_run | 027-01_panic-range-multiple-rebound_4h | PanicRangeMultipleComponent

## attempt 1

answer: built
class: FallGatedRangeMultipleComponent
settings: {"period": 6, "base_period": 180, "fall_period": 6}
reason: No component divides a `period`-bar stretch range by the mean of that same rolling stretch range. The nearest, `RangeCompressionRatioComponent`, uses either the long window's whole range or the mean single-bar range as its base, and no component applies a gate on close[t] < close[t-6]. The gated multiple is one measure, so one new class computes it.

table: Regime measures
row: | `FallGatedRangeMultipleComponent` | `period` (6), `base_period` (180), `fall_period` (6) | G x S(t) / mean(S(t-`base_period`+1) .. S(t)), where S(i) = max(high[i-`period`+1 .. i]) − min(low[i-`period`+1 .. i]) and G = 1 when close[t] < close[t-`fall_period`], else 0. It is 0.0 when that mean is 0 | 0 and up, at most `base_period` (the mean includes S(t)), never negative; no direction. It is 1 when the current stretch's range equals its average and grows with the multiple. It is 0 when the close is not below its value `fall_period` bars ago | regime measure | dimensionless (multiples of the mean `period`-bar range) | max(`base_period` + `period` − 1, `fall_period` + 1) (185) | high, low (last `base_period` + `period` − 1 rows), close (bar t and bar t-`fall_period`). A NaN high or low in those rows, or a NaN close[t] or close[t-`fall_period`], gives NaN. A mean of 0 (185 zero-range bars in a row, never on real bars) gives 0.0, because S(t) is then 0 too. These settings raise when the component is built: `period` < 1, `base_period` < 1, `fall_period` < 1 | stateless. It is continuous in the highs and lows while the gate is on. It drops to 0 where close[t] crosses close[t-`fall_period`] upward. On 4h bars the defaults give the 24h range in multiples of its 30-day average, during a 24h fall. With `period` 1 the base is the mean bar range. No `scaling_factor`: scale it with transforms |

```python class
class FallGatedRangeMultipleComponent(SubStrategyComponent):
    """
    The range of the latest stretch in multiples of its own usual size, read only while the close is falling:

        S(i) = max(high[i - period + 1 .. i]) - min(low[i - period + 1 .. i])
        B    = mean(S(t - base_period + 1) .. S(t))                     (S(t) included)
        G    = 1 if close[t] < close[t - fall_period] else 0
        raw_value = G * S(t) / B                                        (0.0 when B = 0)

    Range & sign: 0 and up, at most base_period (S(t) is one of the averaged ranges), never negative, no direction.
    It is 1 when the current stretch's range equals its average and grows continuously with the multiple while the
    gate is on. It is 0 when close[t] is not below close[t - fall_period].
    Warm-up: max(base_period + period - 1, fall_period + 1) rows, bar t included (185 at the defaults).
    NaN: a NaN high or low in the last base_period + period - 1 rows, or a NaN close[t] or close[t - fall_period],
    gives NaN (even when the gate is off). B = 0 (base_period + period - 1 zero-range bars, never on real bars)
    gives 0.0, since S(t) is then 0 too.
    Building the component raises for period, base_period or fall_period below 1.

    WHY THIS CANNOT LEAK: it reads high and low over the last base_period + period - 1 rows ending at bar t (the last
    row of data), and close at bar t and bar t - fall_period. All of these are known at bar t's close.
    """

    def __init__(self, name="FallGatedRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        if self.period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: period must be >= 1, got {self.period}")
        self.base_period = int(self.parameters.get("base_period", 180))
        if self.base_period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: base_period must be >= 1, got {self.base_period}")
        self.fall_period = int(self.parameters.get("fall_period", 6))
        if self.fall_period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: fall_period must be >= 1, got {self.fall_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        hw = self.base_period + self.period - 1
        hi = data['high'].astype(float).iloc[-hw:].reset_index(drop=True)
        lo = data['low'].astype(float).iloc[-hw:].reset_index(drop=True)
        close = data['close'].astype(float)
        c_now = float(close.iloc[-1])
        c_then = float(close.iloc[-(self.fall_period + 1)])
        if hi.isna().any() or lo.isna().any() or np.isnan(c_now) or np.isnan(c_then):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        stretch = (hi.rolling(self.period).max() - lo.rolling(self.period).min()).iloc[-self.base_period:]
        s_now = float(stretch.iloc[-1])
        base = float(stretch.mean())
        if not c_now < c_then:
            value = 0.0
        elif not base > 0:
            value = 0.0
        else:
            value = s_now / base
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'stretch_range': s_now, 'mean_stretch_range': base,
                           'falling': bool(c_now < c_then)}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.base_period + self.period - 1, self.fall_period + 1)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 6))
    bp = int(params.get("base_period", 180))
    fp = int(params.get("fall_period", 6))
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    first = t - (bp + p - 1) + 1
    j = first
    while j <= t:
        if h[j] != h[j] or l[j] != l[j]:
            return float("nan")
        j = j + 1
    if c[t] != c[t] or c[t - fp] != c[t - fp]:
        return float("nan")

    def stretch(i):
        top = h[i - p + 1]
        bot = l[i - p + 1]
        k = i - p + 1
        while k <= i:
            if h[k] > top:
                top = h[k]
            if l[k] < bot:
                bot = l[k]
            k = k + 1
        return top - bot

    total = 0.0
    i = t - bp + 1
    while i <= t:
        total = total + stretch(i)
        i = i + 1
    mean = total / bp
    if not c[t] < c[t - fp]:
        return 0.0
    if not mean > 0:
        return 0.0
    return stretch(t) / mean
```

checks:
FallGatedRangeMultipleComponent: every check passed
the bot's suite: == 1610 passed, 16 skipped, 75 deselected, 2244 warnings in 89.16s (0:01:29) ===
