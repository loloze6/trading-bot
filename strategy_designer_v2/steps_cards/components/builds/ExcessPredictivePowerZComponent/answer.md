# ExcessPredictivePowerZComponent: night3_learned_run | 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d | centred-power counter-bet

## attempt 1

answer: built
class: ExcessPredictivePowerZComponent
settings: {"high_period": 90, "corr_lookback": 365, "horizon": 5, "z_window": 365, "mean_window": 365}
reason: The catalogue has the correlation w(t) alone (`SignalPredictivePowerComponent`, `signal` "high") and w(t) x z(t) (`PastPredictivePowerWeightedCompositeComponent`, "single"), but nothing measures w's excess over its own prior-365-bar mean times z. This new class computes (w(t) − mean w) x z(t); the wished counter-bet is its negative, which a `negate` step gives exactly.

table: Directional components
row: | `ExcessPredictivePowerZComponent` | `high_period` (90), `corr_lookback` (365), `horizon` (5), `z_window` (365), `mean_window` (365) | (w(t) − wbar(t)) x z(t). s(i) = close[i] / max(close[i-`high_period`+1 .. i]) − 1. w(u) = Pearson corr of s(i) with y(i) = close[i+`horizon`] / close[i] − 1 over i = u-`corr_lookback` .. u-`horizon` (0 when either side is flat). wbar(t) = mean of w(t-`mean_window`) .. w(t-1). z(t) = (s(t) − mean) / std (ddof 1) of s over bars t-`z_window`+1 .. t (0 when that std is 0) | signed; abs at most 2 x (`z_window`−1)/sqrt(`z_window`) (about 38.1). Positive when the nearness signal's power is above its usual level and the close sits nearer its high than usual, or when power is below usual and the close is further from its high than usual; `negate` gives the counter-bet | graded | z-score x correlation | max(`mean_window` + `corr_lookback`, `z_window` − 1) + `high_period` (820) | closes only. A NaN close, or a close not above 0, in the last 820 rows gives NaN. These settings raise when the component is built: `high_period` < 2, `horizon` < 1, `corr_lookback` − `horizon` < 2, `z_window` < 2, `mean_window` < 1 | stateless; every w is recomputed on every bar. The latest forward return used ends at bar t (inside w(t)). It is continuous in the closes. With wbar replaced by 0 it would be the "single"/"high" term of `PastPredictivePowerWeightedCompositeComponent`. No `scaling_factor`: scale it with transforms |

```python class
class ExcessPredictivePowerZComponent(SubStrategyComponent):
    """
    Excess past predictive power of nearness to the high, times that nearness's z-score:

        s(i)    = close[i] / max(close[i - high_period + 1 .. i]) - 1
        y(i)    = close[i + horizon] / close[i] - 1
        w(u)    = Pearson corr of s(i) with y(i), i = u - corr_lookback .. u - horizon
                  (0 when s or y is flat over those rows)
        wbar(t) = mean of w(t - mean_window) .. w(t - 1)
        z(t)    = (s(t) - mean(S)) / std(S, ddof 1), S = s(t - z_window + 1 .. t)  (0 when std is 0)
        raw_value = (w(t) - wbar(t)) * z(t)

    Range and sign: signed. abs(w - wbar) <= 2 and abs(z) <= (z_window - 1) / sqrt(z_window), so the value is
    at most about 38.1 in size at the defaults. It is positive when the power is above its usual level and s is
    above its mean. `negate` gives the counter-bet -(w - wbar) * z.
    Warm-up: max(mean_window + corr_lookback, z_window - 1) + high_period rows, bar t included (820 at defaults).
    NaN: a NaN close, or a close not above 0, in those rows gives NaN.
    Building raises for high_period < 2, horizon < 1, corr_lookback - horizon < 2, z_window < 2 or
    mean_window < 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last get_required_periods() rows up to and
    including bar t. Each y(i) used by w(u), u <= t, ends at close[i + horizon] with i + horizon <= u <= t.
    """

    def __init__(self, name="ExcessPredictivePowerZ", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.high_period = int(self.parameters.get("high_period", 90))
        self.corr_lookback = int(self.parameters.get("corr_lookback", 365))
        self.horizon = int(self.parameters.get("horizon", 5))
        self.z_window = int(self.parameters.get("z_window", 365))
        self.mean_window = int(self.parameters.get("mean_window", 365))
        if self.high_period < 2:
            raise ValueError(f"ExcessPredictivePowerZComponent: high_period must be >= 2, got {self.high_period}")
        if self.horizon < 1:
            raise ValueError(f"ExcessPredictivePowerZComponent: horizon must be >= 1, got {self.horizon}")
        if self.corr_lookback - self.horizon < 2:
            raise ValueError("ExcessPredictivePowerZComponent: corr_lookback - horizon must be >= 2")
        if self.z_window < 2:
            raise ValueError(f"ExcessPredictivePowerZComponent: z_window must be >= 2, got {self.z_window}")
        if self.mean_window < 1:
            raise ValueError(f"ExcessPredictivePowerZComponent: mean_window must be >= 1, got {self.mean_window}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        self.confidence = 1.0
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            return
        h, L, H, Z, M = self.high_period, self.corr_lookback, self.horizon, self.z_window, self.mean_window
        t = n - 1
        rmax = pd.Series(c).rolling(h).max().to_numpy()
        s = c / rmax - 1.0
        y = np.full(n, np.nan)
        y[:n - H] = c[H:] / c[:n - H] - 1.0

        def corr_at(u):
            xs = s[u - L:u - H + 1]
            ys = y[u - L:u - H + 1]
            dx = xs - xs.mean()
            dy = ys - ys.mean()
            sxx = float(np.dot(dx, dx))
            syy = float(np.dot(dy, dy))
            if not (sxx > 0 and syy > 0):
                return 0.0
            return float(np.dot(dx, dy) / np.sqrt(sxx * syy))

        w_now = corr_at(t)
        w_past = [corr_at(u) for u in range(t - M, t)]
        wbar = float(np.mean(w_past))
        win = s[t - Z + 1:t + 1]
        sd = float(np.std(win, ddof=1))
        z = float((s[t] - win.mean()) / sd) if sd > 0 else 0.0
        self._raw_value = float((w_now - wbar) * z)
        self.debug_info = {'w': w_now, 'w_mean': wbar, 'z': z}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.mean_window + self.corr_lookback, self.z_window - 1) + self.high_period
```

```python hand
def hand(df, params):
    import math
    hp = int(params.get("high_period", 90))
    L = int(params.get("corr_lookback", 365))
    H = int(params.get("horizon", 5))
    Z = int(params.get("z_window", 365))
    M = int(params.get("mean_window", 365))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(M + L, Z - 1) + hp
    for k in range(t - need + 1, t + 1):
        if c[k] != c[k] or not c[k] > 0:
            return float("nan")

    def near(i):
        m = c[i]
        for j in range(i - hp + 1, i + 1):
            if c[j] > m:
                m = c[j]
        return c[i] / m - 1.0

    def fwd(i):
        return c[i + H] / c[i] - 1.0

    def pearson(xs, ys):
        k = len(xs)
        mx = sum(xs) / k
        my = sum(ys) / k
        sxy = 0.0
        sxx = 0.0
        syy = 0.0
        for a, b in zip(xs, ys):
            sxy += (a - mx) * (b - my)
            sxx += (a - mx) ** 2
            syy += (b - my) ** 2
        if sxx <= 0 or syy <= 0:
            return 0.0
        return sxy / math.sqrt(sxx * syy)

    def power(u):
        rows = list(range(u - L, u - H + 1))
        return pearson([near(i) for i in rows], [fwd(i) for i in rows])

    w_t = power(t)
    past = [power(u) for u in range(t - M, t)]
    wbar = sum(past) / len(past)
    vals = [near(i) for i in range(t - Z + 1, t + 1)]
    mu = sum(vals) / Z
    var = 0.0
    for v in vals:
        var += (v - mu) ** 2
    sd = math.sqrt(var / (Z - 1))
    z = (near(t) - mu) / sd if sd > 0 else 0.0
    return (w_t - wbar) * z
```

checks:
ExcessPredictivePowerZComponent: every check passed
the bot's suite: ======= 1581 passed, 16 skipped, 75 deselected, 2244 warnings in 56.96s ========
