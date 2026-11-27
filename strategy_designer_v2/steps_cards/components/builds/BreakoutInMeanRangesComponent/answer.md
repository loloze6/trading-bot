# BreakoutInMeanRangesComponent: night9_chopstretch_run | 076-01_agitated-wide-high-close-fades_1d | CloseAboveLowInMeanRangesComponent

## attempt 1

answer: built
class: BreakoutInMeanRangesComponent
settings: {"period": 1, "base_period": 20, "side": "above", "high_current": 1, "base_exclude_current": 0, "source": "high", "extreme": "low"}
reason: `BreakoutInMeanRangesComponent` already measures the close's distance from a recent extreme in mean bar ranges, but only from the high. The wished measure is the same distance taken from the low (low[t] with `period` 1, `high_current` 1), and no config step gives it, so the class gains an `extreme` setting whose default "high" keeps today's output exactly.

table: Directional components
row: | `BreakoutInMeanRangesComponent` | `period` (12), `base_period` (180), `side` ("above"), `high_current` (0), `base_exclude_current` (0), `source` ("high"), `extreme` ("high") | R = max(X[t-`period`..t-1]) (`high_current` 0) or max(X[t-`period`+1..t]) (`high_current` 1) with `extreme` "high"; min over the same bars with `extreme` "low". X is the close (`source` "close") or the bar's extreme on the `extreme` side (`source` "high": the `high` column for "high", the `low` column for "low"). `side` "above": max(0, close[t] − R) / B. `side` "below": max(0, R − close[t]) / B. B = mean(high[i] − low[i]) over bars t-`base_period`+1 .. t (`base_exclude_current` 0) or t-`base_period` .. t-1 (`base_exclude_current` 1). 0.0 when B = 0. With `period` 1, `base_period` 20, "above", `high_current` 1, `base_exclude_current` 0, `source` "high", `extreme` "low": (close[t] − low[t]) / mean(high[i] − low[i], i = t-19 .. t) | 0 and up, unbounded above, never negative; no direction. "above": 0 when the close is at or below R. "below": 0 when the close is at or above R. Both grow linearly with the distance. With `extreme` "low", `source` "high" and `high_current` 1, "above" is the close's height above the low in mean bar ranges, at most `base_period` with `base_exclude_current` 0 (the mean includes bar t's range); "below" is then 0 on every real bar | graded | mean bar ranges | max(`base_period` + `base_exclude_current`, `period` + 1 − `high_current`) (180; 20 at the wished settings) | close, high, low. A NaN in the stretch's X values, a NaN high or low in the base rows, or a NaN close[t] gives NaN. B = 0 (`base_period` zero-range bars in a row, never on real bars) gives 0.0. These settings raise when the component is built: `period` < 1, `base_period` < 1, `side` other than "above" or "below", `high_current` not 0 or 1, `base_exclude_current` not 0 or 1, `source` other than "high" or "close", `extreme` other than "high" or "low" | stateless. `extreme` "high" (default) is the original output, unchanged, and so are all earlier settings. `extreme` "low" measures from the window's low; no config step gives it (`negate` of a distance from the high is not it), hence the setting. At the wished settings on 1d bars it equals `CloseLocationInRangeComponent` (`reference` "low") x the day's range over its 20-day mean range (bar t included). It is continuous in the prices. With `high_current` 0 the stretch excludes bar t, so bar t's own move cannot change R. No `scaling_factor`: scale it with transforms |

```python class
class BreakoutInMeanRangesComponent(SubStrategyComponent):
    """
    Distance of the close from a recent extreme, in mean bar ranges, on every bar:

        stretch = bars t-period .. t-1 (high_current 0) or t-period+1 .. t (high_current 1)
        X = close (source "close"), or the bar's extreme on the `extreme` side (source "high"):
            the high column with extreme "high", the low column with extreme "low"
        R = max(X over the stretch) (extreme "high", default) or min(X over the stretch) (extreme "low")
        B = mean(high[i] - low[i]) over bars t-base_period+1 .. t (base_exclude_current 0)
            or t-base_period .. t-1 (base_exclude_current 1)
        side "above": raw_value = max(0, close[t] - R) / B
        side "below": raw_value = max(0, R - close[t]) / B
        raw_value = 0.0 when B = 0.

    With period 1, base_period 20, side "above", high_current 1, base_exclude_current 0, source "high" and
    extreme "low": (close[t] - low[t]) / mean(high[i] - low[i], i = t-19 .. t), the close location in the bar
    times the bar's range multiple.
    The defaults (extreme "high" and every earlier default) give the original output, unchanged.
    Range: 0 and up, unbounded above, never negative; no direction; graded, linear in the distance.
    Warm-up: max(base_period + base_exclude_current, period + 1 - high_current) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the high, low and close of rows up to and including bar t (the last row
    of data): the stretch ends at bar t-1 or t, the base rows end at bar t or t-1, and close[t] is known at
    bar t's close.

    NaN: a NaN X value in the stretch, a NaN high or low in the base rows, or a NaN close[t] gives NaN.
    Building the component raises for period < 1, base_period < 1, side not "above"/"below", high_current or
    base_exclude_current not 0 or 1, source not "high"/"close", extreme not "high"/"low".
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
        bex = self.parameters.get("base_exclude_current", 0)
        if bex not in (0, 1):
            raise ValueError(f"BreakoutInMeanRangesComponent: base_exclude_current must be 0 or 1, got {bex!r}")
        self.base_exclude_current = int(bex)
        self.source = self.parameters.get("source", "high")
        if self.source not in ("high", "close"):
            raise ValueError(f"BreakoutInMeanRangesComponent: source must be 'high' or 'close', got {self.source!r}")
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
        n = len(data)
        t = n - 1
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        if self.source == "close":
            col = close
        elif self.extreme == "high":
            col = high
        else:
            col = low
        if self.high_current == 1:
            stretch = col[t - self.period + 1:t + 1]
        else:
            stretch = col[t - self.period:t]
        b_stop = n - self.base_exclude_current
        b_start = b_stop - self.base_period
        bh = high[b_start:b_stop]
        bl = low[b_start:b_stop]
        c = close[t]
        self.confidence = 1.0
        if np.isnan(stretch).any() or np.isnan(bh).any() or np.isnan(bl).any() or np.isnan(c):
            self._raw_value = float("nan")
            return
        level = float(np.max(stretch)) if self.extreme == "high" else float(np.min(stretch))
        base = float(np.mean(bh - bl))
        if self.side == "above":
            dist = max(0.0, float(c) - level)
        else:
            dist = max(0.0, level - float(c))
        self._raw_value = 0.0 if base == 0 else float(dist / base)
        self.debug_info = {'level': level, 'mean_bar_range': base, 'distance': dist,
                           'extreme': self.extreme, 'side': self.side}

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
    bex = int(params.get("base_exclude_current", 0))
    source = params.get("source", "high")
    extreme = params.get("extreme", "high")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    if source == "close":
        x = c
    elif extreme == "high":
        x = h
    else:
        x = l

    # stretch bars
    if hc == 1:
        idx = [t - k for k in range(p)]          # t-p+1 .. t
    else:
        idx = [t - 1 - k for k in range(p)]      # t-p .. t-1
    vals = [x[i] for i in idx]

    # base rows
    last = t - bex
    ranges = []
    for k in range(bp):
        i = last - k
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
        ranges.append(h[i] - l[i])

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
        total = total + r
    mean_range = total / len(ranges)

    if side == "above":
        d = c[t] - level
    else:
        d = level - c[t]
    if d < 0:
        d = 0.0
    if mean_range == 0:
        return 0.0
    return d / mean_range
```

checks:
BreakoutInMeanRangesComponent: every check passed
the bot's suite: == 1677 passed, 16 skipped, 75 deselected, 2244 warnings in 151.78s (0:02:31) ==
