# RangeCompressionRatioComponent: night_006_run | 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation_1d | RangeWidthRatio

## attempt 1

answer: built
class: RangeCompressionRatioComponent
settings: {"short_period": 20, "long_period": 100, "form": "width"}
reason: The wished ratio, short range / long range with both windows ending at bar t, is the exact mirror (1 minus) of `RangeCompressionRatioComponent`. No config step gives 1 minus a value, so it is a new setting `form` on that class: "width" gives the ratio, and the default "compression" keeps today's output unchanged.

table: Regime measures
row: | `RangeCompressionRatioComponent` | `short_period` (20), `long_period` (100), `exclude_current` (0), `form` ("compression") | ratio = (max(high) − min(low) over the last `short_period` bars) / (max(high) − min(low) over the last `long_period` bars). Both windows end at bar t inclusive (`exclude_current` 0) or at bar t-1 (`exclude_current` 1: bars t-`short_period` .. t-1 and t-`long_period` .. t-1). `form` "compression": 1 − ratio, 0.0 when the long range is 0. `form` "width": ratio, 1.0 when the long range is 0 | 0 to 1, never negative; no direction. "compression": 0 when the short range spans the whole long range, near 1 when the short band is very narrow. "width": near 0 when the short band is very narrow, 1 when the short range spans the whole long range | regime measure | dimensionless | `long_period` + `exclude_current` (100) | high, low. A NaN high or low anywhere in the long window gives NaN. These settings raise when the component is built: `short_period` < 1, `short_period` >= `long_period`, `exclude_current` not 0 or 1, `form` other than "compression" or "width" | stateless. The short window is inside the long one, so the ratio never exceeds 1. `form` "compression" (default) is the original output, unchanged. "width" is 1 minus it (no config step gives 1 minus a value, hence the setting); it grows as the short range widens toward the full long range. `exclude_current` 1 gives the band before bar t, which bar t's own move cannot alter |

```python class
class RangeCompressionRatioComponent(SubStrategyComponent):
    """
    How narrow the recent high-low band is against a longer one, on every bar:

        exclude_current = 0 (default): end = t      (windows end at bar t, included)
        exclude_current = 1:           end = t - 1  (windows end at bar t-1)
        S = max(high[end-short_period+1 .. end]) - min(low[end-short_period+1 .. end])
        L = max(high[end-long_period+1 .. end])  - min(low[end-long_period+1 .. end])
        form = "compression" (default): raw_value = 1 - S / L   (0.0 when L is 0)
        form = "width":                  raw_value = S / L       (1.0 when L is 0)

    "width" is exactly 1 minus "compression". No config step gives 1 minus a value, so it is a setting.
    The defaults (form "compression", exclude_current 0) give the original output, unchanged.
    With short_period 20, long_period 100 and form "width", the output is
    (max high - min low over the last 20 bars) / (max high - min low over the last 100 bars).

    Range and sign: 0 to 1, never negative, no direction. The short window lies inside the long one, so S <= L.
    Graded: the value moves continuously with the two ranges.
    Warm-up: long_period + exclude_current rows, bar t included.

    NaN: a NaN high or low anywhere in the long window gives NaN. A missing high or low column raises.
    Building the component raises for a short_period below 1, a short_period at or above long_period, an
    exclude_current other than 0 or 1, or a form other than "compression" or "width".

    WHY THIS CANNOT LEAK: it reads only the high and low columns of the last long_period + exclude_current rows
    of data, the last of which is bar t; a bar's high and low are known at that bar's close.
    """

    def __init__(self, name="RangeCompressionRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 20))
        self.long_period = int(self.parameters.get("long_period", 100))
        if self.short_period < 1:
            raise ValueError(f"RangeCompressionRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"RangeCompressionRatioComponent: short_period must be below long_period, got "
                f"{self.short_period} and {self.long_period}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"RangeCompressionRatioComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        form = self.parameters.get("form", "compression")
        if form not in ("compression", "width"):
            raise ValueError(
                f"RangeCompressionRatioComponent: form must be 'compression' or 'width', got {form!r}")
        self.form = form
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        end = len(high) - self.exclude_current
        lh = high[end - self.long_period:end]
        ll = low[end - self.long_period:end]
        sh = high[end - self.short_period:end]
        sl = low[end - self.short_period:end]
        if np.isnan(lh).any() or np.isnan(ll).any():
            self._raw_value = float("nan")
            self.debug_info = {'short_range': float("nan"), 'long_range': float("nan")}
        else:
            long_range = float(lh.max() - ll.min())
            short_range = float(sh.max() - sl.min())
            if not long_range > 0:
                compression = 0.0
                width = 1.0
            else:
                ratio = short_range / long_range
                compression = 1.0 - ratio
                width = ratio
            self._raw_value = float(width if self.form == "width" else compression)
            self.debug_info = {'short_range': short_range, 'long_range': long_range, 'form': self.form}
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.long_period + self.exclude_current
```

```python hand
def hand(df, params):
    sp = int(params.get("short_period", 20))
    lp = int(params.get("long_period", 100))
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "compression")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    last = len(h) - 1 - ex
    for i in range(last - lp + 1, last + 1):
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
    hi_l = h[last - lp + 1]
    lo_l = l[last - lp + 1]
    for i in range(last - lp + 1, last + 1):
        if h[i] > hi_l:
            hi_l = h[i]
        if l[i] < lo_l:
            lo_l = l[i]
    hi_s = h[last - sp + 1]
    lo_s = l[last - sp + 1]
    for i in range(last - sp + 1, last + 1):
        if h[i] > hi_s:
            hi_s = h[i]
        if l[i] < lo_s:
            lo_s = l[i]
    long_range = hi_l - lo_l
    short_range = hi_s - lo_s
    if form == "width":
        if not long_range > 0:
            return 1.0
        return short_range / long_range
    if not long_range > 0:
        return 0.0
    return 1.0 - short_range / long_range
```

checks:
RangeCompressionRatioComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1536 passed, 8 skipped, 74 deselected, 2170 warnings in 57.03s ========
