# IchimokuCloudWidthComponent: night3_ichimoku_run | 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d | IchimokuCloudThinness

## attempt 1

answer: built
class: IchimokuCloudWidthComponent
settings: {"form": "proximity"}
reason: The wished value 1 / (1 + W) is the same measure as `IchimokuCloudWidthComponent` (W, the cloud width in percent of the close), put in another form. It is not its negative and not 1 minus it, and no config step gives it exactly. So it is a new `form` setting on that class, and the default "width" keeps today's output unchanged, as `IchimokuCloudSlopeComponent` does with its "proximity" form.

table: Regime measures
row: | `IchimokuCloudWidthComponent` | `tenkan_period` (9), `kijun_period` (26), `senkou_period` (52), `displacement` (26), `form` ("width") | W = abs(A − B) / close[t] x 100. With e = t − `displacement` and M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2, A = (M(`tenkan_period`) + M(`kijun_period`)) / 2 and B = M(`senkou_period`). These are the leading spans plotted at bar t. `form` "width": W. `form` "proximity": 1 / (1 + W) | "width": 0 and up, unbounded above, never negative; no direction; 0 when the two spans meet, larger the thicker the cloud against the current price. "proximity": above 0, up to 1, never negative; no direction; 1 when the spans meet, shrinking toward 0 as the cloud thickens, growing smoothly as it thins | regime measure | "width": percent of the close. "proximity": dimensionless (0 to 1) | max(`tenkan_period`, `kijun_period`, `senkou_period`) + `displacement` (78) | high, low, close. A NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN; a close[t] not above 0 gives NaN (never on real bars). These settings raise when the component is built: any period < 1, `displacement` < 0, `form` other than "width" or "proximity" | stateless; graded, continuous in the highs and lows; the cloud at bar t uses no bar after t-`displacement`. Same spans as `IchimokuCloudPositionComponent` and `IchimokuCloudSlopeComponent`. `form` "width" (default) is the original output, unchanged. "proximity" is 1 / (1 + width), which no config step gives; it grows as the cloud thins. `negate` on "width" also grows as the cloud thins, but it is not this bounded form. No `scaling_factor`: scale it with transforms |

```python class
class IchimokuCloudWidthComponent(SubStrategyComponent):
    """
    Thickness of the Ichimoku cloud plotted at bar t, against the current close:

        e = t - displacement
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A = (M(tenkan_period) + M(kijun_period)) / 2          (leading span A plotted at bar t)
        B = M(senkou_period)                                  (leading span B plotted at bar t)
        W = abs(A - B) / close[t] x 100
        form = "width" (default):  raw_value = W
        form = "proximity":        raw_value = 1 / (1 + W)

    "width": 0 and up, unbounded above, never negative, no direction; 0 when the spans meet.
    "proximity": above 0, up to 1, never negative, no direction; 1 when the spans meet, growing smoothly
    as the cloud thins against the price. The default "width" is the original output, unchanged.
    Graded and continuous in the highs and lows.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement rows, bar t included.

    NaN: a NaN high or low in any span window ending at bar e, or a NaN close[t], gives NaN; a close[t]
    not above 0 gives NaN (never on real bars). Building the component raises for any period below 1, a
    displacement below 0, or a form other than "width" or "proximity".

    WHY THIS CANNOT LEAK: the spans read only the high and low of bars up to e = t - displacement, and the
    divisor is close[t], the last row of data; no row after bar t is read.
    """

    def __init__(self, name="IchimokuCloudWidth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        for nm, p in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if p < 1:
                raise ValueError(f"IchimokuCloudWidthComponent: {nm} must be >= 1, got {p}")
        if self.displacement < 0:
            raise ValueError(
                f"IchimokuCloudWidthComponent: displacement must be >= 0, got {self.displacement}")
        self.form = self.parameters.get("form", "width")
        if self.form not in ("width", "proximity"):
            raise ValueError(
                f"IchimokuCloudWidthComponent: form must be 'width' or 'proximity', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        e = len(data) - 1 - self.displacement

        def mid(p):
            h = high[e - p + 1:e + 1]
            l = low[e - p + 1:e + 1]
            if np.isnan(h).any() or np.isnan(l).any():
                return float("nan")
            return (float(np.max(h)) + float(np.min(l))) / 2.0

        a = (mid(self.tenkan_period) + mid(self.kijun_period)) / 2.0
        b = mid(self.senkou_period)
        c = float(close[-1])
        if np.isnan(a) or np.isnan(b) or np.isnan(c) or not c > 0:
            self._raw_value = float("nan")
        else:
            w = abs(a - b) / c * 100.0
            self._raw_value = float(w) if self.form == "width" else float(1.0 / (1.0 + w))
        self.confidence = 1.0
        self.debug_info = {'span_a': a, 'span_b': b, 'close': c, 'form': self.form}

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
    d = int(params.get("displacement", 26))
    form = params.get("form", "width")
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1
    e = t - d

    def midpoint(p):
        top = None
        bot = None
        j = e - p + 1
        while j <= e:
            h = hi[j]
            l = lo[j]
            if h != h or l != l:
                return float("nan")
            if top is None or h > top:
                top = h
            if bot is None or l < bot:
                bot = l
            j = j + 1
        return (top + bot) / 2.0

    m_t = midpoint(tp)
    m_k = midpoint(kp)
    m_s = midpoint(sp)
    c = cl[t]
    if m_t != m_t or m_k != m_k or m_s != m_s or c != c:
        return float("nan")
    if not c > 0:
        return float("nan")
    span_a = (m_t + m_k) / 2.0
    span_b = m_s
    diff = span_a - span_b
    if diff < 0:
        diff = -diff
    width = diff / c * 100.0
    if form == "proximity":
        return 1.0 / (1.0 + width)
    return width
```

checks:
IchimokuCloudWidthComponent: every check passed
the bot's suite: ======= 1583 passed, 16 skipped, 75 deselected, 2244 warnings in 49.08s ========
