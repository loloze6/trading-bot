# VolScaledBreakAboveHighComponent: night3_1h_run | 018-02_hourly-breakout-multiday-continuation_1h | VolScaledBreakAboveHighComponent

## attempt 1

answer: built
class: VolScaledBreakAboveHighComponent
settings: {"period": 480, "step": 24, "steps": 30}
reason: No component computes the close's break above the prior high scaled by the mean absolute daily move. `DistanceFromHighComponent` (`source` "high", `exclude_current` 1) measures the break against R, not close[t], has no volatility scaling, and is signed rather than clipped at 0. No existing class computes the same measure, so a new class is needed.

table: Directional components
row: | `VolScaledBreakAboveHighComponent` | `period` (480), `step` (24), `steps` (30) | max(0, close[t] − H) / close[t] / m. H = max(high[t-`period`] .. high[t-1]), bar t excluded. m = mean over k = 0 .. `steps`-1 of abs(close[t-k·`step`] / close[t-(k+1)·`step`] − 1), the last `steps` non-overlapping `step`-bar returns ending at bar t. The output is 0 when m = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 while the close is at or below the prior high and grows as the close sits more usual daily moves above it | graded | usual `step`-bar moves | max(`period` + 1, `step` × `steps` + 1) (721) | high, close. A NaN high in bars t-`period` .. t-1, a NaN close[t], or a NaN among the `steps` + 1 closes used gives NaN. A close not above 0 among those gives NaN (never on real bars). m = 0 gives 0: the numerator is then 0 too, because high[t-`step`] ≥ close[t-`step`] = close[t]. These settings raise when the component is built: `period` < 1, `step` < 1, `steps` < 1 | stateless. One-sided, a breakout-continuation reading; it is exactly 0 on most bars but continuous in the prices. The numerator is divided by close[t], not by H. On 1h bars the defaults are a 20-day prior high and the mean absolute 24-bar return over 30 days. No `scaling_factor`: scale it with transforms |

```python class
class VolScaledBreakAboveHighComponent(SubStrategyComponent):
    """
    How far the close has broken above the prior high, in usual step-bar moves, on every bar:

        H = max(high[t - period] .. high[t - 1])                         (bar t excluded)
        m = mean over k = 0 .. steps-1 of abs(close[t - k*step] / close[t - (k+1)*step] - 1)
        raw_value = max(0, close[t] - H) / close[t] / m                  (0 when m = 0)

    With the defaults (period 480, step 24, steps 30) on 1h bars: the break above the prior 20-day high,
    as a fraction of the close, divided by the mean absolute daily return over the last 30 daily steps.
    Range: 0 and up, unbounded above, never negative. It is 0 while close[t] <= H and grows continuously
    as the close sits further above the prior high, in usual moves. Graded, one-sided, with no direction.
    m = 0 happens only when close[t] = close[t-step]. Then high[t-step] >= close[t] lies inside the prior
    window, so the numerator is 0 too, and the output is 0.
    Warm-up: max(period + 1, step * steps + 1) rows, bar t included (721 at the defaults).

    WHY THIS CANNOT LEAK: it reads the `high` column of rows t-period .. t-1 and the `close` column of
    rows t, t-step, ..., t-steps*step, all at or before bar t (the last row of data). Each value is known
    at its bar's close.

    NaN: a NaN high in the prior window, a NaN close[t] or a NaN among the closes used gives NaN. A close
    not above 0 among them gives NaN (never on real bars). Building the component raises for a period,
    step or steps below 1.
    """

    def __init__(self, name="VolScaledBreakAboveHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 480))
        if self.period < 1:
            raise ValueError(f"VolScaledBreakAboveHighComponent: period must be >= 1, got {self.period}")
        self.step = int(self.parameters.get("step", 24))
        if self.step < 1:
            raise ValueError(f"VolScaledBreakAboveHighComponent: step must be >= 1, got {self.step}")
        self.steps = int(self.parameters.get("steps", 30))
        if self.steps < 1:
            raise ValueError(f"VolScaledBreakAboveHighComponent: steps must be >= 1, got {self.steps}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        high = data['high'].astype(float).to_numpy()
        close = data['close'].astype(float).to_numpy()
        n = len(close)
        prior = high[n - 1 - self.period:n - 1]
        c = close[n - 1]
        if np.isnan(prior).any() or np.isnan(c) or not c > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        h = float(prior.max())
        idx = [n - 1 - k * self.step for k in range(self.steps + 1)]
        pts = close[idx]
        if np.isnan(pts).any() or not (pts > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        moves = np.abs(pts[:-1] / pts[1:] - 1.0)
        m = float(moves.mean())
        brk = max(0.0, c - h) / c
        self._raw_value = float(brk / m) if m > 0 else 0.0
        self.confidence = 1.0
        self.debug_info = {'prior_high': h, 'break_frac': brk, 'mean_abs_move': m}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period + 1, self.step * self.steps + 1)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 480))
    step = int(params.get("step", 24))
    steps = int(params.get("steps", 30))
    hi = [float(x) for x in list(df["high"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1
    c = cl[t]
    if c != c or not c > 0:
        return float("nan")
    h = None
    j = t - p
    while j <= t - 1:
        x = hi[j]
        if x != x:
            return float("nan")
        if h is None or x > h:
            h = x
        j = j + 1
    total = 0.0
    k = 0
    while k < steps:
        a = cl[t - k * step]
        b = cl[t - (k + 1) * step]
        if a != a or b != b or not a > 0 or not b > 0:
            return float("nan")
        r = a / b - 1.0
        if r < 0:
            r = -r
        total = total + r
        k = k + 1
    m = total / steps
    diff = c - h
    if diff < 0:
        diff = 0.0
    if not m > 0:
        return 0.0
    return (diff / c) / m
```

checks:
VolScaledBreakAboveHighComponent: every check passed
the bot's suite: ======= 1579 passed, 16 skipped, 75 deselected, 2244 warnings in 56.45s ========
