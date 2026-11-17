# VolumeRatioComponent: night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g2_rising-volume-precedes-gains_1d | VolumeRatioComponent

## attempt 1

answer: built
class: VolumeRatioComponent
settings: {"period": 30, "short_period": 5, "centred": true}
reason: `VolumeRatioComponent` already measures volume against its own recent average, but its numerator is always bar t's volume alone. No config step adds a constant, so neither the 5-bar mean numerator nor the minus 1 is available today. The whole class is written again with two new settings, `short_period` (default 1, the bar's own volume) and `centred` (default false, no minus 1), so its output at the defaults is exactly what it is now.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (0), `short_period` (1), `centred` (false) | mean(volume[t-`short_period`+1 .. t]) / mean(volume over the last `period` bars, bar t included); with `exclude_current` 1 the denominator is mean(volume[t-period] .. volume[t-1]), bar t excluded; minus 1 when `centred` is true | not centred: 0 to `period`/`short_period` at `exclude_current` 0, 0 and up (unbounded) at `exclude_current` 1, never negative; centred: the same minus 1, so signed, positive when the recent volume is above the longer average and negative when it is thinner; no direction | graded | ratio (centred: ratio minus 1) | `period` + `exclude_current` (30) | volume. A NaN volume in the numerator window or in the averaged bars, or an average of 0, gives NaN. These settings raise when the component is built: `period` below 2, `exclude_current` other than 0 or 1, `short_period` below 1 or above `period`, `short_period` equal to `period` with `exclude_current` 0, `centred` not a boolean | stateless; how heavy recent volume is against its own longer average. `short_period` 1 is the bar's own volume (today's output). `centred` true gives a signed reading around 0. No `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    Recent volume against its own longer average, on every bar:

        num = mean(volume[t - short_period + 1 .. t])                 (short_period 1: volume[t])
        exclude_current = 0 (default):
            den = mean(volume[t - period + 1 .. t])                   (the average includes bar t)
        exclude_current = 1:
            den = mean(volume[t - period .. t - 1])                   (the prior `period` bars)
        raw_value = num / den            (centred = False, default)
        raw_value = num / den - 1        (centred = True)

    Graded. Not centred: never negative, 1 at an average level, 2 at twice the average. At exclude_current 0 it is at
    most period / short_period; at exclude_current 1 it is unbounded above. Centred: the same minus 1, positive when
    recent volume is above the longer average and negative when it is thinner. No direction.
    At the defaults (short_period 1, centred False) the output is exactly volume[t] / den, as before.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the rows up to and including bar t (the last row of
    data); the numerator uses the last short_period rows and the denominator the last period (or period + 1) rows.

    NaN: a NaN volume in the numerator window or in the averaged bars, or an average of 0, gives NaN. A missing
    `volume` column raises. These settings raise when the component is built: period < 2, exclude_current not 0 or 1,
    short_period < 1 or > period, short_period == period with exclude_current 0, centred not a boolean.
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
                f"VolumeRatioComponent: short_period must be in 1 .. period ({self.period}), got {self.short_period}")
        if self.exclude_current == 0 and self.short_period == self.period:
            raise ValueError("VolumeRatioComponent: short_period equal to period with exclude_current 0 is always 1")
        centred = self.parameters.get("centred", False)
        if not isinstance(centred, (bool, np.bool_)) and centred not in (0, 1):
            raise ValueError(f"VolumeRatioComponent: centred must be a boolean, got {centred!r}")
        self.centred = bool(centred)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        vol = data['volume'].astype(float)
        if self.short_period == 1:
            num = float(vol.iloc[-1])
        else:
            num = float(vol.iloc[-self.short_period:].mean(skipna=False))
        if self.exclude_current:
            base = vol.iloc[-(self.period + 1):-1]
        else:
            base = vol.iloc[-self.period:]
        mean = float(base.mean(skipna=False))
        if mean > 0:
            value = num / mean
            if self.centred:
                value = value - 1.0
        else:
            value = float("nan")
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'recent_volume': num, 'mean_volume': mean}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    n = int(params.get("period", 30))
    ex = int(params.get("exclude_current", 0))
    s = int(params.get("short_period", 1))
    centred = bool(params.get("centred", False))
    v = [float(x) for x in list(df["volume"])]
    recent = v[len(v) - s:]
    rsum = 0.0
    for x in recent:
        rsum = rsum + x
    num = rsum / s
    if ex == 1:
        base = v[len(v) - n - 1:len(v) - 1]
    else:
        base = v[len(v) - n:]
    bsum = 0.0
    for x in base:
        bsum = bsum + x
    den = bsum / n
    if num != num or den != den or not den > 0:
        return float("nan")
    out = num / den
    if centred:
        out = out - 1.0
    return out
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 251, in <module>
    main()
    ~~~~^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 228, in main
    spec = load_spec(args.spec)
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 210, in load_spec
    spec.loader.exec_module(mod)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/user/trading-bot/trading-bot/tests/built_components/VolumeRatioComponent.py", line 3, in <module>
    SETTINGS = [{}, {"period": 30}, {"period": 10}, {"period": 2}, {"period": 20, "exclude_current": 1}, {"period": 30, "short_period": 5, "centred": true}]
                                                                                                                                                      ^^^^
NameError: name 'true' is not defined. Did you mean: 'True'?

## attempt 2

answer: built
class: VolumeRatioComponent
settings: {"period": 30, "short_period": 5, "centred": 1}
reason: `VolumeRatioComponent` measures volume against its own recent average, but its numerator is always the single bar (a window of 1). It also cannot subtract 1, and no config step gives that offset (`standardise` does not centre). So the class is written again with two settings, `short_period` (default 1) and `centred` (default 0, an integer 0/1), and the defaults keep today's output exactly.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (0), `short_period` (1), `centred` (0) | mean(volume over the last `short_period` bars, bar t included) / mean(volume over the last `period` bars, bar t included), minus `centred`; with `exclude_current` 1 the denominator is mean(volume[t-period] .. volume[t-1]), bar t excluded. At the defaults: volume[t] / mean(last `period` volumes) | `centred` 0: 0 to `period` / `short_period` with `exclude_current` 0, 0 and up (unbounded) with 1, never negative, 1 at average volume. `centred` 1: the same minus 1, so it is signed: positive when recent volume is above the longer average, negative when it is thin. No direction | graded | ratio (`centred` 1: ratio minus 1) | `period` + `exclude_current` (30) | volume. A NaN volume in either window, or an average of 0, gives NaN. These settings raise when the component is built: `period` < 2, `exclude_current` not 0 or 1, `short_period` < 1 or > `period`, `centred` not 0 or 1 | stateless. `short_period` 5 with `period` 30 gives the 5-bar against 30-bar volume ratio, and `centred` 1 subtracts 1. No `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    Recent volume against its own longer average, on every bar:

        num = mean(volume[t - short_period + 1 .. t])                (bar t included)
        exclude_current = 0 (default): den = mean(volume[t - period + 1 .. t])
        exclude_current = 1:           den = mean(volume[t - period .. t - 1])
        raw_value = num / den - centred

    Defaults (short_period 1, centred 0) give volume[t] / mean volume, the original output.
    Graded. With centred 0 it is non-negative and equals 1 at average volume. With exclude_current 0 it is at most
    period / short_period; with exclude_current 1 it is unbounded above. With centred 1 the value is shifted down
    by 1, so it is positive when recent volume is above the longer average and negative when that volume is thin.
    No direction.
    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the rows up to and including bar t (the last row of
    data), over at most the last period + exclude_current rows; a bar's volume is known at that bar's close.

    NaN: a NaN volume in either window, or an average of 0, gives NaN. A missing `volume` column raises.
    Building the component raises for a period below 2, an exclude_current other than 0 or 1, a short_period
    below 1 or above period, or a centred other than 0 or 1.
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
    n = int(params.get("period", 30))
    ex = int(params.get("exclude_current", 0))
    s = int(params.get("short_period", 1))
    c = int(params.get("centred", 0))
    v = [float(x) for x in list(df["volume"])]
    recent = v[len(v) - s:]
    if ex == 1:
        longw = v[len(v) - n - 1:len(v) - 1]
    else:
        longw = v[len(v) - n:]
    for x in recent + longw:
        if x != x:
            return float("nan")
    num = 0.0
    for x in recent:
        num = num + x
    num = num / s
    den = 0.0
    for x in longw:
        den = den + x
    den = den / n
    if not den > 0:
        return float("nan")
    return num / den - c
```

checks:
VolumeRatioComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1529 passed, 8 skipped, 74 deselected, 2170 warnings in 64.58s (0:01:04) ===
