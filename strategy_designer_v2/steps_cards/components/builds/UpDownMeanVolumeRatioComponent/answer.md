# UpDownMeanVolumeRatioComponent: night10_fallcalmlong_run | 089-02_calm-decline-up-down-volume-ratio_1d | UpDownDayMeanVolumeRatio

## attempt 1

answer: built
class: UpDownMeanVolumeRatioComponent
settings: {"period": 20, "form": "ratio"}
reason: `UpDayVolumeShareComponent` gives the up bars' share of the window's total volume. That share moves with how many bars closed up, not only with how heavily each up bar traded against each down bar, so it is a different measure, and no class divides the mean up-bar volume by the mean down-bar volume. The new class computes that ratio, with "log" and "centred" forms that read 0 at equality, which no config step gives.

table: Regime measures
row: | `UpDownMeanVolumeRatioComponent` | `period` (20), `form` ("ratio") | r = mean(volume[i] : close[i] > close[i-1]) / mean(volume[i] : close[i] < close[i-1]), over i = t-`period`+1 .. t, bar t included. `form` "ratio": r. `form` "log": ln(r). `form` "centred": r − 1 | "ratio": above 0, unbounded above, never negative; no direction; 1 when up bars and down bars trade the same mean volume, above 1 as up bars trade heavier per bar. "log": signed, unbounded, 0 at equality. "centred": −1 and up, signed, 0 at equality | graded | "ratio": ratio of mean volumes (up over down). "log": natural log of that ratio. "centred": that ratio minus 1 | `period` + 1 (21) | close (last `period` + 1 rows), volume (last `period` rows). A NaN close or NaN volume among them gives NaN. A window with no up bar or no down bar gives NaN (never on real 1d bars at `period` 20). A mean volume not above 0 also gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `form` other than "ratio", "log" or "centred" | stateless. A flat bar (equal close) is in neither mean. The value is continuous in the volumes. It steps when a bar's close crosses its prior close, because that bar's volume moves between the two means. Not `UpDayVolumeShareComponent`, which is the up bars' share of total volume and so depends on the count of up bars. On 1d bars the defaults give the mean volume of the last 20 days' up days over that of their down days. No `scaling_factor`: scale it with transforms |

```python class
class UpDownMeanVolumeRatioComponent(SubStrategyComponent):
    """
    Mean volume of up bars against mean volume of down bars, over the last `period` bars:

        for i = t-period+1 .. t (bar t included):
            up bar   when close[i] > close[i-1]
            down bar when close[i] < close[i-1]
            a flat bar (equal close) is in neither group
        r = mean(volume of up bars) / mean(volume of down bars)
        form = "ratio" (default): raw_value = r
        form = "log":             raw_value = ln(r)
        form = "centred":         raw_value = r - 1

    Range & sign: "ratio" is above 0 and unbounded above, with no direction. It is 1 when up and down bars
    trade the same mean volume, and above 1 when up bars trade heavier per bar. "log" is signed and 0 at
    equality. "centred" is -1 and up, signed, and 0 at equality. The value is graded and continuous in the
    volumes. It steps when a bar's close crosses its prior close.
    Warm-up: period + 1 rows (closes t-period .. t), bar t included.

    NaN: a NaN close in the last period + 1 rows or a NaN volume in the last period rows gives NaN. A window
    with no up bar or no down bar gives NaN (never on real 1d bars at period 20). A mean volume not above 0
    gives NaN (never on real bars). A missing column raises.
    Building the component raises for a period below 2 or a form other than "ratio", "log" or "centred".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows and the `volume` column
    of the last period rows of data, the last row being bar t. Every value is known at bar t's close.
    """

    def __init__(self, name="UpDownMeanVolumeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 2:
            raise ValueError(f"UpDownMeanVolumeRatioComponent: period must be >= 2, got {self.period}")
        self.form = self.parameters.get("form", "ratio")
        if self.form not in ("ratio", "log", "centred"):
            raise ValueError(
                f"UpDownMeanVolumeRatioComponent: form must be 'ratio', 'log' or 'centred', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        c = data["close"].astype(float).to_numpy()[-(p + 1):]
        v = data["volume"].astype(float).to_numpy()[-p:]
        if np.isnan(c).any() or np.isnan(v).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        ch = c[1:] - c[:-1]
        up = v[ch > 0]
        dn = v[ch < 0]
        if len(up) == 0 or len(dn) == 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            self.debug_info = {"n_up": int(len(up)), "n_down": int(len(dn))}
            return
        mu = float(up.mean())
        md = float(dn.mean())
        if not (mu > 0 and md > 0):
            self._raw_value = float("nan")
        else:
            r = mu / md
            if self.form == "log":
                self._raw_value = float(np.log(r))
            elif self.form == "centred":
                self._raw_value = float(r - 1.0)
            else:
                self._raw_value = float(r)
        self.confidence = 1.0
        self.debug_info = {"mean_up_volume": mu, "mean_down_volume": md,
                           "n_up": int(len(up)), "n_down": int(len(dn))}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 20))
    form = params.get("form", "ratio")
    close = [float(x) for x in list(df["close"])]
    vol = [float(x) for x in list(df["volume"])]
    t = len(close) - 1
    up_sum = 0.0
    up_n = 0
    dn_sum = 0.0
    dn_n = 0
    for i in range(t - p + 1, t + 1):
        a = close[i - 1]
        b = close[i]
        w = vol[i]
        if a != a or b != b or w != w:
            return float("nan")
        if b > a:
            up_sum += w
            up_n += 1
        elif b < a:
            dn_sum += w
            dn_n += 1
    if up_n == 0 or dn_n == 0:
        return float("nan")
    mu = up_sum / up_n
    md = dn_sum / dn_n
    if not (mu > 0 and md > 0):
        return float("nan")
    r = mu / md
    if form == "log":
        return math.log(r)
    if form == "centred":
        return r - 1.0
    return r
```

checks:
UpDownMeanVolumeRatioComponent: every check passed
the bot's suite: = 1687 passed, 16 skipped, 75 deselected, 95636 warnings in 131.84s (0:02:11) ==
