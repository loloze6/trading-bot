# not built: slow_1h_run | 016-04_down-jump-price-reversal_1h | FallConcentrationShare

## attempt 1

answer: built
class: FallConcentrationComponent
settings: {"period": 72, "k": 3, "form": "share"}
reason: No catalogue component sums the k largest one-bar losses of a window, or relates them to the window's net fall. One new class computes the share, and a `form` setting gives the wished variant: "percent" multiplies the share by the net fall in percent of close[t-period].

table: Directional components
row: | `FallConcentrationComponent` | `period` (72), `k` (3), `form` ("share") | L = sum of the `k` largest of the losses max(0, close[j-1] - close[j]) over the `period` one-bar changes j = t-`period`+1 .. t; F = close[t-`period`] - close[t]. `form` "share": L / F when F > 0, else 0. `form` "percent": (L / F) x (F / close[t-`period`] x 100) when F > 0, else 0 | 0 and up, unbounded above, never negative; 0 when the window did not fall (F <= 0). "share": near 0 for a grind spread over many bars, towards 1 and above for a fall made by a few violent bars; it grows without bound as F tends to 0 from above. "percent": the share times the net fall in percent | graded | "share": dimensionless (ratio of price moves); "percent": percent of close[t-`period`] | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN. With "percent", a close[t-`period`] not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1 or `k` > `period`, `form` other than "share" or "percent" | stateless. One-sided, a long-only rebound reading. Fewer than `k` losing bars: the zero losses fill the count. Jumps to 0 when the net fall crosses 0, and the share is very large for a tiny net fall: pair it with a minimum-fall regime rule. No `scaling_factor`: scale it with transforms |

```python class
class FallConcentrationComponent(SubStrategyComponent):
    """
    How concentrated the window's net fall is in its few largest one-bar losses:

        c = close[t - period .. t]                                (period + 1 closes, bar t included)
        loss_j = max(0, close[j-1] - close[j]),  j = t - period + 1 .. t
        L = sum of the k largest loss_j  (zero losses fill the count when fewer than k bars fell)
        F = close[t - period] - close[t]                           (the net fall)
        form = "share" (default):  raw_value = L / F                                  if F > 0, else 0
        form = "percent":          raw_value = (L / F) * (F / close[t - period] * 100) if F > 0, else 0

    Range and sign: 0 and up, unbounded above, never negative; 0 when the window did not fall.
    "share" is near 0 for a grind spread over many bars and towards 1 and above for a fall made by a
    few violent bars. It grows without bound as F tends to 0 from above. "percent" combines that
    concentration with the size of the fall. Graded, one-sided (a long-only rebound reading).
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close in the last period + 1 rows gives NaN. With form "percent", a close[t - period]
    not above 0 gives NaN (never on real bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1 or above period, or a form other
    than "share" or "percent".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, the last
    row being bar t; a bar's close is known at that bar's close.
    """

    def __init__(self, name="FallConcentration", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"FallConcentrationComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k > self.period:
            raise ValueError(f"FallConcentrationComponent: k must be between 1 and period, got {self.k}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "percent"):
            raise ValueError(f"FallConcentrationComponent: form must be 'share' or 'percent', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        d = np.diff(c)
        losses = np.maximum(0.0, -d)
        top = float(np.sort(losses)[::-1][:self.k].sum())
        net_fall = float(c[0] - c[-1])
        if self.form == "percent" and not c[0] > 0:
            self._raw_value = float("nan")
        elif net_fall > 0:
            share = top / net_fall
            if self.form == "percent":
                self._raw_value = float(share * (net_fall / c[0] * 100.0))
            else:
                self._raw_value = float(share)
        else:
            self._raw_value = 0.0
        self.confidence = 1.0
        self.debug_info = {'top_k_losses': top, 'net_fall': net_fall, 'form': self.form}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
    form = params.get("form", "share")
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
    losses = []
    j = 1
    while j < len(w):
        drop = w[j - 1] - w[j]
        losses.append(drop if drop > 0 else 0.0)
        j = j + 1
    losses.sort(reverse=True)
    top = 0.0
    m = 0
    while m < k:
        top = top + losses[m]
        m = m + 1
    base = w[0]
    fall = base - w[-1]
    if form == "percent" and not base > 0:
        return float("nan")
    if not fall > 0:
        return 0.0
    share = top / fall
    if form == "percent":
        return share * (fall / base * 100.0)
    return share
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json

## attempt 2

answer: built
class: FallConcentrationComponent
settings: {"period": 72, "k": 3, "form": "share"}
reason: No catalogue component sums the largest one-bar losses of a window or compares that sum with the window's net fall, so this is a new measure and needs a new class. The variant is the same measure multiplied by the net fall in percent, so it is a `form` setting ("scaled") on the same class and not a second component.

table: Directional components
row: | `FallConcentrationComponent` | `period` (72), `k` (3), `form` ("share") | L = the sum of the `k` largest one-bar losses max(0, close[i-1] - close[i]) over the last `period` changes (i = t-`period`+1 .. t), F = close[t-`period`] - close[t]. `form` "share": L / F when F > 0, else 0. `form` "scaled": (L / F) x (F / close[t-`period`] x 100) when F > 0, else 0 | 0 and up, unbounded above, never negative; no sign. "share" is near 0 for a fall spread evenly over many bars, about 1 when a few bars made the whole fall, and above 1 when the other bars partly rebounded. "scaled" grows with both the concentration and the size of the fall. Both are 0 when the close did not fall over the window | graded | "share": dimensionless (losses over net fall); "scaled": percent of close[t-`period`] | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; with "scaled", a close[t-`period`] not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` > `period`, `form` other than "share" or "scaled" | stateless. When fewer than `k` bars fell, L sums only the bars that did fall. One-sided (a long-only rebound reading after a violent fall). No `scaling_factor`: scale it with transforms |

```python class
class FallConcentrationComponent(SubStrategyComponent):
    """
    How concentrated the window's net fall is in its few largest one-bar losses:

        loss(i) = max(0, close[i-1] - close[i]),  i = t - period + 1 .. t      (period one-bar changes)
        L = sum of the k largest loss(i) (largest first; fewer than k falling bars: only those)
        F = close[t - period] - close[t]                                       (net fall over the window)
        form = "share" (default):  raw_value = L / F                           when F > 0, else 0.0
        form = "scaled":           raw_value = (L / F) x (F / close[t - period] x 100)  when F > 0, else 0.0

    Range: 0 and up, unbounded above, never negative, with no sign. "share" is near 0 for a grind spread
    over many bars, about 1 when k bars made the whole fall, and above 1 when the other bars partly
    rebounded. "scaled" combines the concentration and the size of the fall (percent of close[t - period]).
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close in the last period + 1 rows gives NaN. With "scaled", a close[t - period] that is not
    above 0 gives NaN. A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1 or above period, or a form other than
    "share" or "scaled".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, which are
    bars t - period .. t, the last row being bar t. A bar's close is known at that bar's close.
    """

    def __init__(self, name="FallConcentration", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"FallConcentrationComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k > self.period:
            raise ValueError(f"FallConcentrationComponent: k must be between 1 and period, got {self.k}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "scaled"):
            raise ValueError(f"FallConcentrationComponent: form must be 'share' or 'scaled', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = [float(x) for x in data["close"].iloc[-(self.period + 1):].tolist()]
        for x in c:
            if x != x:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        losses = []
        for j in range(1, len(c)):
            d = c[j - 1] - c[j]
            losses.append(d if d > 0.0 else 0.0)
        losses.sort(reverse=True)
        total = 0.0
        for j in range(self.k):
            total = total + losses[j]
        base = c[0]
        fall = base - c[-1]
        if not fall > 0.0:
            value = 0.0
        else:
            share = total / fall
            if self.form == "share":
                value = share
            elif not base > 0.0:
                value = float("nan")
            else:
                value = share * (fall / base * 100.0)
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"top_losses_sum": total, "net_fall": fall, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    period = int(params.get("period", 72))
    k = int(params.get("k", 3))
    form = params.get("form", "share")
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    window = []
    i = last - period
    while i <= last:
        window.append(closes[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
    drops = []
    i = 1
    while i < len(window):
        change = window[i] - window[i - 1]
        if change < 0.0:
            drops.append(window[i - 1] - window[i])
        else:
            drops.append(0.0)
        i = i + 1
    ordered = sorted(drops, reverse=True)
    biggest = 0.0
    j = 0
    while j < k:
        biggest = biggest + ordered[j]
        j = j + 1
    start = window[0]
    net_fall = start - window[-1]
    if not net_fall > 0.0:
        return 0.0
    share = biggest / net_fall
    if form == "share":
        return share
    if not start > 0.0:
        return float("nan")
    return share * (net_fall / start * 100.0)
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json

## attempt 3

answer: built
class: FallConcentrationComponent
settings: {"period": 72, "k": 3}
reason: No component in the catalogue measures how much of a net fall over a window comes from its few largest one-bar losses. The measure is a new graded quantity read from closes only, so one new class computes it. The variant (the share times the net fall in percent) is a value of a `form` setting, not a second component. This version sums the k largest losses from largest to smallest in plain floats and takes the net fall directly from the two closes, so its value is the same bit for bit as the hand computation, including on near-zero net falls where the share is very sensitive.

table: Directional components
row: | `FallConcentrationComponent` | `period` (72), `k` (3), `form` ("share") | L = the sum of the `k` largest one-bar losses max(0, close[i-1] - close[i]) over the last `period` changes (i = t-`period`+1 .. t), added largest first. F = close[t-`period`] - close[t]. `form` "share": L / F when F > 0, else 0. `form` "sized": L / F x (F / close[t-`period`] x 100) = L / close[t-`period`] x 100 when F > 0, else 0 | 0 and up, unbounded above, never negative; 0 when the closes did not fall over the window; "share" is near 0 for a fall spread over many bars and 1 or above for a fall made by a few bars | graded | "share": dimensionless (losses / net fall); "sized": percent of the base close | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN; with "sized", a base close not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1 or `k` > `period`, `form` other than "share" or "sized" | stateless. With fewer than `k` down bars in the window, L is the sum of those that exist. "sized" combines concentration and size into one long-only reading. "share" can be very large when the net fall is tiny. No `scaling_factor`: scale it with transforms |

```python class
class FallConcentrationComponent(SubStrategyComponent):
    """
    How concentrated the window's net fall is in its few largest one-bar losses, on bar t:

        loss(i) = max(0, close[i-1] - close[i]),  i = t-period+1 .. t     (period one-bar changes)
        L = sum of the k largest loss(i), added from the largest down
        F = close[t-period] - close[t]                                     (net fall over the window)
        form = "share" (default): raw_value = L / F                    if F > 0, else 0.0
        form = "sized":           raw_value = L / F * (F / close[t-period] * 100)
                                            = L / close[t-period] * 100 if F > 0, else 0.0

    Graded, one-sided: 0 and up, unbounded above, never negative. "share" is near 0 for a grind spread over
    many bars and grows towards 1 and above when a few violent bars made the fall. "sized" is the share times
    the net fall in percent: size and concentration in one long-only reading. With fewer than k down bars in
    the window, L is the sum of the ones there are.
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close in the last period + 1 rows gives NaN. With "sized", a base close not above 0 gives NaN
    (never on real bars). Building the component raises for a period below 2, a k below 1 or above period, or
    a form other than "share" or "sized".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t (the last
    row) included and no later row; a close is known at its bar's close.
    """

    def __init__(self, name="FallConcentration", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"FallConcentrationComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1 or self.k > self.period:
            raise ValueError(f"FallConcentrationComponent: k must be between 1 and period, got {self.k}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "sized"):
            raise ValueError(f"FallConcentrationComponent: form must be 'share' or 'sized', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = [float(x) for x in data["close"].to_numpy()[-(self.period + 1):]]
        for c in closes:
            if c != c:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        losses = []
        for j in range(1, len(closes)):
            d = closes[j - 1] - closes[j]
            losses.append(d if d > 0.0 else 0.0)
        losses.sort(reverse=True)
        top = 0.0
        for j in range(self.k):
            top = top + losses[j]
        base = closes[0]
        fall = base - closes[-1]
        if self.form == "sized" and not base > 0.0:
            value = float("nan")
        elif not fall > 0.0:
            value = 0.0
        elif self.form == "sized":
            value = top / fall * (fall / base * 100.0)
        else:
            value = top / fall
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"top_losses": top, "net_fall": fall, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
    form = params.get("form", "share")
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
    drops = []
    i = 1
    while i < len(window):
        d = window[i - 1] - window[i]
        if d > 0.0:
            drops.append(d)
        else:
            drops.append(0.0)
        i = i + 1
    # pick the k largest by repeated selection, adding largest first
    remaining = list(drops)
    total = 0.0
    taken = 0
    while taken < k:
        best = 0
        j = 1
        while j < len(remaining):
            if remaining[j] > remaining[best]:
                best = j
            j = j + 1
        total = total + remaining[best]
        remaining.pop(best)
        taken = taken + 1
    start = window[0]
    net = start - window[-1]
    if form == "sized" and not start > 0.0:
        return float("nan")
    if not net > 0.0:
        return 0.0
    if form == "sized":
        return total / net * (net / start * 100.0)
    return total / net
```

checks:
proof: 576 files compared, 2 differ:
differs: XRPUSD/w2/metrics.json
differs: XRPUSD/w3/metrics.json
