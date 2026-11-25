# MeanAbsScaledReturnComponent: night7_panic_run | 036-02_range-scaled-rally-continuation_1d | RangeScaledReturnComponent

## attempt 1

answer: built
class: MeanAbsScaledReturnComponent
settings: {"period": 3, "window": 30, "base": "mean_relative_range"}
reason: The wished measure is a `period`-bar return counted in usual moves, which `MeanAbsScaledReturnComponent` already computes. The only difference is the base: the mean of the bar range over the close instead of the mean absolute `period`-bar return. Under rule 1 that is the same measure with another base, so I rewrote that class with a new `base` setting whose default ("mean_abs_return") keeps today's output exactly.

table: Directional components
row: | `MeanAbsScaledReturnComponent` | `period` (24), `window` (720), `base` ("mean_abs_return") | (close[t] / close[t-`period`] - 1) / m. `base` "mean_abs_return": m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`period`] - 1), the overlapping `period`-bar simple returns ending at each of the last `window` bars, bar t included. `base` "mean_relative_range": m = mean over i = t-`window`+1 .. t of (high[i] - low[i]) / close[i], bar t included. 0 when m = 0. With `period` 3, `window` 30 and "mean_relative_range": the 3-bar return over the 30-bar mean of the bar range as a fraction of its close | unbounded in practice, signed like the `period`-bar return; 0 for a flat move. "mean_abs_return": its size is at most `window` (today's return is one of the `window` returns averaged in m), about -1 for a fall of one usual move. "mean_relative_range": its size grows as the move gets larger against the usual bar range, unbounded above | graded | "mean_abs_return": usual `period`-bar moves. "mean_relative_range": mean bar ranges (as a fraction of the close) | `window` + `period` (744) with "mean_abs_return"; max(`window`, `period` + 1) with "mean_relative_range" (30 at the wished settings) | "mean_abs_return": closes only; a NaN close in the last `window` + `period` rows gives NaN, and so does a close not above 0 there (never on real bars). "mean_relative_range": close (bars t-`window`+1 .. t and bar t-`period`), high and low (last `window` rows); a NaN in any of those gives NaN, and so does a close not above 0 among them (never on real bars). m = 0 gives 0 (never on real bars). These settings raise when the component is built: `period` < 1, `window` < 1, `base` other than "mean_abs_return" or "mean_relative_range" | stateless. `base` "mean_abs_return" (default) is the original output, unchanged. "mean_relative_range" counts the move in usual daily ranges (high − low over the close) rather than in usual `period`-bar moves, and no config step divides by a window's mean range, hence the setting. With "mean_relative_range" the value is continuous in the prices. On 1d bars, `period` 3, `window` 30 and "mean_relative_range" give the 3-day return in multiples of the 30-day mean daily range. `negate` gives the fall-positive reading. No `scaling_factor`: scale it with transforms |

```python class
class MeanAbsScaledReturnComponent(SubStrategyComponent):
    """
    A period-bar simple return counted in usual moves, on every bar:

        R = close[t] / close[t - period] - 1
        base = "mean_abs_return" (default):
            m = mean over i = t-window+1 .. t of abs(close[i] / close[i - period] - 1)
                (the overlapping period-bar returns ending at each of the last window bars, bar t included)
        base = "mean_relative_range":
            m = mean over i = t-window+1 .. t of (high[i] - low[i]) / close[i]   (bar t included)
        raw_value = R / m, and 0.0 when m = 0

    The default base is the original output, unchanged. With period 3, window 30 and base "mean_relative_range"
    on 1d bars it is the 3-day return in multiples of the 30-day mean daily range (as a fraction of the close).
    Range and sign: unbounded in practice, signed like the period-bar return, 0 for a flat move. With
    "mean_abs_return" its size is at most window.
    Warm-up: window + period rows ("mean_abs_return"), max(window, period + 1) rows ("mean_relative_range"),
    bar t included.

    NaN: "mean_abs_return": a NaN close, or a close not above 0, in the last window + period rows gives NaN.
    "mean_relative_range": a NaN close, high or low in the last window rows, or a NaN close[t - period], gives
    NaN, and so does a close not above 0 among those read (never on real bars). m = 0 gives 0.0.
    Building raises for period < 1, window < 1, or a base other than "mean_abs_return" or "mean_relative_range".

    WHY THIS CANNOT LEAK: it reads only the close (and, with "mean_relative_range", the high and low) of rows up
    to and including bar t, the last row of data: at most the last window + period rows ("mean_abs_return") or
    the last max(window, period + 1) rows ("mean_relative_range"). Every value is known at bar t's close.
    """

    def __init__(self, name="MeanAbsScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        if self.period < 1:
            raise ValueError(f"MeanAbsScaledReturnComponent: period must be >= 1, got {self.period}")
        self.window = int(self.parameters.get("window", 720))
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledReturnComponent: window must be >= 1, got {self.window}")
        self.base = self.parameters.get("base", "mean_abs_return")
        if self.base not in ("mean_abs_return", "mean_relative_range"):
            raise ValueError(
                "MeanAbsScaledReturnComponent: base must be 'mean_abs_return' or 'mean_relative_range', "
                f"got {self.base!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        w = self.window
        c = data["close"].astype(float).to_numpy()
        n = len(c)
        t = n - 1
        if self.base == "mean_abs_return":
            seg = c[n - w - p:]
            if np.isnan(seg).any() or not (seg > 0).all():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            rets = np.abs(seg[p:] / seg[:-p] - 1.0)
            m = float(np.mean(rets))
        else:
            h = data["high"].astype(float).to_numpy()[n - w:]
            lo = data["low"].astype(float).to_numpy()[n - w:]
            cw = c[n - w:]
            cb = c[t - p]
            if (np.isnan(h).any() or np.isnan(lo).any() or np.isnan(cw).any() or np.isnan(cb)
                    or not (cw > 0).all() or not cb > 0):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            m = float(np.mean((h - lo) / cw))
        r = float(c[t] / c[t - p] - 1.0)
        if np.isnan(r):
            self._raw_value = float("nan")
        elif m == 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float(r / m)
        self.confidence = 1.0
        self.debug_info = {"return": r, "usual_move": m, "base": self.base}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        if self.base == "mean_relative_range":
            return max(self.window, self.period + 1)
        return self.window + self.period
```

```python hand
def hand(df, params):
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    base = params.get("base", "mean_abs_return")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    def bad(x):
        return x != x or not x > 0

    if base == "mean_relative_range":
        h = [float(x) for x in list(df["high"])]
        lo = [float(x) for x in list(df["low"])]
        total = 0.0
        for i in range(t - w + 1, t + 1):
            if h[i] != h[i] or lo[i] != lo[i] or bad(c[i]):
                return float("nan")
            total = total + (h[i] - lo[i]) / c[i]
        if bad(c[t - p]):
            return float("nan")
        m = total / w
    else:
        for i in range(t - w - p + 1, t + 1):
            if bad(c[i]):
                return float("nan")
        total = 0.0
        for i in range(t - w + 1, t + 1):
            total = total + abs(c[i] / c[i - p] - 1.0)
        m = total / w
    r = c[t] / c[t - p] - 1.0
    if m == 0:
        return 0.0
    return r / m
```

checks:
MeanAbsScaledReturnComponent: every check passed
the bot's suite: == 1658 passed, 16 skipped, 75 deselected, 2244 warnings in 117.53s (0:01:57) ==
