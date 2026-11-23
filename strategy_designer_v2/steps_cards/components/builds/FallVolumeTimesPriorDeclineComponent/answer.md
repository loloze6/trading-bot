# FallVolumeTimesPriorDeclineComponent: brief_absorption_run | 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d2_absorption-rebound-after-declines_1d | FallVolumeTimesPriorDeclineComponent

## attempt 1

answer: built
class: FallVolumeTimesPriorDeclineComponent
settings: {"vol_period": 20, "volume_period": 20, "decline_period": 20}
reason: No component multiplies the day's fall in usual moves, its volume over the prior mean (bar t excluded) and the depth of the decline ending the day before. `FallVolumeVolatilityWeightedComponent` uses the fall in percent and a volatility ratio. `FallTimesFallComponent` uses both falls ending at bar t, with no volume. One new class computes this product.

table: Directional components
row: | `FallVolumeTimesPriorDeclineComponent` | `vol_period` (20), `volume_period` (20), `decline_period` (20) | max(0, −(close[t] / close[t-1] − 1) / s) x volume[t] / mean(volume[t-`volume_period`] .. volume[t-1]) x max(0, −(close[t-1] / close[t-1-`decline_period`] − 1)) x 100. s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included. The first factor is 0 when s = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 on up bars and flat bars, and 0 when close[t-1] is not below close[t-1-`decline_period`]. It grows with the day's fall in usual one-bar moves, with the day's volume against its prior mean (ratio above 0, unbounded, bar t excluded from its base), and with the prior decline in percent (0 to 100) | graded | usual one-bar moves x volume ratio x percent | max(`vol_period` + 1, `volume_period` + 1, `decline_period` + 2) (22) | close (last max(`vol_period` + 1, `decline_period` + 2) rows), volume (bar t and bars t-`volume_period` .. t-1). A NaN in any value read gives NaN, whatever the sign of the move. A close not above 0 among those read gives NaN, and so does a base mean volume not above 0 (neither is ever seen on real bars). s = 0 (a flat return window, never on real bars) gives 0. These settings raise when the component is built: `vol_period` < 2, `volume_period` < 1, `decline_period` < 1 | stateless. Equals max(0, −`VolatilityScaledReturnComponent` (`period` 1, `vol_period`)) x `VolumeRatioComponent` (`period` = `volume_period`, `exclude_current` 1) x max(0, −`PriceEvolutionOnPeriodComponent` (`comparison_period` = `decline_period`) read at bar t-1). The prior decline ends at bar t-1, so the falling day cannot deepen it. The volume base excludes bar t. It is continuous in the closes and volumes and exactly 0 on most bars. One-sided, an absorption-rebound reading. On 1d bars the defaults give the day's fall in usual daily moves, times its volume over the prior 20 days' mean, times the 20-day decline in percent into yesterday. No `scaling_factor`: scale it with transforms |

```python class
class FallVolumeTimesPriorDeclineComponent(SubStrategyComponent):
    """
    The day's fall in usual moves, times its volume multiple, times the decline before it:

        r(j) = close[j] / close[j-1] - 1
        s    = std (ddof 1) of r(j), j = t-vol_period+1 .. t            (bar t's return included)
        F    = max(0, -r(t)) / s                                        (0 when s = 0)
        V    = volume[t] / mean(volume[t-volume_period] .. volume[t-1])  (bar t excluded from the base)
        P    = max(0, -(close[t-1] / close[t-1-decline_period] - 1)) x 100
        raw_value = F x V x P

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 on up and flat bars, and 0 when
    close[t-1] is not below close[t-1-decline_period]. It grows with the fall in usual moves, with the volume
    multiple and with the prior decline in percent.
    Warm-up: max(vol_period + 1, volume_period + 1, decline_period + 2) rows, bar t included (22 at the defaults).

    NaN: a NaN close among the last max(vol_period + 1, decline_period + 2) rows, or a NaN volume at bar t or in
    the base, gives NaN whatever the sign of the move. A close not above 0 there gives NaN, and so does a base
    mean volume not above 0 (neither is seen on real bars). s = 0 gives 0.
    Building the component raises for vol_period < 2, volume_period < 1 or decline_period < 1.

    WHY THIS CANNOT LEAK: it reads only the close and volume columns of the last rows of data, up to and
    including bar t (the last row); the prior decline ends at bar t-1 and the volume base ends at bar t-1.
    """

    def __init__(self, name="FallVolumePriorDecline", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"FallVolumeTimesPriorDeclineComponent: vol_period must be >= 2, got {self.vol_period}")
        self.volume_period = int(self.parameters.get("volume_period", 20))
        if self.volume_period < 1:
            raise ValueError(
                f"FallVolumeTimesPriorDeclineComponent: volume_period must be >= 1, got {self.volume_period}")
        self.decline_period = int(self.parameters.get("decline_period", 20))
        if self.decline_period < 1:
            raise ValueError(
                f"FallVolumeTimesPriorDeclineComponent: decline_period must be >= 1, got {self.decline_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n_close = max(self.vol_period + 1, self.decline_period + 2)
        close = data["close"].astype(float).to_numpy()[-n_close:]
        vol = data["volume"].astype(float).to_numpy()[-(self.volume_period + 1):]
        if np.isnan(close).any() or np.isnan(vol).any() or not (close > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        vp = self.vol_period
        rets = close[-vp:] / close[-vp - 1:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        r_t = float(close[-1] / close[-2] - 1.0)
        fall = max(0.0, -r_t) / s if s > 0 else 0.0
        base_mean = float(np.mean(vol[:-1]))
        if not base_mean > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        vratio = float(vol[-1]) / base_mean
        dp = self.decline_period
        decline = max(0.0, -(float(close[-2]) / float(close[-2 - dp]) - 1.0)) * 100.0
        self._raw_value = float(fall * vratio * decline)
        self.confidence = 1.0
        self.debug_info = {"fall_in_usual_moves": fall, "volume_ratio": vratio, "prior_decline_pct": decline,
                           "std": s}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.vol_period + 1, self.volume_period + 1, self.decline_period + 2)
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("vol_period", 20))
    volp = int(params.get("volume_period", 20))
    dp = int(params.get("decline_period", 20))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1

    # closes read: bars t-vp .. t (returns) and bar t-1-dp (decline base)
    first = min(t - vp, t - 1 - dp)
    for i in range(first, t + 1):
        x = c[i]
        if x != x or not x > 0:
            return float("nan")
    # volumes read: bars t-volp .. t
    for i in range(t - volp, t + 1):
        if v[i] != v[i]:
            return float("nan")

    # std (ddof 1) of the vp one-bar returns ending at bar t
    rets = []
    for j in range(t - vp + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mu = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - mu) ** 2
    s = math.sqrt(ss / (len(rets) - 1))

    today = c[t] / c[t - 1] - 1.0
    fall = 0.0
    if today < 0 and s > 0:
        fall = -today / s

    total = 0.0
    for i in range(t - volp, t):
        total += v[i]
    base = total / volp
    if not base > 0:
        return float("nan")
    vr = v[t] / base

    prior = c[t - 1] / c[t - 1 - dp] - 1.0
    decline = -prior * 100.0 if prior < 0 else 0.0

    return fall * vr * decline
```

checks:
FallVolumeTimesPriorDeclineComponent: every check passed
the bot's suite: == 1639 passed, 16 skipped, 75 deselected, 2244 warnings in 72.79s (0:01:12) ===
