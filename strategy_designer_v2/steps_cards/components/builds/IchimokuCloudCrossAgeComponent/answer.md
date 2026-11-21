# IchimokuCloudCrossAgeComponent: night3_ichimoku_run | 021-03_thin-cloud-upward-breakout_1d | CloudCrossUpAgeComponent

## attempt 1

answer: built
class: IchimokuCloudCrossAgeComponent
settings: {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "max_bars": 120, "window": 250}
reason: No component in the catalogue counts how long the close has held a side of the Ichimoku cloud since it crossed through from the opposite side. `MovingAverageAgeComponent` counts this kind of age only against an SMA, and the Ichimoku components measure distance, width or slope, not age. This new class computes that age from the coin's own highs, lows and closes, signed and capped. It looks back over a fixed `window` of bars, so it keeps no state.

table: Regime measures
row: | `IchimokuCloudCrossAgeComponent` | `tenkan_period` (9), `kijun_period` (26), `senkou_period` (52), `displacement` (26), `max_bars` (120), `window` (250) | For each bar i, e = i − `displacement`, M(p) = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2, A = (M(`tenkan_period`) + M(`kijun_period`)) / 2, B = M(`senkou_period`), top = max(A, B), bottom = min(A, B). The side of bar i is +1 if close[i] > top, −1 if close[i] < bottom, and 0 (inside the cloud, edges included) otherwise. Sides are read for bars t-`window`+1 .. t. With s = side(t) and n = the number of consecutive bars ending at t with side s, the output is s x min(n, `max_bars`) when s ≠ 0 and the nearest earlier bar of the window with a nonzero side has side −s. Otherwise it is 0: inside the cloud, or the close left the cloud on the side it entered from, or no earlier outside bar is in the window | −`max_bars` .. +`max_bars`, integers. Positive above the cloud after a cross up from below, negative below it after a cross down from above, 0 otherwise. The size grows by one each further bar on the same side | regime measure | bars | `window` + max(periods) + `displacement` − 1 (327) | high, low, close. A NaN high or low in any span window, or a NaN close, used for a side in the window gives NaN. These settings raise when the component is built: any period < 1, `displacement` < 0, `max_bars` < 1, `window` <= `max_bars` | stateless. Like `MovingAverageAgeComponent`, it jumps at a cross (from ±n to 0 or ∓1), so it is for regime rules, not a forecast source. The spans are the same as those of `IchimokuCloudPositionComponent`; the cloud at bar i uses no bar after i-`displacement`. A run longer than `window` − 1 bars has no visible origin and reads 0. No `scaling_factor` |

```python class
class IchimokuCloudCrossAgeComponent(SubStrategyComponent):
    """
    How long the close has stayed outside the Ichimoku cloud since it crossed through it from the other side:

        for each bar i: e = i - displacement
            M(p)   = (max(high[e-p+1 .. e]) + min(low[e-p+1 .. e])) / 2
            A      = (M(tenkan_period) + M(kijun_period)) / 2,  B = M(senkou_period)
            top    = max(A, B),  bottom = min(A, B)
            side(i) = +1 if close[i] > top, -1 if close[i] < bottom, 0 otherwise (inside or on an edge)
        sides are read for bars i = t-window+1 .. t
        s = side(t); n = number of consecutive bars ending at t with side s
        q = side of the nearest bar before that run (inside the window) whose side is not 0
        raw_value = s * min(n, max_bars)  if s != 0 and q == -s
                    0                     otherwise (inside the cloud, re-exit on the same side,
                                                     or no earlier outside bar in the window)

    Range: integers -max_bars .. +max_bars. Positive above the cloud after a cross up from below, negative
    below it after a cross down from above. Its size grows by one per bar spent on that side. A regime measure
    for rules (it jumps at a cross), not a forecast source.
    Warm-up: window + max(tenkan_period, kijun_period, senkou_period) + displacement - 1 rows (327 at the
    defaults), bar t included.
    NaN: a NaN high or low in any span window, or a NaN close, used for a side in the window gives NaN.

    WHY THIS CANNOT LEAK: it reads only the high, low and close columns of the last
    get_required_periods() rows of data, bar t (the last row) included. The cloud at bar i uses only bars up to
    i - displacement, and the side of bar i uses close[i]; no row after t is read.
    """

    def __init__(self, name="IchimokuCloudCrossAge", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.tenkan_period = int(self.parameters.get("tenkan_period", 9))
        self.kijun_period = int(self.parameters.get("kijun_period", 26))
        self.senkou_period = int(self.parameters.get("senkou_period", 52))
        self.displacement = int(self.parameters.get("displacement", 26))
        self.max_bars = int(self.parameters.get("max_bars", 120))
        self.window = int(self.parameters.get("window", 250))
        for nm, v in (("tenkan_period", self.tenkan_period), ("kijun_period", self.kijun_period),
                      ("senkou_period", self.senkou_period)):
            if v < 1:
                raise ValueError(f"IchimokuCloudCrossAgeComponent: {nm} must be >= 1, got {v}")
        if self.displacement < 0:
            raise ValueError(f"IchimokuCloudCrossAgeComponent: displacement must be >= 0, got {self.displacement}")
        if self.max_bars < 1:
            raise ValueError(f"IchimokuCloudCrossAgeComponent: max_bars must be >= 1, got {self.max_bars}")
        if self.window <= self.max_bars:
            raise ValueError(
                f"IchimokuCloudCrossAgeComponent: window must be > max_bars, got {self.window} <= {self.max_bars}")
        self._offset = max(self.tenkan_period, self.kijun_period, self.senkou_period) + self.displacement - 1
        self._raw_value = 0.0

    @staticmethod
    def _mid(h, l, e, p):
        hw = h[e - p + 1:e + 1]
        lw = l[e - p + 1:e + 1]
        if np.isnan(hw).any() or np.isnan(lw).any():
            return float("nan")
        return (float(hw.max()) + float(lw.min())) / 2.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        rows = self.get_required_periods()
        h = data["high"].astype(float).to_numpy()[-rows:]
        l = data["low"].astype(float).to_numpy()[-rows:]
        c = data["close"].astype(float).to_numpy()[-rows:]
        sides = []
        for i in range(self._offset, rows):
            e = i - self.displacement
            a = (self._mid(h, l, e, self.tenkan_period) + self._mid(h, l, e, self.kijun_period)) / 2.0
            b = self._mid(h, l, e, self.senkou_period)
            ci = c[i]
            if np.isnan(a) or np.isnan(b) or np.isnan(ci):
                self._raw_value = float("nan")
                self.confidence = 1.0
                self.debug_info = {"nan": True}
                return
            top = max(a, b)
            bottom = min(a, b)
            if ci > top:
                sides.append(1)
            elif ci < bottom:
                sides.append(-1)
            else:
                sides.append(0)
        s = sides[-1]
        value = 0.0
        n = 0
        prior = 0
        if s != 0:
            j = len(sides) - 1
            while j >= 0 and sides[j] == s:
                n += 1
                j -= 1
            while j >= 0 and sides[j] == 0:
                j -= 1
            prior = sides[j] if j >= 0 else 0
            if prior == -s:
                value = float(s * min(n, self.max_bars))
        self._raw_value = value
        self.confidence = 1.0
        self.debug_info = {"side": s, "run": n, "prior_side": prior}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.window + self._offset
```

```python hand
def hand(df, params):
    tk = int(params.get("tenkan_period", 9))
    kj = int(params.get("kijun_period", 26))
    sk = int(params.get("senkou_period", 52))
    d = int(params.get("displacement", 26))
    cap = int(params.get("max_bars", 120))
    w = int(params.get("window", 250))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1

    def is_nan(x):
        return x != x

    def midpoint(end, p):
        hi = None
        lo = None
        k = end - p + 1
        while k <= end:
            if is_nan(highs[k]) or is_nan(lows[k]):
                return float("nan")
            if hi is None or highs[k] > hi:
                hi = highs[k]
            if lo is None or lows[k] < lo:
                lo = lows[k]
            k = k + 1
        return (hi + lo) / 2.0

    # side of each bar from t-w+1 to t, oldest first
    side_list = []
    bar = last - w + 1
    while bar <= last:
        e = bar - d
        span_a = (midpoint(e, tk) + midpoint(e, kj)) / 2.0
        span_b = midpoint(e, sk)
        cl = closes[bar]
        if is_nan(span_a) or is_nan(span_b) or is_nan(cl):
            return float("nan")
        upper = span_a if span_a > span_b else span_b
        lower = span_b if span_a > span_b else span_a
        if cl > upper:
            side_list.append(1)
        elif cl < lower:
            side_list.append(-1)
        else:
            side_list.append(0)
        bar = bar + 1

    current = side_list[len(side_list) - 1]
    if current == 0:
        return 0.0
    run = 0
    pos = len(side_list) - 1
    while pos >= 0 and side_list[pos] == current:
        run = run + 1
        pos = pos - 1
    origin = 0
    while pos >= 0:
        if side_list[pos] != 0:
            origin = side_list[pos]
            break
        pos = pos - 1
    if origin != -current:
        return 0.0
    if run > cap:
        run = cap
    return float(current * run)
```

checks:
IchimokuCloudCrossAgeComponent: every check passed
the bot's suite: ======= 1582 passed, 16 skipped, 75 deselected, 2244 warnings in 45.50s ========
