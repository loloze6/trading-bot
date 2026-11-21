# IchimokuCloudWidthComponent: night3_ichimoku_run | 021-03_thin-cloud-upward-breakout_1d | IchimokuCloudWidthComponent

## attempt 1

answer: built
class: IchimokuCloudWidthComponent
settings: {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26}
reason: No component measures the cloud's thickness. `IchimokuCloudPositionComponent` reads the close against the cloud top or nearest edge, and `IchimokuCloudSlopeComponent` reads the change of the cloud's mid level, so one new class computes abs(span A − span B) / close[t] x 100 from the same displaced spans. No inverse `form` is added: `negate` already gives the reading that grows as the cloud thins, and 1 / width is infinite when the two spans meet, which real bars can show.

table: Regime measures
row: | `IchimokuCloudWidthComponent` | `tenkan_period` (9), `kijun_period` (26), `senkou_period` (52), `displacement` (26) | abs(A − B) / close[t] x 100. With e = t − `displacement` and M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2, A = (M(`tenkan_period`) + M(`kijun_period`)) / 2 and B = M(`senkou_period`). These are the leading spans plotted at bar t | 0 and up, unbounded above, never negative; no direction; 0 when the two spans meet, larger the thicker the cloud against the current price | regime measure | percent of the close | max(`tenkan_period`, `kijun_period`, `senkou_period`) + `displacement` (78) | high, low, close. A NaN high or low in the windows ending at bar e, or a NaN close[t], gives NaN; a close[t] not above 0 gives NaN (never on real bars). These settings raise when the component is built: any period < 1, `displacement` < 0 | stateless; graded, continuous in the highs and lows; the cloud at bar t uses no bar after t-`displacement`. Same spans as `IchimokuCloudPositionComponent` and `IchimokuCloudSlopeComponent`. `negate` gives the reading that grows as the cloud thins. No `scaling_factor`: scale it with transforms |

```python class
class IchimokuCloudWidthComponent(SubStrategyComponent):
    """
    The thickness of the Ichimoku cloud plotted at bar t, as a percent of the current close:

        e = t - displacement
        M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        A = (M(tenkan_period) + M(kijun_period)) / 2          (leading span A plotted at bar t)
        B = M(senkou_period)                                   (leading span B plotted at bar t)
        raw_value = abs(A - B) / close[t] x 100

    Range and sign: 0 and up, unbounded above, never negative, with no direction. It is 0 when the two spans
    meet and grows continuously as the cloud thickens against the price. `negate` gives the reading that grows
    as the cloud thins.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement rows, bar t included (78 at the
    defaults).

    NaN: a NaN high or low in any window ending at bar e, or a NaN close[t], gives NaN. A close[t] not above 0
    gives NaN, which never happens on real bars.
    Building the component raises for any period below 1 or a displacement below 0.

    WHY THIS CANNOT LEAK: it reads the `high` and `low` columns of rows e-p+1 .. e only, e = t - displacement
    <= t, and the `close` of bar t (the last row of data). Every row it reads is at or before bar t.
    """

    def __init__(self, name="Ichimoku cloud width", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        for key, val in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                         ("senkou_period", self.senkou_period)):
            if val < 1:
                raise ValueError(f"IchimokuCloudWidthComponent: {key} must be >= 1, got {val}")
        if self.displacement < 0:
            raise ValueError(
                f"IchimokuCloudWidthComponent: displacement must be >= 0, got {self.displacement}")
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
        e = len(close) - 1 - self.displacement

        def mid(p):
            hw = high[e - p + 1:e + 1]
            lw = low[e - p + 1:e + 1]
            if np.isnan(hw).any() or np.isnan(lw).any():
                return float("nan")
            return (float(hw.max()) + float(lw.min())) / 2.0

        span_a = (mid(self.tenkan_period) + mid(self.kijun_period)) / 2.0
        span_b = mid(self.senkou_period)
        c_t = float(close[-1])
        if np.isnan(span_a) or np.isnan(span_b) or np.isnan(c_t) or not c_t > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(abs(span_a - span_b) / c_t * 100.0)
        self.confidence = 1.0
        self.debug_info = {'span_a': span_a, 'span_b': span_b, 'close': c_t}

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
    d = int(params.get("displacement", 26))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    e = last - d

    def midpoint(p):
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

    m_tk = midpoint(tk)
    m_kj = midpoint(kj)
    m_sk = midpoint(sk)
    if m_tk != m_tk or m_kj != m_kj or m_sk != m_sk:
        return float("nan")
    span_a = (m_tk + m_kj) / 2.0
    span_b = m_sk
    c = closes[last]
    if c != c or not c > 0:
        return float("nan")
    width = span_a - span_b
    if width < 0:
        width = -width
    return width / c * 100.0
```

checks:
IchimokuCloudWidthComponent: every check passed
the bot's suite: ======= 1581 passed, 16 skipped, 75 deselected, 2244 warnings in 47.86s ========
