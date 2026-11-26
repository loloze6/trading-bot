# ClosingRangeInUsualMovesComponent: night7c_rangefail_run | 032-02.b1.e1.e1_tight-range-breakouts-continue_1d | ClosingRangeInUsualMovesComponent

## attempt 1

answer: built
class: ClosingRangeInUsualMovesComponent
settings: {"period": 60, "window": 60, "form": "width"}
reason: No catalogue component divides the closing range of the bars before t by the usual one-bar move. `RangeCompressionRatioComponent` reads highs and lows against a range or mean bar range, and `DonchianBreakoutComponent` "close" gives a position, not a width. The bounded "compression" form 1 / (1 + width) is given by no config step, so it is a `form` setting on the same class.

table: Regime measures
row: | `ClosingRangeInUsualMovesComponent` | `period` (60), `window` (60), `form` ("width") | W = (max(close[t-`period` .. t-1]) − min(close[t-`period` .. t-1])) / close[t-1] / m, where m = mean of abs(close[j] / close[j-1] − 1) over the last `window` one-bar returns, j = t-`window`+1 .. t, bar t's included. `form` "width": W. `form` "compression": 1 / (1 + W). W is 0 when m = 0 | "width": 0 and up, unbounded above, never negative; no direction; grows as the closing range before bar t widens in usual one-bar moves. "compression": above 0, up to 1, never negative; no direction; 1 for a zero range, growing as the range narrows | regime measure | "width": usual one-bar moves. "compression": dimensionless (0 to 1) | max(`period`, `window`) + 1 (61) | Closes only (bars t-max(`period`, `window`) .. t). A NaN close among those rows gives NaN, and so does a close not above 0 there (never on real bars). m = 0 gives W = 0 (never on real bars). These settings raise when the component is built: `period` < 2, `window` < 1, `form` other than "width" or "compression" | Stateless. The range excludes bar t, so bar t's break cannot widen it. The usual move includes bar t's return. Graded and continuous in the closes. "compression" is 1 / (1 + "width"), which no config step gives, hence the setting. Not `RangeCompressionRatioComponent`, which reads highs and lows. No `scaling_factor`: scale it with transforms |

```python class
class ClosingRangeInUsualMovesComponent(SubStrategyComponent):
    """
    The closing range of the bars before bar t, counted in usual one-bar moves:

        H = max(close[t-period .. t-1]), L = min(close[t-period .. t-1])    (bar t excluded)
        m = mean(abs(close[j] / close[j-1] - 1)), j = t-window+1 .. t      (bar t's return included)
        W = (H - L) / close[t-1] / m       (W = 0 when m = 0)
        form = "width" (default):  raw_value = W
        form = "compression":      raw_value = 1 / (1 + W)

    Range and sign: "width" is 0 and up, unbounded above, never negative, with no direction. It grows as the
    closing range widens in usual moves. "compression" is above 0 and up to 1, never negative. It is 1 for a
    zero range and grows as the range narrows.
    Warm-up: max(period, window) + 1 rows, bar t included.
    NaN: a NaN close among the rows read gives NaN, and so does a close not above 0 there (never on real bars).
    m = 0 gives W = 0 (never on real bars).
    Building the component raises for a period below 2, a window below 1, or a form other than "width" or
    "compression".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, window) + 1 rows of data,
    the last row being bar t; no later row exists in data, and the range itself stops at bar t-1.
    """

    def __init__(self, name="ClosingRangeInUsualMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 60))
        if self.period < 2:
            raise ValueError(f"ClosingRangeInUsualMovesComponent: period must be >= 2, got {self.period}")
        self.window = int(self.parameters.get("window", 60))
        if self.window < 1:
            raise ValueError(f"ClosingRangeInUsualMovesComponent: window must be >= 1, got {self.window}")
        self.form = self.parameters.get("form", "width")
        if self.form not in ("width", "compression"):
            raise ValueError(
                f"ClosingRangeInUsualMovesComponent: form must be 'width' or 'compression', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        req = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-req:]
        t = len(c) - 1
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rng = c[t - self.period:t]
        hi = float(np.max(rng))
        lo = float(np.min(rng))
        seg = c[t - self.window:t + 1]
        m = float(np.mean(np.abs(seg[1:] / seg[:-1] - 1.0)))
        if m == 0.0:
            w = 0.0
        else:
            w = (hi - lo) / c[t - 1] / m
        if self.form == "compression":
            self._raw_value = float(1.0 / (1.0 + w))
        else:
            self._raw_value = float(w)
        self.confidence = 1.0
        self.debug_info = {"range_high": hi, "range_low": lo, "usual_move": m, "width": w}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period, self.window) + 1
```

```python hand
def hand(df, params):
    period = int(params.get("period", 60))
    window = int(params.get("window", 60))
    form = params.get("form", "width")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    first = t - max(period, window)
    for i in range(first, t + 1):
        x = c[i]
        if x != x or not x > 0:
            return float("nan")
    # closing range over bars t-period .. t-1
    hi = c[t - period]
    lo = c[t - period]
    for i in range(t - period, t):
        if c[i] > hi:
            hi = c[i]
        if c[i] < lo:
            lo = c[i]
    # usual one-bar move: returns j = t-window+1 .. t
    total = 0.0
    for j in range(t - window + 1, t + 1):
        r = c[j] / c[j - 1] - 1.0
        total = total + (r if r >= 0 else -r)
    m = total / window
    if m == 0.0:
        w = 0.0
    else:
        w = (hi - lo) / c[t - 1] / m
    if form == "compression":
        return 1.0 / (1.0 + w)
    return w
```

checks:
ClosingRangeInUsualMovesComponent: every check passed
the bot's suite: == 1658 passed, 16 skipped, 75 deselected, 2244 warnings in 95.51s (0:01:35) ===
