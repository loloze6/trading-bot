# IchimokuCloudPositionComponent: night3_ichimoku_run | 021-03_thin-cloud-upward-breakout_1d | IchimokuCloudPositionComponent

## attempt 1

answer: built
class: IchimokuCloudPositionComponent
settings: {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "edge": "nearest", "base": "close"}
reason: `IchimokuCloudPositionComponent` with `edge` "nearest" measures the same distance outside the cloud, but it divides by the cloud edge, and the wish divides by close[t]. The two values differ on real bars. The same quantity against another base is a setting on that class, so the class is written again with a new `base` setting. Its default "edge" keeps today's output exactly.

table: Directional components
row: | `IchimokuCloudPositionComponent` | `tenkan_period` (9), `kijun_period` (26), `senkou_period` (52), `displacement` (26), `edge` ("top"), `base` ("edge") | With e = t - `displacement` and M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2: A = (M(`tenkan_period`) + M(`kijun_period`)) / 2, B = M(`senkou_period`), top = max(A, B), bottom = min(A, B). The distance d is close[t] - top for `edge` "top". For `edge` "nearest", d is close[t] - top when close[t] > top, close[t] - bottom when close[t] < bottom, and 0 inside the cloud. The divisor is the edge used (top, or bottom below the cloud) for `base` "edge", or close[t] for `base` "close". Output = d / divisor x 100 | `base` "edge": -100 and up, signed. `base` "close": below +100, unbounded below, signed. With "top" it is positive above the cloud top and negative at or below it. With "nearest" it is positive above the cloud, negative below it, 0 inside it, and grows in size the further the close sits outside the cloud; it is continuous at both edges | graded | percent of the cloud edge (`base` "edge") or of the close (`base` "close") | max(`tenkan_period`, `kijun_period`, `senkou_period`) + `displacement` (78) | high, low, close. A NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN. A divisor not above 0 gives NaN, which never happens on real bars. These settings raise when the component is built: any period < 1, `displacement` < 0, `edge` other than "top" or "nearest", `base` other than "edge" or "close" | stateless. The spans are displaced forward, so the cloud at bar t uses no bar after t-`displacement`. `edge` "top" with `base` "edge" (the defaults) is the original output, unchanged. `base` "close" gives the distance outside the cloud as a percent of the current close. Use `clip` with `max` 0 to keep only the below-cloud reading. No `scaling_factor`: scale it with transforms |

```python class
class IchimokuCloudPositionComponent(SubStrategyComponent):
    """
    Where the close sits against the Ichimoku cloud, on every bar.

        e = t - displacement
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A = (M(tenkan_period) + M(kijun_period)) / 2,  B = M(senkou_period)
        top = max(A, B),  bottom = min(A, B)

        edge = "top" (default):  d = close[t] - top,  edge value = top
        edge = "nearest":        d = close[t] - top     (edge value top)    when close[t] > top
                                 d = close[t] - bottom  (edge value bottom) when close[t] < bottom
                                 d = 0                  (edge value bottom) when bottom <= close[t] <= top

        base = "edge" (default): raw_value = d / edge value x 100
        base = "close":          raw_value = d / close[t] x 100

    The defaults ("top", "edge") give the original output, unchanged.
    Range: with base "edge" it is -100 and up; with base "close" it is below +100 and unbounded below.
    Signed: positive above the cloud. With "nearest" it is negative below the cloud and 0 inside it, and it is
    continuous at both edges. Graded.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement rows, bar t included.

    NaN: a NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN. A divisor that is not
    above 0 gives NaN; this never happens on real bars.
    Building raises for any period < 1, a displacement < 0, an edge other than "top" or "nearest", or a base
    other than "edge" or "close".

    WHY THIS CANNOT LEAK: it reads the high and low of rows up to bar e = t - displacement, and the close of
    bar t, the last row of data. It reads no row after t.
    """

    def __init__(self, name="IchimokuCloudPosition", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        for nm, p in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if p < 1:
                raise ValueError(f"IchimokuCloudPositionComponent: {nm} must be >= 1, got {p}")
        if self.displacement < 0:
            raise ValueError(f"IchimokuCloudPositionComponent: displacement must be >= 0, got {self.displacement}")
        self.edge = self.parameters.get("edge", "top")
        if self.edge not in ("top", "nearest"):
            raise ValueError(f"IchimokuCloudPositionComponent: edge must be 'top' or 'nearest', got {self.edge!r}")
        self.base = self.parameters.get("base", "edge")
        if self.base not in ("edge", "close"):
            raise ValueError(f"IchimokuCloudPositionComponent: base must be 'edge' or 'close', got {self.base!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        h = data['high'].astype(float).to_numpy()
        lo = data['low'].astype(float).to_numpy()
        c = float(data['close'].astype(float).iloc[-1])
        e = len(data) - 1 - self.displacement

        def mid(p):
            hw = h[e - p + 1:e + 1]
            lw = lo[e - p + 1:e + 1]
            if np.isnan(hw).any() or np.isnan(lw).any():
                return float("nan")
            return (float(hw.max()) + float(lw.min())) / 2.0

        a = (mid(self.tenkan_period) + mid(self.kijun_period)) / 2.0
        b = mid(self.senkou_period)
        self.confidence = 1.0
        if np.isnan(a) or np.isnan(b) or np.isnan(c):
            self._raw_value = float("nan")
            return
        top = max(a, b)
        bottom = min(a, b)
        if self.edge == "top":
            d, ref = c - top, top
        elif c > top:
            d, ref = c - top, top
        elif c < bottom:
            d, ref = c - bottom, bottom
        else:
            d, ref = 0.0, bottom
        div = ref if self.base == "edge" else c
        if not div > 0:
            self._raw_value = float("nan")
            return
        self._raw_value = float(d / div * 100.0)
        self.debug_info = {'span_a': a, 'span_b': b, 'top': top, 'bottom': bottom,
                           'edge': self.edge, 'base': self.base}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement
```

```python hand
def hand(df, params):
    tk = int(params.get("tenkan_period", 9))
    kj = int(params.get("kijun_period", 26))
    sk = int(params.get("senkou_period", 52))
    disp = int(params.get("displacement", 26))
    edge = params.get("edge", "top")
    base = params.get("base", "edge")
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    e = t - disp

    def midpoint(p):
        hi = None
        lw = None
        i = e - p + 1
        while i <= e:
            if highs[i] != highs[i] or lows[i] != lows[i]:
                return None
            if hi is None or highs[i] > hi:
                hi = highs[i]
            if lw is None or lows[i] < lw:
                lw = lows[i]
            i = i + 1
        return (hi + lw) / 2.0

    m_tk = midpoint(tk)
    m_kj = midpoint(kj)
    m_sk = midpoint(sk)
    close_t = closes[t]
    if m_tk is None or m_kj is None or m_sk is None or close_t != close_t:
        return float("nan")
    span_a = (m_tk + m_kj) / 2.0
    span_b = m_sk
    top = span_a if span_a > span_b else span_b
    bottom = span_b if span_a > span_b else span_a
    if edge == "top":
        dist = close_t - top
        ref = top
    else:
        if close_t > top:
            dist = close_t - top
            ref = top
        elif close_t < bottom:
            dist = close_t - bottom
            ref = bottom
        else:
            dist = 0.0
            ref = bottom
    divisor = close_t if base == "close" else ref
    if not divisor > 0:
        return float("nan")
    return dist / divisor * 100.0
```

checks:
IchimokuCloudPositionComponent: every check passed
the bot's suite: ======= 1580 passed, 16 skipped, 75 deselected, 2244 warnings in 48.01s ========
