# BreakoutInMeanRangesComponent: night7_steadydecline_run | 036-02_fall-vs-range-next-day-rebound_1d | FallInMeanBarRanges

## attempt 1

answer: built
class: BreakoutInMeanRangesComponent
settings: {"period": 1, "base_period": 30, "side": "below", "high_current": 0, "base_exclude_current": 1, "source": "close"}
reason: `BreakoutInMeanRangesComponent` already measures how far the close sits below a prior reference level, counted in mean bar ranges, and it already offers the 30-day base that excludes bar t. Its level can only be a high, though, so it cannot give the close-to-close fall. A `source` setting ("high" by default, which keeps today's output) lets the level be the prior closes, and with `period` 1 that level is close[t-1].

table: Directional components
row: | `BreakoutInMeanRangesComponent` | `period` (12), `base_period` (180), `side` ("above"), `high_current` (0), `base_exclude_current` (0), `source` ("high") | `side` "above": max(0, close[t] − H) / B. `side` "below": max(0, H − close[t]) / B. H = max(X[t-`period`..t-1]) (`high_current` 0) or max(X[t-`period`+1..t]) (`high_current` 1), where X is the high (`source` "high") or the close (`source` "close"). B = mean(high[i] − low[i]) over bars t-`base_period`+1 .. t (`base_exclude_current` 0, bar t included) or t-`base_period` .. t-1 (`base_exclude_current` 1, bar t excluded). 0.0 when B = 0. With `period` 1, `base_period` 20, `side` "below", `high_current` 1 and `base_exclude_current` 1: (high[t] − close[t]) / mean(high[i] − low[i], i = t-20 .. t-1). With `period` 1, `base_period` 30, `side` "below", `high_current` 0, `base_exclude_current` 1 and `source` "close": max(0, close[t-1] − close[t]) / mean(high[i] − low[i], i = t-30 .. t-1) | 0 and up, unbounded above, never negative; no direction. "above": 0 when the close is at or below H, growing linearly with the size of the break (always 0 with `high_current` 1, since close[t] ≤ H). "below": 0 when the close is at or above H, growing linearly as the close sits deeper below it. With `base_exclude_current` 0, the "below" value with `period` 1 and `high_current` 1 is at most `base_period`; with 1 it is unbounded | graded | mean bar ranges | max(`base_period` + `base_exclude_current`, `period` + 1 − `high_current`) (180; 31 at the wished settings) | close, high, low. A NaN value of the `source` column in the stretch, a NaN high or low in the base rows, or a NaN close[t] gives NaN. These settings raise when the component is built: `period` < 1, `base_period` < 1, `side` other than "above" or "below", `high_current` not 0 or 1, `base_exclude_current` not 0 or 1, `source` other than "high" or "close" | stateless. `side` "above" with `high_current` 0, `base_exclude_current` 0 and `source` "high" (the defaults) is the original output, unchanged. `source` "high" is the original level. `source` "close" takes the level from the prior closes, and no config step gives it, hence the setting. With `period` 1 and `high_current` 0, that level is close[t-1], so "below" is the day's close-to-close fall in prior mean daily ranges (0 on up days, above 1 when the fall exceeds the usual range). With `high_current` 0 the stretch excludes bar t, so bar t's own move cannot change H. `high_current` 1 lets H include bar t. `base_exclude_current` 1 sets the distance against the prior `base_period` bars' mean range, so bar t's own range cannot raise its base. B = 0 needs `base_period` zero-range bars in a row and reads 0.0. Continuous in the close. Not `NarrowRangeBreakoutComponent`. No `scaling_factor`: scale it with transforms |

```python class
class BreakoutInMeanRangesComponent(SubStrategyComponent):
    """
    Distance of the close from a reference level, counted in mean bar ranges:

        X = high   (source "high", default)  or  close  (source "close")
        H = max(X[t-period .. t-1])        (high_current 0, default: bar t excluded)
            max(X[t-period+1 .. t])        (high_current 1: bar t included)
        B = mean(high[i] - low[i]) over i = t-base_period+1 .. t   (base_exclude_current 0, default)
                                     over i = t-base_period .. t-1 (base_exclude_current 1)
        side "above" (default): raw_value = max(0, close[t] - H) / B
        side "below":           raw_value = max(0, H - close[t]) / B
        raw_value = 0.0 when B = 0.

    The defaults (side "above", high_current 0, base_exclude_current 0, source "high") are the
    original output, unchanged. With period 1, base_period 30, side "below", high_current 0,
    base_exclude_current 1 and source "close" the output is
    max(0, close[t-1] - close[t]) / mean(high[i] - low[i], i = t-30 .. t-1): the day's close-to-close
    fall in prior 30-day mean daily ranges, which is 0 on up days.
    Range: 0 and up, unbounded above, never negative; no direction. Graded, linear in the close.
    Warm-up: max(base_period + base_exclude_current, period + 1 - high_current) rows, bar t included.
    NaN: a NaN source value in the stretch, a NaN high or low in the base rows, or a NaN close[t]
    gives NaN. Building raises for period < 1, base_period < 1, side not "above"/"below",
    high_current or base_exclude_current not 0/1, source not "high"/"close".

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data).
    These are the stretch rows t-period .. t (at most), the base rows t-base_period .. t, and close[t].
    All of them are known at bar t's close.
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

        def _flag(key):
            v = self.parameters.get(key, 0)
            if isinstance(v, bool):
                v = int(v)
            if v not in (0, 1):
                raise ValueError(f"BreakoutInMeanRangesComponent: {key} must be 0 or 1, got {v!r}")
            return int(v)

        self.high_current = _flag("high_current")
        self.base_exclude_current = _flag("base_exclude_current")
        self.source = self.parameters.get("source", "high")
        if self.source not in ("high", "close"):
            raise ValueError(f"BreakoutInMeanRangesComponent: source must be 'high' or 'close', got {self.source!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = len(data)
        close = data["close"].astype(float)
        high = data["high"].astype(float)
        low = data["low"].astype(float)
        src = close if self.source == "close" else high

        if self.high_current == 1:
            stretch = src.iloc[n - self.period:n]
        else:
            stretch = src.iloc[n - 1 - self.period:n - 1]
        if self.base_exclude_current == 1:
            b_hi = high.iloc[n - 1 - self.base_period:n - 1]
            b_lo = low.iloc[n - 1 - self.base_period:n - 1]
        else:
            b_hi = high.iloc[n - self.base_period:n]
            b_lo = low.iloc[n - self.base_period:n]
        c = float(close.iloc[-1])

        if stretch.isna().any() or b_hi.isna().any() or b_lo.isna().any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(stretch.max())
        B = float((b_hi.to_numpy() - b_lo.to_numpy()).mean())
        if B == 0:
            self._raw_value = 0.0
        elif self.side == "above":
            self._raw_value = float(max(0.0, c - H) / B)
        else:
            self._raw_value = float(max(0.0, H - c) / B)
        self.confidence = 1.0
        self.debug_info = {"level": H, "mean_bar_range": B, "source": self.source, "side": self.side}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
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
    closes = [float(x) for x in list(df["close"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    xs = closes if source == "close" else highs

    # reference level: stretch ends at t-1 (hc 0) or at t (hc 1), p bars long
    end = t if hc == 1 else t - 1
    level_vals = [xs[i] for i in range(end - p + 1, end + 1)]
    # base: bp bar ranges ending at t (bex 0) or t-1 (bex 1)
    bend = t - bex
    ranges = [highs[i] - lows[i] for i in range(bend - bp + 1, bend + 1)]
    c = closes[t]
    for v in level_vals + ranges + [c]:
        if v != v:
            return float("nan")
    H = level_vals[0]
    for v in level_vals:
        if v > H:
            H = v
    total = 0.0
    for r in ranges:
        total += r
    B = total / len(ranges)
    if B == 0:
        return 0.0
    if side == "above":
        d = c - H
    else:
        d = H - c
    if d < 0:
        d = 0.0
    return d / B
```

checks:
BreakoutInMeanRangesComponent: every check passed
the bot's suite: == 1657 passed, 16 skipped, 75 deselected, 2244 warnings in 118.55s (0:01:58) ==
