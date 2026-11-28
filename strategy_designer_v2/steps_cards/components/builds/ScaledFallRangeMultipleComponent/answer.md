# ScaledFallRangeMultipleComponent: night10_fallagishort_run | 048-01_falling-agitated-wide-rise-giveback_1d | ScaledRiseRangeMultiple

## attempt 1

answer: built
class: ScaledFallRangeMultipleComponent
settings: {"period": 1, "lag": 0, "window": 30, "scale": "std", "side": "up"}
reason: `ScaledFallRangeMultipleComponent` computes this measure only on the fall side. The clip at 0 sits inside the product, so `negate` of the fall reading is not the scaled rise, and no other class gives this product (`RiseTimesRangeMultipleComponent` "up" uses the raw percent rise, not the rise in standard deviations). So the class is written again with a new setting, `side`, whose default "down" keeps today's output exactly.

table: Directional components
row: | `ScaledFallRangeMultipleComponent` | `period` (6), `lag` (6), `window` (180), `scale` ("mean_abs"), `side` ("down") | With e = t - `lag`, R = close[e] / close[e-`period`] - 1. `side` "down": max(0, -R / m) x S(e) / B. `side` "up": max(0, R / m) x S(e) / B. r(i) = close[i] / close[i-`period`] - 1 for i = e-`window`+1 .. e. With `scale` "mean_abs", m = mean of abs(r(i)). With `scale` "std", m = standard deviation (ddof 1) of r(i). S(i) = max(high[i-`period`+1 .. i]) - min(low[i-`period`+1 .. i]). B = mean of S(i) over i = e-`window`+1 .. e. The output is 0 when m = 0 or B = 0. With `period` 1, `lag` 0, `window` 30, "std", "up": max(0, (close[t]/close[t-1] - 1)) / s30 x (high[t] - low[t]) / mean(high[i] - low[i], i = t-29 .. t) | 0 and up, unbounded in practice, never negative; no direction. "down" is 0 when the stretch ending at bar e did not fall, and "up" is 0 when it did not rise. Each grows with the size of the move in usual `period`-bar moves (mean absolute move, or standard deviation with "std") and with the stretch's range in usual `period`-bar ranges. The range factor is at most `window`, because the stretch's own range is among those averaged. With "mean_abs" the move factor is also at most `window`; with "std" it is unbounded | graded | usual `period`-bar moves (mean absolute, or standard deviations) x mean `period`-bar ranges | `window` + `period` + `lag` (192; 31 at the wished settings) | close, high, low. A NaN close in bars t-`lag`-`window`-`period`+1 .. t-`lag`, or a NaN high or low in bars t-`lag`-`window`-`period`+2 .. t-`lag`, gives NaN. A close not above 0 there also gives NaN (never on real bars). m = 0 or B = 0 gives 0 (never on real bars). These settings raise when the component is built: `period` < 1, `lag` < 0, `window` < 1, `scale` other than "mean_abs" or "std", `scale` "std" with `window` < 2, `side` other than "down" or "up" | stateless. `scale` "mean_abs" with `side` "down" (the defaults) is the original output, unchanged. "std" counts the move in standard deviations of the window's `period`-bar returns, which no config step gives, hence that setting. `side` "up" is the rise-side mirror. `negate` on "down" is not it, because the clip at 0 is inside the product, and no config step gives it, hence the setting. Bars after t-`lag` are not read, so the value at t is the `lag` 0 value at bar t-`lag`. It is continuous in the prices while the stretch moved to the counted side, and exactly 0 otherwise. On 1d bars, `period` 1, `lag` 0, `window` 30, "std" and "up" give the day's rise in 30-day standard deviations times the day's range over its 30-day mean range. One-sided for each side. No `scaling_factor`: scale it with transforms |

```python class
class ScaledFallRangeMultipleComponent(SubStrategyComponent):
    """
    A stretch's move in usual moves, times its range in usual ranges, on every bar:

        e = t - lag
        R = close[e] / close[e - period] - 1
        r(i) = close[i] / close[i - period] - 1,            i = e - window + 1 .. e
        scale = "mean_abs" (default): m = mean(abs(r(i)))
        scale = "std":                m = std (ddof 1) of r(i)
        S(i) = max(high[i - period + 1 .. i]) - min(low[i - period + 1 .. i])
        B = mean(S(i)),                                     i = e - window + 1 .. e
        side = "down" (default): raw_value = max(0, -R / m) x S(e) / B
        side = "up":             raw_value = max(0,  R / m) x S(e) / B
        raw_value = 0.0 when m = 0 or B = 0

    With period 1, lag 0, window 30, scale "std", side "up":
    max(0, close[t]/close[t-1] - 1) / s30 x (high[t] - low[t]) / mean(high[i] - low[i], i = t-29 .. t).

    Range and sign: 0 and up, never negative, no direction. "down" is 0 when the stretch did not fall, and
    "up" is 0 when it did not rise. The range factor is at most window. The move factor is at most window
    with "mean_abs" and unbounded with "std".
    The defaults (scale "mean_abs", side "down") are the original output, unchanged.
    Warm-up: window + period + lag rows, bar t included.
    NaN: a NaN close in bars e-window-period+1 .. e, or a NaN high or low in bars e-window-period+2 .. e,
    gives NaN, and so does a close not above 0 there (never on real bars).
    Building the component raises for period < 1, lag < 0, window < 1, an unknown scale, scale "std" with
    window < 2, or a side other than "down" or "up".

    WHY THIS CANNOT LEAK: it reads only close, high and low of the rows from e - window - period + 1 up to
    e = t - lag, all at or before bar t (the last row of data). Every value is known at that bar's close.
    """

    def __init__(self, name="ScaledFallRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.lag = int(self.parameters.get("lag", 6))
        self.window = int(self.parameters.get("window", 180))
        self.scale = self.parameters.get("scale", "mean_abs")
        self.side = self.parameters.get("side", "down")
        if self.period < 1:
            raise ValueError(f"ScaledFallRangeMultipleComponent: period must be >= 1, got {self.period}")
        if self.lag < 0:
            raise ValueError(f"ScaledFallRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        if self.window < 1:
            raise ValueError(f"ScaledFallRangeMultipleComponent: window must be >= 1, got {self.window}")
        if self.scale not in ("mean_abs", "std"):
            raise ValueError(f"ScaledFallRangeMultipleComponent: scale must be 'mean_abs' or 'std', got {self.scale!r}")
        if self.scale == "std" and self.window < 2:
            raise ValueError("ScaledFallRangeMultipleComponent: scale 'std' needs window >= 2")
        if self.side not in ("down", "up"):
            raise ValueError(f"ScaledFallRangeMultipleComponent: side must be 'down' or 'up', got {self.side!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data["close"].astype(float).to_numpy()
        h = data["high"].astype(float).to_numpy()
        lo = data["low"].astype(float).to_numpy()
        p, w = self.period, self.window
        e = len(c) - 1 - self.lag
        cw = c[e - w - p + 1: e + 1]
        hw = h[e - w - p + 2: e + 1]
        lw = lo[e - w - p + 2: e + 1]
        if np.isnan(cw).any() or np.isnan(hw).any() or np.isnan(lw).any() or not (cw > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        idx = np.arange(e - w + 1, e + 1)
        r = c[idx] / c[idx - p] - 1.0
        if self.scale == "std":
            m = float(np.std(r, ddof=1))
        else:
            m = float(np.mean(np.abs(r)))
        S = np.array([np.max(h[i - p + 1: i + 1]) - np.min(lo[i - p + 1: i + 1]) for i in idx])
        B = float(np.mean(S))
        R = float(c[e] / c[e - p] - 1.0)
        if not m > 0 or not B > 0:
            value = 0.0
        else:
            move = -R if self.side == "down" else R
            value = max(0.0, move / m) * float(S[-1]) / B
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"return": R, "m": m, "range": float(S[-1]), "mean_range": B,
                           "scale": self.scale, "side": self.side}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.window + self.period + self.lag
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    w = int(params.get("window", 180))
    scale = params.get("scale", "mean_abs")
    side = params.get("side", "down")
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    e = len(c) - 1 - lag
    # rows read: closes e-w-p+1 .. e, highs/lows e-w-p+2 .. e
    for j in range(e - w - p + 1, e + 1):
        if c[j] != c[j] or not c[j] > 0:
            return float("nan")
    for j in range(e - w - p + 2, e + 1):
        if h[j] != h[j] or l[j] != l[j]:
            return float("nan")
    rets = []
    ranges = []
    for i in range(e - w + 1, e + 1):
        rets.append(c[i] / c[i - p] - 1.0)
        hi = h[i - p + 1]
        lo = l[i - p + 1]
        for j in range(i - p + 1, i + 1):
            if h[j] > hi:
                hi = h[j]
            if l[j] < lo:
                lo = l[j]
        ranges.append(hi - lo)
    n = len(rets)
    if scale == "std":
        mu = sum(rets) / n
        ss = 0.0
        for x in rets:
            ss += (x - mu) ** 2
        m = math.sqrt(ss / (n - 1))
    else:
        m = sum(abs(x) for x in rets) / n
    B = sum(ranges) / len(ranges)
    if not m > 0 or not B > 0:
        return 0.0
    R = c[e] / c[e - p] - 1.0
    move = -R if side == "down" else R
    if move <= 0:
        return 0.0
    return (move / m) * (ranges[-1] / B)
```

checks:
ScaledFallRangeMultipleComponent: every check passed
the bot's suite: = 1685 passed, 16 skipped, 75 deselected, 95636 warnings in 137.93s (0:02:17) ==
