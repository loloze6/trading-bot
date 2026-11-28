# DownDayVolumeShareComponent: night10_fallcalmshort_run | 086-01_down-day-volume-share-drift_1d | DownDayVolumeShareComponent

## attempt 1

answer: built
class: DownDayVolumeShareComponent
settings: {"period": 10, "form": "share"}
reason: No component in the catalogue splits volume by the sign of the bar's close-to-close move. `TopVolumesShareComponent` ranks volumes by size, and `VolumeWeightedCloseLocationComponent` weights the close location within a single bar. The share of the window's volume carried by down closes is a new measure, so it gets a new class. The centred form (share − 0.5) adds a constant, which no config step does (`standardise` does not centre), so it is a `form` setting on the same class.

table: Regime measures
row: | `DownDayVolumeShareComponent` | `period` (10), `form` ("share") | D / V, where D = sum of volume[i] over i = t-`period`+1 .. t with close[i] < close[i-1], and V = sum of volume[i] over i = t-`period`+1 .. t (bar t included). `form` "share": D / V. `form` "centred": D / V − 0.5 | "share": 0 to 1, never negative, no direction. It is 0 when no bar of the window closed down, 1 when every bar did, and rises as more of the window's volume falls on down closes. "centred": −0.5 to +0.5, signed: positive when down-close volume carries more than half, 0 when balanced, negative when it carries less | graded | "share": dimensionless (share of the window's volume). "centred": that share minus 0.5 | `period` + 1 (11) | close (last `period` + 1 rows), volume (last `period` rows). A NaN close or a NaN volume among those gives NaN. A total volume not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `form` other than "share" or "centred" | stateless. A flat bar (equal close) is not a down bar: its volume counts only in the total. The value is continuous in the volumes. It steps where a bar's close crosses the prior close, because that bar's volume then enters or leaves D. The comparison for bar t-`period`+1 reads close[t-`period`], one row before the volume window. On 1d bars the defaults give the share of the last 10 days' volume traded on down closes. No config step adds a constant, hence the "centred" setting. No `scaling_factor`: scale it with transforms |

```python class
class DownDayVolumeShareComponent(SubStrategyComponent):
    """
    Share of the window's volume traded on bars that closed down, on every bar:

        window = bars t - period + 1 .. t                    (bar t included)
        D = sum(volume[i] for i in window if close[i] < close[i-1])
        V = sum(volume[i] for i in window)
        form = "share" (default): raw_value = D / V
        form = "centred":         raw_value = D / V - 0.5

    Range: "share" 0 to 1, never negative, no direction (0 when no bar of the window closed down, 1 when every
    bar did). "centred" -0.5 to +0.5, signed: positive when down-close volume dominates, 0 when balanced.
    A flat bar (close[i] == close[i-1]) is not a down bar; its volume counts in V only.
    Graded: continuous in the volumes; it steps where a close crosses the prior close.
    Warm-up: period + 1 rows (the down test for bar t-period+1 reads close[t-period]).

    NaN: a NaN close among the last period + 1 rows, or a NaN volume among the last period rows, gives NaN.
    A total volume V not above 0 gives NaN (never on real bars).
    Building the component raises for a period below 1 or a form other than "share" or "centred".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows and the `volume` column of
    the last period rows of data, all at or before bar t (the last row); each is known at that bar's close.
    """

    def __init__(self, name="DownDayVolumeShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters.get("period", 10)
        try:
            p_int = int(p)
        except (TypeError, ValueError):
            raise ValueError(f"DownDayVolumeShareComponent: period must be an integer >= 1, got {p!r}")
        if p_int != p or p_int < 1:
            raise ValueError(f"DownDayVolumeShareComponent: period must be an integer >= 1, got {p!r}")
        self.period = p_int
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "centred"):
            raise ValueError(f"DownDayVolumeShareComponent: form must be 'share' or 'centred', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.period
        close = data['close'].astype(float).to_numpy()[-(n + 1):]
        vol = data['volume'].astype(float).to_numpy()[-n:]
        if np.isnan(close).any() or np.isnan(vol).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        down = close[1:] < close[:-1]
        total = float(vol.sum())
        if not total > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        down_vol = float(vol[down].sum())
        share = down_vol / total
        self._raw_value = float(share - 0.5) if self.form == "centred" else float(share)
        self.confidence = 1.0
        self.debug_info = {'down_volume': down_vol, 'total_volume': total,
                           'down_bars': int(down.sum()), 'form': self.form}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 10))
    form = params.get("form", "share")
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    down_total = 0.0
    total = 0.0
    for i in range(t - n + 1, t + 1):
        ci = c[i]
        cp = c[i - 1]
        vi = v[i]
        if ci != ci or cp != cp or vi != vi:
            return float("nan")
        total = total + vi
        if ci < cp:
            down_total = down_total + vi
    if not total > 0:
        return float("nan")
    share = down_total / total
    if form == "centred":
        return share - 0.5
    return share
```

checks:
DownDayVolumeShareComponent: every check passed
the bot's suite: = 1686 passed, 16 skipped, 75 deselected, 95636 warnings in 162.66s (0:02:42) ==
