# not built: slow_1h_run | 016-01_up-grind-price-continuation_1h | grind-share-of-rise

## attempt 1

answer: built
class: RiseBeyondLargestMovesComponent
settings: {"period": 72, "top_k": 3}
reason: No catalogue component isolates the part of a multi-bar rise that does not come from its few largest one-bar moves. The wished value R x (1 - min(T / R, 1)) when R > 0, else 0, equals max(0, R - T), so one new class computes it.

table: Regime measures
row: | `RiseBeyondLargestMovesComponent` | `period` (72), `top_k` (3) | max(0, R − T), which equals R x (1 − min(T / R, 1)) when R > 0 and 0 otherwise. R = ln(close[t] / close[t-`period`]). T = the sum of the `top_k` largest positive one-bar log returns ln(close[j] / close[j-1]), j = t-`period`+1 .. t (all positive ones if fewer than `top_k`) | 0 and up, never negative, never above R; no direction. 0 when the window fell or when its biggest up-moves account for the whole rise; grows as the rise gets larger and less of it comes from its biggest bars | regime measure | log return (natural log units) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `top_k` < 1, `top_k` > `period` | stateless; graded, continuous in the closes (a clip at 0, like `VolatilityRankedFallComponent`). Not a percent: multiply by 100 with a `scale` transform for percent units. No `scaling_factor` |

```python class
class RiseBeyondLargestMovesComponent(SubStrategyComponent):
    """
    The part of a multi-bar rise that does not come from its largest one-bar moves (a "grind" reading):

        R = ln(close[t] / close[t - period])
        r_j = ln(close[j] / close[j-1]),  j = t - period + 1 .. t
        T = sum of the top_k largest positive r_j (all positive ones if fewer than top_k; 0 if none)
        raw_value = max(0, R - T)      ( = R x (1 - min(T / R, 1)) when R > 0, else 0 )

    Range: 0 and up, never negative, never above R. It is 0 when the window fell, or when its top_k
    biggest up-moves account for the whole rise. It grows continuously as the rise gets larger and as
    less of it comes from its biggest bars. No direction. Units: natural log return.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t
    (the last row) included; a bar's close is known at that bar's close.

    NaN: a NaN close in the last period + 1 rows gives NaN; a close not above 0 there gives NaN
    (never on real bars). A missing `close` column raises.
    Building the component raises for a period below 2, a top_k below 1 or a top_k above period.
    """

    def __init__(self, name="RiseBeyondLargestMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"RiseBeyondLargestMovesComponent: period must be >= 2, got {self.period}")
        self.top_k = int(self.parameters.get("top_k", 3))
        if self.top_k < 1 or self.top_k > self.period:
            raise ValueError(
                f"RiseBeyondLargestMovesComponent: top_k must be between 1 and period, got {self.top_k}")
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
        lr = np.diff(np.log(c))
        rise = float(np.log(c[-1] / c[0]))
        pos = np.sort(lr[lr > 0])[::-1][:self.top_k]
        top = float(pos.sum()) if len(pos) > 0 else 0.0
        self._raw_value = float(max(0.0, rise - top))
        self.confidence = 1.0
        self.debug_info = {'rise_log': rise, 'top_k_sum': top}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("period", 72))
    k = int(params.get("top_k", 3))
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
    R = math.log(w[-1] / w[0])
    rets = []
    j = 1
    while j < len(w):
        rets.append(math.log(w[j] / w[j - 1]))
        j = j + 1
    positives = [r for r in rets if r > 0]
    positives.sort(reverse=True)
    T = 0.0
    m = 0
    while m < k and m < len(positives):
        T = T + positives[m]
        m = m + 1
    if R > 0:
        return max(R, 0.0) * (1.0 - min(T / R, 1.0))
    return 0.0
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json

## attempt 2

answer: built
class: RiseNetOfLargestMovesComponent
settings: {"period": 72, "top_k": 3}
reason: No component measures how much of a multi-bar log rise is left after its few biggest up-bars. The output is max(R, 0) x (1 - min(T / R, 1)), which equals max(0, R - T). This version computes it on a float64 slice of exactly the last `period` + 1 closes, so its value does not depend on how much history the run has fed it. It sums the top `k` returns in a fixed descending order and takes each log return as ln(close[i] / close[i-1]), the same form as R.
table: Regime measures
row: | `RiseNetOfLargestMovesComponent` | `period` (72), `top_k` (3) | R = ln(close[t] / close[t-`period`]); T = sum of the `top_k` largest strictly positive one-bar log returns ln(close[i] / close[i-1]), i = t-`period`+1 .. t (all of them if fewer are positive, 0 if none); output R x (1 - min(T / R, 1)) when R > 0, else 0 (equal to max(0, R - T)) | 0 and up, at most R, never negative; no direction; 0 when the window fell or when its `top_k` biggest bars account for the whole rise | graded | natural-log return | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `top_k` < 1, `top_k` >= `period` | stateless; the steady "grind" part of a rise, the share that is not in its few largest bars, in log-return units. Computed on a fixed slice, so it does not depend on the run's history length. No `scaling_factor`: scale it with transforms |

```python class
class RiseNetOfLargestMovesComponent(SubStrategyComponent):
    """
    The part of a multi-bar rise that does not come from its few largest up-bars, on every bar:

        c = close[t - period .. t]                    (period + 1 closes, bar t included)
        R = ln(close[t] / close[t - period])
        r_i = ln(close[i] / close[i - 1]),  i = t - period + 1 .. t
        T = sum of the top_k largest r_i that are > 0 (all positive ones if fewer, 0 if none)
        raw_value = R x (1 - min(T / R, 1))  if R > 0,  else 0.0      (= max(0, R - T))

    Range and sign: 0 and up, at most R, never negative; no direction. It grows as the rise gets larger and as less
    of it comes from its largest bars; 0 when the window fell or when its top_k bars carry the whole rise.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, the last being bar t;
    a bar's close is known at that bar's close.

    NaN: a NaN close in the last period + 1 rows gives NaN; a close not above 0 there gives NaN (never on real
    bars). Building the component raises for a period below 2, a top_k below 1, or a top_k not below period.
    """

    def __init__(self, name="RiseNetOfLargestMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"RiseNetOfLargestMovesComponent: period must be >= 2, got {self.period}")
        self.top_k = int(self.parameters.get("top_k", 3))
        if self.top_k < 1 or self.top_k >= self.period:
            raise ValueError(
                f"RiseNetOfLargestMovesComponent: top_k must be between 1 and period - 1, got {self.top_k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].iloc[-(self.period + 1):].to_numpy(dtype=np.float64)
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        R = float(np.log(c[-1] / c[0]))
        rets = [float(np.log(c[j] / c[j - 1])) for j in range(1, len(c))]
        pos = sorted([x for x in rets if x > 0.0], reverse=True)
        T = 0.0
        for x in pos[:self.top_k]:
            T = T + x
        if R > 0.0:
            value = R * (1.0 - min(T / R, 1.0))
        else:
            value = 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'log_rise': R, 'top_k_sum': T}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("period", 72))
    k = int(params.get("top_k", 3))
    closes = [float(x) for x in list(df["close"])]
    w = closes[len(closes) - (n + 1):]
    for x in w:
        if x != x or not x > 0:
            return float("nan")
    R = math.log(w[n] / w[0])
    positives = []
    i = 1
    while i <= n:
        r = math.log(w[i] / w[i - 1])
        if r > 0.0:
            positives.append(r)
        i = i + 1
    T = 0.0
    taken = 0
    while taken < k and len(positives) > 0:
        best = 0
        j = 1
        while j < len(positives):
            if positives[j] > positives[best]:
                best = j
            j = j + 1
        T = T + positives[best]
        positives.pop(best)
        taken = taken + 1
    if R > 0.0:
        share = T / R
        if share > 1.0:
            share = 1.0
        return max(R, 0.0) * (1.0 - share)
    return 0.0
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json

## attempt 3

answer: built
class: RiseBeyondLargestMovesComponent
settings: {"period": 72, "k": 3}
reason: No component measures how much of a window's log rise is left after its k largest one-bar up-moves are taken out, so this is a new class. The output equals max(R, 0) x (1 - min(T / R, 1)) and is computed as max(0, R - T). That form needs no division by a near-zero R, so it gives the same value whatever the data window and no ratio rounding can tip it near R = 0.

table: Directional components
row: | `RiseBeyondLargestMovesComponent` | `period` (72), `k` (3) | max(0, R - T), with R = ln(close[t] / close[t-`period`]) and T = the sum of the `k` largest strictly positive one-bar log returns ln(close[j] / close[j-1]), j = t-`period`+1 .. t (all of them if fewer than `k` are positive). This equals max(R, 0) x (1 - min(T / R, 1)) when R > 0, and 0 otherwise | 0 and up, never negative; 0 when the window fell or when its `k` biggest up-moves account for the whole rise; grows as the rise gets larger and less of it comes from its biggest bars | graded | natural log return | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 there gives NaN. These settings raise when the component is built: `period` < 2, `k` < 1, `k` >= `period` | stateless; one-sided (a grind-continuation reading); reads a fixed window of `period` + 1 rows, so it does not depend on how many bars the run has seen. No `scaling_factor`: scale it with transforms |

```python class
class RiseBeyondLargestMovesComponent(SubStrategyComponent):
    """
    The part of the window's log rise that its k largest one-bar up-moves do not explain:

        r_j = ln(close[j] / close[j-1]),  j = t - period + 1 .. t        (period one-bar log returns)
        R   = ln(close[t] / close[t - period])                            (the period-bar log return)
        T   = sum of the k largest strictly positive r_j (all positive r_j if fewer than k)
        raw_value = max(0, R - T)

    This equals max(R, 0) x (1 - min(T / R, 1)) when R > 0, and 0 otherwise.
    Range: 0 and up, never negative. It is 0 when the window fell, or when its k biggest up-moves account for the
    whole rise. It grows continuously as the rise gets larger and as less of it comes from its biggest bars.
    Units: natural log return.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN close, or a close not above 0, in the last period + 1 rows gives NaN.
    Building the component raises for period < 2, k < 1 or k >= period.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data (bars t - period .. t,
    bar t being the last row); each close is known at its bar's close.
    """

    def __init__(self, name="RiseBeyondLargestMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"RiseBeyondLargestMovesComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k >= self.period:
            raise ValueError(f"RiseBeyondLargestMovesComponent: k must be >= 1 and < period, got {self.k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = [float(x) for x in data['close'].iloc[-(self.period + 1):].tolist()]
        for c in closes:
            if not (c == c) or not c > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        logs = [float(np.log(c)) for c in closes]
        rets = [logs[i] - logs[i - 1] for i in range(1, len(logs))]
        big_r = logs[-1] - logs[0]
        positives = sorted([r for r in rets if r > 0], reverse=True)
        top_t = 0.0
        for r in positives[:self.k]:
            top_t += r
        value = big_r - top_t
        self._raw_value = float(value) if value > 0 else 0.0
        self.confidence = 1.0
        self.debug_info = {'rise': big_r, 'top_k_up_moves': top_t}

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
    w = c[len(c) - n - 1:]
    for x in w:
        if x != x or not x > 0:
            return float("nan")
    rets = []
    i = 1
    while i < len(w):
        rets.append(math.log(w[i]) - math.log(w[i - 1]))
        i = i + 1
    R = math.log(w[-1]) - math.log(w[0])
    pos = [r for r in rets if r > 0]
    pos.sort()
    pos.reverse()
    T = 0.0
    j = 0
    while j < len(pos) and j < k:
        T = T + pos[j]
        j = j + 1
    if not R > 0:
        return 0.0
    share = T / R
    if share > 1.0:
        share = 1.0
    return R * (1.0 - share)
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json
