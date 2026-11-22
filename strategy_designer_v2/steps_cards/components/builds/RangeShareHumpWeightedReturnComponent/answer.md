# RangeShareHumpWeightedReturnComponent: night4_range_run | 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d | ShareHumpWeightedMomentum

## attempt 1

answer: built
class: RangeShareHumpWeightedReturnComponent
settings: {"period": 30}
reason: No component computes this measure. `NetMoveToRangeRatioComponent` gives s and `PriceEvolutionOnPeriodComponent` gives R (in percent), but no component and no config step forms R x s x (1 − s), so one new class computes the product.

table: Directional components
row: | `RangeShareHumpWeightedReturnComponent` | `period` (30) | R x s x (1 − s), R = close[t] / close[t-`period`] − 1, s = min(1, abs(close[t] − close[t-`period`]) / (H − L)), H = max(high[t-`period`+1 .. t]), L = min(low[t-`period`+1 .. t]); s = 0 when H − L is 0 | −0.25 and up, unbounded above, signed like the `period`-bar return; size at most 0.25 x abs(R); 0 when the net move is 0, when it spans the whole range (s = 1) or for a zero range; largest at s = 0.5 | graded | simple return (fraction, not percent) x share hump (0 to 0.25) | `period` + 1 (31) | close (bars t and t-`period`), high, low (last `period` rows). A NaN in any value read gives NaN; a close[t-`period`] not above 0 gives NaN (never on real bars). `period` < 1 raises when the component is built | stateless; continuous in the prices (the clip at s = 1 meets the hump at 0). s is `NetMoveToRangeRatioComponent` (`period`, `source` "high_low") clipped at 1. No `scaling_factor`: scale it with transforms |

```python class
class RangeShareHumpWeightedReturnComponent(SubStrategyComponent):
    """
    The period-bar return weighted by a hump of the net move's share of the window's high-low range:

        R = close[t] / close[t - period] - 1
        H = max(high[t - period + 1 .. t]),  L = min(low[t - period + 1 .. t])
        s = min(1, abs(close[t] - close[t - period]) / (H - L)),  s = 0 when H - L = 0
        raw_value = R x s x (1 - s)

    Range and sign: -0.25 and up, unbounded above. It is signed like the period-bar return, and its size is
    at most 0.25 x abs(R). It is 0 when the net move is 0, when the net move spans the whole range (s = 1),
    or for a zero range. For a given return it is largest at s = 0.5. Graded and continuous in the prices.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN close at bar t or t - period, or a NaN high or low in the last period rows, gives NaN.
    A close[t - period] not above 0 gives NaN (never on real bars). Building the component raises for a
    period below 1.

    WHY THIS CANNOT LEAK: it reads close of bars t and t - period and high and low of bars
    t - period + 1 .. t, all at or before the last row of data (bar t), and every one of them is known at bar
    t's close.
    """

    def __init__(self, name="RangeShareHumpReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 1:
            raise ValueError(f"RangeShareHumpWeightedReturnComponent: period must be >= 1, got {self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        close = data['close'].astype(float)
        high = data['high'].astype(float).iloc[-p:]
        low = data['low'].astype(float).iloc[-p:]
        c_t = float(close.iloc[-1])
        c_b = float(close.iloc[-(p + 1)])
        if np.isnan(c_t) or np.isnan(c_b) or high.isna().any() or low.isna().any() or not c_b > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rng = float(high.max()) - float(low.min())
        r = c_t / c_b - 1.0
        if rng > 0:
            s = min(1.0, max(0.0, abs(c_t - c_b) / rng))
        else:
            s = 0.0
        self._raw_value = float(r * s * (1.0 - s))
        self.confidence = 1.0
        self.debug_info = {'return': r, 'share': s, 'range': rng}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    p = int(params.get("period", 30))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    last = len(c) - 1
    now = c[last]
    base = c[last - p]
    highs = []
    lows = []
    i = last - p + 1
    while i <= last:
        highs.append(h[i])
        lows.append(lo[i])
        i = i + 1
    for x in [now, base] + highs + lows:
        if x != x:
            return float("nan")
    if not base > 0:
        return float("nan")
    top = highs[0]
    for x in highs:
        if x > top:
            top = x
    bottom = lows[0]
    for x in lows:
        if x < bottom:
            bottom = x
    width = top - bottom
    ret = now / base - 1.0
    if width > 0:
        share = abs(now - base) / width
        if share > 1.0:
            share = 1.0
    else:
        share = 0.0
    return ret * share * (1.0 - share)
```

checks:
RangeShareHumpWeightedReturnComponent: every check passed
the bot's suite: == 1613 passed, 16 skipped, 75 deselected, 2244 warnings in 100.75s (0:01:40) ==
