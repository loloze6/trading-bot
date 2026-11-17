# not built: night_012_run | 012-04_flush-depth-retracement-size_1d | VolumeRatioComponent

## attempt 1

answer: built
class: VolumeRatioComponent
settings: {"period": 20, "exclude_current": true}
reason: `VolumeRatioComponent` measures the bar's volume against its recent average, but its mean includes bar t, while the wish divides by the mean of the prior N bars only. The class is written again with a setting `exclude_current`, whose default `false` keeps today's output exactly.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (false) | volume[t] / mean(volume over the last `period` bars, bar t included); with `exclude_current` true, volume[t] / mean(volume[t-`period`] .. volume[t-1]), the `period` bars before bar t | 0 to `period` at the default (never negative); with `exclude_current` true, 0 and up, unbounded; 1 at an average bar, 2 for twice the average volume; no direction | graded | ratio | `period` (30); `period` + 1 with `exclude_current` true | volume. A window holding a NaN volume (bar t's included), or whose averaged volumes are all zero, gives NaN; a `period` below 2 or a non-boolean `exclude_current` raises when the engine starts | stateless; `exclude_current` true compares the bar with its usual level before it, so a burst does not dilute its own baseline. No `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    The bar's volume against its own recent average, on every bar:

        exclude_current False (default):
            raw_value = volume[t] / mean(volume[t - period + 1 .. t])   (the average includes bar t)
        exclude_current True:
            raw_value = volume[t] / mean(volume[t - period .. t - 1])   (the average of the period bars before t)

    Graded and non-negative, no direction: 1 at an average bar, 2 for a bar with twice the average volume, near 0
    for a very quiet bar. With the default, at most `period`; with `exclude_current` True, unbounded above.
    Warm-up: `period` bars (default), `period + 1` bars with `exclude_current` True, bar t included.

    NaN: a NaN volume in the averaged window or at bar t, or an average of 0 (no level to compare with), gives NaN.
    A `period` below 2 or a non-boolean `exclude_current` raises when the component is built.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the last `period` rows (default) or the last
    `period + 1` rows (exclude_current True) of the data it is given, all of them at or before bar t; a bar's volume
    is known at that bar's close.
    """

    def __init__(self, name="VolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(f"VolumeRatioComponent: period must be >= 2, got {self.period}")
        self.exclude_current = self.parameters.get("exclude_current", False)
        if not isinstance(self.exclude_current, (bool, np.bool_)):
            raise ValueError(
                f"VolumeRatioComponent: exclude_current must be true or false, got {self.exclude_current!r}")
        self.exclude_current = bool(self.exclude_current)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        volume = data['volume'].astype(float)
        if self.exclude_current:
            window = volume.iloc[-(self.period + 1):-1]
        else:
            window = volume.iloc[-self.period:]
        mean = float(window.mean(skipna=False))
        last = float(volume.iloc[-1])
        if np.isnan(mean) or np.isnan(last) or not mean > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = last / mean
        self.confidence = 1.0
        self.debug_info = {'volume': last, 'mean_volume': mean, 'exclude_current': self.exclude_current}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1 if self.exclude_current else self.period
```

```python hand
def hand(df, params):
    n = params.get("period", 30)
    exclude = params.get("exclude_current", False)
    vols = [float(x) for x in list(df["volume"])]
    current = vols[-1]
    if exclude:
        base = vols[len(vols) - n - 1:len(vols) - 1]
    else:
        base = vols[len(vols) - n:]
    total = 0.0
    for x in base:
        if x != x:
            return float("nan")
        total += x
    avg = total / n
    if current != current or not avg > 0:
        return float("nan")
    return current / avg
```

checks:
Extra data: line 1 column 51 (char 50)

## attempt 2

answer: built
class: VolumeRatioComponent
settings: {"period": 20, "include_current": false}
reason: VolumeRatioComponent's average always includes bar t, but the wish divides by the mean of the N bars before bar t. So the same class gets an `include_current` setting; its default (true) keeps today's output exactly.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `include_current` (true) | volume[t] / mean(volume over the last `period` bars, bar t included); with `include_current` false, volume[t] / mean(volume[t-`period`] .. volume[t-1]), the `period` bars before bar t | 0 and up, never negative; 1 at an average bar, 2 for twice the average volume; no direction; at most `period` when bar t is included, unbounded when it is not | graded | ratio | `period` (30); `period` + 1 with `include_current` false | volume. A window holding a NaN volume, or whose averaged volumes are all zero, gives NaN; a `period` below 2 or a non-boolean `include_current` raises when the engine starts | stateless; `include_current` false compares the bar with its usual level before it ("a volume burst against the prior N bars"). No `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    The bar's volume against its own recent average, on every bar:

        include_current true (default):
            raw_value = volume[t] / mean(volume[t - period + 1 .. t])     (the average includes bar t)
        include_current false:
            raw_value = volume[t] / mean(volume[t - period .. t - 1])     (the average of the `period` bars before t)

    Graded and never negative: 1 at an average bar, 2 for a bar with twice the average volume, near 0 for a very
    quiet bar. With bar t included it is at most `period`; with bar t excluded it is unbounded above. It has no
    direction.

    Warm-up: `period` rows (include_current true), `period` + 1 rows (include_current false), bar t included.

    NaN: a window that holds a NaN volume (bar t's or one of the averaged bars), or whose averaged volumes are all
    zero, gives NaN. A `period` below 2 or a non-boolean `include_current` raises when the component is built.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the last `period` (or `period` + 1) rows of the data
    it is given, the last of which is bar t; a bar's volume is known at that bar's close.
    """

    def __init__(self, name="VolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(f"VolumeRatioComponent: period must be >= 2, got {self.period}")
        include_current = self.parameters.get("include_current", True)
        if not isinstance(include_current, (bool, np.bool_)):
            raise ValueError(f"VolumeRatioComponent: include_current must be true or false, got {include_current!r}")
        self.include_current = bool(include_current)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        volume = data['volume'].astype(float)
        last = float(volume.iloc[-1])
        if self.include_current:
            window = volume.iloc[-self.period:]
        else:
            window = volume.iloc[-(self.period + 1):-1]
        mean = float(window.mean(skipna=False))
        if np.isnan(mean) or np.isnan(last):
            self._raw_value = float("nan")
        elif mean > 0:
            self._raw_value = float(last / mean)
        else:
            self._raw_value = float("nan")
        self.confidence = 1.0
        self.debug_info = {'volume': last, 'mean_volume': mean}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period if self.include_current else self.period + 1
```

```python hand
def hand(df, params):
    n = params.get("period", 30)
    inc = params.get("include_current", True)
    vols = [float(x) for x in list(df["volume"])]
    current = vols[len(vols) - 1]
    if inc:
        avg_part = vols[len(vols) - n:]
    else:
        avg_part = vols[len(vols) - n - 1:len(vols) - 1]
    if current != current or any(x != x for x in avg_part):
        return float("nan")
    total = 0.0
    for x in avg_part:
        total += x
    mean = total / n
    if mean <= 0:
        return float("nan")
    return current / mean
```

checks:
Extra data: line 1 column 51 (char 50)

## attempt 3

answer: built
class: VolumeRatioComponent
settings: {"period": 20, "exclude_current": true}
reason: `VolumeRatioComponent` measures the bar's volume against its recent average, but its average always includes bar t, while the wish divides by the mean of the prior N bars only. The class is rewritten whole with an `exclude_current` setting; its default `false` keeps today's output exactly.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (false) | volume[t] / mean(volume over the last `period` bars, bar t included); with `exclude_current` true, volume[t] / mean(volume[t-`period`] .. volume[t-1]), the `period` bars before bar t | `exclude_current` false: 0 to `period`; true: 0 and up, unbounded; never negative; 1 at an average bar, 2 for twice the average volume; no direction | graded | ratio | `period` (30); `period` + 1 with `exclude_current` true | volume. A window holding a NaN volume, or whose averaged volumes are all zero, gives NaN; a `period` below 2 or a non-boolean `exclude_current` raises when the engine starts | how heavy the bar's volume is against its own recent average: "a volume burst", "a quiet day". `exclude_current` true compares the bar with the bars before it only, so a burst does not raise its own baseline. No direction: combine it with a price move, or use it in a regime rule. No `scaling_factor`: scale it with transforms; stateless |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    The bar's volume against its own recent average, on every bar:

        exclude_current false (default):
            raw_value = volume[t] / mean(volume[t - period + 1 .. t])   (the average includes bar t)
        exclude_current true:
            raw_value = volume[t] / mean(volume[t - period .. t - 1])   (the `period` bars before bar t)

    Graded and positive: 1 at an average bar, 2 for a bar with twice the average volume, near 0 for a very quiet bar.
    With bar t included it is at most `period`. With bar t excluded it is unbounded above, 0 and up. It has no
    direction. No lag: everything up to bar t's close.

    Warm-up: `period` rows (default), `period` + 1 rows with `exclude_current` true.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the last `period` rows (default) or the last
    `period` + 1 rows (exclude_current true), all at or before bar t; a bar's volume is known at that bar's close.

    NaN: a window that holds a NaN volume, or whose averaged volumes are all zero (no average to compare with), gives
    NaN. A missing `volume` column raises. A `period` below 2, or an `exclude_current` that is not a boolean, raises
    when the component is built.
    """

    def __init__(self, name="VolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 2:
            raise ValueError(f"VolumeRatioComponent: period must be >= 2, got {self.period}")
        exclude = self.parameters.get("exclude_current", False)
        if not isinstance(exclude, (bool, np.bool_)):
            raise ValueError(f"VolumeRatioComponent: exclude_current must be true or false, got {exclude!r}")
        self.exclude_current = bool(exclude)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        volume = data['volume'].astype(float)
        last = float(volume.iloc[-1])
        if self.exclude_current:
            window = volume.iloc[-(self.period + 1):-1]
        else:
            window = volume.iloc[-self.period:]
        mean = float(window.mean(skipna=False))
        if np.isnan(last) or np.isnan(mean) or not mean > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(last / mean)
        self.confidence = 1.0
        self.debug_info = {'volume': last, 'mean_volume': mean}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1 if self.exclude_current else self.period
```

```python hand
def hand(df, params):
    n = params.get("period", 30)
    exclude = params.get("exclude_current", False)
    vols = list(df["volume"])
    current = float(vols[-1])
    if exclude:
        base = vols[len(vols) - 1 - n:len(vols) - 1]
    else:
        base = vols[len(vols) - n:]
    total = 0.0
    for v in base:
        v = float(v)
        if v != v:
            return float("nan")
        total += v
    if current != current:
        return float("nan")
    avg = total / n
    if avg <= 0:
        return float("nan")
    return current / avg
```

checks:
Extra data: line 1 column 51 (char 50)
