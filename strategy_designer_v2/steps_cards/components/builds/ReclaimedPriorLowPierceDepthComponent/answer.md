# ReclaimedPriorLowPierceDepthComponent: pilot_panic_run | 054-01_deep-reclaimed-low-pierce-rebound_1d | PriorLowPierceDepth

## attempt 1

answer: built
class: ReclaimedPriorLowPierceDepthComponent
settings: {"period": 30}
reason: No component reads how far bar t's own low went under the prior `period`-bar low while the close is back at or above that low. The closest, `DistanceFromHighComponent` (`extreme` "low", `source` "high", `exclude_current` 1), measures the close's distance from L, not the low's pierce, and it has no reclaim gate.

table: Directional components
row: | `ReclaimedPriorLowPierceDepthComponent` | `period` (30) | max(0, L − low[t]) / L x 100 when close[t] >= L, else 0, with L = min(low[t-`period`] .. low[t-1]) (bar t excluded) | 0 to below 100, never negative; no direction; 0 when bar t's low did not go under L or when the close stayed under L; grows linearly with the depth of the pierce | graded | percent of the prior low | `period` + 1 (31) | low (bars t-`period` .. t), close (bar t). A NaN in any value read gives NaN. An L not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1 | stateless. The prior low excludes bar t, so bar t's own low cannot lower it. The value is continuous in low[t]. It jumps between 0 and the depth where close[t] crosses L. A pierce-and-reclaim (spring) reading, one-sided, a rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class ReclaimedPriorLowPierceDepthComponent(SubStrategyComponent):
    """
    Depth of bar t's pierce under the prior low, counted only when the close reclaims that low:

        L = min(low[t - period] .. low[t - 1])          (bar t excluded)
        raw_value = max(0, L - low[t]) / L x 100   if close[t] >= L
        raw_value = 0.0                             otherwise

    Range: 0 to below 100, never negative, no direction. It is 0 when low[t] >= L (no pierce) or
    when close[t] < L (not reclaimed). It grows linearly as the day's low sinks deeper under L.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN low in bars t-period .. t, or a NaN close[t], gives NaN. An L not above 0 gives NaN
    (never on real bars). Building raises for a period below 1.

    WHY THIS CANNOT LEAK: it reads only the `low` column of bars t-period .. t and the `close` of
    bar t (the last row of data); every one of those values is known at bar t's close.
    """

    def __init__(self, name="ReclaimedPriorLowPierceDepth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 1:
            raise ValueError(
                f"ReclaimedPriorLowPierceDepthComponent: period must be >= 1, got {self.period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        low = data["low"].astype(float).to_numpy()
        close_t = float(data["close"].astype(float).to_numpy()[-1])
        prior = low[-(self.period + 1):-1]
        low_t = float(low[-1])
        if np.isnan(prior).any() or np.isnan(low_t) or np.isnan(close_t):
            self._raw_value = float("nan")
        else:
            L = float(np.min(prior))
            if not L > 0:
                self._raw_value = float("nan")
            elif close_t >= L:
                self._raw_value = float(max(0.0, L - low_t) / L * 100.0)
            else:
                self._raw_value = 0.0
            self.debug_info = {"prior_low": L, "low_t": low_t, "close_t": close_t}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 30))
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(lows) - 1
    low_t = lows[t]
    close_t = closes[t]
    if low_t != low_t or close_t != close_t:
        return float("nan")
    L = None
    for i in range(t - n, t):
        x = lows[i]
        if x != x:
            return float("nan")
        if L is None or x < L:
            L = x
    if not L > 0:
        return float("nan")
    if close_t < L:
        return 0.0
    depth = L - low_t
    if depth < 0:
        depth = 0.0
    return depth / L * 100.0
```

checks:
ReclaimedPriorLowPierceDepthComponent: every check passed
the bot's suite: == 1667 passed, 16 skipped, 75 deselected, 2244 warnings in 118.63s (0:01:58) ==
