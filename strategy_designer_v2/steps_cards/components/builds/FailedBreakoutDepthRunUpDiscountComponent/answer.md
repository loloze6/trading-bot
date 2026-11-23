# FailedBreakoutDepthRunUpDiscountComponent: short_1d_run | 029-03_close-below-breakout-bar-low.d2_return-below-old-high-unstretched_1d | FailedBreakoutPriorReturnComponent

## attempt 1

answer: built
class: FailedBreakoutDepthRunUpDiscountComponent
settings: {"period": 20, "fail_window": 10, "rise_period": 20, "window": 120}
reason: `FailedBreakoutDepthComponent` (`period` 20, `fail_window` 10) gives the depth under the old high but has no weight from the rally into the breakout. `BreakoutLowDepthPerRunUpComponent` measures from the breakout bar's low with a high-based breakout and a 1/(1 + run-up in percent) divisor, not a discount in usual 20-bar moves. One new class computes depth x max(0, 1 − R(j)/m).

table: Directional components
row: | `FailedBreakoutDepthRunUpDiscountComponent` | `period` (20), `fail_window` (10), `rise_period` (20), `window` (120) | max(0, H(j) − close[t]) / H(j) x 100 x max(0, 1 − R(j) / m). j is the most recent bar in t-`fail_window`+1 .. t (bar t included) with close[j] > H(j), H(j) = max(close[j-`period`] .. close[j-1]). R(j) = close[j] / close[j-`rise_period`] − 1. m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`rise_period`] − 1). 0 when no bar of the window broke out, when close[t] >= H(j), or when m = 0 | 0 and up, never negative; no direction. The depth is below 100 and the weight is 0 to 1 + 1/m. It is 0 without a failed breakout and 0 when the run-up into the breakout is one usual `rise_period`-bar move or more. It grows linearly as the close sinks under the old high, and grows as the run-up R(j) shrinks (above 1 for a falling run-up) | graded | percent of the old high x (1 − run-up in usual `rise_period`-bar moves) | max(`period` + `fail_window`, `rise_period` + `fail_window`, `window` + `rise_period`) (140) | closes only. A NaN close in the last (warmup) rows gives NaN. A close not above 0 there gives NaN (never on real bars). m = 0 gives 0 (never on real bars). These settings raise when the component is built: `period` < 1, `fail_window` < 1, `rise_period` < 1, `window` < 1 | stateless. The breakout bar j and the failure test are those of `FailedBreakoutDepthComponent` (`period`, `fail_window`, `source` "close", `reference` "prior_high", `exclude_current` 0), and the first factor is that component's output. A breakout needs a strictly higher close, and only the most recent breakout counts, so a breakout on bar t reads 0. The value is continuous in close[t] while the same breakout stays the most recent, and it drops to 0 when that breakout leaves the window. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class FailedBreakoutDepthRunUpDiscountComponent(SubStrategyComponent):
    """
    Depth of a failed closing breakout under the old high, discounted by the rally into the breakout:

        j    = the most recent bar in t-fail_window+1 .. t (bar t included) with close[j] > H(j),
               H(j) = max(close[j-period] .. close[j-1])
        R(j) = close[j] / close[j-rise_period] - 1
        m    = mean over i = t-window+1 .. t of abs(close[i] / close[i-rise_period] - 1)
        raw_value = max(0, H(j) - close[t]) / H(j) x 100 x max(0, 1 - R(j) / m)

    The value is 0 when no bar of the window broke out, when close[t] >= H(j) (so 0 when bar t itself breaks out),
    or when m = 0.
    Range: 0 and up, never negative, no direction. The depth is below 100, and the weight is 0 to 1 + 1/m: it is 0
    once the run-up is one usual rise_period-bar move or more, 1 for a flat run-up, and above 1 for a falling one.
    Graded: continuous in close[t] while the same breakout stays the most recent.
    Warm-up: max(period + fail_window, rise_period + fail_window, window + rise_period) rows, bar t included
    (140 at the defaults).
    NaN: a NaN close in those rows gives NaN, and so does a close not above 0 there (never on real bars).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last get_required_periods() rows of data, ending
    at bar t (the last row). Every H(j), R(j) and m uses closes at or before bar t.
    """

    def __init__(self, name="FailedBreakoutDepthRunUpDiscount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        self.fail_window = int(self.parameters.get("fail_window", 10))
        self.rise_period = int(self.parameters.get("rise_period", 20))
        self.window = int(self.parameters.get("window", 120))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutDepthRunUpDiscountComponent: period must be >= 1, got {self.period}")
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutDepthRunUpDiscountComponent: fail_window must be >= 1, got {self.fail_window}")
        if self.rise_period < 1:
            raise ValueError(
                f"FailedBreakoutDepthRunUpDiscountComponent: rise_period must be >= 1, got {self.rise_period}")
        if self.window < 1:
            raise ValueError(f"FailedBreakoutDepthRunUpDiscountComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        self.confidence = 1.0
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            return
        t = n - 1
        j = None
        hj = None
        for jj in range(t, t - self.fail_window, -1):
            h = float(np.max(c[jj - self.period:jj]))
            if c[jj] > h:
                j = jj
                hj = h
                break
        if j is None or not c[t] < hj:
            self._raw_value = 0.0
            self.debug_info = {"breakout_offset": None if j is None else t - j}
            return
        depth = (hj - c[t]) / hj * 100.0
        idx = np.arange(t - self.window + 1, t + 1)
        m = float(np.mean(np.abs(c[idx] / c[idx - self.rise_period] - 1.0)))
        if not m > 0:
            self._raw_value = 0.0
            return
        r = float(c[j] / c[j - self.rise_period] - 1.0)
        w = max(0.0, 1.0 - r / m)
        self._raw_value = float(depth * w)
        self.debug_info = {"breakout_offset": t - j, "old_high": hj, "depth": depth, "run_up": r,
                           "mean_abs_move": m, "weight": w}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + self.fail_window, self.rise_period + self.fail_window,
                   self.window + self.rise_period)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 20))
    fw = int(params.get("fail_window", 10))
    rp = int(params.get("rise_period", 20))
    w = int(params.get("window", 120))
    need = max(p + fw, rp + fw, w + rp)
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    for k in range(need):
        x = closes[t - k]
        if x != x or not x > 0:
            return float("nan")
    # most recent breakout bar j in t-fw+1 .. t
    j = -1
    old_high = 0.0
    k = 0
    while k < fw:
        cand = t - k
        hi = closes[cand - 1]
        q = 2
        while q <= p:
            if closes[cand - q] > hi:
                hi = closes[cand - q]
            q += 1
        if closes[cand] > hi:
            j = cand
            old_high = hi
            break
        k += 1
    if j < 0:
        return 0.0
    if closes[t] >= old_high:
        return 0.0
    depth = (old_high - closes[t]) / old_high * 100.0
    total = 0.0
    for i in range(t - w + 1, t + 1):
        total += abs(closes[i] / closes[i - rp] - 1.0)
    m = total / w
    if m == 0:
        return 0.0
    run_up = closes[j] / closes[j - rp] - 1.0
    weight = 1.0 - run_up / m
    if weight < 0:
        weight = 0.0
    return depth * weight
```

checks:
FailedBreakoutDepthRunUpDiscountComponent: every check passed
the bot's suite: == 1634 passed, 16 skipped, 75 deselected, 2244 warnings in 79.00s (0:01:19) ===
