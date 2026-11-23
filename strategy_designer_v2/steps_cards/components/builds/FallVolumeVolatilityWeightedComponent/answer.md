# FallVolumeVolatilityWeightedComponent: brief_absorption_run | 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.d1_absorption-rebound-in-stressed-markets_1d | VolatilityRatioWeightedHeavyVolumeFall

## attempt 1

answer: built
class: FallVolumeVolatilityWeightedComponent
settings: {"volume_period": 20, "vol_period": 20, "base_vol_period": 120}
reason: No component of the catalogue multiplies a one-bar fall in percent by the bar's volume against its prior 20-bar mean (bar t excluded) and by the 20-bar return std over the 120-bar return std. `VolumeWeightedScaledReturnComponent` divides the return by its std, includes bar t in its volume base and has no volatility ratio, and `FallCloseLocationComponent` has neither ratio. This product is one new measure, so one new class computes it.

table: Directional components
row: | `FallVolumeVolatilityWeightedComponent` | `volume_period` (20), `vol_period` (20), `base_vol_period` (120) | max(0, −(close[t] / close[t-1] − 1)) x 100 x volume[t] / mean(volume[t-`volume_period` .. t-1]) x s_recent / s_base. s_recent and s_base are the std (ddof 1) of the last `vol_period` and `base_vol_period` one-bar returns close[j] / close[j-1] − 1, both ending at bar t, bar t's return included | 0 and up, unbounded above, never negative; no direction. It is 0 on up bars and flat bars. It grows with the size of today's fall in percent, with today's volume against its prior average (ratio above 0, unbounded, bar t excluded from its base), and with the recent volatility against the longer one (1 at equal volatility) | graded | percent x volume ratio x ratio of volatilities (recent over base) | max(`volume_period` + 1, `vol_period` + 1, `base_vol_period` + 1) (121) | close (last max(`vol_period`, `base_vol_period`) + 1 rows), volume (bar t and bars t-`volume_period` .. t-1). A NaN in any value read gives NaN, whatever the sign of the move. A close not above 0 among those read gives NaN, and so does a base mean volume not above 0 or an s_base of 0 (none of these is ever seen on real bars). These settings raise when the component is built: `volume_period` < 1, `vol_period` < 2, `base_vol_period` < 2 | stateless. It equals max(0, −`PriceEvolutionComponent` (`period` 1, `sf` 1)) x `VolumeRatioComponent` (`period` = `volume_period`, `exclude_current` 1) x `RecentToPriorVolatilityRatioComponent` (`vol_period`, `base_period` = `base_vol_period`, `base_lag` 0). The volume base excludes bar t, so bar t's own volume cannot raise its base. The base volatility window contains the recent one. It is continuous in the closes and volumes, and exactly 0 on up bars. It is one-sided, a heavy-volume-fall (rebound) reading. On 1d bars the defaults give the day's fall times its volume over the prior 20 days' mean, times the 20-day over the 120-day volatility. No `scaling_factor`: scale it with transforms |

```python class
class FallVolumeVolatilityWeightedComponent(SubStrategyComponent):
    """
    One-bar fall, weighted by the bar's volume against its prior average and by recent against longer volatility:

        r(j)      = close[j] / close[j-1] - 1
        fall      = max(0, -r(t)) x 100
        vratio    = volume[t] / mean(volume[t-volume_period .. t-1])        (bar t excluded from the base)
        s_recent  = std (ddof 1) of r(j), j = t-vol_period+1 .. t
        s_base    = std (ddof 1) of r(j), j = t-base_vol_period+1 .. t
        raw_value = fall x vratio x s_recent / s_base

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 on up bars and flat bars, and grows
    with the fall, the volume ratio and the volatility ratio. Graded, and continuous in the prices and volumes.
    Warm-up: max(volume_period + 1, vol_period + 1, base_vol_period + 1) rows, bar t included (121 at the defaults).

    NaN: a NaN close among the closes read, or a NaN volume on bar t or in the base, gives NaN, whatever the move's
    sign. A close not above 0 among those read, a base mean volume not above 0, or an s_base of 0 gives NaN (never
    on real bars).
    Building the component raises for a volume_period below 1, or a vol_period or base_vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the close and volume columns of the last get_required_periods() rows of
    data, the last row being bar t; every value is known at bar t's close.
    """

    def __init__(self, name="FallVolVolWeighted", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 20))
        self.vol_period = int(self.parameters.get("vol_period", 20))
        self.base_vol_period = int(self.parameters.get("base_vol_period", 120))
        if self.volume_period < 1:
            raise ValueError(f"FallVolumeVolatilityWeightedComponent: volume_period must be >= 1, got {self.volume_period}")
        if self.vol_period < 2:
            raise ValueError(f"FallVolumeVolatilityWeightedComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.base_vol_period < 2:
            raise ValueError(
                f"FallVolumeVolatilityWeightedComponent: base_vol_period must be >= 2, got {self.base_vol_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        nc = max(self.vol_period, self.base_vol_period) + 1
        closes = data["close"].astype(float).to_numpy()[-nc:]
        vols = data["volume"].astype(float).to_numpy()
        v_t = float(vols[-1])
        base = vols[-self.volume_period - 1:-1]
        self.confidence = 1.0
        if np.isnan(closes).any() or np.isnan(base).any() or np.isnan(v_t) or not (closes > 0).all():
            self._raw_value = float("nan")
            return
        mean_base = float(np.mean(base))
        if not mean_base > 0:
            self._raw_value = float("nan")
            return
        rets = closes[1:] / closes[:-1] - 1.0
        r_t = float(rets[-1])
        s_recent = float(np.std(rets[-self.vol_period:], ddof=1))
        s_base = float(np.std(rets[-self.base_vol_period:], ddof=1))
        if not s_base > 0:
            self._raw_value = float("nan")
            return
        fall = max(0.0, -r_t) * 100.0
        vratio = v_t / mean_base
        self._raw_value = float(fall * vratio * s_recent / s_base)
        self.debug_info = {"fall_pct": fall, "volume_ratio": vratio, "s_recent": s_recent, "s_base": s_base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.volume_period + 1, self.vol_period + 1, self.base_vol_period + 1)
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("volume_period", 20))
    sp = int(params.get("vol_period", 20))
    bp = int(params.get("base_vol_period", 120))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    n_ret = max(sp, bp)
    used_c = [c[t - k] for k in range(n_ret + 1)]
    used_v = [v[t]] + [v[t - k] for k in range(1, vp + 1)]
    for x in used_c + used_v:
        if x != x:
            return float("nan")
    for x in used_c:
        if not x > 0:
            return float("nan")

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def std1(xs):
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) ** 2
        return math.sqrt(ss / (len(xs) - 1))

    base_vol = [v[t - k] for k in range(1, vp + 1)]
    mean_base = sum(base_vol) / len(base_vol)
    if not mean_base > 0:
        return float("nan")
    s_recent = std1([ret(t - k) for k in range(sp)])
    s_base = std1([ret(t - k) for k in range(bp)])
    if not s_base > 0:
        return float("nan")
    r_t = ret(t)
    fall = -r_t * 100.0 if r_t < 0 else 0.0
    return fall * (v[t] / mean_base) * (s_recent / s_base)
```

checks:
FallVolumeVolatilityWeightedComponent: every check passed
the bot's suite: == 1638 passed, 16 skipped, 75 deselected, 2244 warnings in 78.41s (0:01:18) ===
