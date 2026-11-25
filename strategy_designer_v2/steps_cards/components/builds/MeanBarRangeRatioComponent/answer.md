# MeanBarRangeRatioComponent: night7c_panic_run | 032-02.b2.d2_graded-monthly-low-rebound_1d | mean bar range width ratio

## attempt 1

answer: built
class: MeanBarRangeRatioComponent
settings: {"long_period": 365, "short_period": 30, "form": "inverse"}
reason: The wish is the reciprocal, Q / L, of `MeanBarRangeRatioComponent`'s L / Q. That is the same measure of recent bar width against the long average, and no config step turns a value into its reciprocal. So the existing class gets a `form` setting: its default "ratio" keeps today's output exactly, and "inverse" gives Q / L.

table: Regime measures
row: | `MeanBarRangeRatioComponent` | `long_period` (360), `short_period` (42), `form` ("ratio") | L = mean(high[i] − low[i]) over the last `long_period` bars, and Q = the same mean over the last `short_period` bars, bar t included in both. `form` "ratio": L / Q. `form` "inverse": Q / L | "ratio": `short_period`/`long_period` (0.117 at the defaults) and up, unbounded above, never negative; no direction; 1 when the recent bars are as wide as the long average, above 1 as they get quieter, below 1 as they get wider. "inverse": 0 and up, at most `long_period`/`short_period` (the short window lies inside the long one), never negative; no direction; 1 at equal width, above 1 as recent bars widen, below 1 as they quieten | regime measure | dimensionless (ratio of mean bar ranges) | `long_period` (360) | high, low. A NaN high or low in the last `long_period` rows gives NaN. With "ratio", Q = 0 (`short_period` zero-range bars in a row, never seen on real bars) gives NaN. With "inverse", L = 0 (`long_period` zero-range bars, never seen on real bars) gives NaN. These settings raise when the component is built: `short_period` < 1, `short_period` >= `long_period`, `form` other than "ratio" or "inverse" | stateless; graded and continuous in the highs and lows. `form` "ratio" (default) is the original output, unchanged. "inverse" is its reciprocal, recent width over the long average, which grows as recent ranges widen; no config step gives a reciprocal, hence the setting. "ratio" is the L / Q factor of `NarrowRangeBreakoutRangeRatioComponent` (`ratio_long_period`, `ratio_short_period`) on its own. On 1d bars, `long_period` 365, `short_period` 30 and "inverse" give the 30-day mean daily range over the past year's. No `scaling_factor`: scale it with transforms |

```python class
class MeanBarRangeRatioComponent(SubStrategyComponent):
    """
    Mean bar range over a long window against the same mean over a short window, on every bar:

        L = mean(high[i] - low[i]) for i = t-long_period+1 .. t     (bar t included)
        Q = mean(high[i] - low[i]) for i = t-short_period+1 .. t    (bar t included)
        form = "ratio" (default): raw_value = L / Q
        form = "inverse":         raw_value = Q / L

    Range and sign: "ratio" is short_period/long_period and up, unbounded above, never negative, no direction; it is
    1 at equal width and rises as the recent bars get quieter. "inverse" is 0 and up, at most long_period/short_period
    (the short window lies inside the long one), never negative, no direction; it is 1 when the recent bars are as
    wide as the long average and grows as they widen. Graded, continuous in the highs and lows.
    form "ratio" is the original output, unchanged.
    Warm-up: long_period rows, bar t included.
    NaN: a NaN high or low in the last long_period rows gives NaN. With "ratio", Q = 0 gives NaN. With "inverse",
    L = 0 gives NaN. Neither zero is ever seen on real bars.
    Building the component raises for a short_period below 1, a short_period >= long_period, or a form other than
    "ratio" or "inverse".

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the last long_period rows of data, ending at
    bar t (the last row); a bar's high and low are known at that bar's close.
    """

    def __init__(self, name="MeanBarRangeRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.long_period = int(self.parameters.get("long_period", 360))
        self.short_period = int(self.parameters.get("short_period", 42))
        if self.short_period < 1:
            raise ValueError(f"MeanBarRangeRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"MeanBarRangeRatioComponent: short_period must be < long_period, got "
                f"{self.short_period} >= {self.long_period}")
        self.form = self.parameters.get("form", "ratio")
        if self.form not in ("ratio", "inverse"):
            raise ValueError(f"MeanBarRangeRatioComponent: form must be 'ratio' or 'inverse', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).iloc[-self.long_period:]
        low = data['low'].astype(float).iloc[-self.long_period:]
        rng = (high - low).to_numpy()
        if np.isnan(rng).any():
            self._raw_value = float("nan")
        else:
            L = float(np.mean(rng))
            Q = float(np.mean(rng[-self.short_period:]))
            if self.form == "inverse":
                self._raw_value = float(Q / L) if L != 0 else float("nan")
            else:
                self._raw_value = float(L / Q) if Q != 0 else float("nan")
            self.debug_info = {'long_mean_range': L, 'short_mean_range': Q, 'form': self.form}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.long_period
```

```python hand
def hand(df, params):
    lp = int(params.get("long_period", 360))
    sp = int(params.get("short_period", 42))
    form = params.get("form", "ratio")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(h) - 1
    long_sum = 0.0
    short_sum = 0.0
    for k in range(lp):
        hi = h[t - k]
        lo = l[t - k]
        if hi != hi or lo != lo:
            return float("nan")
        r = hi - lo
        long_sum = long_sum + r
        if k < sp:
            short_sum = short_sum + r
    L = long_sum / lp
    Q = short_sum / sp
    if form == "inverse":
        if L == 0:
            return float("nan")
        return Q / L
    if Q == 0:
        return float("nan")
    return L / Q
```

checks:
MeanBarRangeRatioComponent: every check passed
the bot's suite: == 1657 passed, 16 skipped, 75 deselected, 2244 warnings in 100.40s (0:01:40) ==
