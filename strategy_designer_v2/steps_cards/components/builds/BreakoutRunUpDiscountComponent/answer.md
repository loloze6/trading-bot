# BreakoutRunUpDiscountComponent: night7c_rangefail_run | 032-02.b1.e1.e2_unextended-breakouts-keep-rising_1d | BreakoutRunUpDiscount

## attempt 1

answer: built
class: BreakoutRunUpDiscountComponent
settings: {"period": 60, "rise_period": 20, "rise_lag": 1, "window": 120}
reason: No component gates a run-up discount on a closing breakout. `FailedBreakoutDepthRunUpDiscountComponent` uses the same discount max(0, 1 − R / m), but multiplies it by a failure depth, takes R at the breakout bar j, and is 0 on the breakout bar itself. One new class gives the discount on the bar whose close breaks above the prior 60 closes, with R ending the bar before the break.

table: Directional components
row: | `BreakoutRunUpDiscountComponent` | `period` (60), `rise_period` (20), `rise_lag` (1), `window` (120) | G x max(0, 1 − R / m). G = 1 when close[t] > max(close[t-`period`] .. close[t-1]), else 0. R = close[t-`rise_lag`] / close[t-`rise_lag`-`rise_period`] − 1. m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`rise_period`] − 1), the overlapping `rise_period`-bar returns ending at each of the last `window` bars, bar t included. 0.0 when m = 0 | 0 and up, at most 1 + 1/m (R ≥ −1), never negative; no direction. It is 0 on bars that do not close above the prior `period` closes, and 0 on a break whose prior run-up is one usual `rise_period`-bar move or more. On a break it is 1 at a flat run-up, above 1 after a prior fall, and grows as the run-up shrinks | graded | dimensionless (1 − run-up in usual `rise_period`-bar moves) | max(`period` + 1, `window` + `rise_period`, `rise_lag` + `rise_period` + 1) (140) | closes only (last (warmup) rows). A NaN close among them gives NaN, whatever the gate. A close not above 0 there gives NaN (never on real bars). m = 0 gives 0.0: on a break bar m is above 0 because close[t] > close[t-`rise_period`] when `rise_period` ≤ `period`. These settings raise when the component is built: `period` < 1, `rise_period` < 1, `rise_lag` < 0, `window` < 1 | stateless. A break needs a strictly higher close than every prior close of the window; a tie is not a break. With `rise_lag` 1 the run-up ends at bar t-1, so the breaking bar's own move cannot enlarge it. m includes bar t's `rise_period`-bar return. The value is continuous in the closes while bar t breaks out, and jumps between 0 and its reading where close[t] crosses the prior high. On 1d bars the defaults give a close above the prior 60-day closing high, weighted by 1 minus the 20-day return into yesterday in usual 20-day moves over 120 days. One-sided, an unextended-breakout (long-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class BreakoutRunUpDiscountComponent(SubStrategyComponent):
    """
    Run-up discount on a closing breakout above the prior closes:

        G = 1 when close[t] > max(close[t-period] .. close[t-1]), else 0   (strictly higher; bar t excluded)
        R = close[t-rise_lag] / close[t-rise_lag-rise_period] - 1         (the run-up before the break)
        m = mean over i = t-window+1 .. t of abs(close[i] / close[i-rise_period] - 1)
        raw_value = G x max(0, 1 - R / m)      (0.0 when m = 0)

    Defaults: period 60, rise_period 20, rise_lag 1, window 120.
    Range: 0 and up, at most 1 + 1/m (R >= -1), never negative, no direction. It is 0 without a break, and 0
    when the run-up is one usual rise_period-bar move or more. On a break it is 1 at a flat run-up and above 1
    after a prior fall. Graded and continuous in the closes while bar t breaks out.
    Warm-up: max(period + 1, window + rise_period, rise_lag + rise_period + 1) rows (140), bar t included.
    NaN: a NaN close among those rows gives NaN, whatever the gate. A close not above 0 there gives NaN.
    m = 0 gives 0.0.
    Building raises for period < 1, rise_period < 1, rise_lag < 0 or window < 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last get_required_periods() rows of data,
    the last of which is bar t; every close used is at or before bar t.
    """

    def __init__(self, name="BreakoutRunUpDiscount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 60))
        self.rise_period = int(self.parameters.get("rise_period", 20))
        self.rise_lag = int(self.parameters.get("rise_lag", 1))
        self.window = int(self.parameters.get("window", 120))
        if self.period < 1:
            raise ValueError(f"BreakoutRunUpDiscountComponent: period must be >= 1, got {self.period}")
        if self.rise_period < 1:
            raise ValueError(f"BreakoutRunUpDiscountComponent: rise_period must be >= 1, got {self.rise_period}")
        if self.rise_lag < 0:
            raise ValueError(f"BreakoutRunUpDiscountComponent: rise_lag must be >= 0, got {self.rise_lag}")
        if self.window < 1:
            raise ValueError(f"BreakoutRunUpDiscountComponent: window must be >= 1, got {self.window}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        t = len(c) - 1
        rp = self.rise_period
        prior_high = float(np.max(c[t - self.period:t]))
        brk = bool(c[t] > prior_high)
        cur = c[t - self.window + 1:t + 1]
        base = c[t - self.window + 1 - rp:t + 1 - rp]
        m = float(np.mean(np.abs(cur / base - 1.0)))
        r = float(c[t - self.rise_lag] / c[t - self.rise_lag - rp] - 1.0)
        if not brk or m == 0.0:
            value = 0.0
        else:
            value = max(0.0, 1.0 - r / m)
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"prior_high": prior_high, "breakout": brk, "run_up": r, "mean_abs_return": m}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + 1, self.window + self.rise_period, self.rise_lag + self.rise_period + 1)
```

```python hand
def hand(df, params):
    period = int(params.get("period", 60))
    rp = int(params.get("rise_period", 20))
    lag = int(params.get("rise_lag", 1))
    window = int(params.get("window", 120))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    need = max(period + 1, window + rp, lag + rp + 1)
    used = closes[t - need + 1:]
    for x in used:
        if x != x or not x > 0:
            return float("nan")
    # breakout: close[t] strictly above each of the prior `period` closes
    high = closes[t - 1]
    for k in range(1, period + 1):
        if closes[t - k] > high:
            high = closes[t - k]
    broke = closes[t] > high
    # usual rise_period-bar move: mean abs return ending at each of the last `window` bars
    total = 0.0
    for i in range(t - window + 1, t + 1):
        ret = closes[i] / closes[i - rp] - 1.0
        total += ret if ret >= 0 else -ret
    m = total / window
    run_up = closes[t - lag] / closes[t - lag - rp] - 1.0
    if not broke or m == 0.0:
        return 0.0
    w = 1.0 - run_up / m
    return w if w > 0 else 0.0
```

checks:
BreakoutRunUpDiscountComponent: every check passed
the bot's suite: == 1659 passed, 16 skipped, 75 deselected, 2244 warnings in 93.72s (0:01:33) ===
