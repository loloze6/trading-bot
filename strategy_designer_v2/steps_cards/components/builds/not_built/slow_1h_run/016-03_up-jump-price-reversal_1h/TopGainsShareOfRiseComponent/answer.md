# not built: slow_1h_run | 016-03_up-jump-price-reversal_1h | TopGainsShareOfRiseComponent

## attempt 1

answer: built
class: TopGainsShareOfRiseComponent
settings: {"period": 72, "k": 3}
reason: No component in the catalogue compares the sum of a window's largest one-bar gains with the window's net rise. The nearest ones are `EfficiencyRatioRegimeComponent`, which uses the sum of absolute changes, and `PriceEvolutionComponent`, which uses the net move alone. Neither has a top-k statistic, so this is a new measure, computed from closes only.

table: Regime measures
row: | `TopGainsShareOfRiseComponent` | `period` (72), `k` (3) | R = close[t] / close[t-`period`] - 1; S = sum of the `k` largest positive values among the `period` one-bar returns close[j] / close[j-1] - 1, j = t-`period`+1 .. t (all the positive ones if fewer than `k`); output min(1, S / R) when R > 0, else 0.0 | 0 to 1, never negative; no direction; 0 when the net move over `period` bars is not above 0; above 0 on any net rise, near 0 for a rise made of many small gains (a grind), 1 when the `k` biggest gains alone reach or exceed the whole rise | regime measure | dimensionless (share of the net rise) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 among the bases gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` > `period` | stateless. S uses simple returns that are not compounded, so S can exceed R; the cap at 1 binds then. The value is graded within net rises, but it falls from its cap to 0 when the net move crosses 0: use it in a regime rule together with a net-rise condition, not as a forecast source. No `scaling_factor`: scale it with transforms |

```python class
class TopGainsShareOfRiseComponent(SubStrategyComponent):
    """
    The share of a net rise that its few biggest one-bar gains account for, on every bar:

        r_j = close[j] / close[j-1] - 1,            j = t - period + 1 .. t   (period returns)
        R   = close[t] / close[t - period] - 1      (net move over the window)
        S   = sum of the k largest positive r_j     (all positive r_j if fewer than k)
        raw_value = min(1, S / R) if R > 0, else 0.0

    Range: 0 to 1, never negative, no direction. It is 0 when the net move is not above 0 and above 0 on any net
    rise, because a net rise has at least one positive return. It is near 0 when the rise is a grind of many small
    gains, and it reaches 1 when the k biggest gains alone make up (or exceed: the returns are simple, not
    compounded) the whole rise. Graded within net rises; it drops from its cap to 0 when the net move crosses 0.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, rows t - period
    .. t; bar t is the last row, and its close is known at that bar's close.

    NaN: a NaN close among those rows gives NaN. A close not above 0 among rows t - period .. t - 1 (the return
    bases) gives NaN, which never happens on real bars. A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, or a k above period.
    """

    def __init__(self, name="TopGainsShareOfRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopGainsShareOfRiseComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k > self.period:
            raise ValueError(f"TopGainsShareOfRiseComponent: k must be between 1 and period, got {self.k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).iloc[-(self.period + 1):].to_numpy()
        if np.isnan(c).any() or not (c[:-1] > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = c[1:] / c[:-1] - 1.0
        pos = np.sort(r[r > 0])[::-1]
        s = float(pos[:self.k].sum())
        net = float(c[-1] / c[0] - 1.0)
        if net > 0:
            self._raw_value = float(min(1.0, s / net))
        else:
            self._raw_value = 0.0
        self.confidence = 1.0
        self.debug_info = {'top_gains_sum': s, 'net_rise': net}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
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
    i = 0
    while i < n:
        if not window[i] > 0:
            return float("nan")
        i = i + 1
    gains = []
    i = 1
    while i <= n:
        g = window[i] / window[i - 1] - 1.0
        if g > 0:
            gains.append(g)
        i = i + 1
    total = 0.0
    taken = 0
    while taken < k and len(gains) > 0:
        best = 0
        j = 1
        while j < len(gains):
            if gains[j] > gains[best]:
                best = j
            j = j + 1
        total = total + gains[best]
        gains.pop(best)
        taken = taken + 1
    rise = window[n] / window[0] - 1.0
    if not rise > 0:
        return 0.0
    share = total / rise
    if share > 1.0:
        return 1.0
    return share
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json

## attempt 2

answer: built
class: TopGainsShareOfRiseComponent
settings: {"period": 72, "k": 3}
reason: No catalogue component measures how much of a net rise comes from its few largest one-bar gains. This new class computes that share from closes only. It sums the `k` largest positive returns in a fixed descending order, so the class and the hand computation give the same floating-point result.

table: Regime measures
row: | `TopGainsShareOfRiseComponent` | `period` (72), `k` (3) | R = close[t] / close[t-`period`] - 1; G = the sum of the `k` largest positive values among the `period` one-bar returns close[j] / close[j-1] - 1, j = t-`period`+1 .. t (fewer if fewer are positive), summed largest first; output = 0 when R is not above 0, else min(1, G / R) | 0 to 1, never negative; no direction; near 0 for a broad grind up, 1 when the few biggest bars make up the whole rise (and 0 on a net fall or flat) | regime measure | dimensionless (share of the net rise) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 among them gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` > `period` | stateless. The returns are simple returns, not log returns, and the net rise is compounded, so G / R can exceed 1 before the cap. The value drops from up to 1 to 0 as the net move crosses 0. No `scaling_factor`: scale it with transforms |

```python class
class TopGainsShareOfRiseComponent(SubStrategyComponent):
    """
    Share of the net rise made by the few largest one-bar gains, on every bar:

        r_j = close[j] / close[j-1] - 1,  j = t-period+1 .. t      (period one-bar returns, bar t's included)
        R   = close[t] / close[t-period] - 1                        (the net move over the window)
        G   = sum of the k largest r_j that are > 0 (fewer if fewer are positive), summed largest first
        raw_value = 0.0                if R is not above 0
                    min(1.0, G / R)    otherwise

    Range 0 to 1, never negative, no direction. It is near 0 when the rise is spread over many small bars (a
    grind) and grows toward 1 as the rise comes from fewer, bigger bars. It is 0 on a net fall or a flat window.
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close among the last period + 1 rows gives NaN; a close not above 0 among them gives NaN
    (never on real bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, or a k above period.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t (the last
    row) included; every close it uses is known at bar t's close.
    """

    def __init__(self, name="TopGainsShareOfRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopGainsShareOfRiseComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k > self.period:
            raise ValueError(f"TopGainsShareOfRiseComponent: k must be between 1 and period, got {self.k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        tail = data['close'].iloc[-(self.period + 1):].astype(float).to_numpy()
        closes = [float(x) for x in tail]
        for c in closes:
            if c != c or not c > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        rets = []
        for j in range(1, len(closes)):
            rets.append(closes[j] / closes[j - 1] - 1.0)
        net = closes[-1] / closes[0] - 1.0
        positives = sorted([r for r in rets if r > 0.0], reverse=True)
        gains = 0.0
        for r in positives[:self.k]:
            gains = gains + r
        if not net > 0.0:
            value = 0.0
        else:
            value = gains / net
            if value > 1.0:
                value = 1.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'net_rise': net, 'top_gains_sum': gains}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
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
    rets = []
    i = 1
    while i < len(window):
        rets.append(window[i] / window[i - 1] - 1.0)
        i = i + 1
    net = window[-1] / window[0] - 1.0
    pool = []
    for r in rets:
        if r > 0.0:
            pool.append(r)
    picked = []
    while len(picked) < k and len(pool) > 0:
        best = 0
        m = 1
        while m < len(pool):
            if pool[m] > pool[best]:
                best = m
            m = m + 1
        picked.append(pool[best])
        pool.pop(best)
    total = 0.0
    for r in picked:
        total = total + r
    if not net > 0.0:
        return 0.0
    share = total / net
    if share > 1.0:
        share = 1.0
    return share
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json

## attempt 3

answer: built
class: TopGainsShareOfRiseComponent
settings: {"period": 72, "k": 3}
reason: No component in the catalogue measures how much of a net rise came from its few largest one-bar gains, so a new class is needed. This version returns NaN for a NaN close in the window instead of reading it as "no rise" and giving 0. It also does all arithmetic as plain floats in a fixed order, so it matches the hand computation exactly.

table: Regime measures
row: | `TopGainsShareOfRiseComponent` | `period` (72), `k` (3) | min(1, S / N), with N = close[t] / close[t-`period`] - 1 and S = the sum of the `k` largest positive values among the `period` one-bar returns close[j] / close[j-1] - 1, j = t-`period`+1 .. t (fewer than `k` if fewer are positive); 0 when N is not above 0 | 0 to 1, never negative; no direction; near 0 for a rise spread over many bars, 1 when the top `k` bars carry the whole rise or more | regime measure | dimensionless (share of the net rise) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` > `period` | stateless. The returns are simple and the net rise is compounded, so S can exceed N; the cap at 1 binds then. No `scaling_factor`: scale it with transforms |

```python class
class TopGainsShareOfRiseComponent(SubStrategyComponent):
    """
    Share of the net rise carried by the few largest one-bar gains, on every bar:

        r(j) = close[j] / close[j-1] - 1,  j = t-period+1 .. t      (the last `period` one-bar returns)
        N    = close[t] / close[t-period] - 1                       (the net move over the window)
        S    = sum of the k largest positive r(j)                   (all positive ones if fewer than k)
        raw_value = min(1, S / N) when N > 0, else 0.0

    Graded, with no direction: 0 to 1, never negative. It is near 0 when the rise is a grind spread over many bars.
    It rises toward 1 as the rise comes from fewer, bigger bars, and it is 1 when the top k bars carry the whole
    net rise or more.
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close in the last period + 1 rows gives NaN, never 0. A close not above 0 there gives NaN, which
    never happens on real bars.
    Building the component raises for a period below 2, a k below 1, or a k above period.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, which end at bar t
    (the last row); a bar's close is known at that bar's close.
    """

    def __init__(self, name="TopGainsShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopGainsShareOfRiseComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k > self.period:
            raise ValueError(f"TopGainsShareOfRiseComponent: k must be between 1 and period, got {self.k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = [float(x) for x in data['close'].iloc[-(self.period + 1):].tolist()]
        bad = False
        for c in closes:
            if c != c or not c > 0:
                bad = True
                break
        if bad:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = []
        for i in range(1, len(closes)):
            rets.append(closes[i] / closes[i - 1] - 1.0)
        net = closes[-1] / closes[0] - 1.0
        if not net > 0:
            value = 0.0
            top_sum = 0.0
        else:
            pos = sorted([r for r in rets if r > 0], reverse=True)[:self.k]
            top_sum = 0.0
            for r in pos:
                top_sum = top_sum + r
            value = top_sum / net
            if value > 1.0:
                value = 1.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'net_rise': net, 'top_gains_sum': top_sum}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
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
        if x != x:
            return float("nan")
        if not x > 0:
            return float("nan")
    net = w[n] / w[0] - 1.0
    if not net > 0:
        return 0.0
    gains = []
    j = 1
    while j <= n:
        r = w[j] / w[j - 1] - 1.0
        if r > 0:
            gains.append(r)
        j = j + 1
    total = 0.0
    taken = 0
    while taken < k and len(gains) > 0:
        best = 0
        m = 1
        while m < len(gains):
            if gains[m] > gains[best]:
                best = m
            m = m + 1
        total = total + gains[best]
        gains.pop(best)
        taken = taken + 1
    share = total / net
    if share > 1.0:
        share = 1.0
    return share
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json
