# VolumeRatioComponent: night4_weekend_run | 026-04_thinner-weekend-larger-reversal_1h | LaggedBaseVolumeRatio

## attempt 1

answer: built
class: VolumeRatioComponent
settings: {"period": 120, "exclude_current": 49, "short_period": 48}
reason: `VolumeRatioComponent` already computes the mean of the recent volume over a base mean. Its only way to move the base back in time is `exclude_current`, which allows 0 or 1 bar, so it cannot place the base at t-168..t-49. Under one setting per purpose, the wished lag of 49 becomes a new value of `exclude_current` (any integer ≥ 0, the base ending `exclude_current` bars before t). Values 0 and 1 give exactly today's windows, so today's output is unchanged.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (0), `short_period` (1), `form` ("ratio"), `statistic` ("mean"), `short_statistic` ("mean") | r = A / B. A is the `short_statistic` of the volume over the last `short_period` bars, bar t included ("mean": the mean; "median": the median, the average of the two middle values for an even count). B is the `statistic` (same choices) of the volume over the `period` bars volume[t-`period`-`exclude_current`+1 .. t-`exclude_current`], the base ending `exclude_current` bars before t (0: bar t included; 1: volume[t-period] .. volume[t-1]). The output is r (`form` "ratio"), r - 1 (`form` "centred"), or ln(r) (`form` "log"). At the defaults it is volume[t] / mean(last `period` volumes). With `period` 72, `short_period` 72 and `short_statistic` "median" it is median / mean of the last 72 volumes, the evenness of volume over the window. With `period` 120, `exclude_current` 49 and `short_period` 48 it is mean(volume[t-47..t]) / mean(volume[t-168..t-49]) | "ratio": never negative, 1 when A equals the base. With both statistics "mean" and `exclude_current` 0, it runs 0 to `period` / `short_period`. With `short_period` = `period`, `exclude_current` 0, `short_statistic` "median" and `statistic` "mean", it runs 0 to 2 and nears 1 as the volume spreads evenly. Otherwise it is unbounded above; with a lagged base it falls as recent volume thins against the earlier base. "centred": the same minus 1, signed. "log": signed, 0 at the base. No direction | graded | ratio ("centred": ratio minus 1; "log": natural log of the ratio) | `period` + `exclude_current` (30) | volume. A NaN volume in either window, or a base of 0, gives NaN. With "log", a recent statistic of 0 (never seen on real bars) gives NaN. These settings raise when the component is built: `period` < 2, `exclude_current` not an integer ≥ 0, `short_period` < 1 or > `period`, `form` other than "ratio", "centred" or "log", `statistic` or `short_statistic` other than "mean" or "median" | stateless. `statistic` sets the base (the denominator) and `short_statistic` sets the numerator. The defaults and `exclude_current` 0 and 1 are the original outputs, unchanged. `exclude_current` above 1 lags the base: with `exclude_current` ≥ `short_period` the two windows do not overlap (at 120 / 49 / 48, bar t-48 is in neither). This is the inverse of the volume factor of `ThinVolumeScaledReturnComponent` (`volume_period` 48, `base_near` 49, `base_far` 168). No `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    Recent volume against its own longer base, on every bar:

        R = volume[t - short_period + 1 .. t]                             (bar t included)
        short_statistic = "mean" (default): num = mean(R)
        short_statistic = "median":         num = median(R)  (average of the two middle values for an even count)
        W = volume[t - period - exclude_current + 1 .. t - exclude_current]  (the base ends exclude_current bars before t)
            exclude_current = 0 (default): W = volume[t - period + 1 .. t]
            exclude_current = 1:           W = volume[t - period .. t - 1]
            exclude_current = 49, period 120: W = volume[t - 168 .. t - 49]
        statistic = "mean" (default):  den = mean(W)
        statistic = "median":          den = median(W)  (average of the two middle values for an even count)
        form = "ratio" (default):  raw_value = num / den
        form = "centred":          raw_value = num / den - 1
        form = "log":              raw_value = ln(num / den)

    The defaults (exclude_current 0, short_period 1, form "ratio", statistic "mean", short_statistic "mean") give
    volume[t] / mean volume, the original output, unchanged; exclude_current 0 and 1 are the original windows.
    exclude_current above 1 lags the base: with period 120, exclude_current 49 and short_period 48 the output is
    mean(volume[t-47..t]) / mean(volume[t-168..t-49]), falling as recent volume thins against the earlier base.
    With period 72, short_period 72 and short_statistic "median" the output is median / mean of the last 72 volumes
    (0 to 2, nearing 1 as the volume spreads evenly).
    Graded, with no direction. With form "ratio" the value is non-negative and equals 1 when the numerator equals
    the base. With both statistics "mean" and exclude_current 0 it is at most period / short_period. form
    "centred" shifts the value down by 1, and form "log" gives the natural log of the ratio.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the rows up to and including bar t (the last row of
    data), over at most the last period + exclude_current rows; a bar's volume is known at that bar's close.

    NaN: a NaN volume in either window, or a base of 0, gives NaN. With form "log", a recent statistic of 0 gives
    NaN (zero volume, never seen on real bars). A missing `volume` column raises.
    Building the component raises for a period below 2, an exclude_current that is not an integer >= 0, a
    short_period below 1 or above period, a form other than "ratio", "centred" or "log", or a statistic or
    short_statistic other than "mean" or "median".
    """

    def __init__(self, name="VolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(f"VolumeRatioComponent: period must be >= 2, got {self.period}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        try:
            ex_int = int(ex)
        except (TypeError, ValueError):
            raise ValueError(f"VolumeRatioComponent: exclude_current must be an integer >= 0, got {ex!r}")
        if ex_int != ex or ex_int < 0:
            raise ValueError(f"VolumeRatioComponent: exclude_current must be an integer >= 0, got {ex!r}")
        self.exclude_current = ex_int
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
        ex = self.exclude_current
        start = len(vol) - self.period - ex
        stop = len(vol) - ex
        base = vol.iloc[start:stop]
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
                           'short_statistic': self.short_statistic, 'exclude_current': ex}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("period", 30))
    lag = int(params.get("exclude_current", 0))
    s = int(params.get("short_period", 1))
    form = params.get("form", "ratio")
    st = params.get("statistic", "mean")
    sst = params.get("short_statistic", "mean")
    v = [float(x) for x in list(df["volume"])]
    t = len(v) - 1

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

    # recent: bars t-s+1 .. t
    recent = []
    for k in range(s):
        recent.append(v[t - k])
    # base: the n bars ending lag bars before t, i.e. t-lag-n+1 .. t-lag
    base = []
    for k in range(n):
        base.append(v[t - lag - k])
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
    if form == "centred":
        return ratio - 1.0
    return ratio
```

checks:
VolumeRatioComponent: every check passed
the bot's suite: == 1610 passed, 16 skipped, 75 deselected, 2244 warnings in 99.17s (0:01:39) ===
