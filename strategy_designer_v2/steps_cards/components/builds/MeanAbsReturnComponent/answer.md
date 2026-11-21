# MeanAbsReturnComponent: night3_1h_run | 018-02_hourly-breakout-multiday-continuation_1h | MeanAbsDailyReturnComponent

## attempt 1

answer: built
class: MeanAbsReturnComponent
settings: {"period": 24, "window": 720}
reason: No catalogue component outputs the mean absolute `period`-bar return over a window. `VolScaledBreakAboveHighComponent` uses a similar mean only as an internal divisor, over 30 non-overlapping 24-bar returns rather than 720 overlapping ones, and `VolatilityFromStdDevComponent` is a standard deviation of one-bar returns. One new class computes it, with the return horizon and the window as settings.

table: Hedges and filters
row: | `MeanAbsReturnComponent` | `period` (24), `window` (720) | mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`period`] - 1): the overlapping `period`-bar simple returns ending at each of the last `window` bars, bar t included | 0 and up, unbounded above, never negative; no direction; grows with the coin's usual `period`-bar move size | graded | fraction of price (simple return, not percent) | `window` + `period` (744) | closes only. A NaN close in the last `window` + `period` rows gives NaN; a close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `window` < 1 | stateless. On 1h bars the defaults are the mean absolute daily (24-bar) return over the last 30 days. The returns overlap, unlike the non-overlapping mean inside `VolScaledBreakAboveHighComponent`. Always non-negative, so it is a scale or divisor for a comparison or a regime input, not a bet. No `scaling_factor`: scale it with transforms |

```python class
class MeanAbsReturnComponent(SubStrategyComponent):
    """
    The usual size of a `period`-bar move, on every bar:

        r(i) = close[i] / close[i - period] - 1,  i = t - window + 1 .. t   (bar t included)
        raw_value = (1 / window) x sum over those i of abs(r(i))

    The returns overlap: one is taken ending at each of the last `window` bars.
    Range & sign: 0 and up, unbounded above, never negative; no direction. It grows with the coin's
    usual `period`-bar move. Units: a fraction of price (a simple return, not percent).
    Warm-up: window + period rows, bar t included (744 at the defaults).
    NaN: a NaN close anywhere in the last window + period rows gives NaN. A close not above 0 there
    gives NaN (never on real bars). A missing `close` column raises.
    Building the component raises for a period below 1 or a window below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data.
    Those are bars t - window - period + 1 .. t, and the last row is bar t. A bar's close is known at
    that bar's close.
    """

    def __init__(self, name="MeanAbsReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        if self.period < 1:
            raise ValueError(f"MeanAbsReturnComponent: period must be >= 1, got {self.period}")
        self.window = int(self.parameters.get("window", 720))
        if self.window < 1:
            raise ValueError(f"MeanAbsReturnComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.window + self.period
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
        else:
            r = c[self.period:] / c[:-self.period] - 1.0
            self._raw_value = float(np.mean(np.abs(r)))
        self.confidence = 1.0
        self.debug_info = {'period': self.period, 'window': self.window}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.window + self.period
```

```python hand
def hand(df, params):
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    first = last - w - p + 1
    j = first
    while j <= last:
        x = c[j]
        if x != x or not x > 0:
            return float("nan")
        j = j + 1
    total = 0.0
    i = last - w + 1
    while i <= last:
        move = c[i] / c[i - p] - 1.0
        if move < 0:
            move = -move
        total = total + move
        i = i + 1
    return total / w
```

checks:
MeanAbsReturnComponent: every check passed
the bot's suite: ======= 1580 passed, 16 skipped, 75 deselected, 2244 warnings in 56.06s ========
