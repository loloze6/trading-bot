# DownBarVolumeFadeComponent: night10_fallcalmlong_run | 089-03_calm-decline-thinning-down-volume_1d | DownDayVolumeFadeRatio

## attempt 1

answer: built
class: DownBarVolumeFadeComponent
settings: {"short_period": 10, "base_period": 20}
reason: No catalogue component compares the mean volume of down bars in a recent window with the mean volume of down bars in an earlier, adjacent window. `UpDownMeanVolumeRatioComponent` sets up bars against down bars in one window, `DownStreakVolumeFadeComponent` reads only the current streak, and `VolumeRatioComponent` counts every bar. One new class computes this ln ratio.

table: Regime measures
row: | `DownBarVolumeFadeComponent` | `short_period` (10), `base_period` (20) | ln(B / A). A = mean(volume[i]) over the bars i in t-`short_period`+1 .. t with close[i] < close[i-1]. B = the same mean over the bars i in t-`short_period`-`base_period`+1 .. t-`short_period`. 0.0 when either window has no down bar. At the wished settings: A over bars t-9 .. t, B over bars t-29 .. t-10 | unbounded, signed. 0 when the two down-bar means are equal (and when a window has no down bar). Positive and growing as the recent down bars get lighter than the earlier ones, negative as they get heavier | regime measure | natural log of a volume ratio (earlier down-bar mean over recent down-bar mean) | `short_period` + `base_period` + 1 (31) | close (last `short_period` + `base_period` + 1 rows), volume (last `short_period` + `base_period` rows). A NaN close or a NaN volume among them gives NaN. A down-bar mean volume not above 0 gives NaN (never on real bars). A window with no down bar reads 0.0, which is rare on real 1d bars for the 10-bar window. These settings raise when the component is built: `short_period` < 1, `base_period` < 1 | stateless. The two windows are adjacent and do not overlap. A flat bar (equal close) is not a down bar, so its volume is in neither mean. Continuous in the volumes. It steps when a bar's close crosses its prior close, because that bar's volume moves in or out of a mean. Not `UpDownMeanVolumeRatioComponent` (up against down in one window) and not `DownStreakVolumeFadeComponent` (the current streak only). On 1d bars the defaults give the mean down-day volume of days t-29 .. t-10 over that of the last 10 days, in log. No `scaling_factor`: scale it with transforms |

```python class
class DownBarVolumeFadeComponent(SubStrategyComponent):
    """
    How the volume of down bars has changed from an earlier window to a recent one:

        down bar i: close[i] < close[i-1]
        recent window: bars t-short_period+1 .. t          (bar t included)
        base window:   bars t-short_period-base_period+1 .. t-short_period
        A = mean(volume[i]) over the down bars of the recent window
        B = mean(volume[i]) over the down bars of the base window
        raw_value = ln(B / A); 0.0 when either window holds no down bar

    At the defaults (short_period 10, base_period 20): A over bars t-9 .. t, B over bars t-29 .. t-10.
    Range: unbounded, signed. It is 0 when the two means are equal. It is positive and grows as the recent down bars
    get lighter than the earlier ones, and negative as they get heavier. A flat bar is not a down bar.
    Warm-up: short_period + base_period + 1 rows, bar t included (the first base bar needs its prior close).

    NaN: a NaN close in the last short_period + base_period + 1 rows, or a NaN volume in the last
    short_period + base_period rows, gives NaN. A down-bar mean volume not above 0 gives NaN (never on real bars).
    Building the component raises for a short_period or base_period below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` and `volume` columns of the rows up to and including bar t (the
    last row of data), over at most the last short_period + base_period + 1 rows; each is known at its bar's close.
    """

    def __init__(self, name="DownBarVolumeFade", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 10))
        if self.short_period < 1:
            raise ValueError(f"DownBarVolumeFadeComponent: short_period must be >= 1, got {self.short_period}")
        self.base_period = int(self.parameters.get("base_period", 20))
        if self.base_period < 1:
            raise ValueError(f"DownBarVolumeFadeComponent: base_period must be >= 1, got {self.base_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = len(data)
        w = self.short_period + self.base_period
        close = data['close'].astype(float).to_numpy()[n - w - 1:]
        vol = data['volume'].astype(float).to_numpy()[n - w:]
        if np.isnan(close).any() or np.isnan(vol).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        # position k in vol corresponds to close index k + 1 (its prior close is close[k])
        down = close[1:] < close[:-1]
        base_mask = down[:self.base_period]
        recent_mask = down[self.base_period:]
        base_vol = vol[:self.base_period]
        recent_vol = vol[self.base_period:]
        if not base_mask.any() or not recent_mask.any():
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {'recent_down_bars': int(recent_mask.sum()), 'base_down_bars': int(base_mask.sum())}
            return
        a = float(recent_vol[recent_mask].mean())
        b = float(base_vol[base_mask].mean())
        if not a > 0 or not b > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(np.log(b / a))
        self.confidence = 1.0
        self.debug_info = {'recent_down_mean_volume': a, 'base_down_mean_volume': b,
                           'recent_down_bars': int(recent_mask.sum()), 'base_down_bars': int(base_mask.sum())}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.short_period + self.base_period + 1
```

```python hand
def hand(df, params):
    import math
    s = int(params.get("short_period", 10))
    b = int(params.get("base_period", 20))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    # closes read: bars t-s-b .. t; volumes read: bars t-s-b+1 .. t
    for i in range(t - s - b, t + 1):
        if c[i] != c[i]:
            return float("nan")
    for i in range(t - s - b + 1, t + 1):
        if v[i] != v[i]:
            return float("nan")
    recent = []
    for i in range(t - s + 1, t + 1):
        if c[i] < c[i - 1]:
            recent.append(v[i])
    base = []
    for i in range(t - s - b + 1, t - s + 1):
        if c[i] < c[i - 1]:
            base.append(v[i])
    if len(recent) == 0 or len(base) == 0:
        return 0.0
    a_mean = sum(recent) / len(recent)
    b_mean = sum(base) / len(base)
    if not a_mean > 0 or not b_mean > 0:
        return float("nan")
    return math.log(b_mean / a_mean)
```

checks:
DownBarVolumeFadeComponent: every check passed
the bot's suite: = 1688 passed, 16 skipped, 75 deselected, 95636 warnings in 136.57s (0:02:16) ==
