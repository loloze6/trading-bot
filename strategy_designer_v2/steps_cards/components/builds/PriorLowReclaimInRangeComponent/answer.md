# PriorLowReclaimInRangeComponent: pilot_panic_run | 054-04_weak-reclaim-low-continuation_1d | ReclaimNearnessInRange

## attempt 1

answer: built
class: PriorLowReclaimInRangeComponent
settings: {"period": 30, "form": "nearness"}
reason: The wished value is 1 minus `PriorLowReclaimInRangeComponent`'s reading, over the same prior low L and the same pierce-and-reclaim condition, and 0 otherwise. That is the same measure's mirror. No config step gives 1 minus a value, so it becomes a `form` setting on that class. The default "reclaim" keeps today's output exactly.

table: Directional components
row: | `PriorLowReclaimInRangeComponent` | `period` (30), `form` ("reclaim") | With L = min(low[t-`period`] .. low[t-1]) (bar t excluded), x = (close[t] − L) / (high[t] − low[t]) when low[t] < L < close[t]. `form` "reclaim": x. `form` "nearness": 1 − x. Both are 0 when the condition does not hold | "reclaim": 0 to below 1, never negative; no direction. It nears 1 as the close sits at the day's high and the pierce is shallow. "nearness": 0, or above 0 and below 1 when the condition holds, never negative; no direction. It nears 1 as the close sits just above the pierced low against the day's range, and shrinks as the close climbs toward the day's high | graded | dimensionless (share of the bar's range) | `period` + 1 (31) | low (bars t-`period` .. t), high and close (bar t). A NaN in any value read gives NaN. A zero range cannot meet the condition on real bars and reads 0.0. These settings raise when the component is built: `period` < 1, `form` other than "reclaim" or "nearness" | stateless. `form` "reclaim" (default) is the original output, unchanged. "nearness" is 1 minus "reclaim" while the bar pierced and reclaimed L, and 0 otherwise. No config step gives 1 minus a value, hence the setting. The prior low excludes bar t, so bar t's own low cannot lower it. "reclaim" is continuous in close[t] (0 at close = L). "nearness" is 1 there and jumps to 0 where close[t] falls to L. Both jump where low[t] crosses L. A weak-reclaim reading, one-sided; `negate` gives the short forecast. No `scaling_factor`: scale it with transforms |

```python class
class PriorLowReclaimInRangeComponent(SubStrategyComponent):
    """
    Pierce-and-reclaim of the prior low, read inside bar t's range:

        L = min(low[t - period] .. low[t - 1])           (bar t excluded)
        condition: low[t] < L < close[t]                 (bar t pierced L and closed back above it)
        x = (close[t] - L) / (high[t] - low[t])
        form = "reclaim" (default): raw_value = x       when the condition holds, else 0.0
        form = "nearness":          raw_value = 1 - x   when the condition holds, else 0.0

    form "reclaim" is the original output, unchanged. On real bars, while the condition holds, x lies in
    (0, (high[t] - L) / (high[t] - low[t])], which is below 1. So "reclaim" is 0 to below 1, and "nearness"
    is 0, or above 0 and below 1. Both are never negative and have no direction. "nearness" grows as the
    close sits nearer the pierced low against the day's range.
    A zero range cannot meet the condition on real bars (close <= high = low < L) and reads 0.0.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads the `low` column of the last period + 1 rows (bars t-period .. t) and the
    `high` and `close` of the last row (bar t) only. All of them are known at bar t's close.

    NaN: a NaN low in bars t-period .. t, or a NaN high[t] or close[t], gives NaN.
    Building the component raises for a period below 1, or a form other than "reclaim" or "nearness".
    """

    def __init__(self, name="PriorLowReclaimInRange", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 1:
            raise ValueError(f"PriorLowReclaimInRangeComponent: period must be >= 1, got {self.period}")
        self.form = self.parameters.get("form", "reclaim")
        if self.form not in ("reclaim", "nearness"):
            raise ValueError(
                f"PriorLowReclaimInRangeComponent: form must be 'reclaim' or 'nearness', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.period
        lows = data['low'].astype(float).iloc[-(n + 1):]
        prior = lows.iloc[:-1]
        low_t = float(lows.iloc[-1])
        high_t = float(data['high'].astype(float).iloc[-1])
        close_t = float(data['close'].astype(float).iloc[-1])
        if prior.isna().any() or np.isnan(low_t) or np.isnan(high_t) or np.isnan(close_t):
            self._raw_value = float("nan")
            self.confidence = 1.0
            self.debug_info = {'prior_low': float("nan")}
            return
        L = float(prior.min())
        rng = high_t - low_t
        value = 0.0
        if low_t < L < close_t and rng > 0:
            share = (close_t - L) / rng
            value = share if self.form == "reclaim" else 1.0 - share
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'prior_low': L, 'range': rng, 'form': self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 30))
    form = params.get("form", "reclaim")
    lo = [float(x) for x in list(df["low"])]
    hi = [float(x) for x in list(df["high"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1
    # prior low over bars t-n .. t-1
    prior = []
    for k in range(1, n + 1):
        prior.append(lo[t - k])
    vals = prior + [lo[t], hi[t], cl[t]]
    for x in vals:
        if x != x:
            return float("nan")
    L = prior[0]
    for x in prior:
        if x < L:
            L = x
    low_t = lo[t]
    high_t = hi[t]
    close_t = cl[t]
    rng = high_t - low_t
    if not (low_t < L and L < close_t) or not rng > 0:
        return 0.0
    reclaim_share = (close_t - L) / rng
    if form == "nearness":
        return 1.0 - reclaim_share
    return reclaim_share
```

checks:
PriorLowReclaimInRangeComponent: every check passed
the bot's suite: == 1668 passed, 16 skipped, 75 deselected, 2244 warnings in 106.05s (0:01:46) ==
