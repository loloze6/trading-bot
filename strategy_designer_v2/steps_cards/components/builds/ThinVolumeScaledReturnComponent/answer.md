# ThinVolumeScaledReturnComponent: night4_weekend_run | 026-04_thinner-weekend-larger-reversal_1h | WeekendThinVolumeReversal

## attempt 1

answer: built
class: ThinVolumeScaledReturnComponent
settings: {"period": 48, "window": 720, "volume_period": 48, "base_near": 49, "base_far": 168}
reason: No class in the catalogue computes this product. It multiplies the 48-bar return in usual moves (the measure of `MeanAbsScaledReturnComponent`) by an earlier-base / recent volume ratio, and that base window (t−168..t−49) leaves a gap at t−48 that `VolumeRatioComponent` cannot express, so one new class computes it. The wished sign (against the move) is its mirror, which `negate` gives exactly. The class is therefore signed like the return and the config appends `negate`.

table: Directional components
row: | `ThinVolumeScaledReturnComponent` | `period` (48), `window` (720), `volume_period` (48), `base_near` (49), `base_far` (168) | (close[t] / close[t-`period`] - 1) / m x (mean(volume[t-`base_far` .. t-`base_near`]) / mean(volume[t-`volume_period`+1 .. t])). m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`period`] - 1), the overlapping `period`-bar returns ending at each of the last `window` bars, bar t included. The first factor is 0 when m = 0 | unbounded, signed like the `period`-bar return. The size grows with the move in usual moves and as recent volume falls below the earlier base (the volume factor is above 0, 1 when the two means are equal). `negate` gives the against-the-move reading | graded | usual `period`-bar moves x volume ratio (base over recent) | max(`window` + `period`, `base_far` + 1) (768) | close, volume. A NaN close in the last `window` + `period` rows, or a NaN volume in either volume window, gives NaN. A close not above 0 there gives NaN (never on real bars), and so does a recent mean volume not above 0 (never on real bars). m = 0 gives 0 (never on real bars). These settings raise when the component is built: `period` < 1, `window` < 1, `volume_period` < 1, `base_near` < `volume_period`, `base_far` < `base_near` | stateless. It equals `MeanAbsScaledReturnComponent` (`period`, `window`) x base / recent mean volume. The volume windows do not overlap, and at the defaults bar t-48 is in neither. On 1h bars the defaults give the 48h return in usual 48h moves times the prior five days' mean volume over the last two days'. No `scaling_factor`: scale it with transforms |

```python class
class ThinVolumeScaledReturnComponent(SubStrategyComponent):
    """
    A return in usual moves, weighted by how thin recent volume is against an earlier base:

        r(i)  = close[i] / close[i - period] - 1
        m     = mean(abs(r(i))) over i = t - window + 1 .. t           (bar t included)
        Vr    = mean(volume[t - volume_period + 1 .. t])               (bar t included)
        Vb    = mean(volume[t - base_far .. t - base_near])
        raw_value = r(t) / m * Vb / Vr      (r(t) / m read as 0 when m = 0)

    Range & sign: unbounded, signed like the period-bar return. Its size grows with the move in usual
    moves and as recent volume falls below the base (Vb / Vr above 0, 1 when the means are equal).
    `negate` gives the reading signed against the move.
    Warm-up: max(window + period, base_far + 1) rows, bar t included (768 at the defaults).
    NaN: a NaN close in the last window + period rows, or a NaN volume in either volume window, gives NaN.
    A close not above 0 there gives NaN, and so does Vr not above 0 (neither happens on real bars).
    Building raises for period < 1, window < 1, volume_period < 1, base_near < volume_period,
    or base_far < base_near.

    WHY THIS CANNOT LEAK: it reads only the close and volume of the rows up to and including bar t (the last
    row of data): the closes of the last window + period rows and the volumes of bars t - base_far .. t.
    """

    def __init__(self, name="ThinVolumeScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        self.window = int(self.parameters.get("window", 720))
        self.volume_period = int(self.parameters.get("volume_period", 48))
        self.base_near = int(self.parameters.get("base_near", 49))
        self.base_far = int(self.parameters.get("base_far", 168))
        if self.period < 1:
            raise ValueError(f"ThinVolumeScaledReturnComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"ThinVolumeScaledReturnComponent: window must be >= 1, got {self.window}")
        if self.volume_period < 1:
            raise ValueError(
                f"ThinVolumeScaledReturnComponent: volume_period must be >= 1, got {self.volume_period}")
        if self.base_near < self.volume_period:
            raise ValueError(
                f"ThinVolumeScaledReturnComponent: base_near must be >= volume_period, got {self.base_near}")
        if self.base_far < self.base_near:
            raise ValueError(
                f"ThinVolumeScaledReturnComponent: base_far must be >= base_near, got {self.base_far}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float).to_numpy()
        vol = data["volume"].astype(float).to_numpy()
        n = len(close)
        c = close[-(self.window + self.period):]
        recent = vol[-self.volume_period:]
        base = vol[n - 1 - self.base_far: n - self.base_near]
        self.confidence = 1.0
        if np.isnan(c).any() or np.isnan(recent).any() or np.isnan(base).any() or (c <= 0).any():
            self._raw_value = float("nan")
            return
        r = c[self.period:] / c[:-self.period] - 1.0
        m = float(np.mean(np.abs(r)))
        vr = float(np.mean(recent))
        vb = float(np.mean(base))
        if not vr > 0:
            self._raw_value = float("nan")
            return
        scaled = 0.0 if m == 0 else float(r[-1]) / m
        self._raw_value = float(scaled * vb / vr)
        self.debug_info = {"return": float(r[-1]), "mean_abs_return": m,
                           "recent_volume": vr, "base_volume": vb}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.window + self.period, self.base_far + 1)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 48))
    w = int(params.get("window", 720))
    vp = int(params.get("volume_period", 48))
    bn = int(params.get("base_near", 49))
    bf = int(params.get("base_far", 168))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    for j in range(t - w - p + 1, t + 1):
        if c[j] != c[j] or not c[j] > 0:
            return float("nan")
    total = 0.0
    for i in range(t - w + 1, t + 1):
        total += abs(c[i] / c[i - p] - 1.0)
    m = total / w
    ret = c[t] / c[t - p] - 1.0
    rs = 0.0
    for i in range(t - vp + 1, t + 1):
        if v[i] != v[i]:
            return float("nan")
        rs += v[i]
    bs = 0.0
    cnt = 0
    for i in range(t - bf, t - bn + 1):
        if v[i] != v[i]:
            return float("nan")
        bs += v[i]
        cnt += 1
    vr = rs / vp
    vb = bs / cnt
    if not vr > 0:
        return float("nan")
    scaled = 0.0 if m == 0 else ret / m
    return scaled * vb / vr
```

checks:
ThinVolumeScaledReturnComponent: every check passed
the bot's suite: == 1610 passed, 16 skipped, 75 deselected, 2244 warnings in 101.11s (0:01:41) ==
