# IchimokuBelowCloudDistancePerWidthComponent: night3_ichimoku_run | 021-04_thin-cloud-downward-breakdown_1d | CloudThinnessBreakBelowComponent

## attempt 1

answer: built
class: IchimokuBelowCloudDistancePerWidthComponent
settings: {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26}
reason: No component computes this ratio. It is the below-cloud distance as a percent of the close (`IchimokuCloudPositionComponent` with `edge` "nearest" and `base` "close", sign flipped and kept below the cloud) divided by 1 plus `IchimokuCloudWidthComponent`, and no config step divides one component by another, so one new class computes it.

table: Directional components
row: | `IchimokuBelowCloudDistancePerWidthComponent` | `tenkan_period` (9), `kijun_period` (26), `senkou_period` (52), `displacement` (26) | max(0, bottom − close[t]) / close[t] x 100 / (1 + abs(A − B) / close[t] x 100). With e = t − `displacement` and M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2: A = (M(`tenkan_period`) + M(`kijun_period`)) / 2, B = M(`senkou_period`), bottom = min(A, B). These are the leading spans plotted at bar t | 0 and up, unbounded above, never negative. It is 0 inside the cloud (edges included) or above it, and continuous at the bottom edge. It grows as the close falls further below the cloud bottom and as the cloud thins, and equals the plain below-bottom distance in percent of the close when the cloud has zero width | graded | percent of the close per (1 + cloud width in percent of the close) | max(`tenkan_period`, `kijun_period`, `senkou_period`) + `displacement` (78) | high, low, close. A NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN. A close[t] not above 0 gives NaN (never on real bars). These settings raise when the component is built: any period < 1, `displacement` < 0 | stateless. It is one-sided: a below-cloud break reading. Same spans as `IchimokuCloudPositionComponent` and `IchimokuCloudWidthComponent`, and the cloud at bar t uses no bar after t-`displacement`. It equals −`IchimokuCloudPositionComponent` (`edge` "nearest", `base` "close") clipped at 0, divided by (1 + `IchimokuCloudWidthComponent`). `negate` gives the signed-negative reading. No `scaling_factor`: scale it with transforms |

```python class
class IchimokuBelowCloudDistancePerWidthComponent(SubStrategyComponent):
    """
    Distance of the close below the Ichimoku cloud bottom, per (1 + cloud width), on every bar:

        e = t - displacement
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A = (M(tenkan_period) + M(kijun_period)) / 2,  B = M(senkou_period)
        bottom = min(A, B)
        D = max(0, bottom - close[t]) / close[t] x 100       (distance below the bottom, percent of close)
        W = abs(A - B) / close[t] x 100                        (cloud width, percent of close)
        raw_value = D / (1 + W)

    Range and sign: 0 and up, unbounded above, never negative. The value is 0 inside the cloud (edges included)
    or above it, continuous at the bottom edge, and grows as the close falls further below a thinner cloud.
    Graded, one-sided.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement rows (78 at the defaults), bar t
    included.
    NaN: a NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN; a close[t] not above 0
    gives NaN (never on real bars).

    WHY THIS CANNOT LEAK: it reads high and low only on bars up to e = t - displacement, and the close of bar t,
    the last row of data; every value is known at bar t's close.
    """

    def __init__(self, name="Ichimoku Below Cloud Per Width", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        for nm, p in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if p < 1:
                raise ValueError(f"IchimokuBelowCloudDistancePerWidthComponent: {nm} must be >= 1, got {p}")
        if self.displacement < 0:
            raise ValueError(
                f"IchimokuBelowCloudDistancePerWidthComponent: displacement must be >= 0, got {self.displacement}")
        self._raw_value = 0.0

    def _mid(self, high, low, e, p):
        h = high.iloc[e - p + 1:e + 1]
        l = low.iloc[e - p + 1:e + 1]
        if h.isna().any() or l.isna().any():
            return float("nan")
        return (float(h.max()) + float(l.min())) / 2.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float)
        low = data['low'].astype(float)
        close_t = float(data['close'].astype(float).iloc[-1])
        n = len(data)
        e = n - 1 - self.displacement
        mt = self._mid(high, low, e, self.tenkan_period)
        mk = self._mid(high, low, e, self.kijun_period)
        ms = self._mid(high, low, e, self.senkou_period)
        a = (mt + mk) / 2.0
        b = ms
        if np.isnan(a) or np.isnan(b) or np.isnan(close_t) or not close_t > 0:
            self._raw_value = float("nan")
        else:
            bottom = min(a, b)
            dist = max(0.0, bottom - close_t) / close_t * 100.0
            width = abs(a - b) / close_t * 100.0
            self._raw_value = float(dist / (1.0 + width))
            self.debug_info = {'span_a': a, 'span_b': b, 'distance_below_pct': dist, 'width_pct': width}
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement
```

```python hand
def hand(df, params):
    tp = int(params.get("tenkan_period", 9))
    kp = int(params.get("kijun_period", 26))
    sp = int(params.get("senkou_period", 52))
    disp = int(params.get("displacement", 26))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    e = t - disp

    def mid(p):
        hi = None
        lo = None
        j = e - p + 1
        while j <= e:
            h = highs[j]
            l = lows[j]
            if h != h or l != l:
                return float("nan")
            if hi is None or h > hi:
                hi = h
            if lo is None or l < lo:
                lo = l
            j = j + 1
        return (hi + lo) / 2.0

    a = (mid(tp) + mid(kp)) / 2.0
    b = mid(sp)
    c = closes[t]
    if a != a or b != b or c != c or not c > 0:
        return float("nan")
    bottom = a if a < b else b
    below = bottom - c
    if below < 0:
        below = 0.0
    dist_pct = below / c * 100.0
    width_pct = (a - b if a >= b else b - a) / c * 100.0
    return dist_pct / (1.0 + width_pct)
```

checks:
IchimokuBelowCloudDistancePerWidthComponent: every check passed
the bot's suite: ======= 1583 passed, 16 skipped, 75 deselected, 2244 warnings in 47.05s ========
