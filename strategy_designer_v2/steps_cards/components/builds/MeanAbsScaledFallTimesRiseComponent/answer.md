# MeanAbsScaledFallTimesRiseComponent: night4_volumehour_run | 028-04_low-volume-down-fade.d1_quiet-dip-in-rising-day_1h | FallTimesPriorRise

## attempt 1

answer: built
class: MeanAbsScaledFallTimesRiseComponent
settings: {"fall_period": 1, "window": 720, "rise_period": 24, "rise_lag": 1}
reason: `MeanAbsScaledFallTimesRiseComponent` computes this measure, but its rise always ends at bar t. No setting ends the rise at bar t-1, and `rise_period` 25 would count the falling bar inside the rise, which changes the output on real data. This version of the same class adds `rise_lag` (default 0, today's output unchanged); `rise_lag` 1 gives close[t-1] / close[t-25] - 1.

table: Directional components
row: | `MeanAbsScaledFallTimesRiseComponent` | `fall_period` (24), `window` (720), `rise_period` (720), `rise_lag` (0) | max(0, -(close[t] / close[t-`fall_period`] - 1) / m) x max(0, close[t-`rise_lag`] / close[t-`rise_lag`-`rise_period`] - 1) x 100. m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`fall_period`] - 1), the overlapping `fall_period`-bar returns ending at each of the last `window` bars, bar t included. The first factor is 0 when m = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 when the last `fall_period` bars did not fall, or when the `rise_period`-bar return ending at bar t-`rise_lag` is not positive. It grows with the depth of the fall in usual `fall_period`-bar moves and with the size of the rise | graded | usual `fall_period`-bar moves x percent | max(`window` + `fall_period`, `rise_period` + `rise_lag` + 1) (744) | closes only. A NaN close in the last max(`window` + `fall_period`, `rise_period` + `rise_lag` + 1) rows gives NaN, and so does a close not above 0 there (never on real bars). m = 0 gives 0 (never on real bars; the fall is then 0 too). These settings raise when the component is built: `fall_period` < 1, `window` < 1, `rise_period` < 1, `rise_lag` < 0 | stateless. `rise_lag` 0 (default) is the original output, unchanged. With `rise_lag` 1 the rise ends at bar t-1, so it is the rise before the falling bar and that bar cannot shrink it. With `fall_period` 1, `window` 720, `rise_period` 24 and `rise_lag` 1 on 1h bars, the output is the hour's fall in usual one-bar moves times the prior 24h percent rise. The first factor is the negated, clipped `fall_period`-bar return divided by `MeanAbsReturnComponent` (`period` = `fall_period`, `window`). One-sided, a long-only rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class MeanAbsScaledFallTimesRiseComponent(SubStrategyComponent):
    """
    A fall in usual moves times a prior rise, on every bar:

        F = close[t] / close[t - fall_period] - 1
        m = mean over i = t-window+1 .. t of abs(close[i] / close[i - fall_period] - 1)   (bar t included)
        R = close[t - rise_lag] / close[t - rise_lag - rise_period] - 1
        raw_value = max(0, -F / m) x max(0, R) x 100      (first factor 0 when m = 0)

    rise_lag 0 (default) ends the rise at bar t: this is the original output, unchanged. rise_lag 1 ends it at bar t-1,
    so it is the rise before the falling bar.
    Range: 0 and up, unbounded above, never negative, no direction. It is 0 unless the fall_period-bar return is negative
    and R is positive, and it grows with both.
    Warm-up: max(window + fall_period, rise_period + rise_lag + 1) rows, bar t included (744 at the defaults).
    NaN: a NaN close in those rows gives NaN; a close not above 0 there gives NaN (never on real bars). m = 0 gives 0.
    Building the component raises for fall_period < 1, window < 1, rise_period < 1 or rise_lag < 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window + fall_period,
    rise_period + rise_lag + 1) rows of data, the last of which is bar t; no later row exists in data.
    """

    def __init__(self, name="MeanAbsScaledFallTimesRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.fall_period = int(self.parameters.get("fall_period", 24))
        self.window = int(self.parameters.get("window", 720))
        self.rise_period = int(self.parameters.get("rise_period", 720))
        self.rise_lag = int(self.parameters.get("rise_lag", 0))
        if self.fall_period < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: fall_period must be >= 1, got {self.fall_period}")
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: window must be >= 1, got {self.window}")
        if self.rise_period < 1:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: rise_period must be >= 1, got {self.rise_period}")
        if self.rise_lag < 0:
            raise ValueError(f"MeanAbsScaledFallTimesRiseComponent: rise_lag must be >= 0, got {self.rise_lag}")
        self._raw_value = 0.0

    def update(self, data):
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
        last = len(c) - 1
        fp = self.fall_period
        fall = c[last] / c[last - fp] - 1.0
        cur = c[len(c) - self.window:]
        prev = c[len(c) - self.window - fp:len(c) - fp]
        m = float(np.mean(np.abs(cur / prev - 1.0)))
        first = 0.0 if m == 0 else max(0.0, -fall / m)
        rise = c[last - self.rise_lag] / c[last - self.rise_lag - self.rise_period] - 1.0
        second = max(0.0, rise)
        self._raw_value = float(first * second * 100.0)
        self.confidence = 1.0
        self.debug_info = {'fall': float(fall), 'mean_abs_move': m, 'rise': float(rise)}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.window + self.fall_period, self.rise_period + self.rise_lag + 1)
```

```python hand
def hand(df, params):
    fp = int(params.get("fall_period", 24))
    w = int(params.get("window", 720))
    rp = int(params.get("rise_period", 720))
    lag = int(params.get("rise_lag", 0))
    c = [float(x) for x in list(df["close"])]
    need = max(w + fp, rp + lag + 1)
    used = c[len(c) - need:]
    for x in used:
        if x != x or not x > 0:
            return float("nan")
    t = len(c) - 1
    fall = c[t] / c[t - fp] - 1.0
    total = 0.0
    i = t - w + 1
    while i <= t:
        r = c[i] / c[i - fp] - 1.0
        total = total + (r if r >= 0 else -r)
        i = i + 1
    m = total / w
    if m == 0:
        first = 0.0
    else:
        first = -fall / m
        if first < 0:
            first = 0.0
    rise = c[t - lag] / c[t - lag - rp] - 1.0
    if rise < 0:
        rise = 0.0
    return first * rise * 100.0
```

checks:
MeanAbsScaledFallTimesRiseComponent: every check passed
the bot's suite: == 1609 passed, 16 skipped, 75 deselected, 2244 warnings in 75.69s (0:01:15) ===
