# VolumeChangeTimesFallDepthComponent: night8_fallingcalm_run | 060-02.d1.d2.d1_volume-signal-in-deeper-falls_1d | VolumeChangeTimesFallDepth

## attempt 1

answer: built
class: VolumeChangeTimesFallDepthComponent
settings: {"volume_period": 30, "fall_period": 20}
reason: `VolumeRatioComponent` (`period` 30, `exclude_current` 30, `short_period` 30, `form` "log") gives the volume factor, and the fall depth is the negated, clipped `PriceEvolutionOnPeriodComponent` (20). No config step multiplies two components, and `VolumeDryUpTimesFallModerationComponent` is a different measure: it clips the volume change at 0 and weights by 1 / (1 + fall). So one new class computes the product.

table: Directional components
row: | `VolumeChangeTimesFallDepthComponent` | `volume_period` (30), `fall_period` (20) | ln(mean(volume[t-`volume_period`+1 .. t]) / mean(volume[t-2·`volume_period`+1 .. t-`volume_period`])) x max(0, -(close[t] / close[t-`fall_period`] - 1) x 100) | unbounded, signed like the volume change: positive when recent volume is above the prior base, negative when it is below; 0 when the `fall_period`-bar return is 0 or positive, or when the two volume means are equal; its size grows with the size of the log volume change and with the depth of the fall (the fall factor is 0 to below 100) | graded | natural log of a volume ratio (recent over prior) x percent | max(2 x `volume_period`, `fall_period` + 1) (60) | volume (last 2 x `volume_period` rows), close (bars t and t-`fall_period`). A NaN in any value read gives NaN, whatever the sign of the return. A mean volume not above 0 gives NaN, and so does a close[t-`fall_period`] not above 0 (never on real bars). These settings raise when the component is built: `volume_period` < 1, `fall_period` < 1 | stateless. The volume factor equals `VolumeRatioComponent` (`period` = `volume_period`, `exclude_current` = `volume_period`, `short_period` = `volume_period`, `form` "log"). The fall factor is max(0, -`PriceEvolutionOnPeriodComponent` (`comparison_period` = `fall_period`)). The two volume windows are adjacent and do not overlap. The value is continuous in the volumes and closes, and exactly 0 whenever the window did not fall. On 1d bars the defaults give the last 30 days' log volume change against the 30 days before, times the 20-day fall in percent. Not `VolumeDryUpTimesFallModerationComponent`. No `scaling_factor`: scale it with transforms |

```python class
class VolumeChangeTimesFallDepthComponent(SubStrategyComponent):
    """
    Volume change times fall depth, on every bar:

        A = mean(volume[t - volume_period + 1 .. t])                       (bar t included)
        B = mean(volume[t - 2*volume_period + 1 .. t - volume_period])     (the volume_period bars before them)
        F = max(0, -(close[t] / close[t - fall_period] - 1) x 100)
        raw_value = ln(A / B) x F

    Range & sign: unbounded and signed like the volume change. It is positive when recent volume is above the
    prior base and negative when below. It is 0 when the fall_period-bar return is 0 or positive, or when
    A equals B. F is 0 to below 100. Graded: continuous in the volumes and the closes.
    Warm-up: max(2 * volume_period, fall_period + 1) rows, bar t included (60 at the defaults).
    NaN: a NaN volume in the last 2*volume_period rows, or a NaN close[t] or close[t-fall_period], gives NaN
    whatever the sign of the return. A mean volume not above 0, or a close[t-fall_period] not above 0, also
    gives NaN (never on real bars).
    Building raises for volume_period < 1 or fall_period < 1.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the last 2*volume_period rows and the `close`
    of the last row (bar t) and of the row fall_period rows before it, all at or before bar t.
    """

    def __init__(self, name="VolumeChangeTimesFallDepth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 30))
        if self.volume_period < 1:
            raise ValueError(
                f"VolumeChangeTimesFallDepthComponent: volume_period must be >= 1, got {self.volume_period}")
        self.fall_period = int(self.parameters.get("fall_period", 20))
        if self.fall_period < 1:
            raise ValueError(
                f"VolumeChangeTimesFallDepthComponent: fall_period must be >= 1, got {self.fall_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = len(data)
        vp = self.volume_period
        vol = data["volume"].astype(float).to_numpy()
        close = data["close"].astype(float).to_numpy()
        recent = vol[n - vp:n]
        base = vol[n - 2 * vp:n - vp]
        c_now = close[n - 1]
        c_base = close[n - 1 - self.fall_period]
        if np.isnan(recent).any() or np.isnan(base).any() or np.isnan(c_now) or np.isnan(c_base):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        a = float(recent.mean())
        b = float(base.mean())
        if not a > 0 or not b > 0 or not c_base > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        change = float(np.log(a / b))
        fall = max(0.0, -(c_now / c_base - 1.0) * 100.0)
        self._raw_value = float(change * fall)
        self.confidence = 1.0
        self.debug_info = {"recent_volume": a, "base_volume": b, "log_volume_change": change, "fall_pct": fall}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(2 * self.volume_period, self.fall_period + 1)
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("volume_period", 30))
    fp = int(params.get("fall_period", 20))
    v = [float(x) for x in list(df["volume"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    recent = [v[t - k] for k in range(vp)]
    prior = [v[t - vp - k] for k in range(vp)]
    vals = recent + prior + [c[t], c[t - fp]]
    for x in vals:
        if x != x:
            return float("nan")
    a = sum(recent) / vp
    b = sum(prior) / vp
    if not a > 0 or not b > 0 or not c[t - fp] > 0:
        return float("nan")
    ret = c[t] / c[t - fp] - 1.0
    depth = -ret * 100.0
    if depth < 0.0:
        depth = 0.0
    return math.log(a / b) * depth
```

checks:
VolumeChangeTimesFallDepthComponent: every check passed
the bot's suite: == 1670 passed, 16 skipped, 75 deselected, 2244 warnings in 146.69s (0:02:26) ==
