# UpDayVolumeShareComponent: night10_fallcalmlong_run | 089-04.c1_heavy-up-day-volume-rebounds_1d | UpDayVolumeToUsualVolumeComponent

## attempt 1

answer: built
class: UpDayVolumeShareComponent
settings: {"period": 20, "base": "mean_volume", "base_period": 60}
reason: `UpDayVolumeShareComponent` already sums the volume of the up bars among the last `period` bars, but it divides that sum by the same window's total volume. The wish divides the same sum by the mean volume of the last `base_period` bars. That is the same measure against another base, so the base becomes a setting. Its default ("window") keeps today's output unchanged.

table: Regime measures
row: | `UpDayVolumeShareComponent` | `period` (20), `form` ("share"), `base` ("window"), `base_period` (60) | U / D, where U = sum of volume[i] over i = t-`period`+1 .. t with close[i] > close[i-1]. `base` "window": D = sum of volume[t-`period`+1 .. t], bar t included. `form` "share": U / D. `form` "centred": U / D − 0.5. `base` "mean_volume": D = mean(volume[t-`base_period`+1 .. t]), bar t included, and the output is U / D. With `period` 20, "mean_volume" and `base_period` 60: (sum of the up days' volume over days t-19 .. t) / mean(volume[t-59 .. t]) | "window", "share": 0 to 1, never negative, no direction. It is 0 when no bar of the window closed up and 1 when every bar did. "window", "centred": −0.5 to +0.5, signed. "mean_volume": 0 and up, never negative, no direction. It is 0 when no up day is in the window and grows as the up days carry more volume against usual volume. It is at most `base_period` when `base_period` >= `period` (the base then holds every bar of the window), 60 at the wished settings | regime measure | "window": share of the window's volume ("centred": minus 0.5). "mean_volume": mean bar volumes (usual daily volumes on 1d bars) | `period` + 1 (21) with "window"; max(`period` + 1, `base_period`) with "mean_volume" (60 at the wished settings) | close (last `period` + 1 rows), volume (last `period` rows; last max(`period`, `base_period`) rows with "mean_volume"). A NaN close or NaN volume among the rows read gives NaN. A D not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `form` other than "share" or "centred", `base` other than "window" or "mean_volume", `base_period` < 1, `form` "centred" with `base` "mean_volume" | stateless. `base` "window" (default) is the original output, unchanged, and `base_period` is read only by "mean_volume". "mean_volume" is the up days' summed volume counted in usual bar volumes. Unlike the share, it grows with the number of up days and with how heavy they trade. A flat bar (equal close) counts as not up. The value is continuous in the volumes. It steps when a bar's close crosses its prior close, because that bar's volume moves in or out of U. Not `UpDownMeanVolumeRatioComponent`. On 1d bars the wished settings give the volume traded on up days over the last 20 days, in 60-day mean daily volumes. No `scaling_factor`: scale it with transforms |

```python class
class UpDayVolumeShareComponent(SubStrategyComponent):
    """
    Volume traded on up bars, against a volume base, on every bar:

        U = sum of volume[i] over i = t-period+1 .. t with close[i] > close[i-1]   (bar t included)
        base = "window" (default):  D = sum of volume[t-period+1 .. t]
        base = "mean_volume":       D = mean(volume[t-base_period+1 .. t])          (bar t included)
        form = "share" (default):   raw_value = U / D
        form = "centred":           raw_value = U / D - 0.5   (only with base "window")

    base "window" with either form is the original output, unchanged; base_period is read only by
    "mean_volume".
    Range: "window"/"share" is 0 to 1 and "window"/"centred" is -0.5 to +0.5. "mean_volume" is 0 and up,
    never negative, with no direction: 0 when no bar of the window closed up, and at most base_period when
    base_period >= period. It grows as the up bars carry more volume against the usual bar volume.
    A flat bar (equal close) is not an up bar.
    Warm-up: period + 1 rows ("window"); max(period + 1, base_period) rows ("mean_volume"), bar t included.
    NaN: a NaN close among the last period + 1 rows, or a NaN volume among the volume rows read, gives NaN.
    A D not above 0 gives NaN (never on real bars).
    Building the component raises for a period below 1, a form other than "share" or "centred", a base
    other than "window" or "mean_volume", a base_period below 1, and form "centred" with base "mean_volume".

    WHY THIS CANNOT LEAK: it reads only the `close` and `volume` columns of the last
    max(period + 1, base_period) rows of data, the last of which is bar t; no later row is ever read.
    """

    def __init__(self, name="UpDayVolumeShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"UpDayVolumeShareComponent: period must be >= 1, got {self.period}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "centred"):
            raise ValueError(f"UpDayVolumeShareComponent: form must be 'share' or 'centred', got {self.form!r}")
        self.base = self.parameters.get("base", "window")
        if self.base not in ("window", "mean_volume"):
            raise ValueError(
                f"UpDayVolumeShareComponent: base must be 'window' or 'mean_volume', got {self.base!r}")
        self.base_period = int(self.parameters.get("base_period", 60))
        if self.base_period < 1:
            raise ValueError(f"UpDayVolumeShareComponent: base_period must be >= 1, got {self.base_period}")
        if self.base == "mean_volume" and self.form == "centred":
            raise ValueError("UpDayVolumeShareComponent: form 'centred' applies only to base 'window'")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        close = data["close"].astype(float).to_numpy()
        vol = data["volume"].astype(float).to_numpy()
        c = close[-(p + 1):]
        v = vol[-p:]
        if np.isnan(c).any() or np.isnan(v).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        up = c[1:] > c[:-1]
        U = float(v[up].sum())
        if self.base == "mean_volume":
            b = vol[-self.base_period:]
            if np.isnan(b).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            D = float(b.mean())
        else:
            D = float(v.sum())
        if not D > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(U / D - (0.5 if self.form == "centred" else 0.0))
        self.confidence = 1.0
        self.debug_info = {"up_volume": U, "base": D, "up_bars": int(up.sum())}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "mean_volume":
            return max(self.period + 1, self.base_period)
        return self.period + 1
```

```python hand
def hand(df, params):
    p = int(params.get("period", 20))
    form = params.get("form", "share")
    base = params.get("base", "window")
    bp = int(params.get("base_period", 60))
    closes = [float(x) for x in list(df["close"])]
    vols = [float(x) for x in list(df["volume"])]
    t = len(closes) - 1
    # up-day volume over bars t-p+1 .. t
    U = 0.0
    total = 0.0
    for i in range(t - p + 1, t + 1):
        ci = closes[i]
        cp = closes[i - 1]
        vi = vols[i]
        if ci != ci or cp != cp or vi != vi:
            return float("nan")
        total += vi
        if ci > cp:
            U += vi
    if base == "mean_volume":
        s = 0.0
        for i in range(t - bp + 1, t + 1):
            if vols[i] != vols[i]:
                return float("nan")
            s += vols[i]
        D = s / bp
    else:
        D = total
    if not D > 0:
        return float("nan")
    val = U / D
    if form == "centred":
        val -= 0.5
    return val
```

checks:
UpDayVolumeShareComponent: every check passed
the bot's suite: = 1688 passed, 16 skipped, 75 deselected, 95636 warnings in 138.40s (0:02:18) ==
