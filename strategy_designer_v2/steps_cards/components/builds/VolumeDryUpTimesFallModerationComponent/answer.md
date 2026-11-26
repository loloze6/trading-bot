# VolumeDryUpTimesFallModerationComponent: night8_fallingcalm_run | 060-01.d2_dry-up-in-moderate-declines_1d | VolumeDryUpTimesFallModerationComponent

## attempt 1

answer: built
class: VolumeDryUpTimesFallModerationComponent
settings: {"volume_period": 30, "fall_period": 20}
reason: `VolumeRatioComponent` (`period` 30, `exclude_current` 30, `short_period` 30, `form` "log") gives the log volume ratio, and `negate` with a `clip` gives its shrinkage. No component weights that shrinkage by 1 / (1 + the 20-day fall in percent), and no config step multiplies two components, so one new class computes the product.

table: Directional components
row: | `VolumeDryUpTimesFallModerationComponent` | `volume_period` (30), `fall_period` (20) | max(0, −ln(mean(volume[t-`volume_period`+1 .. t]) / mean(volume[t-2·`volume_period`+1 .. t-`volume_period`]))) x 1 / (1 + D), D = max(0, (close[t-`fall_period`] − close[t]) / close[t-`fall_period`] x 100) | 0 and up, unbounded above, never negative; no direction. It is 0 when recent volume is at or above the prior base, and grows with the shrinkage. The weight is above 0 and up to 1: it is 1 when the close is at or above its value `fall_period` bars ago, and it fades toward 0 as the fall deepens | graded | natural log of a volume ratio (base over recent, clipped at 0) x proximity (0 to 1) | max(2 x `volume_period`, `fall_period` + 1) (60) | volume (last 2 x `volume_period` rows), close (bars t and t-`fall_period`). A NaN in any value read gives NaN. A mean volume not above 0, or a close[t-`fall_period`] not above 0, gives NaN (never on real bars). These settings raise when the component is built: `volume_period` < 1, `fall_period` < 1 | stateless. The first factor equals max(0, −`VolumeRatioComponent` (`period` = `volume_period`, `exclude_current` = `volume_period`, `short_period` = `volume_period`, `form` "log")). The two volume windows are adjacent and do not overlap. The value is continuous in the volumes and the closes, and exactly 0 when volume did not shrink. On 1d bars the defaults give the last 30 days' volume dry-up against the 30 days before, weighted by the mildness of the 20-day fall. `standardise` then `negate` gives the short forecast. No `scaling_factor`: scale it with transforms |

```python class
class VolumeDryUpTimesFallModerationComponent(SubStrategyComponent):
    """
    Volume dry-up weighted by how mild the recent fall is, on every bar:

        A = mean(volume[t - volume_period + 1 .. t])                     (bar t included)
        B = mean(volume[t - 2*volume_period + 1 .. t - volume_period])   (the adjacent base before it)
        dry = max(0, -ln(A / B))
        D = max(0, (close[t - fall_period] - close[t]) / close[t - fall_period] x 100)
        raw_value = dry x 1 / (1 + D)

    Range: 0 and up, unbounded above, never negative; no direction. The value is 0 when A >= B, and it grows as
    recent volume shrinks against the base. The weight is in (0, 1]: it is 1 when close[t] >= close[t - fall_period],
    and it fades toward 0 as the fall deepens. The value is continuous in the volumes and closes.
    Warm-up: max(2 x volume_period, fall_period + 1) rows, bar t included (60 at the defaults).
    NaN: a NaN volume in the last 2 x volume_period rows, or a NaN close[t] or close[t - fall_period], gives NaN.
    A mean volume not above 0, or a close[t - fall_period] not above 0, gives NaN (never on real bars).
    Building the component raises for volume_period < 1 or fall_period < 1.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the last 2 x volume_period rows and the `close`
    column at bar t and bar t - fall_period, all at or before the last row of data (bar t).
    """

    def __init__(self, name="VolumeDryUpFallModeration", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 30))
        if self.volume_period < 1:
            raise ValueError(
                f"VolumeDryUpTimesFallModerationComponent: volume_period must be >= 1, got {self.volume_period}")
        self.fall_period = int(self.parameters.get("fall_period", 20))
        if self.fall_period < 1:
            raise ValueError(
                f"VolumeDryUpTimesFallModerationComponent: fall_period must be >= 1, got {self.fall_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        vp = self.volume_period
        vol = data["volume"].astype(float).to_numpy()
        close = data["close"].astype(float).to_numpy()
        n = len(vol)
        recent = vol[n - vp:]
        base = vol[n - 2 * vp:n - vp]
        c_now = close[-1]
        c_then = close[-1 - self.fall_period]
        if (np.isnan(recent).any() or np.isnan(base).any()
                or np.isnan(c_now) or np.isnan(c_then)):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        a = float(recent.mean())
        b = float(base.mean())
        if not a > 0 or not b > 0 or not c_then > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        dry = max(0.0, -float(np.log(a / b)))
        d = max(0.0, (c_then - c_now) / c_then * 100.0)
        self._raw_value = float(dry / (1.0 + d))
        self.confidence = 1.0
        self.debug_info = {"recent_volume": a, "base_volume": b, "dry_up": dry, "fall_pct": d}

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
    t = len(v) - 1
    recent = [v[t - k] for k in range(vp)]
    base = [v[t - vp - k] for k in range(vp)]
    for x in recent + base + [c[t], c[t - fp]]:
        if x != x:
            return float("nan")
    s_r = 0.0
    for x in recent:
        s_r += x
    s_b = 0.0
    for x in base:
        s_b += x
    a = s_r / vp
    b = s_b / vp
    if not a > 0 or not b > 0 or not c[t - fp] > 0:
        return float("nan")
    shrink = -math.log(a / b)
    if shrink < 0:
        shrink = 0.0
    fall = (c[t - fp] - c[t]) / c[t - fp] * 100.0
    if fall < 0:
        fall = 0.0
    return shrink * (1.0 / (1.0 + fall))
```

checks:
VolumeDryUpTimesFallModerationComponent: every check passed
the bot's suite: == 1669 passed, 16 skipped, 75 deselected, 2244 warnings in 130.53s (0:02:10) ==
