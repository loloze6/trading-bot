# SignalPredictivePowerComponent: night3_learned_run | 022-04_signal-weights-carry-forward_1d | TrailingPredictivePower

## attempt 1

answer: built
class: SignalPredictivePowerComponent
settings: {"signal": "momentum", "corr_lookback": 365, "horizon": 5}
reason: `PastPredictivePowerWeightedCompositeComponent` computes this correlation w_k internally, but it never outputs it alone. Even "single" outputs w_k x z_k(t), and no config step divides out z_k(t). A signal's trailing correlation with its later return measures how well the signal has predicted, not a forecast, so one new class computes it, with the composite's signal definitions and training rows.

table: Regime measures
row: | `SignalPredictivePowerComponent` | `signal` ("momentum"), `return_period` (28), `reversal_period` (1), `high_period` (90), `vol_period` (30), `corr_lookback` (365), `horizon` (5) | Pearson corr of s(i) with y(i) = close[i+`horizon`]/close[i]-1 over the training rows i = t-`corr_lookback` .. t-`horizon`. The signal s is one of: "momentum" s(i) = close[i]/close[i-`return_period`]-1; "reversal" s(i) = -(close[i]/close[i-`reversal_period`]-1); "high" s(i) = close[i]/max(close[i-`high_period`+1..i])-1; "volatility" s(i) = -std (ddof 1) of the `vol_period` one-bar returns ending at bar i. The output is 0 when either side is flat over the training rows | -1 to +1, signed; positive when high values of the signal were followed by higher returns, negative when it worked in reverse, near 0 when it did not predict | regime measure | dimensionless (correlation) | `corr_lookback` + D + 1, where D is `return_period`, `reversal_period`, `high_period`-1 or `vol_period` for the chosen signal (394 at the defaults) | closes only. A NaN close, or a close not above 0, in the last `corr_lookback` + D + 1 rows gives NaN. These settings raise when the component is built: `return_period` < 1, `reversal_period` < 1, `high_period` < 2, `vol_period` < 2, `horizon` < 1, `corr_lookback` - `horizon` < 2, `signal` other than "momentum", "reversal", "high" or "volatility" | stateless. It is the w_k of `PastPredictivePowerWeightedCompositeComponent` for one signal. The latest forward return used ends at bar t. No `scaling_factor`: scale it with transforms |

```python class
class SignalPredictivePowerComponent(SubStrategyComponent):
    """
    Trailing predictive power of one signal: how well it has forecast the return that followed it.

        L = corr_lookback, h = horizon
        training rows: i = t-L .. t-h  (L - h + 1 rows)
        y(i) = close[i+h] / close[i] - 1
        signal = "momentum" (default): s(i) = close[i] / close[i-return_period] - 1
        signal = "reversal":           s(i) = -(close[i] / close[i-reversal_period] - 1)
        signal = "high":               s(i) = close[i] / max(close[i-high_period+1 .. i]) - 1
        signal = "volatility":         s(i) = -std (ddof 1) of the vol_period returns close[j]/close[j-1]-1,
                                              j = i-vol_period+1 .. i
        raw_value = Pearson corr of s(i) with y(i) over the training rows; 0 when s or y is flat there

    Range: -1 to +1, signed. It is positive when a high signal was followed by a higher return (the signal worked).
    It is negative when the signal worked in reverse, and near 0 when it did not predict.
    It is graded and continuous in the closes.
    Warm-up: corr_lookback + D + 1 rows, bar t included. D is the chosen signal's lag: return_period,
    reversal_period, high_period - 1 or vol_period (394 at the defaults).

    NaN: a NaN close, or a close not above 0, in those rows gives NaN.
    Building the component raises for return_period < 1, reversal_period < 1, high_period < 2, vol_period < 2,
    horizon < 1, corr_lookback - horizon < 2, or a signal other than "momentum", "reversal", "high" or
    "volatility".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last corr_lookback + D + 1 rows, bar t being the
    last row. The latest forward return y(t-h) = close[t]/close[t-h] - 1 ends at bar t, so no row after t is read.
    """

    def __init__(self, name="SignalPredictivePower", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.return_period = int(p.get("return_period", 28))
        self.reversal_period = int(p.get("reversal_period", 1))
        self.high_period = int(p.get("high_period", 90))
        self.vol_period = int(p.get("vol_period", 30))
        self.corr_lookback = int(p.get("corr_lookback", 365))
        self.horizon = int(p.get("horizon", 5))
        self.signal = p.get("signal", "momentum")
        if self.return_period < 1:
            raise ValueError(f"SignalPredictivePowerComponent: return_period must be >= 1, got {self.return_period}")
        if self.reversal_period < 1:
            raise ValueError(
                f"SignalPredictivePowerComponent: reversal_period must be >= 1, got {self.reversal_period}")
        if self.high_period < 2:
            raise ValueError(f"SignalPredictivePowerComponent: high_period must be >= 2, got {self.high_period}")
        if self.vol_period < 2:
            raise ValueError(f"SignalPredictivePowerComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.horizon < 1:
            raise ValueError(f"SignalPredictivePowerComponent: horizon must be >= 1, got {self.horizon}")
        if self.corr_lookback - self.horizon < 2:
            raise ValueError("SignalPredictivePowerComponent: corr_lookback - horizon must be >= 2")
        if self.signal not in ("momentum", "reversal", "high", "volatility"):
            raise ValueError(f"SignalPredictivePowerComponent: unknown signal {self.signal!r}")
        self._raw_value = 0.0

    def _lag(self):
        if self.signal == "momentum":
            return self.return_period
        if self.signal == "reversal":
            return self.reversal_period
        if self.signal == "high":
            return self.high_period - 1
        return self.vol_period

    def _signal_at(self, c, pos):
        if self.signal == "momentum":
            return c[pos] / c[pos - self.return_period] - 1.0
        if self.signal == "reversal":
            return -(c[pos] / c[pos - self.reversal_period] - 1.0)
        if self.signal == "high":
            return c[pos] / np.max(c[pos - self.high_period + 1:pos + 1]) - 1.0
        r = c[pos - self.vol_period + 1:pos + 1] / c[pos - self.vol_period:pos] - 1.0
        return -float(np.std(r, ddof=1))

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
        d = self._lag()
        h = self.horizon
        xs = []
        ys = []
        for k in range(self.corr_lookback - h + 1):
            pos = d + k
            xs.append(self._signal_at(c, pos))
            ys.append(c[pos + h] / c[pos] - 1.0)
        x = np.array(xs, dtype=float)
        y = np.array(ys, dtype=float)
        if x.max() == x.min() or y.max() == y.min():
            corr = 0.0
        else:
            dx = x - x.mean()
            dy = y - y.mean()
            den = float(np.sqrt(np.sum(dx * dx) * np.sum(dy * dy)))
            corr = 0.0 if not den > 0 else float(np.clip(np.sum(dx * dy) / den, -1.0, 1.0))
        self._raw_value = float(corr)
        self.confidence = 1.0
        self.debug_info = {"signal": self.signal, "rows": len(xs), "signal_now": float(self._signal_at(c, n - 1))}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.corr_lookback + self._lag() + 1
```

```python hand
def hand(df, params):
    import math
    rp = int(params.get("return_period", 28))
    rev = int(params.get("reversal_period", 1))
    hp = int(params.get("high_period", 90))
    vp = int(params.get("vol_period", 30))
    L = int(params.get("corr_lookback", 365))
    h = int(params.get("horizon", 5))
    sig = params.get("signal", "momentum")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    if sig == "momentum":
        lag = rp
    elif sig == "reversal":
        lag = rev
    elif sig == "high":
        lag = hp - 1
    else:
        lag = vp
    first = t - L - lag
    for j in range(first, t + 1):
        if c[j] != c[j] or not c[j] > 0:
            return float("nan")

    def s_at(i):
        if sig == "momentum":
            return c[i] / c[i - rp] - 1.0
        if sig == "reversal":
            return -(c[i] / c[i - rev] - 1.0)
        if sig == "high":
            m = c[i]
            for j in range(i - hp + 1, i + 1):
                if c[j] > m:
                    m = c[j]
            return c[i] / m - 1.0
        rets = []
        for j in range(i - vp + 1, i + 1):
            rets.append(c[j] / c[j - 1] - 1.0)
        mu = sum(rets) / len(rets)
        var = sum((r - mu) ** 2 for r in rets) / (len(rets) - 1)
        return -math.sqrt(var)

    xs = []
    ys = []
    for i in range(t - L, t - h + 1):
        xs.append(s_at(i))
        ys.append(c[i + h] / c[i] - 1.0)
    if max(xs) == min(xs) or max(ys) == min(ys):
        return 0.0
    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)
    sxy = 0.0
    sxx = 0.0
    syy = 0.0
    for a, b in zip(xs, ys):
        sxy += (a - mx) * (b - my)
        sxx += (a - mx) ** 2
        syy += (b - my) ** 2
    den = math.sqrt(sxx * syy)
    if not den > 0:
        return 0.0
    r = sxy / den
    return max(-1.0, min(1.0, r))
```

checks:
SignalPredictivePowerComponent: every check passed
the bot's suite: ======= 1580 passed, 16 skipped, 75 deselected, 2244 warnings in 54.26s ========
