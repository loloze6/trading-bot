# ScaledFallRangeMultipleComponent: night7_chopreversal_run | 044-01_agitated-wide-range-fall-rebound_1d | FallStdScaledRangeMultipleComponent

## attempt 1

answer: built
class: ScaledFallRangeMultipleComponent
settings: {"period": 1, "lag": 0, "window": 30, "scale": "std"}
reason: `ScaledFallRangeMultipleComponent` with `period` 1, `lag` 0 and `window` 30 already computes this measure: the day's fall in usual one-bar moves times the day's range over its 30-day mean range, on the same 30 returns and 30 bars. The only difference is that it measures the usual move as the mean absolute return, while the wish uses the standard deviation (ddof 1). That is another statistic of the same base, so the class is rewritten with a `scale` setting whose default "mean_abs" keeps today's output exactly.

table: Directional components
row: | `ScaledFallRangeMultipleComponent` | `period` (6), `lag` (6), `window` (180), `scale` ("mean_abs") | max(0, -(close[e] / close[e-`period`] - 1) / m) x S(e) / B, with e = t - `lag`. r(i) = close[i] / close[i-`period`] - 1 for i = e-`window`+1 .. e. With `scale` "mean_abs", m = mean of abs(r(i)). With `scale` "std", m = standard deviation (ddof 1) of r(i). S(i) = max(high[i-`period`+1 .. i]) - min(low[i-`period`+1 .. i]). B = mean of S(i) over i = e-`window`+1 .. e. The output is 0 when m = 0 or B = 0. With `period` 1, `lag` 0, `window` 30 and "std": max(0, -(close[t]/close[t-1] - 1)) / s30 x (high[t] - low[t]) / mean(high[i] - low[i], i = t-29 .. t) | 0 and up, unbounded in practice, never negative; no direction. It is 0 when the stretch ending at bar e did not fall. It grows with the depth of the fall in usual `period`-bar moves (mean absolute move, or standard deviation with "std") and with the stretch's range in usual `period`-bar ranges. The range factor is at most `window`, because the stretch's own range is among those averaged. With "mean_abs" the fall factor is also at most `window`; with "std" it is unbounded | graded | usual `period`-bar moves (mean absolute, or standard deviations) x mean `period`-bar ranges | `window` + `period` + `lag` (192; 31 at the wished settings) | close, high, low. A NaN close in bars t-`lag`-`window`-`period`+1 .. t-`lag`, or a NaN high or low in bars t-`lag`-`window`-`period`+2 .. t-`lag`, gives NaN. A close not above 0 there also gives NaN (never on real bars). m = 0 or B = 0 gives 0 (never on real bars). These settings raise when the component is built: `period` < 1, `lag` < 0, `window` < 1, `scale` other than "mean_abs" or "std", `scale` "std" with `window` < 2 | stateless. `scale` "mean_abs" (default) is the original output, unchanged. "std" counts the fall in standard deviations of the window's `period`-bar returns, which no config step gives, hence the setting. Bars after t-`lag` are not read, so the value at t is the `lag` 0 value at bar t-`lag`. It is continuous in the prices while the stretch fell, and exactly 0 on stretches that rose or were flat. On 1d bars, `period` 1, `lag` 0, `window` 30 and "std" give the day's fall in 30-day standard deviations times the day's range over its 30-day mean range. One-sided, a rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class ScaledFallRangeMultipleComponent(SubStrategyComponent):
    """
    The fall of a stretch in usual moves, times its range in usual ranges, on every bar:

        e = t - lag
        r(i) = close[i] / close[i - period] - 1,              i = e - window + 1 .. e
        scale = "mean_abs" (default): m = mean(abs(r(i)))
        scale = "std":                m = std (ddof 1) of r(i)
        S(i) = max(high[i - period + 1 .. i]) - min(low[i - period + 1 .. i])
        B = mean(S(i)),                                       i = e - window + 1 .. e
        raw_value = max(0, -r(e) / m) x S(e) / B              (0.0 when m = 0 or B = 0)

    With period 1, lag 0, window 30 and scale "std" the output is
    max(0, -(close[t]/close[t-1] - 1)) / s30 x (high[t] - low[t]) / mean(high[i] - low[i], i = t-29 .. t).
    scale "mean_abs" (default) is the original output, unchanged.

    Range: 0 and up, never negative, no direction. It is 0 when the stretch ending at bar e did not fall.
    The range factor is at most window. The fall factor is at most window with "mean_abs" and unbounded with
    "std". It is graded and continuous in the prices while the stretch fell.
    Warm-up: window + period + lag rows, bar t included.

    NaN: a NaN close in bars e-window-period+1 .. e, or a NaN high or low in bars e-window-period+2 .. e,
    gives NaN. A close not above 0 there gives NaN (never on real bars). m = 0 or B = 0 gives 0.0.
    Building the component raises for period < 1, lag < 0, window < 1, a scale other than "mean_abs" or
    "std", or scale "std" with window < 2.

    WHY THIS CANNOT LEAK: it reads only the close, high and low of rows up to bar t - lag (at most the last
    window + period + lag rows of data, whose last row is bar t); no later row exists in data.
    """

    def __init__(self, name="ScaledFallRangeMultiple", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 6))
        self.lag = int(self.parameters.get("lag", 6))
        self.window = int(self.parameters.get("window", 180))
        self.scale = self.parameters.get("scale", "mean_abs")
        if self.period < 1:
            raise ValueError(f"ScaledFallRangeMultipleComponent: period must be >= 1, got {self.period}")
        if self.lag < 0:
            raise ValueError(f"ScaledFallRangeMultipleComponent: lag must be >= 0, got {self.lag}")
        if self.window < 1:
            raise ValueError(f"ScaledFallRangeMultipleComponent: window must be >= 1, got {self.window}")
        if self.scale not in ("mean_abs", "std"):
            raise ValueError(
                f"ScaledFallRangeMultipleComponent: scale must be 'mean_abs' or 'std', got {self.scale!r}")
        if self.scale == "std" and self.window < 2:
            raise ValueError(
                f"ScaledFallRangeMultipleComponent: scale 'std' needs window >= 2, got {self.window}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p, w = self.period, self.window
        n = len(data)
        e = n - 1 - self.lag
        close = data["close"].astype(float).to_numpy()
        high = data["high"].astype(float).to_numpy()
        low = data["low"].astype(float).to_numpy()
        c_seg = close[e - w - p + 1: e + 1]
        h_seg = high[e - w - p + 2: e + 1]
        l_seg = low[e - w - p + 2: e + 1]
        if np.isnan(c_seg).any() or np.isnan(h_seg).any() or np.isnan(l_seg).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if (c_seg <= 0).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        idx = np.arange(e - w + 1, e + 1)
        rets = close[idx] / close[idx - p] - 1.0
        if self.scale == "std":
            m = float(np.std(rets, ddof=1))
        else:
            m = float(np.mean(np.abs(rets)))
        ranges = np.array([np.max(high[i - p + 1: i + 1]) - np.min(low[i - p + 1: i + 1]) for i in idx])
        b = float(np.mean(ranges))
        r_e = float(rets[-1])
        s_e = float(ranges[-1])
        if m == 0 or b == 0:
            value = 0.0
        else:
            value = max(0.0, -r_e / m) * s_e / b
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"return": r_e, "usual_move": m, "range": s_e, "mean_range": b, "scale": self.scale}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period + self.lag
```

```python hand
def hand(df, params):
    import math
    period = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    window = int(params.get("window", 180))
    scale = params.get("scale", "mean_abs")
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    e = t - lag
    # closes read: e-window-period+1 .. e ; highs/lows read: e-window-period+2 .. e
    for k in range(e - window - period + 1, e + 1):
        if c[k] != c[k]:
            return float("nan")
    for k in range(e - window - period + 2, e + 1):
        if h[k] != h[k] or lo[k] != lo[k]:
            return float("nan")
    for k in range(e - window - period + 1, e + 1):
        if not c[k] > 0:
            return float("nan")
    rets = []
    rngs = []
    for i in range(e - window + 1, e + 1):
        rets.append(c[i] / c[i - period] - 1.0)
        top = h[i - period + 1]
        bot = lo[i - period + 1]
        for k in range(i - period + 1, i + 1):
            if h[k] > top:
                top = h[k]
            if lo[k] < bot:
                bot = lo[k]
        rngs.append(top - bot)
    count = len(rets)
    if scale == "std":
        mu = sum(rets) / count
        ss = 0.0
        for x in rets:
            ss += (x - mu) * (x - mu)
        m = math.sqrt(ss / (count - 1))
    else:
        m = sum(abs(x) for x in rets) / count
    b = sum(rngs) / len(rngs)
    if m == 0 or b == 0:
        return 0.0
    fall = -(c[e] / c[e - period] - 1.0)
    if fall < 0:
        fall = 0.0
    return fall / m * rngs[-1] / b
```

checks:
ScaledFallRangeMultipleComponent: every check passed
the bot's suite: == 1657 passed, 16 skipped, 75 deselected, 2244 warnings in 123.92s (0:02:03) ==
