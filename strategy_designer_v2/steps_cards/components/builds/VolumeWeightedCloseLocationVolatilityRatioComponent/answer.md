# VolumeWeightedCloseLocationVolatilityRatioComponent: brief_absorption_run | 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets_1d | VolumeWeightedLowCloseVolatilityRatioComponent

## attempt 1

answer: built
class: VolumeWeightedCloseLocationVolatilityRatioComponent
settings: {"volume_period": 20, "vol_period": 20, "vol_lookback": 60}
reason: No class computes this product. Two catalogue classes give parts of it: `VolumeWeightedCloseLocationComponent` (`reference` "high", `exclude_current` 1, `volume_period` 20) gives the first two factors, and `VolatilityRatioToAverageComponent` gives a volatility ratio, but its mean includes s(t) where the wish asks for the prior bars only. A product of measures is a measure of its own, so one new class computes it.

table: Directional components
row: | `VolumeWeightedCloseLocationVolatilityRatioComponent` | `volume_period` (20), `vol_period` (20), `vol_lookback` (60) | (high[t] − close[t]) / (high[t] − low[t]) x volume[t] / mean(volume[t-`volume_period` .. t-1]) x s(t) / mean(s(t-`vol_lookback`) .. s(t-1)). s(i) is the std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = i-`vol_period`+1 .. i, bar i's included. The location factor is 0.5 when high[t] = low[t] | 0 and up, unbounded above, never negative; no direction. It is 0 with the close at the bar's high. It grows as the close nears the low, as volume[t] rises above its prior average, and as s(t) rises above its prior mean | graded | dimensionless (share of the bar's range x volume ratio x volatility ratio) | share of range x ratio of volumes x ratio of volatilities | max(`volume_period` + 1, `vol_lookback` + `vol_period` + 1) (81) | high, low, close, volume. Bar t is read for high and low; the last `volume_period` + 1 rows for volume; the last `vol_lookback` + `vol_period` + 1 rows for close. A NaN in any value read gives NaN. A close not above 0 among the return bases gives NaN, and so do a volume base mean not above 0 and a mean of prior s equal to 0 (none is ever seen on real bars). These settings raise when the component is built: `volume_period` < 2, `vol_period` < 2, `vol_lookback` < 1 | stateless. The first two factors equal `VolumeWeightedCloseLocationComponent` (`volume_period`, `exclude_current` 1, `reference` "high"). The third factor is s(t) over the mean of the `vol_lookback` s values before bar t, s(t) excluded, so it is not `VolatilityRatioToAverageComponent`, whose mean includes s(t). It is continuous in the prices and volumes while the bar's range is above 0. It ignores the open. No `scaling_factor`: scale it with transforms |

```python class
class VolumeWeightedCloseLocationVolatilityRatioComponent(SubStrategyComponent):
    """
    Close location measured from the bar's high, weighted by the bar's volume against its prior average and by
    the current volatility against its prior mean:

        loc = (high[t] - close[t]) / (high[t] - low[t])          (0.5 when high[t] = low[t])
        vr  = volume[t] / mean(volume[t - volume_period .. t - 1])  (bar t excluded from the base)
        s(i) = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1, j = i-vol_period+1 .. i
        sr  = s(t) / mean(s(t - vol_lookback) .. s(t - 1))       (s(t) excluded from the mean)
        raw_value = loc x vr x sr

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 with the close at the high and grows
    as the close nears the low, as volume rises above its prior average, and as volatility rises above its prior
    mean.
    Warm-up: max(volume_period + 1, vol_lookback + vol_period + 1) rows, bar t included (81 at the defaults).
    NaN: a NaN high or low on bar t, a NaN volume in the last volume_period + 1 rows, or a NaN close in the last
    vol_lookback + vol_period + 1 rows gives NaN. A close not above 0 there, a volume base mean not above 0, or a
    mean of prior s equal to 0 also gives NaN (never on real bars).
    Building raises for volume_period < 2, vol_period < 2 or vol_lookback < 1.

    WHY THIS CANNOT LEAK: it reads only rows up to and including bar t (the last row of data): high, low and
    close of bar t, volume of the last volume_period + 1 rows, and close of the last
    vol_lookback + vol_period + 1 rows. All are known at bar t's close.
    """

    def __init__(self, name="VolWeightedCloseLocVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 20))
        self.vol_period = int(self.parameters.get("vol_period", 20))
        self.vol_lookback = int(self.parameters.get("vol_lookback", 60))
        if self.volume_period < 2:
            raise ValueError(f"volume_period must be >= 2, got {self.volume_period}")
        if self.vol_period < 2:
            raise ValueError(f"vol_period must be >= 2, got {self.vol_period}")
        if self.vol_lookback < 1:
            raise ValueError(f"vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        nan = float("nan")
        h = float(data["high"].iloc[-1])
        lo = float(data["low"].iloc[-1])
        c_t = float(data["close"].iloc[-1])
        vol = data["volume"].astype(float).to_numpy()[-(self.volume_period + 1):]
        P, L = self.vol_period, self.vol_lookback
        closes = data["close"].astype(float).to_numpy()[-(L + P + 1):]
        if (np.isnan(h) or np.isnan(lo) or np.isnan(c_t) or np.isnan(vol).any()
                or np.isnan(closes).any() or not (closes[:-1] > 0).all()):
            self._raw_value = nan
            self.confidence = 1.0
            return
        rng = h - lo
        loc = 0.5 if rng == 0 else (h - c_t) / rng
        vbase = float(vol[:-1].mean())
        if not vbase > 0:
            self._raw_value = nan
            self.confidence = 1.0
            return
        vr = float(vol[-1]) / vbase
        rets = closes[1:] / closes[:-1] - 1.0          # length L + P, last = bar t's return
        s_t = float(np.std(rets[L:], ddof=1))
        prior = [float(np.std(rets[L - m:L + P - m], ddof=1)) for m in range(1, L + 1)]
        sbase = float(np.mean(prior))
        if not sbase > 0:
            self._raw_value = nan
            self.confidence = 1.0
            return
        sr = s_t / sbase
        self._raw_value = float(loc * vr * sr)
        self.confidence = 1.0
        self.debug_info = {"loc": loc, "volume_ratio": vr, "vol_ratio": sr}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.volume_period + 1, self.vol_lookback + self.vol_period + 1)
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("volume_period", 20))
    P = int(params.get("vol_period", 20))
    L = int(params.get("vol_lookback", 60))
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    vo = [float(x) for x in list(df["volume"])]
    t = len(cl) - 1

    def isnan(x):
        return x != x

    if isnan(hi[t]) or isnan(lo[t]) or isnan(cl[t]):
        return float("nan")
    # location of the close measured from the high
    if hi[t] - lo[t] == 0:
        loc = 0.5
    else:
        loc = (hi[t] - cl[t]) / (hi[t] - lo[t])
    # volume against the prior volume_period bars
    total = 0.0
    for k in range(1, vp + 1):
        x = vo[t - k]
        if isnan(x):
            return float("nan")
        total += x
    if isnan(vo[t]):
        return float("nan")
    vmean = total / vp
    if not vmean > 0:
        return float("nan")
    vr = vo[t] / vmean

    def ret(j):
        a = cl[j - 1]
        b = cl[j]
        if isnan(a) or isnan(b) or not a > 0:
            return None
        return b / a - 1.0

    def s(i):
        xs = []
        for j in range(i - P + 1, i + 1):
            r = ret(j)
            if r is None:
                return None
            xs.append(r)
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (len(xs) - 1))

    s_t = s(t)
    if s_t is None:
        return float("nan")
    acc = 0.0
    for i in range(t - L, t):
        v = s(i)
        if v is None:
            return float("nan")
        acc += v
    sbase = acc / L
    if not sbase > 0:
        return float("nan")
    return loc * vr * (s_t / sbase)
```

refused: the row must start with | `VolumeWeightedCloseLocationVolatilityRatioComponent` | and have the catalogue's nine columns

## attempt 2

answer: built
class: VolumeWeightedCloseLocationVolatilityRatioComponent
settings: {"volume_period": 20, "vol_period": 20, "vol_lookback": 60}
reason: No component computes this product. `VolumeWeightedCloseLocationComponent` (`volume_period` 20, `exclude_current` 1, `reference` "high") gives the first two factors and `VolatilityRatioToAverageComponent` (`vol_period` 20, `vol_lookback`) gives the third. A measure that multiplies them is one new class.

table: Directional components
row: | `VolumeWeightedCloseLocationVolatilityRatioComponent` | `volume_period` (20), `vol_period` (20), `vol_lookback` (60) | (high[t] − close[t]) / (high[t] − low[t]) x volume[t] / mean(volume[t-`volume_period` .. t-1]) x s(t) / mean(s(t-`vol_lookback`+1) .. s(t)). s(i) is the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1 ending at bar i, that bar's included. The location factor is 0.5 when high[t] = low[t] | 0 and up, unbounded above, never negative; no direction. It is 0 with the close at the bar's high and grows as the close nears the low, as volume[t] rises above its prior average (ratio unbounded, bar t excluded from its base), and as the current volatility rises above its average (ratio at most `vol_lookback`, the mean includes s(t)) | graded | dimensionless (share of the bar's range x volume ratio x ratio of volatilities) | max(`volume_period` + 1, `vol_lookback` + `vol_period`) (80) | high, low of bar t; close (last `vol_lookback` + `vol_period` rows); volume (bar t and bars t-`volume_period` .. t-1). A NaN in any value read gives NaN. A close not above 0 among the closes read gives NaN, and so does a base mean volume not above 0 or a mean of s equal to 0 (none of these is ever seen on real bars). These settings raise when the component is built: `volume_period` < 2, `vol_period` < 2, `vol_lookback` < 1 | stateless. Equals `VolumeWeightedCloseLocationComponent` (`volume_period`, `exclude_current` 1, `reference` "high") x `VolatilityRatioToAverageComponent` (`vol_period`, `vol_lookback`). The volume base excludes bar t, so bar t's own volume cannot raise its base. The volatility mean includes s(t), as in `VolatilityRatioToAverageComponent`. It is continuous in the close, the volumes and the closes while the range is above 0. It ignores the open. One-sided, an absorbed-selling reading. No `scaling_factor`: scale it with transforms |

```python class
class VolumeWeightedCloseLocationVolatilityRatioComponent(SubStrategyComponent):
    """
    Low close on heavy volume in a volatile market, on every bar:

        loc   = (high[t] - close[t]) / (high[t] - low[t])      (0.5 when high[t] == low[t])
        vr    = volume[t] / mean(volume[t - volume_period .. t - 1])   (bar t excluded from the base)
        s(i)  = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1, j = i-vol_period+1 .. i
        volr  = s(t) / mean(s(t - vol_lookback + 1) .. s(t))
        raw_value = loc * vr * volr

    Range: 0 and up, unbounded above, never negative, with no direction. It is 0 with the close at the bar's high
    and grows as the close nears the low, as volume rises above its prior average, and as volatility rises above
    its average (volr is at most vol_lookback because the mean includes s(t)).
    Warm-up: max(volume_period + 1, vol_lookback + vol_period) rows, bar t included (80 at the defaults).
    NaN: a NaN in any high, low, close or volume read gives NaN. A close not above 0 among the closes read, a base
    mean volume not above 0, or a mean of s equal to 0 also gives NaN (never seen on real bars).
    Building the component raises for volume_period < 2, vol_period < 2 or vol_lookback < 1.

    WHY THIS CANNOT LEAK: it reads only the rows up to and including bar t (the last row of data). These are
    high[t], low[t], volume of bars t-volume_period .. t, and closes of the last vol_lookback + vol_period rows,
    all known at bar t's close.
    """

    def __init__(self, name="VolumeWeightedCloseLocationVolatilityRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.volume_period = int(self.parameters.get("volume_period", 20))
        if self.volume_period < 2:
            raise ValueError(f"volume_period must be >= 2, got {self.volume_period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"vol_period must be >= 2, got {self.vol_period}")
        self.vol_lookback = int(self.parameters.get("vol_lookback", 60))
        if self.vol_lookback < 1:
            raise ValueError(f"vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        nan = float("nan")
        h = float(data["high"].iloc[-1])
        lo = float(data["low"].iloc[-1])
        c_t = float(data["close"].iloc[-1])
        vol = data["volume"].astype(float).to_numpy()
        v_t = vol[-1]
        base = vol[-(self.volume_period + 1):-1]
        n_c = self.vol_lookback + self.vol_period
        c = data["close"].astype(float).to_numpy()[-n_c:]
        if (np.isnan(h) or np.isnan(lo) or np.isnan(c_t) or np.isnan(v_t)
                or np.isnan(base).any() or np.isnan(c).any() or (c <= 0).any()):
            self._raw_value = nan
            self.confidence = 1.0
            return
        rng = h - lo
        loc = 0.5 if rng == 0 else (h - c_t) / rng
        base_mean = float(base.mean())
        if not base_mean > 0:
            self._raw_value = nan
            self.confidence = 1.0
            return
        vr = v_t / base_mean
        r = c[1:] / c[:-1] - 1.0
        s = np.array([np.std(r[k:k + self.vol_period], ddof=1) for k in range(self.vol_lookback)])
        s_mean = float(s.mean())
        if not s_mean > 0:
            self._raw_value = nan
            self.confidence = 1.0
            return
        volr = float(s[-1]) / s_mean
        self._raw_value = float(loc * vr * volr)
        self.confidence = 1.0
        self.debug_info = {"location": loc, "volume_ratio": vr, "volatility_ratio": volr}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.volume_period + 1, self.vol_lookback + self.vol_period)
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("volume_period", 20))
    sp = int(params.get("vol_period", 20))
    L = int(params.get("vol_lookback", 60))
    high = [float(x) for x in list(df["high"])]
    low = [float(x) for x in list(df["low"])]
    close = [float(x) for x in list(df["close"])]
    volume = [float(x) for x in list(df["volume"])]
    t = len(close) - 1

    def isnan(x):
        return x != x

    # location of the close from the bar's high
    if isnan(high[t]) or isnan(low[t]) or isnan(close[t]):
        return float("nan")
    rng = high[t] - low[t]
    if rng == 0:
        loc = 0.5
    else:
        loc = (high[t] - close[t]) / rng

    # volume today against the mean of the prior vp volumes
    if isnan(volume[t]):
        return float("nan")
    total = 0.0
    for i in range(t - vp, t):
        if isnan(volume[i]):
            return float("nan")
        total += volume[i]
    base_mean = total / vp
    if not base_mean > 0:
        return float("nan")
    vr = volume[t] / base_mean

    # closes used: bars t-L-sp+1 .. t
    for i in range(t - L - sp + 1, t + 1):
        if isnan(close[i]) or not close[i] > 0:
            return float("nan")

    def sd_at(i):
        rets = []
        for j in range(i - sp + 1, i + 1):
            rets.append(close[j] / close[j - 1] - 1.0)
        m = sum(rets) / len(rets)
        ss = 0.0
        for x in rets:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (len(rets) - 1))

    svals = []
    for i in range(t - L + 1, t + 1):
        svals.append(sd_at(i))
    s_mean = sum(svals) / len(svals)
    if not s_mean > 0:
        return float("nan")
    volr = sd_at(t) / s_mean

    return loc * vr * volr
```

checks:
VolumeWeightedCloseLocationVolatilityRatioComponent: every check passed
the bot's suite: == 1637 passed, 16 skipped, 75 deselected, 2244 warnings in 79.15s (0:01:19) ===
