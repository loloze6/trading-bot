# FallTimesFallComponent: night4_range_run | 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.d1_flat-slide-inside-decline_1d | FallTimesFallComponent

## attempt 1

answer: built
class: FallTimesFallComponent
settings: {"short_period": 10, "long_period": 60}
reason: No component computes the product of two clipped falls over two horizons. `MeanAbsScaledFallTimesRiseComponent` multiplies a mean-abs-scaled fall by a rise, which is a different measure. No config step multiplies two components, so one new class computes this product.

table: Directional components
row: | `FallTimesFallComponent` | `short_period` (10), `long_period` (60) | max(0, -(close[t] / close[t-`short_period`] - 1)) x max(0, -(close[t] / close[t-`long_period`] - 1)) x 100 | 0 to below 100, never negative; no direction. It is 0 unless both the `short_period`-bar and the `long_period`-bar returns are negative, and it grows with the size of each fall | graded | fraction x percent (short fall as a fraction x long fall in percent) | `long_period` + 1 (61) | closes only (bars t, t-`short_period`, t-`long_period`). A NaN in any of those three closes gives NaN. A base close not above 0 gives NaN (never on real bars). These settings raise when the component is built: `short_period` < 1, `long_period` < 1, `short_period` >= `long_period` | stateless. Each factor is `PriceEvolutionOnPeriodComponent` / 100, negated and clipped at 0, at its own horizon. It is continuous in the closes and is exactly 0 on most bars. On 1d bars the defaults give the 10-day fall times the 60-day fall in percent. It is one-sided, a falling-situation reading. No `scaling_factor`: scale it with transforms |

```python class
class FallTimesFallComponent(SubStrategyComponent):
    """
    The product of two falls over two horizons, on every bar:

        F_s = max(0, -(close[t] / close[t - short_period] - 1))
        F_l = max(0, -(close[t] / close[t - long_period] - 1))
        raw_value = F_s x F_l x 100

    Range: 0 to below 100, never negative, no direction. It is 0 unless both returns are negative, and it
    grows with the size of each fall. It is graded and continuous in the closes, because the clips at 0 meet
    the product at 0.
    Warm-up: long_period + 1 rows, bar t included.

    NaN: a NaN close at t, t - short_period or t - long_period gives NaN. A base close not above 0 gives NaN
    (never on real bars).
    Building the component raises for a short_period below 1, a long_period below 1, or a short_period at
    or above long_period.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the rows up to and including bar t (the last
    row of data): close[t], close[t - short_period] and close[t - long_period].
    """

    def __init__(self, name="FallTimesFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 10))
        self.long_period = int(self.parameters.get("long_period", 60))
        if self.short_period < 1:
            raise ValueError(f"FallTimesFallComponent: short_period must be >= 1, got {self.short_period}")
        if self.long_period < 1:
            raise ValueError(f"FallTimesFallComponent: long_period must be >= 1, got {self.long_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"FallTimesFallComponent: short_period must be below long_period, got "
                f"{self.short_period} and {self.long_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float)
        c_t = float(close.iloc[-1])
        c_s = float(close.iloc[-(self.short_period + 1)])
        c_l = float(close.iloc[-(self.long_period + 1)])
        if np.isnan(c_t) or np.isnan(c_s) or np.isnan(c_l) or not c_s > 0 or not c_l > 0:
            self._raw_value = float("nan")
        else:
            f_s = max(0.0, -(c_t / c_s - 1.0))
            f_l = max(0.0, -(c_t / c_l - 1.0))
            self._raw_value = float(f_s * f_l * 100.0)
            self.debug_info = {"short_fall": f_s, "long_fall": f_l}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.long_period + 1
```

```python hand
def hand(df, params):
    s = int(params.get("short_period", 10))
    l = int(params.get("long_period", 60))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    now = c[last]
    base_s = c[last - s]
    base_l = c[last - l]
    for x in (now, base_s, base_l):
        if x != x:
            return float("nan")
    if not base_s > 0 or not base_l > 0:
        return float("nan")
    ret_s = (now - base_s) / base_s
    ret_l = (now - base_l) / base_l
    fall_s = -ret_s if ret_s < 0 else 0.0
    fall_l = -ret_l if ret_l < 0 else 0.0
    return fall_s * fall_l * 100.0
```

checks:
FallTimesFallComponent: every check passed
the bot's suite: == 1615 passed, 16 skipped, 75 deselected, 2244 warnings in 101.28s (0:01:41) ==
