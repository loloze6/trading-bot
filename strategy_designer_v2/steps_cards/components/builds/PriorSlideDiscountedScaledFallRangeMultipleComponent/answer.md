# PriorSlideDiscountedScaledFallRangeMultipleComponent: night4_panic_run | 027-01_panic-range-multiple-rebound.d2_panic-after-rising-week_4h | PanicTimesPriorWeekComponent

## attempt 1

answer: built
class: PriorSlideDiscountedScaledFallRangeMultipleComponent
settings: {"period": 6, "lag": 6, "window": 180, "prior_period": 42}
reason: `ScaledFallRangeMultipleComponent` gives the panic reading. No component multiplies it by a factor that is 1 after a non-negative prior return and drops linearly, by one for each usual `prior_period`-bar move of slide, going negative past one usual move. (`PriorFallTimesScaledFallRangeMultipleComponent` multiplies by the prior fall in percent instead, a different measure.) So one new class computes the product.

table: Directional components
row: | `PriorSlideDiscountedScaledFallRangeMultipleComponent` | `period` (6), `lag` (6), `window` (180), `prior_period` (42) | F x Q, with e = t - `lag`. F = max(0, -(close[e] / close[e-`period`] - 1) / m) x S(e) / B, where m = mean over i = e-`window`+1 .. e of abs(close[i] / close[i-`period`] - 1), S(i) = max(high[i-`period`+1 .. i]) - min(low[i-`period`+1 .. i]), and B = mean of S(i) over the same i. F is 0 when m = 0 or B = 0. Q = 1 + min(0, R / u), where R = close[e] / close[e-`prior_period`] - 1 and u = mean over the same i of abs(close[i] / close[i-`prior_period`] - 1). Q is 1 when u = 0. Output 0.0 when F = 0 | Signed. It is 0 when the stretch ending at bar e did not fall. During a fall it equals F (0 and up, at most `window` x `window`) when the prior return is 0 or above. It shrinks as the prior slide deepens, is 0 at a slide of one usual `prior_period`-bar move, and is negative for a deeper slide. Q is 1 - `window` to 1 | graded | usual `period`-bar moves x mean `period`-bar ranges x (1 - prior slide in usual `prior_period`-bar moves) | `lag` + `window` + max(`period`, `prior_period`) (228) | close, high, low. A NaN close in bars t-`lag`-`window`-max(`period`,`prior_period`)+1 .. t-`lag`, or a NaN high or low in bars t-`lag`-`window`-`period`+2 .. t-`lag`, gives NaN. A close not above 0 among those gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `lag` < 0, `window` < 1, `prior_period` < 1 | stateless. F equals `ScaledFallRangeMultipleComponent` (`period`, `lag`, `window`). With `lag` 6 the prior return is close[t-6] / close[t-48] - 1. Its usual size is the mean absolute 42-bar return over the same 180 bars ending at t-6. Bars after t-`lag` are not read. It is continuous in the prices while the stretch fell, and exactly 0 otherwise. One-sided in the fall, a delayed-rebound reading discounted by a prior slide. No `scaling_factor`: scale it with transforms |

```python class
class PriorSlideDiscountedScaledFallRangeMultipleComponent(SubStrategyComponent):
    """
    A delayed panic reading, discounted by the slide that came before it. With e = t - lag:

        m    = mean_{i=e-window+1..e} abs(close[i] / close[i-period] - 1)
        S(i) = max(high[i-period+1 .. i]) - min(low[i-period+1 .. i])
        B    = mean_{i=e-window+1..e} S(i)
        F    = max(0, -(close[e] / close[e-period] - 1) / m) * S(e) / B     (0 when m = 0 or B = 0)
        R    = close[e] / close[e-prior_period] - 1
        u    = mean_{i=e-window+1..e} abs(close[i] / close[i-prior_period] - 1)
        Q    = 1 + min(0, R / u)                                            (1 when u = 0)
        raw_value = F * Q                                                   (0.0 when F = 0)

    F is ScaledFallRangeMultipleComponent(period, lag, window). Q is 1 when the prior return is 0 or above.
    Q falls by one for each usual prior_period-bar move of slide, so it is 0 at one usual move and negative
    beyond. Q >= 1 - window, because abs(R) is one of the averaged terms.
    Range: signed. 0 when the stretch ending at e did not fall. During a fall: positive while the prior slide
    is shallower than one usual move, negative when deeper. F is at most window * window.
    Warm-up: lag + window + max(period, prior_period) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads close over bars e-window+1-max(period, prior_period) .. e, and high and low
    over bars e-window-period+2 .. e, with e = t - lag <= t. Every row read is at or before bar t.

    NaN: a NaN close, high or low among the rows read gives NaN, and so does a close not above 0 there
    (never on real bars).
    Building the component raises for a period below 1, a lag below 0, a window below 1, or a prior_period
    below 1.
    """

    def __init__(self, name="PriorSlideDiscountedPanic", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.lag = int(self.parameters.get("lag", 6))
        self.window = int(self.parameters.get("window", 180))
        self.prior_period = int(self.parameters.get("prior_period", 42))
        if self.period < 1:
            raise ValueError(f"PriorSlideDiscountedScaledFallRangeMultipleComponent: period must be >= 1, got {self.period}")
        if self.lag < 0:
            raise ValueError(f"PriorSlideDiscountedScaledFallRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        if self.window < 1:
            raise ValueError(f"PriorSlideDiscountedScaledFallRangeMultipleComponent: window must be >= 1, got {self.window}")
        if self.prior_period < 1:
            raise ValueError(
                f"PriorSlideDiscountedScaledFallRangeMultipleComponent: prior_period must be >= 1, got {self.prior_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float).to_numpy()
        high = data["high"].astype(float).to_numpy()
        low = data["low"].astype(float).to_numpy()
        p, q, w = self.period, self.prior_period, self.window
        e = len(close) - 1 - self.lag
        c_lo = e - w + 1 - max(p, q)
        hl_lo = e - w - p + 2
        cw = close[c_lo:e + 1]
        hw = high[hl_lo:e + 1]
        lw = low[hl_lo:e + 1]
        if np.isnan(cw).any() or np.isnan(hw).any() or np.isnan(lw).any() or not (cw > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        idx = np.arange(e - w + 1, e + 1)
        m = float(np.mean(np.abs(close[idx] / close[idx - p] - 1.0)))
        s_vals = np.array([np.max(high[i - p + 1:i + 1]) - np.min(low[i - p + 1:i + 1]) for i in idx])
        b = float(np.mean(s_vals))
        r_fall = close[e] / close[e - p] - 1.0
        if m == 0 or b == 0:
            f = 0.0
        else:
            f = max(0.0, -r_fall / m) * float(s_vals[-1]) / b
        r_prior = close[e] / close[e - q] - 1.0
        u = float(np.mean(np.abs(close[idx] / close[idx - q] - 1.0)))
        factor = 1.0 if u == 0 else 1.0 + min(0.0, r_prior / u)
        self._raw_value = float(f * factor) if f > 0 else 0.0
        self.confidence = 1.0
        self.debug_info = {"fall_range_multiple": f, "prior_return": float(r_prior),
                           "prior_usual_move": u, "prior_factor": factor}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.lag + self.window + max(self.period, self.prior_period)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    w = int(params.get("window", 180))
    q = int(params.get("prior_period", 42))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    e = len(c) - 1 - lag
    first = e - w + 1
    deepest = p if p > q else q
    for j in range(first - deepest, e + 1):
        if c[j] != c[j] or not c[j] > 0:
            return float("nan")
    for j in range(first - p + 1, e + 1):
        if h[j] != h[j] or lo[j] != lo[j]:
            return float("nan")

    def stretch_range(i):
        top = h[i - p + 1]
        bot = lo[i - p + 1]
        for j in range(i - p + 1, i + 1):
            if h[j] > top:
                top = h[j]
            if lo[j] < bot:
                bot = lo[j]
        return top - bot

    sum_abs_p = 0.0
    sum_abs_q = 0.0
    sum_s = 0.0
    for i in range(first, e + 1):
        sum_abs_p += abs(c[i] / c[i - p] - 1.0)
        sum_abs_q += abs(c[i] / c[i - q] - 1.0)
        sum_s += stretch_range(i)
    m = sum_abs_p / w
    u = sum_abs_q / w
    b = sum_s / w
    move = c[e] / c[e - p] - 1.0
    if m == 0 or b == 0 or not move < 0:
        return 0.0
    f = (-move / m) * (stretch_range(e) / b)
    if not f > 0:
        return 0.0
    prior = c[e] / c[e - q] - 1.0
    if u == 0 or prior >= 0:
        factor = 1.0
    else:
        factor = 1.0 + prior / u
    return f * factor
```

checks:
PriorSlideDiscountedScaledFallRangeMultipleComponent: every check passed
the bot's suite: == 1614 passed, 16 skipped, 75 deselected, 2244 warnings in 94.43s (0:01:34) ===
