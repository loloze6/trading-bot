# VolumeRatioComponent: night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d | RelativeVolumeComponent

## attempt 1

answer: built
class: VolumeRatioComponent
settings: {"period": 30, "log": 1}
reason: `VolumeRatioComponent` computes this measure, volume[t] against the mean of its last 30 volumes with bar t included, but only as a ratio or a ratio minus 1. No config step takes a logarithm, and the log changes the value on every real bar. So the class gets a `log` setting; its default of 0 keeps today's output exactly.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (0), `short_period` (1), `centred` (0), `log` (0) | r = mean(volume over the last `short_period` bars, bar t included) / mean(volume over the last `period` bars, bar t included); with `exclude_current` 1 the denominator is mean(volume[t-period] .. volume[t-1]), bar t excluded. Output r - `centred` (`log` 0), or ln(r) (`log` 1). At the defaults: volume[t] / mean(last `period` volumes) | `log` 0, `centred` 0: 0 to `period` / `short_period` with `exclude_current` 0, 0 and up (unbounded) with 1, never negative, 1 at average volume. `centred` 1: the same minus 1, signed. `log` 1: signed, 0 at average volume, positive on heavy volume, negative on thin volume; at most ln(`period` / `short_period`) with `exclude_current` 0, unbounded below. No direction | graded | ratio (`centred` 1: ratio minus 1; `log` 1: natural log of the ratio) | `period` + `exclude_current` (30) | volume. A NaN volume in either window, or an average of 0, gives NaN; with `log` 1 a recent mean of 0 (zero volume, never seen on real bars) gives NaN. These settings raise when the component is built: `period` < 2, `exclude_current` not 0 or 1, `short_period` < 1 or > `period`, `centred` not 0 or 1, `log` not 0 or 1, `log` 1 together with `centred` 1 | stateless. `short_period` 5 with `period` 30 gives the 5-bar against 30-bar volume ratio, and `centred` 1 subtracts 1. `log` 1 gives the log relative volume (symmetric: twice and half the average volume are +ln 2 and -ln 2). No `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    Recent volume against its own longer average, on every bar:

        num = mean(volume[t - short_period + 1 .. t])                (bar t included)
        exclude_current = 0 (default): den = mean(volume[t - period + 1 .. t])
        exclude_current = 1:           den = mean(volume[t - period .. t - 1])
        log = 0 (default): raw_value = num / den - centred
        log = 1:           raw_value = ln(num / den)

    Defaults (short_period 1, centred 0, log 0) give volume[t] / mean volume, the original output.
    Graded. With log 0 and centred 0 the value is non-negative and equals 1 at average volume. With
    exclude_current 0 it is at most period / short_period; with exclude_current 1 it is unbounded above.
    With centred 1 the value is shifted down by 1, so it is positive when recent volume is above the longer
    average and negative when that volume is thin. With log 1 it is the natural log of the ratio. That value
    is 0 at average volume, positive and growing on heavy volume, negative on thin volume. It is at most
    ln(period / short_period) with exclude_current 0, and unbounded below. No direction.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the rows up to and including bar t (the last row of
    data), over at most the last period + exclude_current rows; a bar's volume is known at that bar's close.

    NaN: a NaN volume in either window, or an average of 0, gives NaN. With log 1, a recent mean of 0 gives NaN
    (zero volume, never seen on real bars). A missing `volume` column raises.
    Building the component raises for a period below 2, an exclude_current other than 0 or 1, a short_period
    below 1 or above period, a centred other than 0 or 1, a log other than 0 or 1, or log 1 with centred 1.
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
        self.debug_info = {'short_mean_volume': num, 'mean_volume': den}

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
    v = [float(x) for x in list(df["volume"])]
    last = len(v) - 1
    recent = []
    i = last - s + 1
    while i <= last:
        recent.append(v[i])
        i = i + 1
    longw = []
    if ex == 1:
        i = last - n
        while i <= last - 1:
            longw.append(v[i])
            i = i + 1
    else:
        i = last - n + 1
        while i <= last:
            longw.append(v[i])
            i = i + 1
    for x in recent + longw:
        if x != x:
            return float("nan")
    total = 0.0
    for x in recent:
        total = total + x
    num = total / s
    total = 0.0
    for x in longw:
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
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1532 passed, 8 skipped, 74 deselected, 2170 warnings in 71.88s (0:01:11) ===
