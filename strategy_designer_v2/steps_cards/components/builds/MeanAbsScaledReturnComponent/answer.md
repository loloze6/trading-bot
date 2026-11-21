# MeanAbsScaledReturnComponent: night3_1h_run | 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds_1h | DropInMeanAbsDailyMoves

## attempt 1

answer: built
class: MeanAbsScaledReturnComponent
settings: {"period": 24, "window": 720}
reason: No component gives the signed `period`-bar return divided by the mean absolute overlapping `period`-bar return. `VolatilityScaledReturnComponent` divides by a standard deviation, `MeanAbsScaledFallTimesRiseComponent` clips the return and multiplies it by a rise, and `HighProximityScaledReturnComponent` always weights it by a nearness to the high (`power` must be above 0), so a new class computes this ratio.

table: Directional components
row: | `MeanAbsScaledReturnComponent` | `period` (24), `window` (720) | (close[t] / close[t-`period`] - 1) / m, m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`period`] - 1), the overlapping `period`-bar simple returns ending at each of the last `window` bars, bar t included; 0 when m = 0 | unbounded in practice, signed like the `period`-bar return; its size is at most `window` (today's return is one of the `window` returns averaged in m); about -1 for a fall of one usual move, -3 for a fall of three | graded | usual `period`-bar moves | `window` + `period` (744) | closes only. A NaN close in the last `window` + `period` rows gives NaN; a close not above 0 there gives NaN (never on real bars). m = 0 gives 0 (never on real bars; the return is then 0 too). These settings raise when the component is built: `period` < 1, `window` < 1 | stateless. Equals `PriceEvolutionOnPeriodComponent` (`comparison_period` = `period`) / 100 divided by `MeanAbsReturnComponent` (`period`, `window`). On 1h bars the defaults give the 24h return in multiples of the 30-day mean absolute daily return. `negate` gives the fall-positive reading. No `scaling_factor`: scale it with transforms |

```python class
class MeanAbsScaledReturnComponent(SubStrategyComponent):
    """
    The period-bar return in multiples of the coin's usual period-bar move, on every bar:

        r(i) = close[i] / close[i - period] - 1
        m    = mean(abs(r(i)) for i = t - window + 1 .. t)       (overlapping returns, bar t included)
        raw_value = r(t) / m        (0.0 when m = 0)

    Graded and signed like the period-bar return: negative after a fall, more negative the deeper the fall in
    usual moves; positive after a rise. Its size is at most `window`, because r(t) is one of the averaged returns.
    Warm-up: window + period rows, bar t included (the oldest return needs close[t - window + 1 - period]).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data, the last
    row being bar t; a bar's close is known at that bar's close.

    NaN: a NaN close in the last window + period rows gives NaN, and so does a close not above 0 there (never on
    real bars). m = 0 (every return flat, never on real bars) gives 0.0; the return is then 0 as well.
    Building the component raises for a period below 1 or a window below 1.
    """

    def __init__(self, name="MeanAbsScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        if self.period < 1:
            raise ValueError(f"MeanAbsScaledReturnComponent: period must be >= 1, got {self.period}")
        self.window = int(self.parameters.get("window", 720))
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledReturnComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[self.period:] / c[:-self.period] - 1.0
        m = float(np.mean(np.abs(r)))
        ret = float(r[-1])
        self._raw_value = float(ret / m) if m > 0 else 0.0
        self.confidence = 1.0
        self.debug_info = {'return': ret, 'mean_abs_return': m}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period
```

```python hand
def hand(df, params):
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    first = last - w + 1 - p
    j = first
    while j <= last:
        x = c[j]
        if x != x or not x > 0:
            return float("nan")
        j = j + 1
    total = 0.0
    i = last - w + 1
    while i <= last:
        ri = c[i] / c[i - p] - 1.0
        total = total + (ri if ri >= 0 else -ri)
        i = i + 1
    m = total / w
    ret = c[last] / c[last - p] - 1.0
    if not m > 0:
        return 0.0
    return ret / m
```

checks:
MeanAbsScaledReturnComponent: every check passed
the bot's suite: ======= 1583 passed, 16 skipped, 75 deselected, 2244 warnings in 58.75s ========
