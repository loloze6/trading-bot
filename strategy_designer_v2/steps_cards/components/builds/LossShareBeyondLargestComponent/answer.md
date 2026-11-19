# LossShareBeyondLargestComponent: slow_1h_run | 016-02_down-grind-price-continuation_1h | GrindShareOfFallComponent

## attempt 1

answer: built
class: LossShareBeyondLargestComponent
settings: {"period": 72, "k": 3}
reason: No component measures how much of a window's summed one-bar losses lies outside its `k` largest losses. `RiseBeyondLargestMovesComponent` is the nearest, but it outputs a residual log rise against the net move and is never negative, not a share of all losses signed by the net return. This is a new measure, so it is a new class.

table: Directional components
row: | `LossShareBeyondLargestComponent` | `period` (72), `k` (3) | sign(close[t] / close[t-`period`] - 1) x S, where S = 1 - T / L. L is the sum of all losses -r[j] over the one-bar returns r[j] = close[j] / close[j-1] - 1 with r[j] < 0, j = t-`period`+1 .. t. T is the sum of the `k` largest of those losses (all of them if there are `k` or fewer). S = 0 when there are `k` or fewer losses, or none | -1 to +1, exclusive; signed by the window's net return: negative over a net fall, positive over a net rise, 0 when the net return is 0. Its size is 0 when at most `k` losses carry the whole fall and nears 1 as the losses spread over many small bars | graded | dimensionless (share of the window's summed losses) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` >= `period` | stateless. The size is continuous in the closes. The sign flips where the window's net return crosses 0, so the value jumps there from +S to -S. Losses are simple returns, not log returns. Use `clip` with `max` 0 to keep only net falls. No `scaling_factor`: scale it with transforms |

```python class
class LossShareBeyondLargestComponent(SubStrategyComponent):
    """
    Share of a window's summed one-bar losses not carried by its k largest losses, signed by the window's net return:

        r[j] = close[j] / close[j-1] - 1,                 j = t-period+1 .. t
        losses = { -r[j] : r[j] < 0 }
        L = sum(losses)
        T = sum of the k largest losses (all of them if there are k or fewer)
        S = 1 - T / L    (S = 0 when there are k or fewer losses, which includes L = 0)
        raw_value = sign(close[t] / close[t-period] - 1) x S

    Range: -1 to +1, exclusive. The value is negative over a net fall, positive over a net rise and 0 when the net
    return is 0. Its size is 0 when the k biggest losing bars carry all the losses. It grows towards 1 as the
    losses spread over many small bars.
    Graded: S is continuous in the closes. The sign flips where the net return crosses 0.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN close in the last period + 1 rows gives NaN. A close not above 0 there also gives NaN (never on
    real bars).
    Building the component raises for period < 2, k < 1, or k >= period (every return counted: always 0).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, which end at bar t
    (the last row); a bar's close is known at that bar's close.
    """

    def __init__(self, name="LossShareBeyondLargest", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"LossShareBeyondLargestComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1:
            raise ValueError(f"LossShareBeyondLargestComponent: k must be >= 1, got {self.k}")
        if self.k >= self.period:
            raise ValueError(
                f"LossShareBeyondLargestComponent: k must be below period, got k={self.k}, period={self.period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data["close"].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[1:] / c[:-1] - 1.0
        losses = -r[r < 0]
        if len(losses) <= self.k:
            share = 0.0
        else:
            total = float(losses.sum())
            top = float(np.sort(losses)[::-1][:self.k].sum())
            share = max(0.0, 1.0 - top / total) if total > 0 else 0.0
        net = c[-1] / c[0] - 1.0
        self._raw_value = float(np.sign(net) * share)
        self.confidence = 1.0
        self.debug_info = {"loss_count": int(len(losses)), "share": share, "net_return": float(net)}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    w = []
    i = last - n
    while i <= last:
        w.append(c[i])
        i = i + 1
    for x in w:
        if x != x or not x > 0:
            return float("nan")
    losses = []
    j = 1
    while j < len(w):
        ret = w[j] / w[j - 1] - 1.0
        if ret < 0:
            losses.append(-ret)
        j = j + 1
    if len(losses) <= k:
        share = 0.0
    else:
        total = 0.0
        for x in losses:
            total = total + x
        srt = sorted(losses, reverse=True)
        top = 0.0
        m = 0
        while m < k:
            top = top + srt[m]
            m = m + 1
        share = 1.0 - top / total if total > 0 else 0.0
        if share < 0:
            share = 0.0
    net = w[-1] / w[0] - 1.0
    if net > 0:
        return share
    if net < 0:
        return -share
    return 0.0
```

checks:
LossShareBeyondLargestComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1554 passed, 8 skipped, 74 deselected, 2244 warnings in 52.58s ========
