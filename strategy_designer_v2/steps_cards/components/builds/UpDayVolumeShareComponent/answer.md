# UpDayVolumeShareComponent: night10_fallcalmlong_run | 089-01_calm-decline-up-volume-share_1d | UpDayVolumeShare

## attempt 1

answer: built
class: UpDayVolumeShareComponent
settings: {"period": 20, "form": "share"}
reason: No component of the catalogue splits a window's volume by the direction of each bar's close-to-close move. `TopVolumesShareComponent` ranks volumes by size and `VolumeRatioComponent` compares volume levels, so a new class computes the up-day volume share. The "centred" form (share − 0.5) needs its own setting because no config step adds a constant (`standardise` does not centre).

table: Regime measures
row: | `UpDayVolumeShareComponent` | `period` (20), `form` ("share") | U / V, where U = sum of volume[i] over i = t-`period`+1 .. t with close[i] > close[i-1], and V = sum of volume[t-`period`+1 .. t], bar t included. `form` "share": U / V. `form` "centred": U / V − 0.5 | "share": 0 to 1, never negative, no direction. It is 0 when no bar of the window closed up and 1 when every bar did, rising as more of the window's volume falls on up bars. "centred": −0.5 to +0.5, signed; positive when more than half the window's volume fell on up bars, negative when less | regime measure | dimensionless (share of the window's volume; "centred": minus 0.5) | `period` + 1 (21) | close (last `period` + 1 rows), volume (last `period` rows). A NaN close or NaN volume among them gives NaN. V not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `form` other than "share" or "centred" | stateless. A flat bar (equal close) counts as not up, and its volume stays in V. The value is continuous in the volumes. It steps when a bar's close crosses its prior close, because that bar's volume moves in or out of U. `form` "share" (default) is the plain share. "centred" subtracts 0.5, which no config step gives, hence the setting. Not `TopVolumesShareComponent`. On 1d bars the defaults give the share of the last 20 days' volume traded on up days. No `scaling_factor`: scale it with transforms |

```python class
class UpDayVolumeShareComponent(SubStrategyComponent):
    """
    Share of the window's volume that fell on up bars:

        U = sum of volume[i] for i = t-period+1 .. t with close[i] > close[i-1]
        V = sum of volume[i] for i = t-period+1 .. t            (bar t included)
        form = "share" (default): raw_value = U / V
        form = "centred":         raw_value = U / V - 0.5

    Range: "share" 0 to 1, never negative, no direction (0 = no up bar in the window, 1 = every bar up);
    "centred" -0.5 to +0.5, signed, positive when more than half the window's volume fell on up bars.
    A flat bar (equal close) is not an up bar; its volume stays in V.
    Warm-up: period + 1 rows (close[t-period] is the base of the first bar's move), bar t included.
    NaN: a NaN close in the last period + 1 rows or a NaN volume in the last period rows gives NaN;
    V not above 0 gives NaN (never on real bars, whose volume is positive).
    Building the component raises for a period below 1 or a form other than "share" or "centred".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows and the `volume`
    column of the last period rows of data, all at or before bar t (the last row); each is known at its
    bar's close.
    """

    def __init__(self, name="UpDayVolumeShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"UpDayVolumeShareComponent: period must be >= 1, got {self.period}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "centred"):
            raise ValueError(f"UpDayVolumeShareComponent: form must be 'share' or 'centred', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.period
        close = data['close'].astype(float).iloc[-(n + 1):].to_numpy()
        vol = data['volume'].astype(float).iloc[-n:].to_numpy()
        if np.isnan(close).any() or np.isnan(vol).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        up = close[1:] > close[:-1]
        total = float(vol.sum())
        if not total > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        up_vol = float(vol[up].sum())
        share = up_vol / total
        self._raw_value = float(share - 0.5) if self.form == "centred" else float(share)
        self.confidence = 1.0
        self.debug_info = {'up_volume': up_vol, 'total_volume': total, 'up_bars': int(up.sum())}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 20))
    form = params.get("form", "share")
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    up_sum = 0.0
    total = 0.0
    for i in range(t - n + 1, t + 1):
        ci = c[i]
        cp = c[i - 1]
        vi = v[i]
        if ci != ci or cp != cp or vi != vi:
            return float("nan")
        total = total + vi
        if ci > cp:
            up_sum = up_sum + vi
    if not total > 0:
        return float("nan")
    share = up_sum / total
    if form == "centred":
        return share - 0.5
    return share
```

checks:
UpDayVolumeShareComponent: every check passed
the bot's suite: = 1686 passed, 16 skipped, 75 deselected, 95636 warnings in 134.63s (0:02:14) ==
