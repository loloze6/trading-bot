# TopGainsShareOfRiseComponent: slow_1h_run | 016-03_up-jump-price-reversal_1h | TopGainsShareOfRiseComponent

## attempt 1

answer: built
class: TopGainsShareOfRiseComponent
settings: {"period": 72, "k": 3}
reason: No component gives the share of a window's net simple rise that its `k` largest one-bar gains carry. `RiseBeyondLargestMovesComponent` outputs the leftover log rise max(0, R − T), which is in log-return units and is not this share or its mirror. `LossShareBeyondLargestComponent` measures losses, not gains. So one new class computes this ratio.

table: Regime measures
row: | `TopGainsShareOfRiseComponent` | `period` (72), `k` (3) | min(T / R, 1) when R > 0, else 0. R = close[t] / close[t-`period`] - 1 is the net simple rise. T is the sum of the `k` largest positive one-bar returns close[j] / close[j-1] - 1, j = t-`period`+1 .. t (all the positive ones if there are fewer than `k`) | 0 to 1, never negative, no direction. Near 0 when the rise is a grind of many small up-bars. 1 when the `k` largest up-bars carry all of the rise or more. 0 when the window did not rise | graded | dimensionless (share of the net rise) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN. A close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` >= `period` | stateless. Continuous in the closes while the window rose, but it jumps from 1 to 0 where the net return crosses 0, because a tiny positive rise is capped at 1 and a fall reads 0. Use it in a regime rule together with a rise condition. Simple returns, not log returns. Not 1 minus `RiseBeyondLargestMovesComponent`, which is the residual log rise in log units. No `scaling_factor`: scale it with transforms |

```python class
class TopGainsShareOfRiseComponent(SubStrategyComponent):
    """
    The share of the window's net rise carried by its k largest one-bar gains, on every bar:

        R = close[t] / close[t - period] - 1                          (net simple rise of the window)
        r[j] = close[j] / close[j-1] - 1, j = t - period + 1 .. t     (the period one-bar returns, bar t's included)
        T = sum of the k largest positive r[j] (all the positive ones if there are fewer than k)
        raw_value = min(T / R, 1.0) if R > 0, else 0.0

    Range 0 to 1, never negative, no direction. Near 0 when the rise is a grind of many small up-bars. It grows
    toward 1 as the rise comes from fewer, bigger bars. It is 1 when the k largest gains carry the whole rise or
    more, and 0 when the window did not rise. Graded while the window rose. It jumps from 1 to 0 where the net
    return crosses 0 (a tiny positive rise is capped at 1).
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data (bars
    t - period .. t, the last row being bar t); a bar's close is known at that bar's close.

    NaN: a NaN close in the last period + 1 rows gives NaN; a close not above 0 there gives NaN (never on real
    bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, or a k of period or more.
    """

    def __init__(self, name="TopGainsShareOfRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopGainsShareOfRiseComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k >= self.period:
            raise ValueError(
                f"TopGainsShareOfRiseComponent: k must be between 1 and period - 1, got {self.k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).iloc[-(self.period + 1):].to_numpy()
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[1:] / c[:-1] - 1.0
        net = float(c[-1] / c[0] - 1.0)
        if not net > 0:
            share = 0.0
            top = 0.0
        else:
            pos = np.sort(r[r > 0])[::-1]
            top = float(pos[:self.k].sum())
            share = float(min(top / net, 1.0))
        self._raw_value = share
        self.confidence = 1.0
        self.debug_info = {'net_rise': net, 'top_k_gains': top}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    p = int(params.get("period", 72))
    k = int(params.get("k", 3))
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    window = []
    i = last - p
    while i <= last:
        window.append(closes[i])
        i = i + 1
    for x in window:
        if x != x or not x > 0:
            return float("nan")
    gains = []
    j = 1
    while j < len(window):
        ret = window[j] / window[j - 1] - 1.0
        if ret > 0:
            gains.append(ret)
        j = j + 1
    rise = window[-1] / window[0] - 1.0
    if not rise > 0:
        return 0.0
    gains.sort(reverse=True)
    total = 0.0
    n = 0
    for g in gains:
        if n >= k:
            break
        total = total + g
        n = n + 1
    share = total / rise
    if share > 1.0:
        share = 1.0
    return share
```

checks:
TopGainsShareOfRiseComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1555 passed, 8 skipped, 74 deselected, 2244 warnings in 48.72s ========
