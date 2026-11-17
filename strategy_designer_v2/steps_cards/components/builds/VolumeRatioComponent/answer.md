# VolumeRatioComponent: night_012_run | 012-04_flush-depth-retracement-size_1d | VolumeRatioComponent

## attempt 1

answer: built
class: VolumeRatioComponent
settings: {"period": 20, "exclude_current": true}
reason: `VolumeRatioComponent` computes this measure, but its average always includes bar t, and the wish divides by the mean of the N bars before bar t. The new setting `exclude_current` (default false, which keeps today's output exactly) moves the averaging window to bars t-N .. t-1.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (false) | volume[t] / mean(volume over the last `period` bars, bar t included); with `exclude_current` true, volume[t] / mean(volume[t-`period`] .. volume[t-1]), the `period` bars before bar t | default: 0 to `period`, never negative; with `exclude_current`: 0 and up, unbounded, never negative; 1 at an average bar, 2 for twice the usual volume; no direction | graded | ratio | `period` (30); `period` + 1 with `exclude_current` | volume. A window holding a NaN volume (bar t's included), or whose averaged volumes are all zero, gives NaN; a `period` below 2 raises when the engine starts | how heavy the bar's volume is against its own recent level ("a volume burst", "a quiet day"). With `exclude_current` the bar is compared with the bars before it only, so a burst does not inflate its own average. No direction; no `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    The bar's volume against its own recent average, on every bar:

        exclude_current = False (default):
            raw_value = volume[t] / mean(volume[t - period + 1 .. t])   (the average includes bar t)
        exclude_current = True:
            raw_value = volume[t] / mean(volume[t - period .. t - 1])   (the `period` bars before bar t)

    Graded and non-negative: 1 at an average bar, 2 for a bar with twice the average volume, near 0 for a very quiet
    bar. With the default it is at most `period`, reached when every other bar of the window has zero volume. With
    `exclude_current` it is unbounded above. It has no direction: a config combines it with a price move, or uses it
    in a regime rule. No lag: everything up to bar t's close.

    Warm-up: `period` rows with the default; `period` + 1 rows with `exclude_current` (the prior window plus bar t).

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the bars up to and including bar t, the last row of
    the data it is given. A bar's volume is known at that bar's close.

    NaN: a window that holds a NaN volume (bar t's included) gives NaN. So does a window whose averaged volumes are
    all zero, since there is no average to compare with. The engine refuses that NaN loudly rather than reading it as
    a quiet bar. A missing `volume` column raises. A `period` below 2 raises when the component is built.
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
        self._raw_value = last / mean if mean > 0 else float("nan")
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
    v = [float(x) for x in list(df["volume"])]
    current = v[-1]
    if exclude:
        base = v[-(n + 1):-1]
    else:
        base = v[-n:]
    total = 0.0
    for x in base:
        total += x
    mean = total / n
    if mean != mean or not mean > 0:
        return float("nan")
    return current / mean
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 226, in <module>
    main()
    ~~~~^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 205, in main
    spec = load_spec(args.spec)
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 187, in load_spec
    spec.loader.exec_module(mod)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "<frozen importlib._bootstrap_external>", line 1027, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/user/trading-bot/trading-bot/tests/built_components/VolumeRatioComponent.py", line 3, in <module>
    SETTINGS = [{}, {"period": 30}, {"period": 10}, {"period": 2}, {"period": 20, "exclude_current": true}]
                                                                                                     ^^^^
NameError: name 'true' is not defined. Did you mean: 'True'?

## attempt 2

answer: built
class: VolumeRatioComponent
settings: {"period": 20, "exclude_current": 1}
reason: `VolumeRatioComponent` computes this measure, but its average includes bar t, and the wish asks for the mean over the prior N bars only. A setting `exclude_current` is added: an integer, 0 by default, which keeps today's output; 1 compares volume[t] with the mean of the `period` bars before it.

table: Hedges and filters
row: | `VolumeRatioComponent` | `period` (30), `exclude_current` (0) | volume[t] / mean(volume over the last `period` bars, bar t included); with `exclude_current` 1: volume[t] / mean(volume[t-period] .. volume[t-1]), bar t excluded from the average | 0 to `period` at the default, never negative; with `exclude_current` 1: 0 and up, unbounded; 1 at an average bar, 2 for twice the average volume; no direction | graded | ratio | `period` + `exclude_current` (30) | volume. A window (bar t and the averaged bars) holding a NaN volume, or an average of 0, gives NaN; a `period` below 2 or an `exclude_current` other than 0 or 1 raises when the engine starts | how heavy the bar's volume is against its own recent average; `exclude_current` 1 keeps the current bar out of its own baseline (a burst is not diluted by itself). Stateless; no `scaling_factor`: scale it with transforms |

```python class
class VolumeRatioComponent(SubStrategyComponent):
    """
    The bar's volume against its own recent average, on every bar:

        exclude_current = 0 (default):
            raw_value = volume[t] / mean(volume[t - period + 1 .. t])   (the average includes bar t)
        exclude_current = 1:
            raw_value = volume[t] / mean(volume[t - period .. t - 1])   (the average of the prior `period` bars)

    Graded and non-negative: 1 at an average bar, 2 for a bar with twice the average volume, near 0 for a very quiet
    bar. With exclude_current 0 it is at most `period`; with exclude_current 1 it is unbounded above. No direction.
    Warm-up: `period` rows (exclude_current 0) or `period + 1` rows (exclude_current 1), bar t included.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the bars up to and including bar t (the last row of
    data); a bar's volume is known at that bar's close.

    NaN: a NaN volume at bar t or in the averaged bars, or an average of 0, gives NaN. A missing `volume` column
    raises. A `period` below 2, or an `exclude_current` other than 0 or 1, raises when the component is built.
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
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        vol = data['volume'].astype(float)
        last = float(vol.iloc[-1])
        if self.exclude_current:
            base = vol.iloc[-(self.period + 1):-1]
        else:
            base = vol.iloc[-self.period:]
        mean = float(base.mean(skipna=False))
        self._raw_value = last / mean if mean > 0 else float("nan")
        self.confidence = 1.0
        self.debug_info = {'volume': last, 'mean_volume': mean}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    n = int(params.get("period", 30))
    ex = int(params.get("exclude_current", 0))
    v = [float(x) for x in list(df["volume"])]
    cur = v[-1]
    if ex == 1:
        prior = v[-(n + 1):-1]
    else:
        prior = v[-n:]
    total = 0.0
    for x in prior:
        total = total + x
    mean = total / n
    if mean != mean or not mean > 0:
        return float("nan")
    return cur / mean
```

checks:
VolumeRatioComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1523 passed, 8 skipped, 74 deselected, 2170 warnings in 56.49s ========
