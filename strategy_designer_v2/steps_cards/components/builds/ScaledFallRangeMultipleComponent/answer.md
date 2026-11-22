# ScaledFallRangeMultipleComponent: night4_panic_run | 027-04_panic-delayed-recovery-drift_4h | LaggedPanicStretchIntensity

## attempt 1

answer: built
class: ScaledFallRangeMultipleComponent
settings: {"period": 6, "lag": 6, "window": 180}
reason: No component computes this measure. It is a stretch's fall in usual `period`-bar moves times its range in multiples of the usual `period`-bar range, read on a stretch ending `lag` bars back. `MeanAbsScaledReturnComponent` has the fall factor but no lag and no range factor. `FallGatedRangeMultipleComponent` has a range multiple gated on/off by a fall, with no depth and no lag. A new class computes the product. With `lag` 0 it reads the stretch ending at bar t.

table: Regime measures
row: | `ScaledFallRangeMultipleComponent` | `period` (6), `lag` (6), `window` (180) | max(0, -(close[e] / close[e-`period`] - 1) / m) x S(e) / B, with e = t - `lag`. m = mean over i = e-`window`+1 .. e of abs(close[i] / close[i-`period`] - 1). S(i) = max(high[i-`period`+1 .. i]) - min(low[i-`period`+1 .. i]). B = mean of S(i) over i = e-`window`+1 .. e. The output is 0 when m = 0 or B = 0 | 0 and up, unbounded in practice, never negative; no direction. It is 0 when the stretch ending at bar e did not fall. It grows with the depth of the fall in usual `period`-bar moves and with the stretch's range in usual `period`-bar ranges. Each factor is at most `window`, because the stretch's own return and range are among those averaged | graded | usual `period`-bar moves x mean `period`-bar ranges | `window` + `period` + `lag` (192) | close, high, low. A NaN close in bars t-`lag`-`window`-`period`+1 .. t-`lag`, or a NaN high or low in bars t-`lag`-`window`-`period`+2 .. t-`lag`, gives NaN. A close not above 0 there also gives NaN (never on real bars). m = 0 or B = 0 gives 0 (never on real bars; the fall or the range is then 0 too). These settings raise when the component is built: `period` < 1, `lag` < 0, `window` < 1 | stateless. Bars after t-`lag` are not read, so the value at t is the `lag` 0 value at bar t-`lag`. It is continuous in the prices while the stretch fell, and exactly 0 on stretches that rose. On 4h bars the defaults give a 24h fall that ended 24h ago, in usual 24h moves over 30 days, times its 24h range in multiples of the 30-day mean 24h range. One-sided, a delayed-rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class ScaledFallRangeMultipleComponent(SubStrategyComponent):
    """
    The fall of a stretch in usual moves, times its range in usual ranges, for the stretch ending `lag` bars back:

        e    = t - lag
        R    = close[e] / close[e - period] - 1
        m    = mean over i = e-window+1 .. e of abs(close[i] / close[i - period] - 1)
        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        B    = mean over i = e-window+1 .. e of S(i)
        raw_value = max(0, -R / m) x S(e) / B      (0 when m = 0 or B = 0)

    Range: 0 and up, unbounded in practice, never negative; no direction. It is 0 when the stretch did not fall.
    It grows with the depth of the fall in usual period-bar moves and with how many usual period-bar ranges the
    stretch spanned. Each factor is at most `window`.
    Warm-up: window + period + lag rows, bar t included.
    NaN: a NaN close among closes[e-window-period+1 .. e], or a NaN high or low among bars e-window-period+2 .. e,
    gives NaN. A close not above 0 there also gives NaN. m = 0 or B = 0 gives 0.0, because the fall or the range is
    then 0 too.
    Building it raises for period < 1, lag < 0 or window < 1.

    WHY THIS CANNOT LEAK: it reads only close, high and low of rows up to and including bar t - lag. These are at or
    before bar t, the last row of data, and each is known at that bar's close.
    """

    def __init__(self, name="ScaledFallRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        if self.period < 1:
            raise ValueError(f"ScaledFallRangeMultipleComponent: period must be >= 1, got {self.period}")
        self.lag = int(self.parameters.get("lag", 6))
        if self.lag < 0:
            raise ValueError(f"ScaledFallRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        self.window = int(self.parameters.get("window", 180))
        if self.window < 1:
            raise ValueError(f"ScaledFallRangeMultipleComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p, w = self.period, self.window
        c = data['close'].astype(float).to_numpy()
        h = data['high'].astype(float).to_numpy()
        lo = data['low'].astype(float).to_numpy()
        e = len(c) - 1 - self.lag
        cs = c[e - w - p + 1: e + 1]
        hs = h[e - w - p + 2: e + 1]
        ls = lo[e - w - p + 2: e + 1]
        self.confidence = 1.0
        if np.isnan(cs).any() or np.isnan(hs).any() or np.isnan(ls).any() or not (cs > 0).all():
            self._raw_value = float("nan")
            return
        rets = cs[p:] / cs[:-p] - 1.0
        m = float(np.mean(np.abs(rets)))
        hw = np.lib.stride_tricks.sliding_window_view(hs, p).max(axis=1)
        lw = np.lib.stride_tricks.sliding_window_view(ls, p).min(axis=1)
        ranges = hw - lw
        b = float(np.mean(ranges))
        r = float(rets[-1])
        s = float(ranges[-1])
        if m == 0 or b == 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float(max(0.0, -r / m) * s / b)
        self.debug_info = {'stretch_return': r, 'usual_move': m, 'stretch_range': s, 'usual_range': b}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period + self.lag
```

```python hand
def hand(df, params):
    p = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    w = int(params.get("window", 180))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    e = len(c) - 1 - lag
    k = e - w - p + 1
    while k <= e:
        if c[k] != c[k] or not c[k] > 0:
            return float("nan")
        k = k + 1
    k = e - w - p + 2
    while k <= e:
        if h[k] != h[k] or lo[k] != lo[k]:
            return float("nan")
        k = k + 1

    def ret(i):
        return c[i] / c[i - p] - 1.0

    def rng(i):
        top = h[i - p + 1]
        bot = lo[i - p + 1]
        j = i - p + 1
        while j <= i:
            if h[j] > top:
                top = h[j]
            if lo[j] < bot:
                bot = lo[j]
            j = j + 1
        return top - bot

    sum_abs = 0.0
    sum_rng = 0.0
    i = e - w + 1
    while i <= e:
        sum_abs = sum_abs + abs(ret(i))
        sum_rng = sum_rng + rng(i)
        i = i + 1
    m = sum_abs / w
    b = sum_rng / w
    if m == 0 or b == 0:
        return 0.0
    fall = -ret(e) / m
    if fall < 0:
        fall = 0.0
    return fall * rng(e) / b
```

checks:
ScaledFallRangeMultipleComponent: every check passed
the bot's suite: == 1611 passed, 16 skipped, 75 deselected, 2244 warnings in 85.17s (0:01:25) ===
