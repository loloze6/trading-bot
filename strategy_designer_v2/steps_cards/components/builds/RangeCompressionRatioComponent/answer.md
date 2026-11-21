# RangeCompressionRatioComponent: night3_4h_run | 019-04_downward-breakout-quiet-continuation_4h | StretchRangeToAverageBarRange

## attempt 1

answer: built
class: RangeCompressionRatioComponent
settings: {"short_period": 12, "long_period": 180, "exclude_current": 2, "form": "compression", "base": "mean_bar_range"}
reason: `RangeCompressionRatioComponent` with `base` "mean_bar_range" and `form` "compression" computes this measure, but its `exclude_current` moves both windows together. It cannot take the stretch from bars t-12..t-1 while averaging bar ranges over t-179..t, and that one-bar shift of the base changes the output on real bars. The class is written again with a new value of the same setting, `exclude_current` 2 (bar t left out of the short window only); values 0 and 1 keep today's output exactly.

table: Regime measures
row: | `RangeCompressionRatioComponent` | `short_period` (20), `long_period` (100), `exclude_current` (0), `form` ("compression"), `base` ("range") | S = max(high) − min(low) over the short window, B over the long window. `exclude_current` 0: short = bars t-`short_period`+1 .. t, long = bars t-`long_period`+1 .. t. `exclude_current` 1: short = bars t-`short_period` .. t-1, long = bars t-`long_period` .. t-1. `exclude_current` 2: short = bars t-`short_period` .. t-1, long = bars t-`long_period`+1 .. t (bar t excluded from the stretch only). With `base` "range", B = max(high) − min(low) over the long window. With `base` "mean_bar_range", B = mean(high[i] − low[i]) over it. ratio = S / B. `form` "compression": 1 − ratio, 0.0 when B is 0. `form` "width": ratio, 1.0 when B is 0 | `base` "range": 0 to 1, never negative, no direction. "compression" is 0 when the short range spans the whole long range and near 1 when the short band is very narrow; "width" is the reverse (with `exclude_current` 2 the short window can reach outside the long one by one bar only when `short_period` = `long_period` − 1, so "range" can then exceed its bounds slightly). `base` "mean_bar_range": "width" is 0 and up, unbounded, typically above 1 (a stretch counted in average bar ranges), falling as the stretch narrows; "compression" is 1 − that, up to 1, signed, rising as it narrows | regime measure | dimensionless | `long_period` + 1 if `exclude_current` is 1, else `long_period` (100) | high, low. A NaN high or low in any row read (the long window, and the short window) gives NaN. These settings raise when the component is built: `short_period` < 1, `short_period` >= `long_period`, `exclude_current` not 0, 1 or 2, `form` other than "compression" or "width", `base` other than "range" or "mean_bar_range" | stateless. `exclude_current` 0 and 1 and `base` "range" are the original outputs, unchanged. `exclude_current` 2 gives the stretch before bar t (which bar t's own move cannot widen) against the average bar range including bar t, the base `NarrowRangeBreakoutComponent` uses. "width" is 1 minus "compression" (no config step gives 1 minus a value, hence the setting) |

```python class
class RangeCompressionRatioComponent(SubStrategyComponent):
    """
    How narrow a short stretch of bars is against a longer base, on every bar.

        exclude_current = 0 (default): short = bars t-short_period+1 .. t,  long = bars t-long_period+1 .. t
        exclude_current = 1:           short = bars t-short_period .. t-1,  long = bars t-long_period .. t-1
        exclude_current = 2:           short = bars t-short_period .. t-1,  long = bars t-long_period+1 .. t
        S = max(high[short]) - min(low[short])
        base = "range" (default):    B = max(high[long]) - min(low[long])
        base = "mean_bar_range":     B = mean(high[i] - low[i] for i in long)
        ratio = S / B
        form = "compression" (default): raw_value = 1 - ratio   (0.0 when B == 0)
        form = "width":                 raw_value = ratio       (1.0 when B == 0)

    Range & sign: base "range": 0 to 1, never negative, no direction ("compression" near 1 when the short band is
    very narrow, 0 when it spans the whole long range; "width" the reverse). base "mean_bar_range": "width" is 0 and
    up, unbounded (the stretch counted in average bar ranges); "compression" is 1 minus that, up to 1, signed,
    rising as the stretch narrows. Graded.
    Warm-up: long_period + 1 rows when exclude_current is 1, else long_period rows (bar t included); the short
    window needs short_period + 1 rows at most, never more than long_period since short_period < long_period.
    exclude_current 0 and 1 and base "range" are the original outputs, unchanged. exclude_current 2 leaves bar t
    out of the stretch only, so bar t's own move cannot widen it, while the base of average bar ranges includes it.

    NaN: a NaN high or low in any row read (long window or short window) gives NaN. A missing column raises.
    Building the component raises for short_period < 1, short_period >= long_period, exclude_current not 0, 1 or 2,
    form other than "compression" or "width", base other than "range" or "mean_bar_range".

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the last long_period + 1 rows at most of
    data, the last row being bar t; no later row exists in the data it is given.
    """

    def __init__(self, name="RangeCompression", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 20))
        self.long_period = int(self.parameters.get("long_period", 100))
        if self.short_period < 1:
            raise ValueError(f"RangeCompressionRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"RangeCompressionRatioComponent: short_period must be < long_period, "
                f"got {self.short_period} and {self.long_period}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1, 2):
            raise ValueError(f"RangeCompressionRatioComponent: exclude_current must be 0, 1 or 2, got {ex!r}")
        self.exclude_current = int(ex)
        self.form = self.parameters.get("form", "compression")
        if self.form not in ("compression", "width"):
            raise ValueError(
                f"RangeCompressionRatioComponent: form must be 'compression' or 'width', got {self.form!r}")
        self.base = self.parameters.get("base", "range")
        if self.base not in ("range", "mean_bar_range"):
            raise ValueError(
                f"RangeCompressionRatioComponent: base must be 'range' or 'mean_bar_range', got {self.base!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float)
        low = data['low'].astype(float)
        sp = self.short_period
        lp = self.long_period
        if self.exclude_current == 1:
            lh, ll = high.iloc[-(lp + 1):-1], low.iloc[-(lp + 1):-1]
            sh, sl = high.iloc[-(sp + 1):-1], low.iloc[-(sp + 1):-1]
        elif self.exclude_current == 2:
            lh, ll = high.iloc[-lp:], low.iloc[-lp:]
            sh, sl = high.iloc[-(sp + 1):-1], low.iloc[-(sp + 1):-1]
        else:
            lh, ll = high.iloc[-lp:], low.iloc[-lp:]
            sh, sl = high.iloc[-sp:], low.iloc[-sp:]
        if lh.isna().any() or ll.isna().any() or sh.isna().any() or sl.isna().any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        s_range = float(sh.max() - sl.min())
        if self.base == "mean_bar_range":
            b = float((lh - ll).mean())
        else:
            b = float(lh.max() - ll.min())
        if b == 0:
            self._raw_value = 0.0 if self.form == "compression" else 1.0
        else:
            ratio = s_range / b
            self._raw_value = float(1.0 - ratio) if self.form == "compression" else float(ratio)
        self.confidence = 1.0
        self.debug_info = {'short_range': s_range, 'base': b, 'base_kind': self.base,
                           'exclude_current': self.exclude_current}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.long_period + (1 if self.exclude_current == 1 else 0)
```

```python hand
def hand(df, params):
    sp = int(params.get("short_period", 20))
    lp = int(params.get("long_period", 100))
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "compression")
    base = params.get("base", "range")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(h) - 1

    if ex == 1:
        long_idx = list(range(t - lp, t))
        short_idx = list(range(t - sp, t))
    elif ex == 2:
        long_idx = list(range(t - lp + 1, t + 1))
        short_idx = list(range(t - sp, t))
    else:
        long_idx = list(range(t - lp + 1, t + 1))
        short_idx = list(range(t - sp + 1, t + 1))

    for i in long_idx + short_idx:
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")

    top = h[short_idx[0]]
    bottom = l[short_idx[0]]
    for i in short_idx:
        if h[i] > top:
            top = h[i]
        if l[i] < bottom:
            bottom = l[i]
    s_range = top - bottom

    if base == "mean_bar_range":
        total = 0.0
        for i in long_idx:
            total = total + (h[i] - l[i])
        b = total / len(long_idx)
    else:
        top = h[long_idx[0]]
        bottom = l[long_idx[0]]
        for i in long_idx:
            if h[i] > top:
                top = h[i]
            if l[i] < bottom:
                bottom = l[i]
        b = top - bottom

    if b == 0:
        return 0.0 if form == "compression" else 1.0
    ratio = s_range / b
    if form == "compression":
        return 1.0 - ratio
    return ratio
```

checks:
RangeCompressionRatioComponent: every check passed
the bot's suite: ======= 1586 passed, 16 skipped, 75 deselected, 2244 warnings in 43.20s ========
