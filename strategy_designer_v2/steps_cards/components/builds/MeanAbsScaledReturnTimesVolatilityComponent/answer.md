# MeanAbsScaledReturnTimesVolatilityComponent: retest_weekend_run | 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week.d2_sunday-move-reverses-on-monday.d3_moderate-sunday-moves-reverse-most_1h | CappedScaledReturnTimesVolatilityComponent

## attempt 1

answer: built
class: MeanAbsScaledReturnTimesVolatilityComponent
settings: {"period": 24, "window": 720, "vol_period": 720, "cap": 2.0}
reason: `MeanAbsScaledReturnTimesVolatilityComponent` (24, 720, 720) already computes (return / m) x s, but it has no cap on the scaled move. A config `clip` on the product clips at a fixed level of the product, not at two usual moves before the multiplication by s, so no config step gives this. Scaled 24h moves beyond two usual moves are common on real bars, so the class is written again with a `cap` setting whose default (none) keeps today's output.

table: Directional components
row: | `MeanAbsScaledReturnTimesVolatilityComponent` | `period` (24), `window` (720), `vol_period` (720), `cap` (none) | x x s. x = (close[t] / close[t-`period`] - 1) / m, clipped to [-`cap`, +`cap`] when `cap` is set. m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`period`] - 1), the overlapping `period`-bar simple returns ending at each of the last `window` bars, bar t included. s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1, j = t-`vol_period`+1 .. t, bar t's included. x is 0 when m = 0 | unbounded, signed like the `period`-bar return; 0 for a flat move. Its size grows with the move in usual `period`-bar moves and with the hourly volatility s (s is 0 and up). The first factor is at most `window` in size, and at most `cap` when `cap` is set: linear up to `cap` usual moves, then flat | graded | usual `period`-bar moves (capped) x one-bar return std (fraction) | max(`window` + `period`, `vol_period` + 1) (744) | closes only. A NaN close in the last max(`window` + `period`, `vol_period` + 1) rows gives NaN, and so does a close not above 0 there (never on real bars). m = 0 gives 0 (never on real bars; the return is then 0 too). These settings raise when the component is built: `period` < 1, `window` < 1, `vol_period` < 2, `cap` set and not above 0 | stateless. `cap` none (default) is the original output, unchanged. With `cap` 2 the scaled move is clipped at two usual moves before it is multiplied by s. A `clip` on the output is not this, because it clips the product at a fixed level. It is continuous in the closes. On 1h bars the defaults give the 24h return in usual 24h moves over 30 days, times the 30-day hourly volatility. `negate` gives the against-the-move reading. No `scaling_factor`: scale it with transforms |

```python class
class MeanAbsScaledReturnTimesVolatilityComponent(SubStrategyComponent):
    """
    The period-bar return in usual period-bar moves (optionally capped), times the one-bar volatility:

        x = (close[t] / close[t-period] - 1) / m
        m = mean over i = t-window+1 .. t of abs(close[i] / close[i-period] - 1)   (bar t included)
        x = 0 when m = 0
        cap = None (default): x unchanged (the original output)
        cap = c > 0:          x = clip(x, -c, +c)
        s = std (ddof 1) of r[j] = close[j] / close[j-1] - 1, j = t-vol_period+1 .. t
        raw_value = x * s

    Range: unbounded, signed like the period-bar return, 0 for a flat move. abs(x) is at most window (today's
    return is one of those averaged), and at most cap when cap is set. s is 0 and up.
    Graded: linear in the scaled move (up to cap usual moves, then flat), and growing with s.
    Warm-up: max(window + period, vol_period + 1) rows, bar t included (744 at the defaults).
    NaN: a NaN close, or a close not above 0, in the last max(window + period, vol_period + 1) rows gives NaN.
    m = 0 gives x = 0 (never on real bars).
    Building raises for period < 1, window < 1, vol_period < 2, or a cap that is set and not above 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window + period, vol_period + 1)
    rows of data, the last row being bar t; no later row exists in data.
    """

    def __init__(self, name="MeanAbsScaledReturnTimesVol", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 24))
        self.window = int(self.parameters.get("window", 720))
        self.vol_period = int(self.parameters.get("vol_period", 720))
        if self.period < 1:
            raise ValueError(f"MeanAbsScaledReturnTimesVolatilityComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"MeanAbsScaledReturnTimesVolatilityComponent: window must be >= 1, got {self.window}")
        if self.vol_period < 2:
            raise ValueError(
                f"MeanAbsScaledReturnTimesVolatilityComponent: vol_period must be >= 2, got {self.vol_period}")
        cap = self.parameters.get("cap", None)
        if cap is not None:
            try:
                cap = float(cap)
            except (TypeError, ValueError):
                raise ValueError(f"MeanAbsScaledReturnTimesVolatilityComponent: cap must be a number > 0, got {cap!r}")
            if not cap > 0:
                raise ValueError(f"MeanAbsScaledReturnTimesVolatilityComponent: cap must be > 0, got {cap!r}")
        self.cap = cap
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-need:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        t = len(c) - 1
        p = self.period
        idx = np.arange(t - self.window + 1, t + 1)
        rets = c[idx] / c[idx - p] - 1.0
        m = float(np.mean(np.abs(rets)))
        x = (c[t] / c[t - p] - 1.0) / m if m > 0 else 0.0
        if self.cap is not None:
            x = min(max(x, -self.cap), self.cap)
        j = np.arange(t - self.vol_period + 1, t + 1)
        r1 = c[j] / c[j - 1] - 1.0
        s = float(np.std(r1, ddof=1))
        self._raw_value = float(x * s)
        self.confidence = 1.0
        self.debug_info = {"scaled_move": float(x), "mean_abs_return": m, "vol": s, "cap": self.cap}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.window + self.period, self.vol_period + 1)
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    vp = int(params.get("vol_period", 720))
    cap = params.get("cap", None)
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(w + p, vp + 1)
    for k in range(need):
        x = c[t - k]
        if x != x or not x > 0:
            return float("nan")
    # usual period-bar move: mean abs of the overlapping returns ending at t-w+1 .. t
    total = 0.0
    for i in range(t - w + 1, t + 1):
        total += abs(c[i] / c[i - p] - 1.0)
    m = total / w
    if m > 0:
        x = (c[t] / c[t - p] - 1.0) / m
    else:
        x = 0.0
    if cap is not None:
        cap = float(cap)
        if x > cap:
            x = cap
        if x < -cap:
            x = -cap
    # ddof-1 std of the last vp one-bar returns
    r = []
    for j in range(t - vp + 1, t + 1):
        r.append(c[j] / c[j - 1] - 1.0)
    mean_r = sum(r) / len(r)
    ss = 0.0
    for v in r:
        ss += (v - mean_r) ** 2
    s = math.sqrt(ss / (len(r) - 1))
    return x * s
```

checks:
MeanAbsScaledReturnTimesVolatilityComponent: every check passed
the bot's suite: == 1637 passed, 16 skipped, 75 deselected, 2244 warnings in 96.97s (0:01:36) ===
