# RangeCompressionRatioComponent: night_006_run | 006-04_upside-squeeze-break-continuation_1d | RangeCompressionRatioComponent

## attempt 1

answer: built
class: RangeCompressionRatioComponent
settings: {"short_period": 20, "long_period": 100}
reason: No catalogue component compares a short high-low range with a longer one. The nearest ones are `DonchianBreakoutComponent`, which gives the close's position within a range of closes, and `VolatilityPercentileRegimeComponent`, which ranks a return std. So a new class computes 1 − (20-bar high-low range) / (100-bar high-low range) from the high and low columns.

table: Regime measures
row: | `RangeCompressionRatioComponent` | `short_period` (20), `long_period` (100) | 1 − (max(high) − min(low) over the last `short_period` bars) / (max(high) − min(low) over the last `long_period` bars), both windows ending at bar t inclusive; 0.0 when the long range is 0 | 0 to 1, never negative; no direction; 0 when the short range spans the whole long range, near 1 when the short band is very narrow against the long range | regime measure | dimensionless | `long_period` (100) | high, low. A NaN high or low anywhere in the last `long_period` rows gives NaN; `short_period` < 1 or `short_period` >= `long_period` raises | stateless; the short window is inside the long one, so the ratio never exceeds 1; graded, for regime rules ("the 20-bar band is in the narrowest part of its 100-bar range") or as a forecast source after transforms |

```python class
class RangeCompressionRatioComponent(SubStrategyComponent):
    """
    How narrow the recent high-low band is against a longer high-low range, on every bar:

        R_s = max(high[t-short_period+1 .. t]) - min(low[t-short_period+1 .. t])
        R_l = max(high[t-long_period+1  .. t]) - min(low[t-long_period+1  .. t])
        raw_value = 1 - R_s / R_l          (0.0 if R_l == 0)

    Range and sign: 0 to 1, never negative, no direction. The short window lies inside the long one, so
    0 <= R_s <= R_l. The value is 0 when the short band spans the whole long range and grows continuously
    towards 1 as the short band narrows. If every bar of the long window has the same high and low
    (R_l == 0), there is no range to compare with. The short band then equals the long one, so the value is 0.0.

    Warm-up: `long_period` bars (100 at the defaults), bar t included.

    NaN: a NaN high or low anywhere in the last `long_period` rows gives NaN, never a fabricated value.
    `short_period` < 1 or `short_period` >= `long_period` raises when the component is built.

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the last `long_period` rows of the data it
    is given, bar t (the last row) included. A bar's high and low are known at that bar's close.
    """

    def __init__(self, name="RangeCompressionRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 20))
        self.long_period = int(self.parameters.get("long_period", 100))
        if self.short_period < 1:
            raise ValueError(
                f"RangeCompressionRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                "RangeCompressionRatioComponent: short_period must be < long_period, got "
                f"{self.short_period} and {self.long_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high_l = data['high'].iloc[-self.long_period:].astype(float).to_numpy()
        low_l = data['low'].iloc[-self.long_period:].astype(float).to_numpy()
        if np.isnan(high_l).any() or np.isnan(low_l).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            self.debug_info = {'nan_input': True}
            return
        high_s = high_l[-self.short_period:]
        low_s = low_l[-self.short_period:]
        r_long = float(high_l.max() - low_l.min())
        r_short = float(high_s.max() - low_s.min())
        if r_long > 0:
            value = 1.0 - r_short / r_long
        else:
            value = 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'short_range': r_short, 'long_range': r_long}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.long_period
```

```python hand
def hand(df, params):
    s = params.get("short_period", 20)
    n = params.get("long_period", 100)
    highs = list(df["high"])
    lows = list(df["low"])
    hl = highs[len(highs) - n:]
    ll = lows[len(lows) - n:]
    for x in hl + ll:
        if x != x:
            return float("nan")
    top_long = hl[0]
    bottom_long = ll[0]
    for i in range(n):
        if hl[i] > top_long:
            top_long = hl[i]
        if ll[i] < bottom_long:
            bottom_long = ll[i]
    top_short = hl[n - s]
    bottom_short = ll[n - s]
    for i in range(n - s, n):
        if hl[i] > top_short:
            top_short = hl[i]
        if ll[i] < bottom_short:
            bottom_short = ll[i]
    long_range = top_long - bottom_long
    short_range = top_short - bottom_short
    if long_range == 0:
        return 0.0
    return 1.0 - short_range / long_range
```

checks:
RangeCompressionRatioComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1520 passed, 8 skipped, 74 deselected, 2170 warnings in 51.32s ========
