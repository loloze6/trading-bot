# PriorFallTimesScaledFallRangeMultipleComponent: night4_panic_run | 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h | PriorFallGatedPanicComponent

## attempt 1

answer: built
class: PriorFallTimesScaledFallRangeMultipleComponent
settings: {"period": 6, "lag": 6, "window": 180, "prior_period": 540}
reason: No component of the catalogue gives the product of the prior long fall, ending at the stretch's start, with `ScaledFallRangeMultipleComponent`. No config step multiplies two components, so one new class computes this combined measure. On 4h bars, 540 bars are 90 days, so the prior fall runs from close[t-552] to close[t-12].

table: Directional components
row: | `PriorFallTimesScaledFallRangeMultipleComponent` | `period` (6), `lag` (6), `window` (180), `prior_period` (540) | P x max(0, -(close[e] / close[e-`period`] - 1) / m) x S(e) / B, with e = t - `lag`. P = max(0, -(close[e-`period`] / close[e-`period`-`prior_period`] - 1)) x 100. m = mean over i = e-`window`+1 .. e of abs(close[i] / close[i-`period`] - 1). S(i) = max(high[i-`period`+1 .. i]) - min(low[i-`period`+1 .. i]). B = mean of S(i) over i = e-`window`+1 .. e. The second factor is 0 when m = 0 or B = 0 | 0 and up, never negative; no direction. P is 0 to 100, and each of the two multiples is at most `window`. It is 0 unless the prior `prior_period`-bar return ending at the stretch's start is negative and the stretch ending at bar e fell. It grows with the depth of the prior fall, the depth of the stretch's fall in usual moves, and its range in usual ranges | graded | percent x usual `period`-bar moves x mean `period`-bar ranges | max(`lag` + `window` + `period`, `lag` + `period` + `prior_period` + 1) (553) | close, high, low. A NaN close in bars t-`lag`-`window`-`period`+1 .. t-`lag` or at bar t-`lag`-`period`-`prior_period` gives NaN. So does a NaN high or low in bars t-`lag`-`window`-`period`+2 .. t-`lag`. A close not above 0 among those also gives NaN (never on real bars). m = 0 or B = 0 gives 0. These settings raise when the component is built: `period` < 1, `lag` < 0, `window` < 1, `prior_period` < 1 | stateless. Equals max(0, -`PriceEvolutionOnPeriodComponent`(`comparison_period` = `prior_period`) read at bar t-`lag`-`period`) x `ScaledFallRangeMultipleComponent` (`period`, `lag`, `window`). Bars after t-`lag` are not read. It is continuous in the prices while both falls hold, and exactly 0 otherwise. One-sided, a delayed-rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class PriorFallTimesScaledFallRangeMultipleComponent(SubStrategyComponent):
    """
    The prior long fall that ended at the stretch's start, times the scaled fall and range multiple of the stretch:

        e = t - lag
        P = max(0, -(close[e-period] / close[e-period-prior_period] - 1)) x 100
        r(i) = close[i] / close[i-period] - 1
        m = mean(abs(r(i)), i = e-window+1 .. e)
        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        B = mean(S(i), i = e-window+1 .. e)
        F = max(0, -r(e) / m) x S(e) / B          (F = 0 when m = 0 or B = 0)
        raw_value = P x F

    F is ScaledFallRangeMultipleComponent(period, lag, window). The output is graded, 0 and up, never negative,
    with no direction. P is 0 to 100, and each multiple in F is at most window. It is 0 unless both the prior
    prior_period-bar return and the stretch's return are negative.
    Warm-up: max(lag + window + period, lag + period + prior_period + 1) rows, bar t included (553 at the defaults).
    NaN: a NaN close, high or low in any row read gives NaN, and so does a close not above 0 (never on real bars).
    m = 0 or B = 0 gives 0.
    Building the component raises for period < 1, lag < 0, window < 1, or prior_period < 1.

    WHY THIS CANNOT LEAK: it reads close at bars t-lag-window-period+1 .. t-lag and at bar
    t-lag-period-prior_period, and high and low at bars t-lag-window-period+2 .. t-lag. All of these are rows
    at or before bar t (the last row of data).
    """

    def __init__(self, name="PriorFallScaledFallRange", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.lag = int(self.parameters.get("lag", 6))
        self.window = int(self.parameters.get("window", 180))
        self.prior_period = int(self.parameters.get("prior_period", 540))
        if self.period < 1:
            raise ValueError(f"PriorFallTimesScaledFallRangeMultipleComponent: period must be >= 1, got {self.period}")
        if self.lag < 0:
            raise ValueError(f"PriorFallTimesScaledFallRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        if self.window < 1:
            raise ValueError(f"PriorFallTimesScaledFallRangeMultipleComponent: window must be >= 1, got {self.window}")
        if self.prior_period < 1:
            raise ValueError(
                f"PriorFallTimesScaledFallRangeMultipleComponent: prior_period must be >= 1, got {self.prior_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data["close"].astype(float).to_numpy()
        h = data["high"].astype(float).to_numpy()
        lo = data["low"].astype(float).to_numpy()
        n = len(c)
        t = n - 1
        p, w = self.period, self.window
        e = t - self.lag
        cw = c[e - w - p + 1: e + 1]
        hw = h[e - w - p + 2: e + 1]
        lw = lo[e - w - p + 2: e + 1]
        p0 = c[e - p - self.prior_period]
        p1 = c[e - p]
        if (np.isnan(cw).any() or np.isnan(hw).any() or np.isnan(lw).any() or np.isnan(p0)
                or (cw <= 0).any() or not p0 > 0):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        r = cw[p:] / cw[:-p] - 1.0
        m = float(np.mean(np.abs(r)))
        hmax = np.lib.stride_tricks.sliding_window_view(hw, p).max(axis=1)
        lmin = np.lib.stride_tricks.sliding_window_view(lw, p).min(axis=1)
        s = hmax - lmin
        b = float(np.mean(s))
        fall = max(0.0, -float(r[-1]))
        if m == 0 or b == 0:
            f = 0.0
        else:
            f = fall / m * float(s[-1]) / b
        prior = max(0.0, -(float(p1) / float(p0) - 1.0)) * 100.0
        self._raw_value = float(prior * f)
        self.confidence = 1.0
        self.debug_info = {"prior_fall_pct": prior, "scaled_fall_range_multiple": f, "m": m, "B": b}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.lag + self.window + self.period, self.lag + self.period + self.prior_period + 1)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    w = int(params.get("window", 180))
    pp = int(params.get("prior_period", 540))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    e = t - lag
    used_c = [c[k] for k in range(e - w - p + 1, e + 1)] + [c[e - p - pp]]
    used_hl = [h[k] for k in range(e - w - p + 2, e + 1)] + [lo[k] for k in range(e - w - p + 2, e + 1)]
    for x in used_c + used_hl:
        if x != x:
            return float("nan")
    for x in used_c:
        if not x > 0:
            return float("nan")
    abs_sum = 0.0
    for i in range(e - w + 1, e + 1):
        abs_sum += abs(c[i] / c[i - p] - 1.0)
    m = abs_sum / w

    def stretch_range(i):
        hi = h[i - p + 1]
        lw = lo[i - p + 1]
        for k in range(i - p + 1, i + 1):
            if h[k] > hi:
                hi = h[k]
            if lo[k] < lw:
                lw = lo[k]
        return hi - lw

    s_sum = 0.0
    for i in range(e - w + 1, e + 1):
        s_sum += stretch_range(i)
    b = s_sum / w
    ret_e = c[e] / c[e - p] - 1.0
    fall = -ret_e if ret_e < 0 else 0.0
    if m == 0 or b == 0:
        f = 0.0
    else:
        f = (fall / m) * (stretch_range(e) / b)
    prior_ret = c[e - p] / c[e - p - pp] - 1.0
    prior = (-prior_ret if prior_ret < 0 else 0.0) * 100.0
    return prior * f
```

checks:
PriorFallTimesScaledFallRangeMultipleComponent: every check passed
the bot's suite: == 1613 passed, 16 skipped, 75 deselected, 2244 warnings in 93.69s (0:01:33) ===
