# NetMoveRangeAgeComponent: night4_range_run | 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.d1_young-trend-continues-further_1d | NetMoveRangeAgeComponent

## attempt 1

answer: built
class: NetMoveRangeAgeComponent
settings: {"period": 30, "level": 0.5, "max_bars": 30}
reason: `NetMoveToRangeRatioComponent` gives the net-move-to-range ratio on one bar, but no component counts how many consecutive bars that ratio has held at or above a level, or signs that count by the window's return. The ages in the catalogue (`MovingAverageAgeComponent`, `RsiMidlineAgeComponent`) measure other quantities, so this is a new measure and needs one new class.

table: Regime measures
row: | `NetMoveRangeAgeComponent` | `period` (30), `level` (0.5), `max_bars` (30) | sign(close[t] − close[t-`period`]) x n. r(i) = abs(close[i] − close[i-`period`]) / (max(high[i-`period`+1 .. i]) − min(low[i-`period`+1 .. i])), and r(i) = 0.0 when that range is 0. n = the number of consecutive bars i ending at t (bar t included) with r(i) >= `level`, capped at `max_bars`. n = 0, so the output is 0, when r(t) < `level` | −`max_bars` .. +`max_bars`, integers (−30 to +30 at the defaults). Positive while the `period`-bar return is up, negative while it is down, 0 when the ratio on bar t is below `level`. Its size grows by one for each further bar the ratio holds at or above `level` | regime measure | bars | `max_bars` + `period` (60) | close (last `max_bars` + `period` rows), high and low (last `max_bars` + `period` − 1 rows). A NaN in any of those values gives NaN. These settings raise when the component is built: `period` < 1, `max_bars` < 1, `level` not above 0 | stateless. r is `NetMoveToRangeRatioComponent` (`period`, `source` "high_low") on each bar. The run counts the ratio only, so its sign is that of bar t's return even if an earlier bar of the run had the other sign. Like `MovingAverageAgeComponent` it jumps (to 0 when the ratio drops below `level`), so it is for regime rules, not a forecast source. A small size is a fresh trend. No `scaling_factor` |

```python class
class NetMoveRangeAgeComponent(SubStrategyComponent):
    """
    How long the net move has held a large share of the window's high-low range, signed by the move:

        r(i) = abs(close[i] - close[i - period]) / (max(high[i-period+1 .. i]) - min(low[i-period+1 .. i]))
               (r(i) = 0.0 when that range is 0)
        n    = number of consecutive bars i ending at t (bar t included) with r(i) >= level, capped at max_bars
        raw_value = sign(close[t] - close[t - period]) * n

    Range: -max_bars .. +max_bars, integers. Positive while the period-bar return is up, negative while it is
    down. It is 0 when r(t) < level (and when the return is 0, since r(t) is then 0). Its size grows by one for
    each further bar on which the ratio holds at or above level.
    Warm-up: max_bars + period rows, bar t included.
    NaN: a NaN close in the last max_bars + period rows, or a NaN high or low in the last max_bars + period - 1
    rows, gives NaN.
    Building the component raises for period < 1, max_bars < 1, or level not above 0.

    WHY THIS CANNOT LEAK: it reads only the close, high and low of the last max_bars + period rows of data, the
    last of which is bar t; every value is known at bar t's close.
    """

    def __init__(self, name="NetMoveRangeAge", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 1:
            raise ValueError(f"NetMoveRangeAgeComponent: period must be >= 1, got {self.period}")
        self.level = float(self.parameters.get("level", 0.5))
        if not self.level > 0:
            raise ValueError(f"NetMoveRangeAgeComponent: level must be above 0, got {self.level}")
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(f"NetMoveRangeAgeComponent: max_bars must be >= 1, got {self.max_bars}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        m = self.max_bars
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        h = data['high'].astype(float).to_numpy()[-need:]
        lo = data['low'].astype(float).to_numpy()[-need:]
        if np.isnan(c).any() or np.isnan(h[1:]).any() or np.isnan(lo[1:]).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = 0
        for k in range(m):
            i = need - 1 - k
            rng = float(np.max(h[i - p + 1:i + 1]) - np.min(lo[i - p + 1:i + 1]))
            move = abs(float(c[i] - c[i - p]))
            r = move / rng if rng > 0 else 0.0
            if r >= self.level:
                n += 1
            else:
                break
        ret = float(c[-1] - c[-1 - p])
        sign = 1.0 if ret > 0 else (-1.0 if ret < 0 else 0.0)
        self._raw_value = float(sign * n)
        self.confidence = 1.0
        self.debug_info = {'run_length': n, 'net_move': ret}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.max_bars + self.period
```

```python hand
def hand(df, params):
    p = int(params.get("period", 30))
    level = float(params.get("level", 0.5))
    m = int(params.get("max_bars", 30))
    close = [float(x) for x in list(df["close"])]
    high = [float(x) for x in list(df["high"])]
    low = [float(x) for x in list(df["low"])]
    t = len(close) - 1
    first_close = t - (m + p) + 1
    first_hl = first_close + 1
    for j in range(first_close, t + 1):
        if close[j] != close[j]:
            return float("nan")
    for j in range(first_hl, t + 1):
        if high[j] != high[j] or low[j] != low[j]:
            return float("nan")

    def ratio(i):
        hi = high[i - p + 1]
        lw = low[i - p + 1]
        for j in range(i - p + 1, i + 1):
            if high[j] > hi:
                hi = high[j]
            if low[j] < lw:
                lw = low[j]
        rng = hi - lw
        if rng > 0:
            return abs(close[i] - close[i - p]) / rng
        return 0.0

    n = 0
    i = t
    while n < m and ratio(i) >= level:
        n = n + 1
        i = i - 1
    move = close[t] - close[t - p]
    if move > 0:
        return float(n)
    if move < 0:
        return float(-n)
    return 0.0
```

checks:
NetMoveRangeAgeComponent: every check passed
the bot's suite: == 1614 passed, 16 skipped, 75 deselected, 2244 warnings in 100.26s (0:01:40) ==
