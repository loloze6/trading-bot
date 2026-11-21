# IchimokuCloudSlopeComponent: night3_ichimoku_run | 021-01_above-rising-cloud-continues-up_1d | IchimokuCloudSlopeComponent

## attempt 1

answer: built
class: IchimokuCloudSlopeComponent
settings: {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "lookback": 26}
reason: No catalogue component computes how fast the Ichimoku cloud's level moves. `IchimokuCloudPositionComponent` measures only how far the close sits from the cloud top at one bar, not how the cloud's mid level changed over 26 bars. This new class computes that percent change from the high and low.

table: Directional components
row: | `IchimokuCloudSlopeComponent` | `tenkan_period` (9), `kijun_period` (26), `senkou_period` (52), `displacement` (26), `lookback` (26) | (C(t) - C(t-`lookback`)) / C(t-`lookback`) x 100, C(i) = (A(i) + B(i)) / 2. With e = i - `displacement` and M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2: A(i) = (M(`tenkan_period`) + M(`kijun_period`)) / 2 and B(i) = M(`senkou_period`). These are the leading spans plotted at bar i, computed from bars ending `displacement` bars earlier | -100 and up, unbounded above, signed; positive while the cloud's mid level rises, negative while it falls; larger the faster it rises | graded | percent over `lookback` bars | max(`tenkan_period`, `kijun_period`, `senkou_period`) + `displacement` + `lookback` (104) | high, low only. A NaN high or low in any window used for C(t) or C(t-`lookback`) gives NaN; a C(t-`lookback`) not above 0 gives NaN (never on real bars). These settings raise when the component is built: any period < 1, `displacement` < 0, `lookback` < 1 | stateless; the cloud at bar t uses no bar after t-`displacement`. The cloud level is the mid of spans A and B, not the top (`IchimokuCloudPositionComponent` uses the top and reads the close). No `scaling_factor`: scale it with transforms |

```python class
class IchimokuCloudSlopeComponent(SubStrategyComponent):
    """
    Percent change over `lookback` bars of the Ichimoku cloud's mid level, on every bar:

        M_e(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
        for a bar i, e = i - displacement:
            A(i) = (M_e(tenkan_period) + M_e(kijun_period)) / 2     (span A plotted at bar i)
            B(i) = M_e(senkou_period)                               (span B plotted at bar i)
            C(i) = (A(i) + B(i)) / 2                                (the cloud's level)
        raw_value = (C(t) - C(t - lookback)) / C(t - lookback) x 100

    Graded and signed. The value runs from -100 upward and is unbounded above. It is positive while the cloud's
    level rises and grows the faster the cloud rises. Units: percent over `lookback` bars.
    Warm-up: max(tenkan_period, kijun_period, senkou_period) + displacement + lookback rows, bar t included
    (104 at the defaults).

    NaN: a NaN high or low in any window used for C(t) or C(t - lookback) gives NaN. A C(t - lookback) not
    above 0 gives NaN (never on real bars). A missing `high` or `low` column raises.
    Building the component raises for any period below 1, a displacement below 0, or a lookback below 1.

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the rows up to bar t - displacement (the
    last row of data is bar t). Its earliest row is bar t - lookback - displacement - max_period + 1. A bar's
    high and low are known at that bar's close.
    """

    def __init__(self, name="IchimokuCloudSlope", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        self.lookback = int(self.parameters.get("lookback", 26))
        for key, val in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                         ("senkou_period", self.senkou_period)):
            if val < 1:
                raise ValueError(f"IchimokuCloudSlopeComponent: {key} must be >= 1, got {val}")
        if self.displacement < 0:
            raise ValueError(f"IchimokuCloudSlopeComponent: displacement must be >= 0, got {self.displacement}")
        if self.lookback < 1:
            raise ValueError(f"IchimokuCloudSlopeComponent: lookback must be >= 1, got {self.lookback}")
        self._raw_value = 0.0

    def _mid(self, high, low, e, p):
        seg_h = high[e - p + 1:e + 1]
        seg_l = low[e - p + 1:e + 1]
        if np.isnan(seg_h).any() or np.isnan(seg_l).any():
            return float("nan")
        return (float(np.max(seg_h)) + float(np.min(seg_l))) / 2.0

    def _cloud_level(self, high, low, i):
        e = i - self.displacement
        a = (self._mid(high, low, e, self.tenkan_period) + self._mid(high, low, e, self.kijun_period)) / 2.0
        b = self._mid(high, low, e, self.senkou_period)
        return (a + b) / 2.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        low = data['low'].astype(float).to_numpy()
        t = len(high) - 1
        cur = self._cloud_level(high, low, t)
        base = self._cloud_level(high, low, t - self.lookback)
        if np.isnan(cur) or np.isnan(base) or not base > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float((cur - base) / base * 100.0)
        self.confidence = 1.0
        self.debug_info = {'cloud_level_now': cur, 'cloud_level_base': base}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement + self.lookback
```

```python hand
def hand(df, params):
    tk = int(params.get("tenkan_period", 9))
    kj = int(params.get("kijun_period", 26))
    sk = int(params.get("senkou_period", 52))
    d = int(params.get("displacement", 26))
    lb = int(params.get("lookback", 26))
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    last = len(hi) - 1

    def midpoint(e, p):
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

    def level(i):
        e = i - d
        span_a = (midpoint(e, tk) + midpoint(e, kj)) / 2.0
        span_b = midpoint(e, sk)
        return (span_a + span_b) / 2.0

    now = level(last)
    then = level(last - lb)
    if now != now or then != then:
        return float("nan")
    if not then > 0:
        return float("nan")
    return (now - then) / then * 100.0
```

checks:
IchimokuCloudSlopeComponent: every check passed
the bot's suite: ======= 1580 passed, 16 skipped, 75 deselected, 2244 warnings in 47.87s ========
