# VolumeWeightedScaledReturnComponent: night_run | 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d | volume_weighted_fall

## attempt 1

answer: built
class: VolumeWeightedScaledReturnComponent
settings: {"vol_period": 20, "volume_period": 30}
reason: No catalogue class computes the product of the one-bar return in usual moves (`VolatilityScaledReturnComponent` at `period` 1) and the bar's volume ratio (`VolumeRatioComponent` at its defaults), so one new class computes it. The wished "positive after a fall" form is this measure's mirror, which the config step `negate` gives exactly.

table: Directional components
row: | `VolumeWeightedScaledReturnComponent` | `vol_period` (20), `volume_period` (30) | ((close[t] / close[t-1] - 1) / s) x (volume[t] / mean(volume[t-`volume_period`+1 .. t])), s being the standard deviation (ddof 1) of the last `vol_period` one-bar returns close[j] / close[j-1] - 1, bar t's included; the first factor is 0 when s = 0 | unbounded, signed; positive after a rise, negative after a fall; the size grows with the move in usual moves and with the bar's volume against its average (the volume ratio is above 0, up to `volume_period`); `negate` gives the fall-positive reading | graded | usual moves x volume ratio | max(`vol_period` + 1, `volume_period`) (30) | close, volume. A NaN close in the last `vol_period` + 1 rows or a NaN volume in the last `volume_period` rows gives NaN; a mean volume not above 0 gives NaN (never on real bars); a flat return window (s = 0, never on real bars) gives 0. A `vol_period` below 2 or a `volume_period` below 2 raises when the component is built | stateless. Equals `VolatilityScaledReturnComponent` (`period` 1, same `vol_period`) x `VolumeRatioComponent` (`period` = `volume_period`, other settings at their defaults). Use `negate` for "a heavy-volume fall reads positive". No `scaling_factor`: scale it with transforms |

```python class
class VolumeWeightedScaledReturnComponent(SubStrategyComponent):
    """
    The bar's return in usual moves, weighted by the bar's volume against its average, on every bar:

        r(j)  = close[j] / close[j-1] - 1
        s     = std (ddof 1) of r(t - vol_period + 1) .. r(t)              (bar t's return included)
        z     = r(t) / s        (0 when s = 0)
        v     = volume[t] / mean(volume[t - volume_period + 1 .. t])       (bar t included)
        raw_value = z x v

    Graded, signed, unbounded: positive after a rise, negative after a fall. The size grows with the size of
    the move in the coin's usual moves and with how heavy the bar's volume was against its average. v is above
    0 and at most volume_period. The fall-positive reading is its mirror, given exactly by the `negate` step.
    Warm-up: max(vol_period + 1, volume_period) rows, bar t included.

    NaN: a NaN close in the last vol_period + 1 rows, or a NaN volume in the last volume_period rows, gives NaN.
    A mean volume not above 0 gives NaN (never seen on real bars). A flat return window (s = 0, never seen on
    real bars) gives 0. Building the component raises for a vol_period below 2 or a volume_period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last vol_period + 1 rows and the `volume`
    column of the last volume_period rows of data, all up to and including bar t (the last row). A bar's close
    and volume are known at that bar's close.
    """

    def __init__(self, name="VolumeWeightedScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"VolumeWeightedScaledReturnComponent: vol_period must be >= 2, got {self.vol_period}")
        self.volume_period = int(self.parameters.get("volume_period", 30))
        if self.volume_period < 2:
            raise ValueError(
                f"VolumeWeightedScaledReturnComponent: volume_period must be >= 2, got {self.volume_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float).iloc[-(self.vol_period + 1):].to_numpy()
        vol = data['volume'].astype(float).iloc[-self.volume_period:].to_numpy()
        if np.isnan(close).any() or np.isnan(vol).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = close[1:] / close[:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        den = float(vol.mean())
        if not den > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        ratio = float(vol[-1] / den)
        z = 0.0 if s == 0 else float(rets[-1] / s)
        self._raw_value = float(z * ratio)
        self.confidence = 1.0
        self.debug_info = {'scaled_return': z, 'volume_ratio': ratio, 'return_std': s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.vol_period + 1, self.volume_period)
```

```python hand
def hand(df, params):
    import math
    m = int(params.get("vol_period", 20))
    n = int(params.get("volume_period", 30))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    last = len(c) - 1
    closes = []
    i = last - m
    while i <= last:
        closes.append(c[i])
        i = i + 1
    vols = []
    i = last - n + 1
    while i <= last:
        vols.append(v[i])
        i = i + 1
    for x in closes + vols:
        if x != x:
            return float("nan")
    rets = []
    k = 1
    while k < len(closes):
        rets.append(closes[k] / closes[k - 1] - 1.0)
        k = k + 1
    mean_r = 0.0
    for r in rets:
        mean_r = mean_r + r
    mean_r = mean_r / len(rets)
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean_r) * (r - mean_r)
    s = math.sqrt(ss / (len(rets) - 1))
    total = 0.0
    for x in vols:
        total = total + x
    avg = total / n
    if not avg > 0:
        return float("nan")
    ratio = v[last] / avg
    if s == 0:
        z = 0.0
    else:
        z = rets[-1] / s
    return z * ratio
```

checks:
VolumeWeightedScaledReturnComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1534 passed, 8 skipped, 74 deselected, 2170 warnings in 67.00s (0:01:06) ===
