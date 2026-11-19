# RiseBeyondLargestMovesComponent: slow_1h_run | 016-01_up-grind-price-continuation_1h | grind-share-of-rise

## attempt 1

answer: built
class: RiseBeyondLargestMovesComponent
settings: {"period": 72, "k": 3}
reason: No component in the catalogue measures how much of a window's log rise is left after its k largest up-bars are taken out, so this is a new measure. The wished formula max(R, 0) x (1 - min(T / R, 1)) equals R - min(T, R) when R > 0 and 0 otherwise, which is max(0, R - T) on every bar because T is never negative.

table: Regime measures
row: | `RiseBeyondLargestMovesComponent` | `period` (72), `k` (3) | max(0, R - T), R = ln(close[t] / close[t-`period`]), T = the sum of the `k` largest positive one-bar log returns ln(close[j] / close[j-1]), j = t-`period`+1 .. t (all the positive ones if there are fewer than `k`); equal to max(R, 0) x (1 - min(T / R, 1)) | 0 and up, never negative, at most R; no direction; 0 when the window fell, when it is flat, or when its `k` largest up-bars make up all of the rise; grows as the rise gets larger and less of it comes from its biggest bars | graded | log return (natural log units) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` >= `period` (with every bar counted the output would be 0 on every bar) | stateless; the part of the window's log rise not carried by its `k` largest up-bars. It is often exactly 0 (any window that did not rise), but it is continuous in the closes. No `scaling_factor`: scale it with transforms |

```python class
class RiseBeyondLargestMovesComponent(SubStrategyComponent):
    """
    The part of a window's log rise that its k largest up-bars do not account for, on every bar:

        R = ln(close[t]) - ln(close[t - period])                      (the period-bar log return)
        r_j = ln(close[j]) - ln(close[j - 1]),  j = t - period + 1 .. t
        T = sum of the k largest positive r_j (all positive r_j if fewer than k are positive; 0 if none)
        raw_value = max(0, R - T)

    This is the same value as max(R, 0) x (1 - min(T / R, 1)) for R > 0, and 0 for R <= 0, because T >= 0.
    Graded, no direction: 0 and up, never negative, at most R. It is 0 when the window did not rise or when
    its k biggest up-bars carry all of the rise. It grows as the rise gets larger and less of it sits in those bars.
    Units: natural-log return.
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close in the last period + 1 rows gives NaN. A close that is not above 0 there gives NaN
    (never seen on real bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, or a k of period or more (with every bar
    counted, T >= R and the output would be 0 on every bar).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t (the last
    row) included. No later row exists in the data it is given.
    """

    def __init__(self, name="RiseBeyondLargestMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"RiseBeyondLargestMovesComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k >= self.period:
            raise ValueError(
                f"RiseBeyondLargestMovesComponent: k must be between 1 and period - 1, got {self.k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        logc = np.log(c)
        lr = np.diff(logc)
        total_rise = float(logc[-1] - logc[0])
        pos = np.sort(lr[lr > 0])[::-1][:self.k]
        top = float(pos.sum()) if pos.size else 0.0
        self._raw_value = float(max(0.0, total_rise - top))
        self.confidence = 1.0
        self.debug_info = {'log_rise': total_rise, 'top_k_up_sum': top}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    window = []
    i = last - n
    while i <= last:
        window.append(c[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
        if not x > 0:
            return float("nan")
    R = math.log(window[-1] / window[0])
    ups = []
    j = 1
    while j < len(window):
        r = math.log(window[j] / window[j - 1])
        if r > 0:
            ups.append(r)
        j = j + 1
    ups.sort(reverse=True)
    T = 0.0
    m = 0
    while m < k and m < len(ups):
        T = T + ups[m]
        m = m + 1
    if R > 0:
        share = T / R
        if share > 1.0:
            share = 1.0
        return R * (1.0 - share)
    return 0.0
```

checks:
RiseBeyondLargestMovesComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1553 passed, 8 skipped, 74 deselected, 2244 warnings in 56.58s ========
