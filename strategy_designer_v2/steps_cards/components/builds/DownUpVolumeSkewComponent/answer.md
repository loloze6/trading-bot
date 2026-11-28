# DownUpVolumeSkewComponent: night10_fallcalmshort_run | 086-02_down-up-volume-ratio-drift_1d | DownUpVolumeSkewComponent

## attempt 1

answer: built
class: DownUpVolumeSkewComponent
settings: {"period": 20, "form": "centred"}
reason: No catalogue component compares the mean volume of down closes with the mean volume of up closes. `DownDayVolumeShareComponent` is the down-close share of the window's total volume, so it mixes in how many days fell and is not this ratio of averages. A new class computes the ratio, minus 1 (`form` "centred") or its natural log (`form` "log").

table: Regime measures
row: | `DownUpVolumeSkewComponent` | `period` (20), `form` ("centred") | r = mean(volume[i] : close[i] < close[i-1]) / mean(volume[i] : close[i] > close[i-1]) over i = t-`period`+1 .. t (bar t included). `form` "centred": r − 1. `form` "log": ln(r). 0.0 when the window has no down bar or no up bar | "centred": −1 and up, unbounded above, signed. "log": unbounded, signed. Both are 0 when the two means are equal, positive when down-close bars carry heavier volume than up-close bars, and negative when they carry lighter volume. Both grow as down days get heavier and up days thinner | graded | "centred": ratio of mean volumes minus 1. "log": natural log of that ratio | `period` + 1 (21) | close (last `period` + 1 rows), volume (last `period` rows). A NaN close or a NaN volume among those gives NaN. A mean up-bar volume not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `form` other than "centred" or "log" | stateless. A flat bar (equal close) is in neither mean. A window without both a down and an up bar reads 0.0, a neutral reading, since no comparison exists; on real 1d bars this needs `period` one-sided closes in a row. The value is continuous in the volumes. It steps where a bar's close crosses the prior close, because that bar's volume then changes side. The comparison for bar t-`period`+1 reads close[t-`period`], one row before the volume window. Not `DownDayVolumeShareComponent`, which is a share of total volume and depends on the count of down days. No `scaling_factor`: scale it with transforms |

```python class
class DownUpVolumeSkewComponent(SubStrategyComponent):
    """
    Mean down-close volume against mean up-close volume over the last `period` bars:

        for i = t-period+1 .. t (bar t included):
            bar i is down when close[i] < close[i-1], up when close[i] > close[i-1] (a flat bar is neither)
        Dm = mean(volume[i] over the down bars), Um = mean(volume[i] over the up bars)
        r = Dm / Um
        form = "centred" (default): raw_value = r - 1
        form = "log":               raw_value = ln(r)
        raw_value = 0.0 when the window has no down bar or no up bar (no comparison: neutral)

    Range and sign: "centred" is -1 and up, unbounded above; "log" is unbounded. Both are signed and are 0 when
    the two means are equal. They are positive when down days carry heavier volume than up days, negative when
    they carry lighter volume, and grow as down days get heavier and up days thinner. Graded: continuous in the
    volumes; it steps only where a close crosses the prior close.
    Warm-up: period + 1 rows (the close before the first window bar is needed for its direction).

    NaN: a NaN close among the last period + 1 rows, or a NaN volume among the last period rows, gives NaN.
    A mean up-bar volume not above 0 gives NaN (never on real bars, where volume is always positive).
    Building the component raises for a period below 2, or a form other than "centred" or "log".

    WHY THIS CANNOT LEAK: it reads only the close of the last period + 1 rows and the volume of the last period
    rows of data, the last row being bar t; every value is known at bar t's close.
    """

    def __init__(self, name="DownUpVolumeSkew", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 2:
            raise ValueError(f"DownUpVolumeSkewComponent: period must be >= 2, got {self.period}")
        self.form = self.parameters.get("form", "centred")
        if self.form not in ("centred", "log"):
            raise ValueError(f"DownUpVolumeSkewComponent: form must be 'centred' or 'log', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        closes = data["close"].astype(float).to_numpy()[-(p + 1):]
        vols = data["volume"].astype(float).to_numpy()[-p:]
        if np.isnan(closes).any() or np.isnan(vols).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        cur = closes[1:]
        prev = closes[:-1]
        down = vols[cur < prev]
        up = vols[cur > prev]
        if len(down) == 0 or len(up) == 0:
            value = 0.0
        else:
            dm = float(down.mean())
            um = float(up.mean())
            if not um > 0:
                value = float("nan")
            else:
                r = dm / um
                if self.form == "log":
                    value = float(np.log(r)) if r > 0 else float("nan")
                else:
                    value = float(r - 1.0)
        self._raw_value = value
        self.confidence = 1.0
        self.debug_info = {"down_bars": int(len(down)), "up_bars": int(len(up)), "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("period", 20))
    form = params.get("form", "centred")
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    # bars i = t-n+1 .. t, each compared with close[i-1]
    for i in range(t - n, t + 1):
        if c[i] != c[i]:
            return float("nan")
    for i in range(t - n + 1, t + 1):
        if v[i] != v[i]:
            return float("nan")
    down_sum, down_cnt, up_sum, up_cnt = 0.0, 0, 0.0, 0
    for i in range(t - n + 1, t + 1):
        if c[i] < c[i - 1]:
            down_sum += v[i]
            down_cnt += 1
        elif c[i] > c[i - 1]:
            up_sum += v[i]
            up_cnt += 1
    if down_cnt == 0 or up_cnt == 0:
        return 0.0
    dm = down_sum / down_cnt
    um = up_sum / up_cnt
    if not um > 0:
        return float("nan")
    r = dm / um
    if form == "log":
        if not r > 0:
            return float("nan")
        return math.log(r)
    return r - 1.0
```

checks:
DownUpVolumeSkewComponent: every check passed
the bot's suite: = 1687 passed, 16 skipped, 75 deselected, 95636 warnings in 189.16s (0:03:09) ==
