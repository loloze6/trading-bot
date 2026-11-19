# VolumeRatioComponent: slow_1h_run | 016-05_up-even-volume-continuation_1h | VolumeEvenness

## attempt 1

answer: built
class: VolumeRatioComponent
settings: {"period": 72, "short_period": 72, "short_statistic": "median"}
reason: The median of the last 72 volumes over their mean is `VolumeRatioComponent` with the median as the recent statistic instead of the mean. Today the numerator is always a mean (`short_period` 72 with `statistic` "median" gives only the reciprocal, mean over median, and no config step inverts a value), so I added one setting, `short_statistic` ("mean" by default, which leaves today's output unchanged). On real bars the value is 0 to 2, not 0 to 1. It sits below 1 when volume is right-skewed, as hourly volume usually is, and rises toward 1 as the volume spreads evenly.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (0), `short_period` (1), `form` ("ratio"), `statistic` ("mean"), `short_statistic` ("mean") | r = A / B. A is the `short_statistic` of the volume over the last `short_period` bars, bar t included ("mean": the mean; "median": the median, the average of the two middle values for an even count). B is the `statistic` (same choices) of the volume over the last `period` bars, bar t included (`exclude_current` 0), or over volume[t-period] .. volume[t-1], bar t excluded (`exclude_current` 1). The output is r (`form` "ratio"), r - 1 (`form` "centred"), or ln(r) (`form` "log"). At the defaults it is volume[t] / mean(last `period` volumes). With `period` 72, `short_period` 72 and `short_statistic` "median" it is median / mean of the last 72 volumes, the evenness of volume over the window | "ratio": never negative, 1 when A equals the base. With both statistics "mean" and `exclude_current` 0, it runs 0 to `period` / `short_period`. With `short_period` = `period`, `exclude_current` 0, `short_statistic` "median" and `statistic` "mean", it runs 0 to 2 and nears 1 as the volume spreads evenly. Otherwise it is unbounded above. "centred": the same minus 1, signed. "log": signed, 0 at the base. No direction | graded | ratio ("centred": ratio minus 1; "log": natural log of the ratio) | `period` + `exclude_current` (30) | volume. A NaN volume in either window, or a base of 0, gives NaN. With "log", a recent statistic of 0 (never seen on real bars) gives NaN. These settings raise when the component is built: `period` < 2, `exclude_current` not 0 or 1, `short_period` < 1 or > `period`, `form` other than "ratio", "centred" or "log", `statistic` or `short_statistic` other than "mean" or "median" | stateless. `statistic` sets the base (the denominator) and `short_statistic` sets the numerator. The defaults are the original output, unchanged. `short_statistic` "median" with `short_period` = `period` = 72 gives the volume evenness over the last 72 bars. No `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    Recent volume against its own longer base, on every bar:

        R = volume[t - short_period + 1 .. t]                             (bar t included)
        short_statistic = "mean" (default): num = mean(R)
        short_statistic = "median":         num = median(R)  (average of the two middle values for an even count)
        exclude_current = 0 (default): W = volume[t - period + 1 .. t]
        exclude_current = 1:           W = volume[t - period .. t - 1]
        statistic = "mean" (default):  den = mean(W)
        statistic = "median":          den = median(W)  (average of the two middle values for an even count)
        form = "ratio" (default):  raw_value = num / den
        form = "centred":          raw_value = num / den - 1
        form = "log":              raw_value = ln(num / den)

    The defaults (short_period 1, form "ratio", statistic "mean", short_statistic "mean") give
    volume[t] / mean volume, the original output, unchanged. `statistic` sets the base and `short_statistic` sets
    the numerator. With period 72, short_period 72 and short_statistic "median" the output is
    median / mean of the last 72 volumes. That is the evenness of the volume: it runs 0 to 2 (at least half the
    values are >= the median, so the mean is at least median / 2), sits below 1 when a few heavy bars inflate the
    mean, and nears 1 as the volume spreads evenly.
    Graded, with no direction. With form "ratio" the value is non-negative and equals 1 when the numerator equals
    the base. With both statistics "mean" and exclude_current 0 it is at most period / short_period. form
    "centred" shifts the value down by 1, and form "log" gives the natural log of the ratio.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the rows up to and including bar t (the last row of
    data), over at most the last period + exclude_current rows; a bar's volume is known at that bar's close.

    NaN: a NaN volume in either window, or a base of 0, gives NaN. With form "log", a recent statistic of 0 gives
    NaN (zero volume, never seen on real bars). A missing `volume` column raises.
    Building the component raises for a period below 2, an exclude_current other than 0 or 1, a short_period
    below 1 or above period, a form other than "ratio", "centred" or "log", or a statistic or short_statistic
    other than "mean" or "median".
    """

    def __init__(self, name="VolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(f"VolumeRatioComponent: period must be >= 2, got {self.period}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"VolumeRatioComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.short_period = int(self.parameters.get("short_period", 1))
        if self.short_period < 1 or self.short_period > self.period:
            raise ValueError(
                f"VolumeRatioComponent: short_period must be between 1 and period, got {self.short_period}")
        self.form = self.parameters.get("form", "ratio")
        if self.form not in ("ratio", "centred", "log"):
            raise ValueError(f"VolumeRatioComponent: form must be 'ratio', 'centred' or 'log', got {self.form!r}")
        st = self.parameters.get("statistic", "mean")
        if st not in ("mean", "median"):
            raise ValueError(f"VolumeRatioComponent: statistic must be 'mean' or 'median', got {st!r}")
        self.statistic = st
        sst = self.parameters.get("short_statistic", "mean")
        if sst not in ("mean", "median"):
            raise ValueError(f"VolumeRatioComponent: short_statistic must be 'mean' or 'median', got {sst!r}")
        self.short_statistic = sst
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        vol = data['volume'].astype(float)
        recent = vol.iloc[-self.short_period:]
        if recent.isna().any():
            num = float("nan")
        elif self.short_statistic == "median":
            num = float(np.median(recent.to_numpy()))
        else:
            num = float(recent.mean(skipna=False))
        if self.exclude_current:
            base = vol.iloc[-(self.period + 1):-1]
        else:
            base = vol.iloc[-self.period:]
        if base.isna().any():
            den = float("nan")
        elif self.statistic == "median":
            den = float(np.median(base.to_numpy()))
        else:
            den = float(base.mean(skipna=False))
        if np.isnan(num) or np.isnan(den) or not den > 0:
            self._raw_value = float("nan")
        elif self.form == "log":
            self._raw_value = float(np.log(num / den)) if num > 0 else float("nan")
        else:
            self._raw_value = float(num / den - (1.0 if self.form == "centred" else 0.0))
        self.confidence = 1.0
        self.debug_info = {'recent_volume': num, 'base_volume': den, 'statistic': self.statistic,
                           'short_statistic': self.short_statistic}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("period", 30))
    ex = int(params.get("exclude_current", 0))
    s = int(params.get("short_period", 1))
    form = params.get("form", "ratio")
    st = params.get("statistic", "mean")
    sst = params.get("short_statistic", "mean")
    v = [float(x) for x in list(df["volume"])]
    last = len(v) - 1

    def median_of(xs):
        srt = sorted(xs)
        m = len(srt)
        if m % 2 == 1:
            return srt[m // 2]
        return (srt[m // 2 - 1] + srt[m // 2]) / 2.0

    def mean_of(xs):
        total = 0.0
        for x in xs:
            total = total + x
        return total / len(xs)

    recent = []
    i = last - s + 1
    while i <= last:
        recent.append(v[i])
        i = i + 1
    base = []
    if ex == 1:
        i = last - n
        while i <= last - 1:
            base.append(v[i])
            i = i + 1
    else:
        i = last - n + 1
        while i <= last:
            base.append(v[i])
            i = i + 1
    for x in recent + base:
        if x != x:
            return float("nan")
    num = median_of(recent) if sst == "median" else mean_of(recent)
    den = median_of(base) if st == "median" else mean_of(base)
    if not den > 0:
        return float("nan")
    ratio = num / den
    if form == "log":
        if not ratio > 0:
            return float("nan")
        return math.log(ratio)
    return ratio - (1.0 if form == "centred" else 0.0)
```

checks:
VolumeRatioComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1556 passed, 8 skipped, 74 deselected, 2244 warnings in 47.60s ========
