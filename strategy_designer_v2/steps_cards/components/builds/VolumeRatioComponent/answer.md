# VolumeRatioComponent: night_run | 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g2_heavy-volume-fall-rebounds_1d | RelativeVolumeToMedian

## attempt 1

answer: built
class: VolumeRatioComponent
settings: {"period": 20, "exclude_current": 1, "statistic": "median"}
reason: `VolumeRatioComponent` (`period` 20, `exclude_current` 1) already computes volume[t] against the past 20 bars' volume, but only against their mean. Under rule 1 the median is the same measure with another statistic, so the class is rewritten with a `statistic` setting for the denominator; its default "mean" keeps today's output exactly.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (0), `short_period` (1), `centred` (0), `log` (0), `statistic` ("mean") | r = mean(volume over the last `short_period` bars, bar t included) / B, B being the `statistic` ("mean": the mean; "median": the median, the average of the two middle values for an even count) of the volume over the last `period` bars, bar t included (`exclude_current` 0), or over volume[t-period] .. volume[t-1], bar t excluded (`exclude_current` 1). Output r - `centred` (`log` 0), or ln(r) (`log` 1). At the defaults: volume[t] / mean(last `period` volumes). With `period` 20, `exclude_current` 1, `statistic` "median": volume[t] / median(volume[t-20] .. volume[t-1]) | `log` 0, `centred` 0: never negative, 1 when recent volume equals the base. With "mean" the value is 0 to `period` / `short_period` (`exclude_current` 0) or unbounded (1). With "median" it is unbounded above either way. `centred` 1: the same minus 1, signed. `log` 1: signed, 0 at the base volume, positive on heavy volume, negative on thin volume. No direction | graded | ratio (`centred` 1: ratio minus 1; `log` 1: natural log of the ratio) | `period` + `exclude_current` (30) | volume. A NaN volume in either window, or a base of 0, gives NaN. With `log` 1, a recent mean of 0 (zero volume, never seen on real bars) gives NaN. These settings raise when the component is built: `period` < 2, `exclude_current` not 0 or 1, `short_period` < 1 or > `period`, `centred` not 0 or 1, `log` not 0 or 1, `log` 1 together with `centred` 1, `statistic` other than "mean" or "median" | stateless. `statistic` sets only the base (the denominator); the numerator is always a mean. `statistic` "median" with `period` 20 and `exclude_current` 1 gives volume[t] / median of the past 20 volumes, a relative volume that one outlier day in the base does not drag. `short_period` 5 with `period` 30 gives the 5-bar against 30-bar volume ratio, and `centred` 1 subtracts 1. `log` 1 gives the log relative volume. No `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    Recent volume against its own longer base, on every bar:

        num = mean(volume[t - short_period + 1 .. t])                     (bar t included)
        exclude_current = 0 (default): W = volume[t - period + 1 .. t]
        exclude_current = 1:           W = volume[t - period .. t - 1]
        statistic = "mean" (default):  den = mean(W)
        statistic = "median":          den = median(W)  (average of the two middle values for an even count)
        log = 0 (default): raw_value = num / den - centred
        log = 1:           raw_value = ln(num / den)

    The defaults (short_period 1, centred 0, log 0, statistic "mean") give volume[t] / mean volume, the
    original output, unchanged. With period 20, exclude_current 1 and statistic "median" the output is
    volume[t] / median(volume of the past 20 bars).
    Graded, with no direction. With log 0 and centred 0 the value is non-negative and equals 1 when recent
    volume equals the base. With "mean" and exclude_current 0 it is at most period / short_period. With
    exclude_current 1, or with "median", it is unbounded above. centred 1 shifts the value down by 1. log 1
    gives the natural log of the ratio: 0 at the base, positive on heavy volume, negative on thin volume.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the rows up to and including bar t (the last row of
    data), over at most the last period + exclude_current rows; a bar's volume is known at that bar's close.

    NaN: a NaN volume in either window, or a base of 0, gives NaN. With log 1, a recent mean of 0 gives NaN
    (zero volume, never seen on real bars). A missing `volume` column raises.
    Building the component raises for a period below 2, an exclude_current other than 0 or 1, a short_period
    below 1 or above period, a centred other than 0 or 1, a log other than 0 or 1, log 1 with centred 1, or
    a statistic other than "mean" or "median".
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
        c = self.parameters.get("centred", 0)
        if c not in (0, 1):
            raise ValueError(f"VolumeRatioComponent: centred must be 0 or 1, got {c!r}")
        self.centred = int(c)
        lg = self.parameters.get("log", 0)
        if lg not in (0, 1):
            raise ValueError(f"VolumeRatioComponent: log must be 0 or 1, got {lg!r}")
        self.log = int(lg)
        if self.log == 1 and self.centred == 1:
            raise ValueError("VolumeRatioComponent: log 1 cannot be combined with centred 1")
        st = self.parameters.get("statistic", "mean")
        if st not in ("mean", "median"):
            raise ValueError(f"VolumeRatioComponent: statistic must be 'mean' or 'median', got {st!r}")
        self.statistic = st
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        vol = data['volume'].astype(float)
        num = float(vol.iloc[-self.short_period:].mean(skipna=False))
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
        elif self.log == 1:
            if not num > 0:
                self._raw_value = float("nan")
            else:
                self._raw_value = float(np.log(num / den))
        else:
            self._raw_value = float(num / den - self.centred)
        self.confidence = 1.0
        self.debug_info = {'short_mean_volume': num, 'base_volume': den, 'statistic': self.statistic}

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
    c = int(params.get("centred", 0))
    lg = int(params.get("log", 0))
    st = params.get("statistic", "mean")
    v = [float(x) for x in list(df["volume"])]
    last = len(v) - 1
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
    total = 0.0
    for x in recent:
        total = total + x
    num = total / s
    if st == "median":
        srt = sorted(base)
        m = len(srt)
        if m % 2 == 1:
            den = srt[m // 2]
        else:
            den = (srt[m // 2 - 1] + srt[m // 2]) / 2.0
    else:
        total = 0.0
        for x in base:
            total = total + x
        den = total / n
    if not den > 0:
        return float("nan")
    ratio = num / den
    if lg == 1:
        if not ratio > 0:
            return float("nan")
        return math.log(ratio)
    return ratio - c
```

checks:
VolumeRatioComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1535 passed, 8 skipped, 74 deselected, 2170 warnings in 73.67s (0:01:13) ===
