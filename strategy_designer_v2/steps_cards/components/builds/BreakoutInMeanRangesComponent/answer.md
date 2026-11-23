# BreakoutInMeanRangesComponent: brief_absorption_run | 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g1_wide-range-low-close-rebound_1d | CloseDepthBelowDayHighInPriorRangesComponent

## attempt 1

answer: built
class: BreakoutInMeanRangesComponent
settings: {"period": 1, "base_period": 20, "side": "below", "high_current": 1, "base_exclude_current": 1}
reason: No component gives a high-to-close distance in mean bar ranges with the high taken on bar t and a base of the 20 bars before t. `BreakoutInMeanRangesComponent` "below" computes this measure, the close's depth under a high counted in mean bar ranges, but its high always excludes bar t and its base always includes bar t. The class is written again with two settings, `high_current` and `base_exclude_current`, whose defaults (0) keep today's output unchanged.

table: Directional components
row: | `BreakoutInMeanRangesComponent` | `period` (12), `base_period` (180), `side` ("above"), `high_current` (0), `base_exclude_current` (0) | `side` "above": max(0, close[t] − H) / B. `side` "below": max(0, H − close[t]) / B. H = max(high[t-`period`..t-1]) (`high_current` 0) or max(high[t-`period`+1..t]) (`high_current` 1). B = mean(high[i] − low[i]) over bars t-`base_period`+1 .. t (`base_exclude_current` 0, bar t included) or t-`base_period` .. t-1 (`base_exclude_current` 1, bar t excluded). 0.0 when B = 0. With `period` 1, `base_period` 20, `side` "below", `high_current` 1 and `base_exclude_current` 1: (high[t] − close[t]) / mean(high[i] − low[i], i = t-20 .. t-1) | 0 and up, unbounded above, never negative; no direction. "above": 0 when the close is at or below H, growing linearly with the size of the break (always 0 with `high_current` 1, since close[t] ≤ high[t]). "below": 0 when the close is at or above H, growing linearly as the close sits deeper below it. With `base_exclude_current` 0 the "below" value with `period` 1 and `high_current` 1 is at most `base_period`; with 1 it is unbounded | graded | mean bar ranges | max(`base_period` + `base_exclude_current`, `period` + 1 − `high_current`) (180) | close, high, low. A NaN high in the stretch, a NaN high or low in the base rows, or a NaN close[t] gives NaN. These settings raise when the component is built: `period` < 1, `base_period` < 1, `side` other than "above" or "below", `high_current` not 0 or 1, `base_exclude_current` not 0 or 1 | stateless. `side` "above" with `high_current` 0 and `base_exclude_current` 0 (the defaults) is the original output, unchanged. With `high_current` 0 the stretch excludes bar t, so bar t's own move cannot change H. `high_current` 1 lets H include bar t; with `period` 1 it is the bar's own high. `base_exclude_current` 1 sets the distance against the prior `base_period` bars' mean range, so bar t's own range cannot raise its base. On 1d bars, `period` 1, `base_period` 20, "below", 1, 1 give the close's distance under the day's high in prior 20-day mean ranges: the range ratio × (high − close) / (high − low). B = 0 needs `base_period` zero-range bars in a row and reads 0.0. Continuous in the close. Not `NarrowRangeBreakoutComponent`. No `scaling_factor`: scale it with transforms |

```python class
class BreakoutInMeanRangesComponent(SubStrategyComponent):
    """
    The close's distance beyond or under a high, counted in mean bar ranges, on every bar:

        stretch:  high_current = 0 (default): H = max(high[t - period .. t - 1])    (bar t excluded)
                  high_current = 1:           H = max(high[t - period + 1 .. t])    (bar t included)
        base:     base_exclude_current = 0 (default): B = mean(high[i] - low[i]), i = t - base_period + 1 .. t
                  base_exclude_current = 1:           B = mean(high[i] - low[i]), i = t - base_period .. t - 1
        side = "above" (default): raw_value = max(0, close[t] - H) / B
        side = "below":           raw_value = max(0, H - close[t]) / B
        raw_value = 0.0 when B = 0

    The defaults (side "above", high_current 0, base_exclude_current 0) are the original output, unchanged.
    With period 1, base_period 20, side "below", high_current 1 and base_exclude_current 1 the output is
    (high[t] - close[t]) / mean(high[i] - low[i], i = t-20 .. t-1): 0 with the close at the bar's high, growing
    as the close sits lower in a bar whose range is wide against the prior 20 bars' mean range.
    Range: 0 and up, unbounded above, never negative; no direction; graded (linear in the close).
    Warm-up: max(base_period + base_exclude_current, period + 1 - high_current) rows, bar t included.
    NaN: a NaN high in the stretch, a NaN high or low in the base rows, or a NaN close[t] gives NaN.
    B = 0 (base_period zero-range bars in a row, never on real bars) reads 0.0.
    Building the component raises for period < 1, base_period < 1, a side other than "above" or "below",
    a high_current or base_exclude_current other than 0 or 1.

    WHY THIS CANNOT LEAK: it reads only the high, low and close of the rows up to and including bar t (the last
    row of data): highs of bars t-period .. t, lows and highs of bars t-base_period-1 .. t at most, and close[t].
    """

    def __init__(self, name="BreakoutInMeanRanges", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 12))
        if self.period < 1:
            raise ValueError(f"BreakoutInMeanRangesComponent: period must be >= 1, got {self.period}")
        self.base_period = int(self.parameters.get("base_period", 180))
        if self.base_period < 1:
            raise ValueError(f"BreakoutInMeanRangesComponent: base_period must be >= 1, got {self.base_period}")
        self.side = self.parameters.get("side", "above")
        if self.side not in ("above", "below"):
            raise ValueError(f"BreakoutInMeanRangesComponent: side must be 'above' or 'below', got {self.side!r}")
        hc = self.parameters.get("high_current", 0)
        if isinstance(hc, bool):
            hc = int(hc)
        if hc not in (0, 1):
            raise ValueError(f"BreakoutInMeanRangesComponent: high_current must be 0 or 1, got {hc!r}")
        self.high_current = int(hc)
        bx = self.parameters.get("base_exclude_current", 0)
        if isinstance(bx, bool):
            bx = int(bx)
        if bx not in (0, 1):
            raise ValueError(f"BreakoutInMeanRangesComponent: base_exclude_current must be 0 or 1, got {bx!r}")
        self.base_exclude_current = int(bx)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        n = len(close)
        if self.high_current == 1:
            stretch = high[n - self.period:n]
        else:
            stretch = high[n - 1 - self.period:n - 1]
        b_stop = n - self.base_exclude_current
        b_start = b_stop - self.base_period
        bh = high[b_start:b_stop]
        bl = low[b_start:b_stop]
        c = close[-1]
        if np.isnan(stretch).any() or np.isnan(bh).any() or np.isnan(bl).any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(np.max(stretch))
        B = float(np.mean(bh - bl))
        if B == 0:
            value = 0.0
        elif self.side == "above":
            value = max(0.0, c - H) / B
        else:
            value = max(0.0, H - c) / B
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'H': H, 'B': B, 'close': float(c), 'side': self.side,
                           'high_current': self.high_current, 'base_exclude_current': self.base_exclude_current}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.base_period + self.base_exclude_current, self.period + 1 - self.high_current)
```

```python hand
def hand(df, params):
    period = int(params.get("period", 12))
    base_period = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hc = int(params.get("high_current", 0))
    bx = int(params.get("base_exclude_current", 0))
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    # the high's stretch
    if hc == 1:
        idx = [t - k for k in range(period)]            # t-period+1 .. t
    else:
        idx = [t - 1 - k for k in range(period)]        # t-period .. t-1
    highs = [h[i] for i in idx]
    # the base of mean bar ranges
    end = t - bx
    bidx = [end - k for k in range(base_period)]
    ranges = []
    for i in bidx:
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
        ranges.append(h[i] - l[i])
    for x in highs:
        if x != x:
            return float("nan")
    if c[t] != c[t]:
        return float("nan")
    H = highs[0]
    for x in highs:
        if x > H:
            H = x
    total = 0.0
    for r in ranges:
        total += r
    B = total / len(ranges)
    if B == 0:
        return 0.0
    if side == "above":
        d = c[t] - H
    else:
        d = H - c[t]
    if d < 0:
        d = 0.0
    return d / B
```

checks:
BreakoutInMeanRangesComponent: every check passed
the bot's suite: == 1640 passed, 16 skipped, 75 deselected, 2244 warnings in 73.12s (0:01:13) ===
