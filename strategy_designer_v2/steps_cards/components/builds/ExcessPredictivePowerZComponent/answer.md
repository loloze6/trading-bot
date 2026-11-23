# ExcessPredictivePowerZComponent: retest_learned_run | 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d | ExcessPredictivePowerZ (volatility signal)

## attempt 1

answer: built
class: ExcessPredictivePowerZComponent
settings: {"signal": "volatility", "vol_period": 30, "corr_lookback": 365, "horizon": 5, "z_window": 365, "mean_window": 365}
reason: `ExcessPredictivePowerZComponent` computes (w(t) − wbar(t)) x z(t), but only for the nearness-to-high signal, and no setting changes which signal it uses. The wished volatility signal, s(i) = −std of 30 one-bar returns, is the same measure on another base. So the whole class is written again with a `signal` setting (and the `vol_period` it needs). The default "high" keeps today's output exactly.

table: Directional components
row: | `ExcessPredictivePowerZComponent` | `high_period` (90), `corr_lookback` (365), `horizon` (5), `z_window` (365), `mean_window` (365), `signal` ("high"), `vol_period` (30) | (w(t) − wbar(t)) x z(t). The signal s(i) depends on `signal`: "high" s(i) = close[i] / max(close[i-`high_period`+1 .. i]) − 1; "volatility" s(i) = −std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = i-`vol_period`+1 .. i. w(u) = Pearson corr of s(i) with y(i) = close[i+`horizon`] / close[i] − 1 over i = u-`corr_lookback` .. u-`horizon` (0 when either side is flat). wbar(t) = mean of w(t-`mean_window`) .. w(t-1). z(t) = (s(t) − mean) / std (ddof 1) of s over bars t-`z_window`+1 .. t (0 when s is flat there) | signed; abs at most 2 x (`z_window`−1)/sqrt(`z_window`) (about 38.1). Positive when the signal's power is above its usual level and the signal sits above its mean, or when power is below usual and the signal sits below its mean; `negate` gives the counter-bet | graded | z-score x correlation | max(`mean_window` + `corr_lookback`, `z_window` − 1) + D + 1, D = `high_period` − 1 ("high") or `vol_period` ("volatility"): 820 at the defaults, 761 with "volatility" and `vol_period` 30 | closes only. A NaN close, or a close not above 0, in the last (warmup) rows gives NaN. These settings raise when the component is built: `high_period` < 2, `horizon` < 1, `corr_lookback` − `horizon` < 2, `z_window` < 2, `mean_window` < 1, `vol_period` < 2, `signal` other than "high" or "volatility" | stateless; every w is recomputed on every bar. `signal` "high" (default) is the original output, unchanged; `vol_period` is read only by "volatility". With "volatility", s is the volatility signal of `PastPredictivePowerWeightedCompositeComponent` and `SignalPredictivePowerComponent` (s4), and w(t) is `SignalPredictivePowerComponent` (`signal` "volatility"). The latest forward return used ends at bar t (inside w(t)). It is continuous in the closes. No `scaling_factor`: scale it with transforms |

```python class
class ExcessPredictivePowerZComponent(SubStrategyComponent):
    """
    The excess past predictive power of one signal, times that signal's current z-score:

        signal = "high" (default): s(i) = close[i] / max(close[i-high_period+1 .. i]) - 1
        signal = "volatility":     s(i) = -std (ddof 1) of r[j] = close[j] / close[j-1] - 1, j = i-vol_period+1 .. i
        y(i) = close[i+horizon] / close[i] - 1
        w(u) = Pearson corr of s(i) with y(i) over i = u-corr_lookback .. u-horizon (0 when either side is flat)
        wbar(t) = mean of w(t-mean_window) .. w(t-1)
        z(t) = (s(t) - mean) / std (ddof 1) of s over bars t-z_window+1 .. t (0 when s is flat there)
        raw_value = (w(t) - wbar(t)) x z(t)

    Signed. Its absolute value is at most 2 x (z_window-1)/sqrt(z_window), about 38.1. It is positive when the
    signal's power is above its usual level and the signal sits above its mean, or when the power is below usual
    and the signal sits below its mean. Graded, continuous in the closes. signal "high" is the original output,
    unchanged. vol_period is read only by "volatility".
    Warm-up: max(mean_window + corr_lookback, z_window - 1) + D + 1 rows, bar t included, with D = high_period - 1
    ("high") or vol_period ("volatility"). That is 820 at the defaults and 761 for "volatility" with vol_period 30.

    NaN: a NaN close, or a close not above 0, in the last (warm-up) rows gives NaN.
    Building raises for high_period < 2, horizon < 1, corr_lookback - horizon < 2, z_window < 2, mean_window < 1,
    vol_period < 2, or a signal other than "high" or "volatility".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last (warm-up) rows of data, ending at bar t (the
    last row). The forward return y(i) is used only for i <= u - horizon <= t - horizon, so the latest close it
    reads is close[t].
    """

    def __init__(self, name="ExcessPredictivePowerZ", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.high_period = int(p.get("high_period", 90))
        self.corr_lookback = int(p.get("corr_lookback", 365))
        self.horizon = int(p.get("horizon", 5))
        self.z_window = int(p.get("z_window", 365))
        self.mean_window = int(p.get("mean_window", 365))
        self.signal = p.get("signal", "high")
        self.vol_period = int(p.get("vol_period", 30))
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
        if self.vol_period < 2:
            raise ValueError(f"ExcessPredictivePowerZComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.signal not in ("high", "volatility"):
            raise ValueError(
                f"ExcessPredictivePowerZComponent: signal must be 'high' or 'volatility', got {self.signal!r}")
        self._raw_value = 0.0

    def _lead(self):
        return self.high_period - 1 if self.signal == "high" else self.vol_period

    @staticmethod
    def _corr(x, y):
        if x.max() == x.min() or y.max() == y.min():
            return 0.0
        xm = x - x.mean()
        ym = y - y.mean()
        den = np.sqrt(np.sum(xm * xm) * np.sum(ym * ym))
        if not den > 0:
            return 0.0
        return float(np.sum(xm * ym) / den)

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n_rows = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n_rows:]
        if np.isnan(c).any() or (c <= 0).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        t = n_rows - 1
        D = self._lead()
        L, h, zw, mw = self.corr_lookback, self.horizon, self.z_window, self.mean_window

        s = np.full(n_rows, np.nan)
        if self.signal == "high":
            win = np.lib.stride_tricks.sliding_window_view(c, self.high_period)
            s[D:] = c[D:] / win.max(axis=1) - 1.0
        else:
            r = c[1:] / c[:-1] - 1.0
            win = np.lib.stride_tricks.sliding_window_view(r, self.vol_period)
            s[D:] = -win.std(axis=1, ddof=1)

        y = np.full(n_rows, np.nan)
        y[: n_rows - h] = c[h:] / c[: n_rows - h] - 1.0

        def w_at(u):
            lo, hi = u - L, u - h + 1
            return self._corr(s[lo:hi], y[lo:hi])

        w_t = w_at(t)
        wbar = float(np.mean([w_at(u) for u in range(t - mw, t)]))

        zs = s[t - zw + 1: t + 1]
        if zs.max() == zs.min():
            z = 0.0
        else:
            sd = float(np.std(zs, ddof=1))
            z = float((s[t] - zs.mean()) / sd) if sd > 0 else 0.0

        self._raw_value = float((w_t - wbar) * z)
        self.confidence = 1.0
        self.debug_info = {"w": w_t, "wbar": wbar, "z": z, "signal": self.signal}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.mean_window + self.corr_lookback, self.z_window - 1) + self._lead() + 1
```

```python hand
def hand(df, params):
    import math
    hp = int(params.get("high_period", 90))
    L = int(params.get("corr_lookback", 365))
    h = int(params.get("horizon", 5))
    zw = int(params.get("z_window", 365))
    mw = int(params.get("mean_window", 365))
    sig = params.get("signal", "high")
    vp = int(params.get("vol_period", 30))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    D = hp - 1 if sig == "high" else vp
    need = max(mw + L, zw - 1) + D + 1
    for x in c[t - need + 1:]:
        if x != x or not x > 0:
            return float("nan")

    memo = {}

    def s(i):
        if i in memo:
            return memo[i]
        if sig == "high":
            m = c[i]
            for k in range(i - hp + 1, i + 1):
                if c[k] > m:
                    m = c[k]
            v = c[i] / m - 1.0
        else:
            rets = []
            for j in range(i - vp + 1, i + 1):
                rets.append(c[j] / c[j - 1] - 1.0)
            mu = sum(rets) / len(rets)
            var = 0.0
            for r in rets:
                var += (r - mu) ** 2
            var = var / (len(rets) - 1)
            v = -math.sqrt(var)
        memo[i] = v
        return v

    def corr(xs, ys):
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
        if not sxx * syy > 0:
            return 0.0
        return sxy / math.sqrt(sxx * syy)

    def w(u):
        xs = []
        ys = []
        for i in range(u - L, u - h + 1):
            xs.append(s(i))
            ys.append(c[i + h] / c[i] - 1.0)
        return corr(xs, ys)

    total = 0.0
    for u in range(t - mw, t):
        total += w(u)
    wbar = total / mw

    vals = [s(i) for i in range(t - zw + 1, t + 1)]
    if max(vals) == min(vals):
        z = 0.0
    else:
        mu = sum(vals) / len(vals)
        var = 0.0
        for v in vals:
            var += (v - mu) ** 2
        sd = math.sqrt(var / (len(vals) - 1))
        z = (s(t) - mu) / sd if sd > 0 else 0.0

    return (w(t) - wbar) * z
```

checks:
ExcessPredictivePowerZComponent: every check passed
the bot's suite: == 1634 passed, 16 skipped, 75 deselected, 2244 warnings in 84.16s (0:01:24) ===
