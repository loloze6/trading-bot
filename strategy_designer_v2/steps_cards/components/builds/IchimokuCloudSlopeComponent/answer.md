# IchimokuCloudSlopeComponent: night3_ichimoku_run | 021-02_below-falling-cloud-continues-down.b1_slow-cloud-fall-continues_1d | CloudFallGentlenessComponent

## attempt 1

answer: built
class: IchimokuCloudSlopeComponent
settings: {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "lookback": 26, "form": "proximity"}
reason: The wished value 1 / (1 + D) is the same measure as the slope of `IchimokuCloudSlopeComponent` (the change of the cloud mid level over `lookback` bars), read as a proximity to a flat-or-rising cloud, the way `DistanceFromHighComponent` offers its distance as a proximity. No config step gives 1 / (1 + max(0, −x)), so the class is written again with a `form` setting whose default "percent" keeps today's output exactly.

table: Directional components
row: | `IchimokuCloudSlopeComponent` | `tenkan_period` (9), `kijun_period` (26), `senkou_period` (52), `displacement` (26), `lookback` (26), `form` ("percent") | S = (C(t) - C(t-`lookback`)) / C(t-`lookback`) x 100, C(i) = (A(i) + B(i)) / 2. With e = i - `displacement` and M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2: A(i) = (M(`tenkan_period`) + M(`kijun_period`)) / 2 and B(i) = M(`senkou_period`). These are the leading spans plotted at bar i, computed from bars ending `displacement` bars earlier. `form` "percent": S. `form` "proximity": 1 / (1 + D), D = max(0, -S) | "percent": -100 and up, unbounded above, signed; positive while the cloud's mid level rises, negative while it falls. "proximity": above 1/101, up to 1, never negative; no direction; 1 when the cloud is flat or rising, shrinking toward 0 the faster it falls over `lookback` bars | graded | "percent": percent over `lookback` bars. "proximity": dimensionless (0 to 1) | max(`tenkan_period`, `kijun_period`, `senkou_period`) + `displacement` + `lookback` (104) | high, low only. A NaN high or low in any window used for C(t) or C(t-`lookback`) gives NaN; a C(t-`lookback`) not above 0 gives NaN (never on real bars). These settings raise when the component is built: any period < 1, `displacement` < 0, `lookback` < 1, `form` other than "percent" or "proximity" | stateless; the cloud at bar t uses no bar after t-`displacement`. `form` "percent" (default) is the original output, unchanged. "proximity" is 1 / (1 + the cloud's fall in percent), which no config step gives; it grows as the fall slows, and `standardise` then `negate` gives a short that grows as the fall slows. No `scaling_factor`: scale it with transforms |

```python class
class IchimokuCloudSlopeComponent(SubStrategyComponent):
    """
    The slope of the Ichimoku cloud's mid level over `lookback` bars, on every bar:

        for a bar i, e = i - displacement and
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A(i) = (M(tenkan_period) + M(kijun_period)) / 2,  B(i) = M(senkou_period)
        C(i) = (A(i) + B(i)) / 2                       (the leading spans plotted at bar i)
        S = (C(t) - C(t - lookback)) / C(t - lookback) x 100
        form = "percent" (default):  raw_value = S
        form = "proximity":          raw_value = 1 / (1 + D),  D = max(0, -S)

    Range and sign. With "percent" the value is -100 and up, unbounded above, and signed. It is positive while the
    cloud's mid level rises, negative while it falls. With "proximity" it runs above 1/101 up to 1 and is never
    negative. It is 1 when the cloud is flat or rising and shrinks toward 0 as the cloud falls faster. Graded, and
    continuous in the highs and lows. The default "percent" is the original output, unchanged.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement + lookback rows, bar t included.

    NaN: a NaN high or low in any window used for C(t) or C(t - lookback) gives NaN. A C(t - lookback) not above 0
    gives NaN, which never happens on real bars.
    Building the component raises for any period below 1, a displacement below 0, a lookback below 1, or a form
    other than "percent" or "proximity".

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of rows up to bar t - displacement (the last
    row of data is bar t), over windows ending at bars t - displacement and t - lookback - displacement; it never
    reads a row after bar t.
    """

    def __init__(self, name="IchimokuCloudSlope", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        for label, p in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                         ("senkou_period", self.senkou_period)):
            if p < 1:
                raise ValueError(f"IchimokuCloudSlopeComponent: {label} must be >= 1, got {p}")
        self.displacement = int(self.parameters.get("displacement", 26))
        if self.displacement < 0:
            raise ValueError(f"IchimokuCloudSlopeComponent: displacement must be >= 0, got {self.displacement}")
        self.lookback = int(self.parameters.get("lookback", 26))
        if self.lookback < 1:
            raise ValueError(f"IchimokuCloudSlopeComponent: lookback must be >= 1, got {self.lookback}")
        self.form = self.parameters.get("form", "percent")
        if self.form not in ("percent", "proximity"):
            raise ValueError(
                f"IchimokuCloudSlopeComponent: form must be 'percent' or 'proximity', got {self.form!r}")
        self._raw_value = 0.0

    @staticmethod
    def _mid(high, low, e, p):
        h = high[e - p + 1:e + 1]
        l = low[e - p + 1:e + 1]
        if np.isnan(h).any() or np.isnan(l).any():
            return float("nan")
        return (float(np.max(h)) + float(np.min(l))) / 2.0

    def _cloud_mid(self, high, low, i):
        e = i - self.displacement
        m_t = self._mid(high, low, e, self.tenkan_period)
        m_k = self._mid(high, low, e, self.kijun_period)
        m_s = self._mid(high, low, e, self.senkou_period)
        a = (m_t + m_k) / 2.0
        return (a + m_s) / 2.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        t = len(high) - 1
        c_now = self._cloud_mid(high, low, t)
        c_then = self._cloud_mid(high, low, t - self.lookback)
        if np.isnan(c_now) or np.isnan(c_then) or not c_then > 0:
            self._raw_value = float("nan")
        else:
            s = (c_now - c_then) / c_then * 100.0
            if self.form == "proximity":
                d = max(0.0, -s)
                self._raw_value = float(1.0 / (1.0 + d))
            else:
                self._raw_value = float(s)
        self.confidence = 1.0
        self.debug_info = {'cloud_mid_now': c_now, 'cloud_mid_then': c_then, 'form': self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement + self.lookback
```

```python hand
def hand(df, params):
    tp = int(params.get("tenkan_period", 9))
    kp = int(params.get("kijun_period", 26))
    sp = int(params.get("senkou_period", 52))
    disp = int(params.get("displacement", 26))
    lb = int(params.get("lookback", 26))
    form = params.get("form", "percent")
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(highs) - 1

    def midpoint(end, p):
        top = None
        bot = None
        j = end - p + 1
        while j <= end:
            h = highs[j]
            l = lows[j]
            if h != h or l != l:
                return float("nan")
            if top is None or h > top:
                top = h
            if bot is None or l < bot:
                bot = l
            j = j + 1
        return (top + bot) / 2.0

    def cloud_level(bar):
        end = bar - disp
        span_a = (midpoint(end, tp) + midpoint(end, kp)) / 2.0
        span_b = midpoint(end, sp)
        return (span_a + span_b) / 2.0

    now = cloud_level(t)
    then = cloud_level(t - lb)
    if now != now or then != then:
        return float("nan")
    if not then > 0:
        return float("nan")
    slope = (now - then) / then * 100.0
    if form == "proximity":
        fall = -slope
        if fall < 0:
            fall = 0.0
        return 1.0 / (1.0 + fall)
    return slope
```

checks:
IchimokuCloudSlopeComponent: every check passed
the bot's suite: ======= 1583 passed, 16 skipped, 75 deselected, 2244 warnings in 47.13s ========
