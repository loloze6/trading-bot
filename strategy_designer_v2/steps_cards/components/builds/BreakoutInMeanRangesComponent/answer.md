# BreakoutInMeanRangesComponent: night7c_panic_run | 032-02.b2.d1_volatile-ten-day-low-rebound_1d | LowBreakDepthInMeanRangesComponent

## attempt 1

answer: built
class: BreakoutInMeanRangesComponent
settings: {"period": 10, "base_period": 30, "side": "below", "extreme": "low"}
reason: `BreakoutInMeanRangesComponent` already measures how far the close sits beyond a prior `period`-bar extreme, in mean bar ranges, but its level is always the prior high (its "below" is H − close). The break under the prior low is the same measure against the other extreme. No config step gives it (`negate` of either side is not it), so it needs one new setting, `extreme`, whose default "high" keeps today's output exactly.

table: Directional components
row: | `BreakoutInMeanRangesComponent` | `period` (12), `base_period` (180), `side` ("above"), `high_current` (0), `base_exclude_current` (0), `extreme` ("high") | X = the level, the extreme of the stretch. Stretch: bars t-`period` .. t-1 (`high_current` 0) or t-`period`+1 .. t (`high_current` 1). With `extreme` "high", X = max(high) over the stretch. With `extreme` "low", X = min(low) over it. `side` "above": max(0, close[t] − X) / B. `side` "below": max(0, X − close[t]) / B. B = mean(high[i] − low[i]) over bars t-`base_period`+1 .. t (`base_exclude_current` 0) or t-`base_period` .. t-1 (`base_exclude_current` 1). 0.0 when B = 0. With `period` 10, `base_period` 30, "below", "low": max(0, min(low[t-10..t-1]) − close[t]) / mean(high[i] − low[i], i = t-29 .. t) | 0 and up, unbounded above, never negative; no direction. "above" is 0 when the close is at or below X; "below" is 0 when it is at or above X. Both grow linearly with the close's distance beyond X. With `extreme` "high", "above" is always 0 when `high_current` is 1. With `extreme` "low", "below" is always 0 when `high_current` is 1 | graded | mean bar ranges | max(`base_period` + `base_exclude_current`, `period` + 1 − `high_current`) (180; 30 at the wished settings) | close, high, low. Reads the high (`extreme` "high") or the low (`extreme` "low") over the stretch, high and low over the base rows, and close[t]. A NaN in any of those gives NaN. These settings raise when the component is built: `period` < 1, `base_period` < 1, `side` other than "above" or "below", `high_current` not 0 or 1, `base_exclude_current` not 0 or 1, `extreme` other than "high" or "low" | stateless. `extreme` "high" (default) with the other defaults is the original output, unchanged. With `extreme` "low", "below" is the breakdown under the prior `period`-bar low in mean bar ranges; no config step gives it, hence the setting. With `high_current` 0 the stretch excludes bar t, so bar t's own move cannot change X. B = 0 needs `base_period` zero-range bars in a row and reads 0.0. Continuous in the close. On 1d bars the wished settings give the close's depth under the prior 10-day low in 30-day mean daily ranges. Not `NarrowRangeBreakoutComponent` "below". No `scaling_factor`: scale it with transforms |

```python class
class BreakoutInMeanRangesComponent(SubStrategyComponent):
    """
    The close's distance beyond a prior extreme, counted in mean bar ranges, on every bar.

        stretch = bars t-period .. t-1          (high_current 0, default: bar t excluded)
                  bars t-period+1 .. t          (high_current 1: bar t included)
        extreme = "high" (default): X = max(high[stretch])
        extreme = "low":            X = min(low[stretch])
        base    = bars t-base_period+1 .. t     (base_exclude_current 0, default)
                  bars t-base_period .. t-1     (base_exclude_current 1)
        B = mean(high[i] - low[i]) over the base rows
        side = "above" (default): raw_value = max(0, close[t] - X) / B
        side = "below":           raw_value = max(0, X - close[t]) / B
        raw_value = 0.0 when B = 0

    With period 10, base_period 30, side "below" and extreme "low", the value is
    max(0, min(low[t-10..t-1]) - close[t]) / mean(high[i] - low[i], i = t-29 .. t).

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 when the close is not
    beyond X on the chosen side, and it grows linearly with the distance. The defaults (extreme "high",
    side "above", high_current 0, base_exclude_current 0) are the original output, unchanged.
    Warm-up: max(base_period + base_exclude_current, period + 1 - high_current) rows, bar t included.

    NaN: a NaN in the stretch's high (extreme "high") or low (extreme "low"), a NaN high or low in the
    base rows, or a NaN close[t] gives NaN.

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data):
    the stretch ends at bar t-1 (or at bar t with high_current 1), the base ends at bar t or t-1, and the
    close is close[t]; every one of these values is known at bar t's close.

    Building the component raises for period < 1, base_period < 1, side other than "above" or "below",
    high_current not 0 or 1, base_exclude_current not 0 or 1, and extreme other than "high" or "low".
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
        if hc not in (0, 1) or isinstance(hc, float) and hc != int(hc):
            raise ValueError(f"BreakoutInMeanRangesComponent: high_current must be 0 or 1, got {hc!r}")
        self.high_current = int(hc)
        be = self.parameters.get("base_exclude_current", 0)
        if be not in (0, 1):
            raise ValueError(f"BreakoutInMeanRangesComponent: base_exclude_current must be 0 or 1, got {be!r}")
        self.base_exclude_current = int(be)
        self.extreme = self.parameters.get("extreme", "high")
        if self.extreme not in ("high", "low"):
            raise ValueError(f"BreakoutInMeanRangesComponent: extreme must be 'high' or 'low', got {self.extreme!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float)
        low = data['low'].astype(float)
        close = data['close'].astype(float)
        n = len(data)
        hc = self.high_current
        s_start = n - 1 - self.period + hc
        s_stop = n - 1 + hc
        src = high if self.extreme == "high" else low
        stretch = src.iloc[s_start:s_stop]
        be = self.base_exclude_current
        b_start = n - self.base_period - be
        b_stop = n - be
        bh = high.iloc[b_start:b_stop]
        bl = low.iloc[b_start:b_stop]
        c = float(close.iloc[-1])
        if stretch.isna().any() or bh.isna().any() or bl.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        level = float(stretch.max()) if self.extreme == "high" else float(stretch.min())
        B = float((bh - bl).mean())
        if B == 0:
            self._raw_value = 0.0
        else:
            dist = (c - level) if self.side == "above" else (level - c)
            self._raw_value = float(max(0.0, dist) / B)
        self.confidence = 1.0
        self.debug_info = {'level': level, 'mean_bar_range': B, 'side': self.side, 'extreme': self.extreme}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.base_period + self.base_exclude_current, self.period + 1 - self.high_current)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hc = int(params.get("high_current", 0))
    be = int(params.get("base_exclude_current", 0))
    extreme = params.get("extreme", "high")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    # the stretch: bars t-p .. t-1 (hc 0) or t-p+1 .. t (hc 1)
    first = t - p + hc
    last = t - 1 + hc
    vals = []
    i = first
    while i <= last:
        vals.append(h[i] if extreme == "high" else l[i])
        i += 1

    # the base: bars t-bp+1 .. t (be 0) or t-bp .. t-1 (be 1)
    ranges = []
    for k in range(bp):
        j = t - be - k
        if h[j] != h[j] or l[j] != l[j]:
            return float("nan")
        ranges.append(h[j] - l[j])

    for v in vals:
        if v != v:
            return float("nan")
    if c[t] != c[t]:
        return float("nan")

    level = vals[0]
    for v in vals:
        if extreme == "high":
            if v > level:
                level = v
        else:
            if v < level:
                level = v

    total = 0.0
    for r in ranges:
        total += r
    B = total / bp
    if B == 0:
        return 0.0

    if side == "above":
        d = c[t] - level
    else:
        d = level - c[t]
    if d < 0:
        d = 0.0
    return d / B
```

checks:
BreakoutInMeanRangesComponent: every check passed
the bot's suite: == 1657 passed, 16 skipped, 75 deselected, 2244 warnings in 99.41s (0:01:39) ===
