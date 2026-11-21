# MeanAbsScaledFallTimesRiseComponent: night3_1h_run | 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b2_plunge-rebound-in-uptrends_1h | PlungeTimesMonthRiseComponent

## attempt 1

answer: built
class: MeanAbsScaledFallTimesRiseComponent
settings: {"fall_period": 24, "window": 720, "rise_period": 720}
reason: No component of the catalogue computes this product. `VolatilityScaledReturnComponent` divides by a standard deviation of one-bar returns, not by the mean absolute overlapping 24-bar return of `MeanAbsReturnComponent`, and no component multiplies a scaled fall by the positive part of a long return. One new class computes it from closes only.

table: Directional components
row: | `MeanAbsScaledFallTimesRiseComponent` | `fall_period` (24), `window` (720), `rise_period` (720) | max(0, -(close[t] / close[t-`fall_period`] - 1) / m) x max(0, close[t] / close[t-`rise_period`] - 1) x 100. m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`fall_period`] - 1), the overlapping `fall_period`-bar returns ending at each of the last `window` bars, bar t included. The first factor is 0 when m = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 when the last `fall_period` bars did not fall or when the `rise_period`-bar return is not positive. It grows with the depth of the fall in usual `fall_period`-bar moves and with the size of the rise | graded | usual `fall_period`-bar moves x percent | max(`window` + `fall_period`, `rise_period` + 1) (744) | closes only. A NaN close in the last max(`window` + `fall_period`, `rise_period` + 1) rows gives NaN. A close not above 0 there gives NaN (never on real bars). m = 0 gives 0 (never on real bars; the fall is then 0 too). These settings raise when the component is built: `fall_period` < 1, `window` < 1, `rise_period` < 1 | stateless. The first factor is the negated, clipped `fall_period`-bar return divided by `MeanAbsReturnComponent` (`period` = `fall_period`, `window`). The second factor is `PriceEvolutionOnPeriodComponent` (`comparison_period` = `rise_period`) clipped at 0. On 1h bars the defaults give a 24h fall in usual daily moves times the positive 30-day percent return. One-sided, a long-only rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class MeanAbsScaledFallTimesRiseComponent(SubStrategyComponent):
    """
    The depth of a recent fall in usual moves, times the size of a longer rise, on every bar:

        r(i) = close[i] / close[i - fall_period] - 1
        m    = mean(abs(r(i)) for i = t - window + 1 .. t)          (bar t included)
        F    = max(0, -r(t) / m)                                     (0 when m = 0)
        R    = max(0, close[t] / close[t - rise_period] - 1)
        raw_value = F x R x 100

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 when the last fall_period bars did not
    fall or when the rise_period-bar return is not positive. It grows continuously with the depth of the fall in
    usual fall_period-bar moves and with the percent rise over rise_period bars.
    Warm-up: max(window + fall_period, rise_period + 1) rows, bar t included (744 at the defaults).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window + fall_period, rise_period + 1)
    rows of data, the last row being bar t; a bar's close is known at that bar's close.

    NaN: a NaN close in those rows gives NaN. A close not above 0 there gives NaN (never on real bars). m = 0
    (every fall_period-bar return of the window flat, never on real bars) gives a first factor of 0.
    Building the component raises for fall_period < 1, window < 1 or rise_period < 1.
    """

    def __init__(self, name="MeanAbsScaledFallTimesRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.fall_period = int(self.parameters.get("fall_period", 24))
        if self.fall_period < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: fall_period must be >= 1, got {self.fall_period}")
        self.window = int(self.parameters.get("window", 720))
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: window must be >= 1, got {self.window}")
        self.rise_period = int(self.parameters.get("rise_period", 720))
        if self.rise_period < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: rise_period must be >= 1, got {self.rise_period}")
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
        p = self.fall_period
        rets = c[p:] / c[:-p] - 1.0
        rets = rets[-self.window:]
        m = float(np.mean(np.abs(rets)))
        r = float(c[-1] / c[-1 - p] - 1.0)
        fall = 0.0 if m == 0 else max(0.0, -r / m)
        rise = max(0.0, float(c[-1] / c[-1 - self.rise_period] - 1.0))
        self._raw_value = float(fall * rise * 100.0)
        self.confidence = 1.0
        self.debug_info = {'fall_return': r, 'mean_abs_return': m, 'scaled_fall': fall, 'rise': rise}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.window + self.fall_period, self.rise_period + 1)
```

```python hand
def hand(df, params):
    p = int(params.get("fall_period", 24))
    w = int(params.get("window", 720))
    q = int(params.get("rise_period", 720))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(w + p, q + 1)
    first = last - need + 1
    j = first
    while j <= last:
        x = c[j]
        if x != x or not x > 0:
            return float("nan")
        j = j + 1
    total = 0.0
    i = last - w + 1
    while i <= last:
        ret = c[i] / c[i - p] - 1.0
        if ret < 0:
            ret = -ret
        total = total + ret
        i = i + 1
    m = total / w
    today = c[last] / c[last - p] - 1.0
    if m == 0:
        fall = 0.0
    else:
        fall = -today / m
        if fall < 0:
            fall = 0.0
    rise = c[last] / c[last - q] - 1.0
    if rise < 0:
        rise = 0.0
    return fall * rise * 100.0
```

checks:
MeanAbsScaledFallTimesRiseComponent: every check passed
the bot's suite: ======= 1581 passed, 16 skipped, 75 deselected, 2244 warnings in 57.07s ========
