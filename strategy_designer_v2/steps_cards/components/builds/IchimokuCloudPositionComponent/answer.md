# IchimokuCloudPositionComponent: night3_ichimoku_run | 021-01_above-rising-cloud-continues-up_1d | IchimokuCloudPositionComponent

## attempt 1

answer: built
class: IchimokuCloudPositionComponent
settings: {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26}
reason: No component in the catalogue computes Ichimoku spans or any distance to them. The measure uses only the coin's own high, low and close, and its displaced spans read only rows at or before bar t, so it can be computed exactly with no lookahead.

table: Directional components
row: | `IchimokuCloudPositionComponent` | `tenkan_period` (9), `kijun_period` (26), `senkou_period` (52), `displacement` (26) | (close[t] - top) / top x 100, top = max(A, B). With e = t - `displacement` and M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2: A = (M(`tenkan_period`) + M(`kijun_period`)) / 2 and B = M(`senkou_period`). These are the leading spans plotted at bar t, computed from bars ending `displacement` bars earlier | -100 and up, unbounded above, signed; positive when the close is above the cloud top, negative at or below it (inside or under the cloud); grows as the close sits further above the cloud | graded | percent of the cloud top | max(`tenkan_period`, `kijun_period`, `senkou_period`) + `displacement` (78) | high, low, close. A NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN; a top not above 0 gives NaN (never on real bars). These settings raise when the component is built: any period < 1, `displacement` < 0 | stateless; the spans are displaced forward, so the cloud at bar t uses no bar after t-`displacement`. Not a cloud-bottom or inside-cloud measure: only the distance from the top. No `scaling_factor`: scale it with transforms |

```python class
class IchimokuCloudPositionComponent(SubStrategyComponent):
    """
    Percent distance of the close from the top of the Ichimoku cloud plotted at bar t:

        e = t - displacement
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        span A = (M(tenkan_period) + M(kijun_period)) / 2
        span B = M(senkou_period)
        top = max(span A, span B)
        raw_value = (close[t] - top) / top x 100

    Range & sign: -100 and up, unbounded above, signed. It is positive when the close is above the cloud top and
    negative at or below it. It grows continuously as the close sits further above the cloud. Units: percent of
    the cloud top.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement rows, bar t included (78 at the
    defaults).
    NaN: a NaN high or low in any span window, or a NaN close[t], gives NaN. A top not above 0 gives NaN (never
    on real bars).
    Building the component raises for any period below 1 or a displacement below 0.

    WHY THIS CANNOT LEAK: it reads high and low only on rows up to t - displacement, and the close only on row t
    (the last row of data). Every row it reads is known at bar t's close.
    """

    def __init__(self, name="IchimokuCloudPosition", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        for nm, v in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if v < 1:
                raise ValueError(f"IchimokuCloudPositionComponent: {nm} must be >= 1, got {v}")
        if self.displacement < 0:
            raise ValueError(
                f"IchimokuCloudPositionComponent: displacement must be >= 0, got {self.displacement}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        h = data['high'].astype(float).to_numpy()
        lo = data['low'].astype(float).to_numpy()
        c = data['close'].astype(float).to_numpy()
        last = len(c) - 1
        end = last - self.displacement

        def mid(p):
            hw = h[end - p + 1:end + 1]
            lw = lo[end - p + 1:end + 1]
            if np.isnan(hw).any() or np.isnan(lw).any():
                return float("nan")
            return (float(hw.max()) + float(lw.min())) / 2.0

        span_a = (mid(self.tenkan_period) + mid(self.kijun_period)) / 2.0
        span_b = mid(self.senkou_period)
        close_t = float(c[last])
        if np.isnan(span_a) or np.isnan(span_b) or np.isnan(close_t):
            self._raw_value = float("nan")
        else:
            top = max(span_a, span_b)
            if not top > 0:
                self._raw_value = float("nan")
            else:
                self._raw_value = float((close_t - top) / top * 100.0)
            self.debug_info = {'span_a': span_a, 'span_b': span_b, 'cloud_top': top}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement
```

```python hand
def hand(df, params):
    tp = int(params.get("tenkan_period", 9))
    kp = int(params.get("kijun_period", 26))
    sp = int(params.get("senkou_period", 52))
    d = int(params.get("displacement", 26))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    e = t - d

    def midpoint(p):
        hi = None
        lo = None
        j = e - p + 1
        while j <= e:
            if highs[j] != highs[j] or lows[j] != lows[j]:
                return float("nan")
            if hi is None or highs[j] > hi:
                hi = highs[j]
            if lo is None or lows[j] < lo:
                lo = lows[j]
            j = j + 1
        return (hi + lo) / 2.0

    tenkan = midpoint(tp)
    kijun = midpoint(kp)
    span_b = midpoint(sp)
    span_a = (tenkan + kijun) / 2.0
    ct = closes[t]
    if span_a != span_a or span_b != span_b or ct != ct:
        return float("nan")
    top = span_a if span_a >= span_b else span_b
    if not top > 0:
        return float("nan")
    return (ct - top) / top * 100.0
```

checks:
IchimokuCloudPositionComponent: every check passed
the bot's suite: ======= 1579 passed, 16 skipped, 75 deselected, 2244 warnings in 52.88s ========
