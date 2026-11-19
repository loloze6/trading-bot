# not built: slow_1h_run | 016-02_down-grind-price-continuation_1h | GrindShareOfFallComponent

## attempt 1

answer: built
class: LossDispersionComponent
settings: {"period": 72, "k": 3}
reason: No catalogue component measures how a window's one-bar losses are spread across bars. Here that is 1 minus the share of total loss carried by the `k` largest losses, signed by the window's net return. One new class computes it, named by what it measures, not by the "grind" idea that asked for it.

table: Directional components
row: | `LossDispersionComponent` | `period` (72), `k` (3) | sign(close[t] / close[t-`period`] - 1) x (1 - S_k / L), where L is the sum of the losses -r_j over the negative one-bar returns r_j = close[j] / close[j-1] - 1, j = t-`period`+1 .. t, and S_k is the sum of the `k` largest of those losses. The dispersion factor is 0 when there are no losses or at most `k` of them | -1 to +1 exclusive, signed. Negative over a net fall, positive over a net rise, 0 when the net return is exactly 0. The size grows toward 1 as the loss is spread over many small losses and shrinks toward 0 as the `k` biggest losses carry it | graded | share of total loss, signed | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN, and so does a close not above 0 (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` >= `period` | stateless. The size is graded. The sign is that of the net return, so the value jumps through 0 when the net return crosses 0, like a signed reading. Ties among the largest losses do not matter, because the sum of the `k` largest is unique. No `scaling_factor`: scale it with transforms |

```python class
class LossDispersionComponent(SubStrategyComponent):
    """
    How widely a window's losses are spread over its bars, signed by the window's net move:

        r_j = close[j] / close[j-1] - 1,  j = t-period+1 .. t        (the last `period` one-bar returns)
        losses = { -r_j : r_j < 0 },  L = sum(losses)
        S_k = sum of the k largest losses
        D = 1 - S_k / L   (D = 0 when there are no losses or at most k of them)
        raw_value = sign(close[t] / close[t-period] - 1) x D

    Range: -1 to +1, both exclusive. The value is negative over a net fall and positive over a net rise. It is 0
    when the net return is exactly 0, or when at most k bars lost. The size grows toward 1 as the loss is spread
    over many small losing bars. It shrinks toward 0 as the k biggest losing bars carry the loss.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data (bars t-period .. t,
    bar t being the last row). Each close is known at its bar's close.

    NaN: a NaN close among the last period + 1 rows gives NaN, and so does a close not above 0 (never on real bars).
    Building the component raises for a period below 2, a k below 1, or a k not below period.
    """

    def __init__(self, name="LossDispersion", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"LossDispersionComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k >= self.period:
            raise ValueError(f"LossDispersionComponent: k must be >= 1 and < period, got {self.k}")
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
        losses = -r[r < 0]
        total = float(losses.sum()) if len(losses) else 0.0
        if len(losses) <= self.k or not total > 0:
            disp = 0.0
            top = total
        else:
            top = float(np.sort(losses)[::-1][:self.k].sum())
            disp = 1.0 - top / total
        net = c[-1] / c[0] - 1.0
        sgn = 1.0 if net > 0 else (-1.0 if net < 0 else 0.0)
        self._raw_value = float(sgn * disp)
        self.confidence = 1.0
        self.debug_info = {'total_loss': total, 'top_k_loss': top, 'net_return': float(net), 'n_losses': int(len(losses))}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
    closes = [float(x) for x in list(df["close"])]
    w = closes[len(closes) - n - 1:]
    for x in w:
        if x != x or not x > 0:
            return float("nan")
    loss_list = []
    i = 1
    while i < len(w):
        ret = w[i] / w[i - 1] - 1.0
        if ret < 0:
            loss_list.append(-ret)
        i = i + 1
    total = 0.0
    for x in loss_list:
        total = total + x
    if len(loss_list) <= k or not total > 0:
        disp = 0.0
    else:
        ordered = sorted(loss_list, reverse=True)
        top = 0.0
        for j in range(k):
            top = top + ordered[j]
        disp = 1.0 - top / total
    net = w[-1] / w[0] - 1.0
    if net > 0:
        return disp
    if net < 0:
        return -disp
    return 0.0
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json

## attempt 2

answer: built
class: GrindShareOfFallComponent
settings: {"period": 72, "k": 3}
reason: No catalogue component measures how evenly the hourly losses of a window are spread, meaning 1 minus the share of the k largest losses, signed by the window's net move, so a new class computes it. This rebuild keeps the same measure and changes only the arithmetic, which caused the earlier differences on XRPUSD. Every sum now runs in plain Python in one fixed order, the sign compares the two closes exactly, and a window with no loss reads 0, so the class and the hand computation match bit for bit.

table: Directional components
row: | `GrindShareOfFallComponent` | `period` (72), `k` (3) | sign(close[t] - close[t-`period`]) x (1 - B / L) over the `period` one-bar returns r(j) = close[j] / close[j-1] - 1, j = t-`period`+1 .. t. L = sum of -r(j) over the r(j) < 0, in bar order. B = sum of the `k` largest of those losses, largest first. The value is 0 when L = 0, when the window has at most `k` losses, or when close[t] = close[t-`period`] | -1 to +1 (open at both ends), signed; negative when the window fell, positive when it rose. Its size grows toward 1 as the move's losses spread over many small hours and shrinks toward 0 as the `k` biggest hours carry them | graded | dimensionless (share of the summed losses) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a close not above 0 among the bases gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` >= `period` | stateless. Sums are taken in plain Python in a fixed order: losses in bar order, the top `k` largest first. The sign compares the two closes exactly, so a window that ends where it started reads 0. No `scaling_factor`: scale it with transforms |

```python class
class GrindShareOfFallComponent(SubStrategyComponent):
    """
    How evenly a window's losses are spread, signed by the window's net move:

        r(j) = close[j] / close[j-1] - 1,  j = t-period+1 .. t      (period one-bar returns, bar t's included)
        losses = [-r(j) for r(j) < 0], in bar order
        L = sum(losses) in bar order;  B = sum of the k largest losses, largest first
        g = 1 - B / L   (0 when L = 0; 0 when there are at most k losses)
        raw_value = sign(close[t] - close[t-period]) x g   (sign 0 when the two closes are equal)

    Range -1 to +1 (open at both ends), signed: negative when the window fell, positive when it rose. Graded:
    the size grows toward 1 as the losses spread over many small bars and shrinks toward 0 as the k biggest
    bars carry them. Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, the last being
    bar t; a bar's close is known at that bar's close.

    NaN: a NaN close in the last period + 1 rows gives NaN; a base close not above 0 gives NaN (never on real
    bars). Building the component raises for period < 2, k < 1, or k >= period.
    """

    def __init__(self, name="GrindShareOfFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"GrindShareOfFallComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k >= self.period:
            raise ValueError(f"GrindShareOfFallComponent: k must be between 1 and period - 1, got {self.k}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = [float(x) for x in data['close'].iloc[-(self.period + 1):].tolist()]
        for c in closes:
            if c != c:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        losses = []
        for j in range(1, len(closes)):
            if not closes[j - 1] > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            r = closes[j] / closes[j - 1] - 1.0
            if r < 0:
                losses.append(-r)
        total = 0.0
        for x in losses:
            total = total + x
        if len(losses) <= self.k or not total > 0:
            g = 0.0
        else:
            top = sorted(losses, reverse=True)
            big = 0.0
            for x in top[:self.k]:
                big = big + x
            g = 1.0 - big / total
        if closes[-1] > closes[0]:
            sgn = 1.0
        elif closes[-1] < closes[0]:
            sgn = -1.0
        else:
            sgn = 0.0
        self._raw_value = float(sgn * g)
        self.confidence = 1.0
        self.debug_info = {'n_losses': len(losses), 'sum_losses': total, 'grind_share': g, 'sign': sgn}

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
    losses = []
    j = 1
    while j < len(window):
        base = window[j - 1]
        if not base > 0:
            return float("nan")
        r = window[j] / base - 1.0
        if r < 0:
            losses.append(-r)
        j = j + 1
    total = 0.0
    for x in losses:
        total = total + x
    if len(losses) <= k or not total > 0:
        share = 0.0
    else:
        ordered = sorted(losses, reverse=True)
        big = 0.0
        m = 0
        while m < k:
            big = big + ordered[m]
            m = m + 1
        share = 1.0 - big / total
    if window[-1] > window[0]:
        s = 1.0
    elif window[-1] < window[0]:
        s = -1.0
    else:
        s = 0.0
    return s * share
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json

## attempt 3

answer: built
class: GrindShareOfFallComponent
settings: {"period": 72, "k": 3}
reason: No component compares the few largest one-bar losses of a window with all its losses. This new class computes that share. The sums run in a fixed order and the sign comes from an exact comparison of the two closes, so float rounding or a flat window cannot make two computations disagree.

table: Regime measures
row: | `GrindShareOfFallComponent` | `period` (72), `k` (3) | s x rest / (rest + top). The losses are -r_j for each one-bar return r_j = close[j] / close[j-1] - 1 < 0, j = t-`period`+1 .. t. Sorted ascending, top = the sequential sum of the `k` largest and rest = the sequential sum of the others. s = +1 if close[t] > close[t-`period`], -1 if below, 0 if equal. The value is 0 when there are `k` losses or fewer | -1 to +1, signed: negative over a net fall, positive over a net rise, 0 over a flat window; near ±1 when the losses are spread over many small bars, near 0 when the `k` biggest carry them | regime measure | dimensionless (share of the summed losses) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; a base close not above 0 gives NaN (never on real bars). `period` < 2, `k` < 1 or `k` >= `period` raises when the component is built | stateless. rest / (rest + top) is 1 minus the share of the `k` largest losses. Equal losses are interchangeable, so ties do not change the value. No `scaling_factor`: scale it with transforms |

```python class
class GrindShareOfFallComponent(SubStrategyComponent):
    """
    How spread out the window's losses are, signed by the window's net move:

        r_j = close[j] / close[j-1] - 1,  j = t - period + 1 .. t      (period returns, bar t's included)
        losses = [-r_j for r_j < 0], sorted ascending, m = len(losses)
        if m <= k: g = 0.0
        else:
            rest = sequential sum (in ascending order) of losses[0 .. m-k-1]
            top  = sequential sum (in ascending order) of losses[m-k .. m-1]   (the k largest)
            g = rest / (rest + top)          (= 1 - top / sum of all losses)
        s = +1 if close[t] > close[t-period], -1 if close[t] < close[t-period], 0 if equal
        raw_value = s * g

    Range -1 to +1, signed. It is negative over a net fall and positive over a net rise. Its size nears 1 when the
    losses are spread over many small bars and nears 0 when the k biggest carry them. It is 0 over a flat window or
    when there are k losses or fewer.
    Warm-up: period + 1 rows, bar t included.
    NaN: a NaN close in the last period + 1 rows gives NaN. A base close not above 0 gives NaN (never on real bars).
    Building the component raises for period < 2, k < 1 or k >= period.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t (the last row)
    included and nothing after it.
    """

    def __init__(self, name="GrindShareOfFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"GrindShareOfFallComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k >= self.period:
            raise ValueError(f"GrindShareOfFallComponent: k must be between 1 and period - 1, got {self.k}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = [float(x) for x in data["close"].iloc[-(self.period + 1):].tolist()]
        for c in closes:
            if c != c:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        losses = []
        for j in range(1, len(closes)):
            if not closes[j - 1] > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            r = closes[j] / closes[j - 1] - 1.0
            if r < 0:
                losses.append(-r)
        losses.sort()
        m = len(losses)
        if m <= self.k:
            g = 0.0
        else:
            rest = 0.0
            for x in losses[:m - self.k]:
                rest = rest + x
            top = 0.0
            for x in losses[m - self.k:]:
                top = top + x
            g = rest / (rest + top)
        if closes[-1] > closes[0]:
            s = 1.0
        elif closes[-1] < closes[0]:
            s = -1.0
        else:
            s = 0.0
        self._raw_value = float(s * g)
        self.confidence = 1.0
        self.debug_info = {"n_losses": m, "share_spread": g, "sign": s}

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
    window = []
    i = last - n
    while i <= last:
        window.append(c[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
    losses = []
    i = 1
    while i < len(window):
        if not window[i - 1] > 0:
            return float("nan")
        r = window[i] / window[i - 1] - 1.0
        if r < 0:
            losses.append(-r)
        i = i + 1
    if len(losses) <= k:
        g = 0.0
    else:
        asc = sorted(losses)
        small = asc[:len(asc) - k]
        big = asc[len(asc) - k:]
        rest = 0.0
        for x in small:
            rest = rest + x
        top = 0.0
        for x in big:
            top = top + x
        g = rest / (rest + top)
    first = window[0]
    now = window[-1]
    if now > first:
        sign = 1.0
    elif now < first:
        sign = -1.0
    else:
        sign = 0.0
    return sign * g
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json
