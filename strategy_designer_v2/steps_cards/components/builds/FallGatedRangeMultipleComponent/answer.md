# FallGatedRangeMultipleComponent: night4_panic_run | 027-02_panic-fall-depth-rebound.d2_confirmed-panic-bounce-continues.b1_panic-bounce-more-coins_4h | LaggedFallGatedRangeMultiple

## attempt 1

answer: built
class: FallGatedRangeMultipleComponent
settings: {"period": 6, "base_period": 180, "fall_period": 6, "lag": 6}
reason: `FallGatedRangeMultipleComponent` already computes this measure (the gated `period`-bar range in multiples of its mean), but only at bar t. `ScaledFallRangeMultipleComponent` has a `lag`, but it multiplies by the fall depth in usual moves rather than a 0/1 gate, so it is not this measure. Adding a `lag` setting (default 0, today's output unchanged) reads the whole measure at e = t − `lag`, which changes the value on real data.

table: Regime measures
row: | `FallGatedRangeMultipleComponent` | `period` (6), `base_period` (180), `fall_period` (6), `lag` (0) | G x S(e) / mean(S(e-`base_period`+1) .. S(e)), with e = t − `lag`, where S(i) = max(high[i-`period`+1 .. i]) − min(low[i-`period`+1 .. i]) and G = 1 when close[e] < close[e-`fall_period`], else 0. It is 0.0 when that mean is 0 | 0 and up, at most `base_period` (the mean includes S(e)), never negative; no direction. It is 1 when the stretch ending at bar e has a range equal to its average and grows with the multiple. It is 0 when close[e] is not below its value `fall_period` bars earlier | regime measure | dimensionless (multiples of the mean `period`-bar range) | max(`base_period` + `period` − 1, `fall_period` + 1) + `lag` (185) | high, low (bars e-`base_period`-`period`+2 .. e), close (bar e and bar e-`fall_period`). A NaN high or low in those rows, or a NaN close[e] or close[e-`fall_period`], gives NaN. A mean of 0 (never on real bars) gives 0.0, because S(e) is then 0 too. These settings raise when the component is built: `period` < 1, `base_period` < 1, `fall_period` < 1, `lag` < 0 | stateless. `lag` 0 (default) is the original output, unchanged. Bars after t-`lag` are not read, so the value at t is the `lag` 0 value at bar t-`lag`. It is continuous in the highs and lows while the gate is on, and drops to 0 where close[e] crosses close[e-`fall_period`] upward. On 4h bars, `period` 6, `base_period` 180, `fall_period` 6 and `lag` 6 give a 24h range in multiples of its 30-day mean, during a 24h fall that ended 24h ago. No `scaling_factor`: scale it with transforms |

```python class
class FallGatedRangeMultipleComponent(SubStrategyComponent):
    """
    The range of a fall stretch, in multiples of its own average, read at e = t - lag:

        e = t - lag                                          (lag 0, the default: e = t)
        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        M = mean(S(e-base_period+1) .. S(e))
        G = 1 when close[e] < close[e-fall_period], else 0
        raw_value = G x S(e) / M        (0.0 when M is 0)

    Range & sign: 0 and up, at most base_period (M includes S(e)), never negative, no direction. It is 1 when
    the stretch's range equals its mean and 0 when close[e] is not below close[e-fall_period]. lag 0 is the
    original output, unchanged.
    Warm-up: max(base_period + period - 1, fall_period + 1) + lag rows, bar t included.
    NaN: a NaN high or low in bars e-base_period-period+2 .. e, or a NaN close[e] or close[e-fall_period],
    gives NaN, whatever the gate. A mean of 0 gives 0.0 (S(e) is then 0 too).
    Building the component raises for period < 1, base_period < 1, fall_period < 1 or lag < 0.

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data), and of them
    only bars up to e = t - lag: high and low of bars e-base_period-period+2 .. e, and close of bars
    e-fall_period and e. Each is known at its bar's close.
    """

    def __init__(self, name="FallGatedRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.base_period = int(self.parameters.get("base_period", 180))
        self.fall_period = int(self.parameters.get("fall_period", 6))
        self.lag = int(self.parameters.get("lag", 0))
        if self.period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: period must be >= 1, got {self.period}")
        if self.base_period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: base_period must be >= 1, got {self.base_period}")
        if self.fall_period < 1:
            raise ValueError(f"FallGatedRangeMultipleComponent: fall_period must be >= 1, got {self.fall_period}")
        if self.lag < 0:
            raise ValueError(f"FallGatedRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = len(data)
        e = n - 1 - self.lag
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        start = e - self.base_period - self.period + 2
        h = high[start:e + 1]
        lo = low[start:e + 1]
        c_e = close[e]
        c_b = close[e - self.fall_period]
        if np.isnan(h).any() or np.isnan(lo).any() or np.isnan(c_e) or np.isnan(c_b):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        hmax = pd.Series(h).rolling(self.period).max().to_numpy()[self.period - 1:]
        lmin = pd.Series(lo).rolling(self.period).min().to_numpy()[self.period - 1:]
        s = hmax - lmin
        s_e = float(s[-1])
        mean_s = float(np.mean(s))
        gate = 1.0 if c_e < c_b else 0.0
        if mean_s == 0:
            value = 0.0
        else:
            value = gate * s_e / mean_s
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'gate': gate, 'stretch_range': s_e, 'mean_range': mean_s, 'lag': self.lag}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.base_period + self.period - 1, self.fall_period + 1) + self.lag
```

```python hand
def hand(df, params):
    p = int(params.get("period", 6))
    bp = int(params.get("base_period", 180))
    fp = int(params.get("fall_period", 6))
    lag = int(params.get("lag", 0))
    high = [float(x) for x in list(df["high"])]
    low = [float(x) for x in list(df["low"])]
    close = [float(x) for x in list(df["close"])]
    e = len(close) - 1 - lag
    # every high and low the ranges read, and the two gate closes
    j = e - bp - p + 2
    while j <= e:
        if high[j] != high[j] or low[j] != low[j]:
            return float("nan")
        j = j + 1
    if close[e] != close[e] or close[e - fp] != close[e - fp]:
        return float("nan")

    def stretch_range(i):
        top = high[i - p + 1]
        bot = low[i - p + 1]
        k = i - p + 1
        while k <= i:
            if high[k] > top:
                top = high[k]
            if low[k] < bot:
                bot = low[k]
            k = k + 1
        return top - bot

    total = 0.0
    i = e - bp + 1
    while i <= e:
        total = total + stretch_range(i)
        i = i + 1
    mean_s = total / bp
    if mean_s == 0:
        return 0.0
    if close[e] < close[e - fp]:
        return stretch_range(e) / mean_s
    return 0.0
```

checks:
FallGatedRangeMultipleComponent: every check passed
the bot's suite: == 1614 passed, 16 skipped, 75 deselected, 2244 warnings in 94.82s (0:01:34) ===
