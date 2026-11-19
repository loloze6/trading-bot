# TopVolumesShareComponent: slow_1h_run | 016-07_up-volume-burst-reversal_1h | VolumeConcentrationComponent

## attempt 1

answer: built
class: TopVolumesShareComponent
settings: {"period": 72, "top_k": 3}
reason: No component sums the `top_k` largest volumes of a window. `VolumeRatioComponent` only compares a mean or median of recent volume with a mean or median base, and no setting of it gives a top-k share. A new class computes this share of the window's total volume held by its `top_k` heaviest bars. It is named by what it measures, not as "concentration for a reversal".

table: Regime measures
row: | `TopVolumesShareComponent` | `period` (72), `top_k` (3) | (sum of the `top_k` largest volumes among volume[t-`period`+1 .. t]) / (sum of volume[t-`period`+1 .. t]), bar t included | `top_k`/`period` to 1 (0.0417 to 1 at the defaults), never negative; no direction; `top_k`/`period` when every bar of the window has the same volume, near 1 when a few bars carry almost all of it | graded | dimensionless (share of the window's volume) | `period` (72) | volume only. A NaN volume in the last `period` rows gives NaN; a total not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `top_k` < 1, `top_k` >= `period` (the output would be 1 on every bar) | stateless. Ties among the largest volumes do not change the sum. Continuous in the volumes. No `scaling_factor`: scale it with transforms |

```python class
class TopVolumesShareComponent(SubStrategyComponent):
    """
    Share of the window's volume carried by its heaviest bars, on every bar:

        W = volume[t - period + 1 .. t]                     (bar t included)
        T = sum of the top_k largest values of W
        raw_value = T / sum(W)

    Range: top_k / period (every bar the same volume) up to 1 (all the volume in top_k bars); never negative;
    no direction. Graded: continuous in the volumes, growing as the volume bunches into a few bars.
    Warm-up: period rows, bar t included.

    NaN: a NaN volume anywhere in W gives NaN; a sum(W) not above 0 gives NaN (never on real bars, whose volume
    is positive). A missing `volume` column raises.
    Building the component raises for period < 2, top_k < 1, or top_k >= period.

    WHY THIS CANNOT LEAK: it reads only the `volume` column of the last `period` rows of data, the last row being
    bar t; a bar's volume is known at that bar's close.
    """

    def __init__(self, name="TopVolumesShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopVolumesShareComponent: period must be >= 2, got {self.period}")
        self.top_k = int(self.parameters.get("top_k", 3))
        if self.top_k < 1:
            raise ValueError(f"TopVolumesShareComponent: top_k must be >= 1, got {self.top_k}")
        if self.top_k >= self.period:
            raise ValueError(
                f"TopVolumesShareComponent: top_k must be below period, got top_k={self.top_k}, "
                f"period={self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        w = data['volume'].astype(float).iloc[-self.period:].to_numpy()
        if np.isnan(w).any():
            self._raw_value = float("nan")
        else:
            total = float(np.sum(w))
            if not total > 0:
                self._raw_value = float("nan")
            else:
                top = float(np.sum(np.sort(w)[-self.top_k:]))
                self._raw_value = float(top / total)
                self.debug_info = {'top_volume_sum': top, 'total_volume': total}
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period
```

```python hand
def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("top_k", 3))
    v = [float(x) for x in list(df["volume"])]
    last = len(v) - 1
    window = []
    i = last - n + 1
    while i <= last:
        window.append(v[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
    total = 0.0
    for x in window:
        total = total + x
    if not total > 0:
        return float("nan")
    remaining = list(window)
    top = 0.0
    picked = 0
    while picked < k:
        best_idx = 0
        j = 1
        while j < len(remaining):
            if remaining[j] > remaining[best_idx]:
                best_idx = j
            j = j + 1
        top = top + remaining[best_idx]
        remaining.pop(best_idx)
        picked = picked + 1
    return top / total
```

checks:
TopVolumesShareComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1557 passed, 8 skipped, 74 deselected, 2244 warnings in 46.82s ========
