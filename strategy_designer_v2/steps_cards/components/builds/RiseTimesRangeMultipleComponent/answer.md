# RiseTimesRangeMultipleComponent: night7_steadydecline_run | 037-01_wide-day-fall-next-day-rebound_1d | FallTimesRangeMultiple

## attempt 1

answer: built
class: RiseTimesRangeMultipleComponent
settings: {"rise_period": 1, "range_period": 14, "side": "down", "exclude_current": 1}
reason: `RiseTimesRangeMultipleComponent` computes this measure on the rise side, with a range base that includes bar t. No config step gives its fall side, because `negate` of max(0, rise) is not max(0, fall). No step drops bar t from the base either. So the class is rewritten with two settings: `side` ("up" default, "down") and `exclude_current` (0 default, 1), and the defaults keep today's output exactly.

table: Directional components
row: | `RiseTimesRangeMultipleComponent` | `rise_period` (5), `range_period` (20), `side` ("up"), `exclude_current` (0) | M x 100 x (high[t] − low[t]) / mean(high[i] − low[i]). M = max(0, close[t] / close[t-`rise_period`] − 1) for `side` "up" and max(0, −(close[t] / close[t-`rise_period`] − 1)) for `side` "down". The mean is over i = t-`range_period`+1 .. t (`exclude_current` 0, bar t included) or i = t-`range_period` .. t-1 (`exclude_current` 1, bar t excluded). The output is 0.0 when that mean is 0. With `rise_period` 1, `range_period` 14, "down", 1 it is max(0, −(close[t] / close[t-1] − 1)) x 100 x (high[t] − low[t]) / mean(high[i] − low[i], i = t-14 .. t-1) | 0 and up, unbounded above, never negative; no direction. "up" is 0 when the `rise_period`-bar return is 0 or negative, and "down" is 0 when it is 0 or positive. Both are 0 for a zero-range bar t. The value grows with the move in percent and with bar t's range against its average. The range multiple is at most `range_period` with `exclude_current` 0 (the mean includes bar t) and is unbounded with 1 | graded | percent x range multiple (bar range over mean bar range) | max(`rise_period` + 1, `range_period` + `exclude_current`) (20; 15 at the wished settings) | Reads close (bars t and t-`rise_period`), and high and low (bar t and the base rows). A NaN in any value read gives NaN, whatever the sign of the move. A close[t-`rise_period`] not above 0 gives NaN (never on real bars). A mean range of 0 gives 0.0 (needs `range_period` zero-range bars in a row, never on real bars). These settings raise when the component is built: `rise_period` < 1, `range_period` < 2, `side` other than "up" or "down", `exclude_current` not 0 or 1 | Stateless. `side` "up" with `exclude_current` 0 (the defaults) is the original output, unchanged. "down" is the fall-side reading. No config step gives it, because `negate` on "up" is not it, hence the setting. `exclude_current` 1 sets bar t's range against the prior `range_period` bars' mean, so bar t's own range cannot raise its base. It is continuous in the prices and exactly 0 on bars moving to the other side. On 1d bars the wished settings give the day's fall in percent times its range over the prior 14-day mean range, a wide-day-fall (rebound) reading. No `scaling_factor`: scale it with transforms |

```python class
class RiseTimesRangeMultipleComponent(SubStrategyComponent):
    """
    A move in percent times the current bar's range in multiples of its average bar range:

        R = close[t] / close[t - rise_period] - 1
        side = "up" (default): M = max(0, R)
        side = "down":         M = max(0, -R)
        exclude_current = 0 (default): base = mean(high[i] - low[i]), i = t-range_period+1 .. t (bar t included)
        exclude_current = 1:           base = mean(high[i] - low[i]), i = t-range_period .. t-1 (bar t excluded)
        raw_value = M x 100 x (high[t] - low[t]) / base,  0.0 when base = 0

    With rise_period 1, range_period 14, side "down", exclude_current 1:
        max(0, -(close[t]/close[t-1] - 1)) x 100 x (high[t] - low[t]) / mean(high[i] - low[i], i = t-14 .. t-1).
    The defaults (side "up", exclude_current 0) are the original output, unchanged.

    Range & sign: 0 and up, unbounded above, never negative, no direction. It is 0 when the move is not to the
    counted side, and 0 for a zero-range bar t. With exclude_current 0 the range multiple is at most range_period;
    with 1 it is unbounded. Graded: continuous in the prices.
    Warm-up: max(rise_period + 1, range_period + exclude_current) rows, bar t included.
    NaN: a NaN close[t], close[t-rise_period], or a NaN high or low on bar t or in the base rows gives NaN,
    whatever the sign of the move. A close[t-rise_period] not above 0 gives NaN (never on real bars). A base mean
    of 0 gives 0.0 (range_period zero-range bars in a row, never on real bars).
    Building the component raises for rise_period < 1, range_period < 2, side other than "up" or "down", and
    exclude_current not 0 or 1.

    WHY THIS CANNOT LEAK: it reads only close[t], close[t-rise_period], and the high and low of bar t and of the
    base rows (at most bars t-range_period .. t), all rows up to and including bar t, the last row of data.
    """

    def __init__(self, name="RiseTimesRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.rise_period = int(self.parameters.get("rise_period", 5))
        if self.rise_period < 1:
            raise ValueError(f"RiseTimesRangeMultipleComponent: rise_period must be >= 1, got {self.rise_period}")
        self.range_period = int(self.parameters.get("range_period", 20))
        if self.range_period < 2:
            raise ValueError(f"RiseTimesRangeMultipleComponent: range_period must be >= 2, got {self.range_period}")
        self.side = self.parameters.get("side", "up")
        if self.side not in ("up", "down"):
            raise ValueError(f"RiseTimesRangeMultipleComponent: side must be 'up' or 'down', got {self.side!r}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"RiseTimesRangeMultipleComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float)
        high = data["high"].astype(float)
        low = data["low"].astype(float)
        n = len(data)
        c_t = float(close.iloc[-1])
        c_b = float(close.iloc[-1 - self.rise_period])
        h_t = float(high.iloc[-1])
        l_t = float(low.iloc[-1])
        ex = self.exclude_current
        start = n - self.range_period - ex
        stop = n - ex
        hb = high.iloc[start:stop]
        lb = low.iloc[start:stop]
        if (np.isnan(c_t) or np.isnan(c_b) or np.isnan(h_t) or np.isnan(l_t)
                or hb.isna().any() or lb.isna().any()):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if not c_b > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c_t / c_b - 1.0
        move = max(0.0, r) if self.side == "up" else max(0.0, -r)
        base = float((hb - lb).mean())
        if base == 0:
            value = 0.0
        else:
            value = move * 100.0 * (h_t - l_t) / base
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"move_pct": move * 100.0, "bar_range": h_t - l_t, "base_range": base,
                           "side": self.side, "exclude_current": ex}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.rise_period + 1, self.range_period + self.exclude_current)
```

```python hand
def hand(df, params):
    rp = int(params.get("rise_period", 5))
    rg = int(params.get("range_period", 20))
    side = params.get("side", "up")
    ex = int(params.get("exclude_current", 0))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    # base bars: t-rg+1 .. t (ex 0) or t-rg .. t-1 (ex 1)
    idx = [t - ex - k for k in range(rg)]
    vals = [c[t], c[t - rp], h[t], l[t]]
    for i in idx:
        vals.append(h[i])
        vals.append(l[i])
    for v in vals:
        if v != v:
            return float("nan")
    if not c[t - rp] > 0:
        return float("nan")
    ret = c[t] / c[t - rp] - 1.0
    if side == "up":
        move = ret if ret > 0 else 0.0
    else:
        move = -ret if ret < 0 else 0.0
    total = 0.0
    for i in idx:
        total = total + (h[i] - l[i])
    mean_range = total / rg
    if mean_range == 0:
        return 0.0
    return move * 100.0 * (h[t] - l[t]) / mean_range
```

checks:
RiseTimesRangeMultipleComponent: every check passed
the bot's suite: == 1657 passed, 16 skipped, 75 deselected, 2244 warnings in 126.98s (0:02:06) ==
