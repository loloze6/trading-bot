# PastPredictivePowerWeightedCompositeComponent: night3_learned_run | 022-03_combined-extremes-larger-moves_1d | PerformanceWeightedSignal

## attempt 1

answer: built
class: PastPredictivePowerWeightedCompositeComponent
settings: {"weighting": "single", "signal": "momentum"}
reason: The composite already computes each effect's z-score z_k(t) and its trailing correlation w_k with the realised 5-bar forward return, using only returns that end by bar t. None of its weightings outputs one chosen effect times its own correlation, w_k x z_k(t). "correlation" divides by the summed |w| and mixes all four effects, and "best" keeps only the sign of w. So the class is written again with a new `weighting` value "single" and a `signal` setting that picks the effect. The default "correlation" is unchanged.

table: Directional components
row: | `PastPredictivePowerWeightedCompositeComponent` | `return_period` (28), `reversal_period` (1), `high_period` (90), `vol_period` (30), `z_window` (365), `corr_lookback` (365), `horizon` (5), `weighting` ("correlation"), `signal` ("momentum") | Four signals s_k(i): s1 = close[i]/close[i-28]-1; s2 = -(close[i]/close[i-1]-1); s3 = close[i]/max(close[i-89..i])-1; s4 = -std (ddof 1) of the 30 one-bar returns ending at bar i. Training rows are i = t-365..t-5, with y(i) = close[i+5]/close[i]-1. z_k(t) = (s_k(t) - mean) / std (ddof 1) of s_k over bars t-364..t (0 when s_k is flat there). w_k = Pearson corr of s_k(i) with y(i) over the training rows (0 when either side is flat). "correlation": sum_k w_k x z_k(t) / sum_k abs(w_k), 0 when sum abs(w_k) = 0. "best": sign(w_k*) x z_k*(t), k* = the largest abs(w_k) (first in s1..s4 on a tie), 0 when every w_k is 0. "single": w_k x z_k(t) for the effect named by `signal` ("momentum" s1, "reversal" s2, "high" s3, "volatility" s4). "regression": 100 x sum_k b_k x x_k(t), x_k(i) = (s_k(i) - m_k) / sd_k with m_k, sd_k (ddof 1) over the training rows, a signal with sd_k = 0 dropped; b_k = least-squares slopes of y on the x_k with an intercept; 0 if every signal is dropped | "correlation" and "best": signed, abs at most max_k abs(z_k(t)) (about 19.05). "single": signed, abs at most abs(z_k(t)) (about 19.05) since abs(w_k) <= 1; positive when the effect is above its mean and has recently worked, or below its mean and has recently worked in reverse; grows with the effect's strength and with abs(w_k). "regression": unbounded, signed | graded | "correlation", "best": z-score; "single": z-score x correlation; "regression": percent (fitted 5-bar return in excess of its window mean) | max(`z_window`-1, `corr_lookback`) + max(`return_period`, `reversal_period`, `high_period`-1, `vol_period`) + 1 (455) | closes only. A NaN close or a close not above 0 in the last 455 rows gives NaN. These settings raise: `return_period` < 1, `reversal_period` < 1, `high_period` < 2, `vol_period` < 2, `z_window` < 2, `horizon` < 1, `corr_lookback` - `horizon` < 2, `weighting` other than "correlation", "best", "single" or "regression", `signal` other than "momentum", "reversal", "high" or "volatility", and with "regression" `corr_lookback` - `horizon` < 5 | stateless: weights and slopes are relearned on every bar. `weighting` "correlation" (default) is the original output, unchanged. `signal` is read only by "single". "single" is one effect's own term of the "correlation" numerator, not normalised: it is continuous in the closes and flips sign with w_k when the effect has recently worked in reverse. "regression" does not read `z_window`. The forward returns used end at bar t at the latest. No `scaling_factor`: scale it with transforms |

```python class
class PastPredictivePowerWeightedCompositeComponent(SubStrategyComponent):
    """
    Four price effects, weighted by how well each predicted the realised forward return over a past window.

    Signals on bar i (closes only):
        s1(i) = close[i] / close[i - return_period] - 1                         (momentum)
        s2(i) = -(close[i] / close[i - reversal_period] - 1)                    (reversal)
        s3(i) = close[i] / max(close[i - high_period + 1 .. i]) - 1             (distance from high)
        s4(i) = -std_ddof1(r[i - vol_period + 1 .. i]), r[j] = close[j]/close[j-1] - 1   (volatility level)
    z_k(t) = (s_k(t) - mean(s_k[t-z_window+1 .. t])) / std_ddof1(same window), 0 when that std is 0.
    Training rows: i = t - corr_lookback .. t - horizon, y(i) = close[i + horizon] / close[i] - 1.
    w_k = Pearson corr(s_k(i), y(i)) over the training rows, 0 when either side is flat.
    weighting "correlation" (default): sum_k w_k z_k(t) / sum_k |w_k|, 0 when sum |w_k| = 0.
    weighting "best":   sign(w_k*) z_k*(t), k* = argmax |w_k| (first of s1..s4 on a tie); 0 when all w_k = 0.
    weighting "single": w_k z_k(t), k the effect named by `signal`
                        ("momentum" s1, "reversal" s2, "high" s3, "volatility" s4).
    weighting "regression": 100 sum_k b_k x_k(t), x_k = (s_k - m_k) / sd_k with m_k, sd_k (ddof 1) over the
                        training rows (signals with sd_k = 0 dropped), b_k the OLS slopes of y on the x_k with an
                        intercept; 0 when every signal is dropped.

    Range & sign: "correlation", "best" and "single" are signed, with abs at most max |z_k(t)| (about 19.05 at
    z_window 365). "single" grows with the effect's strength and with |w_k|, and its sign flips when the effect
    recently worked in reverse. "regression" is unbounded and signed.
    Warm-up: max(z_window - 1, corr_lookback) + max(return_period, reversal_period, high_period - 1, vol_period)
    + 1 rows (455), bar t included.
    NaN: a NaN close, or a close not above 0, in the last warm-up rows gives NaN.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last warm-up rows of data, ending at bar t.
    The latest forward return used is y(t - horizon) = close[t] / close[t - horizon] - 1, which is fully realised
    at bar t's close.
    """

    _SIGNALS = ("momentum", "reversal", "high", "volatility")

    def __init__(self, name="PastPredictivePowerComposite", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.return_period = int(p.get("return_period", 28))
        self.reversal_period = int(p.get("reversal_period", 1))
        self.high_period = int(p.get("high_period", 90))
        self.vol_period = int(p.get("vol_period", 30))
        self.z_window = int(p.get("z_window", 365))
        self.corr_lookback = int(p.get("corr_lookback", 365))
        self.horizon = int(p.get("horizon", 5))
        self.weighting = p.get("weighting", "correlation")
        self.signal = p.get("signal", "momentum")
        if self.return_period < 1:
            raise ValueError(f"return_period must be >= 1, got {self.return_period}")
        if self.reversal_period < 1:
            raise ValueError(f"reversal_period must be >= 1, got {self.reversal_period}")
        if self.high_period < 2:
            raise ValueError(f"high_period must be >= 2, got {self.high_period}")
        if self.vol_period < 2:
            raise ValueError(f"vol_period must be >= 2, got {self.vol_period}")
        if self.z_window < 2:
            raise ValueError(f"z_window must be >= 2, got {self.z_window}")
        if self.horizon < 1:
            raise ValueError(f"horizon must be >= 1, got {self.horizon}")
        if self.corr_lookback - self.horizon < 2:
            raise ValueError("corr_lookback - horizon must be >= 2")
        if self.weighting not in ("correlation", "best", "single", "regression"):
            raise ValueError(f"unknown weighting {self.weighting!r}")
        if self.signal not in self._SIGNALS:
            raise ValueError(f"unknown signal {self.signal!r}")
        if self.weighting == "regression" and self.corr_lookback - self.horizon < 5:
            raise ValueError("regression needs corr_lookback - horizon >= 5")
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
        t = n - 1
        first = t - max(self.z_window - 1, self.corr_lookback)
        S = np.full((4, n), np.nan)
        for i in range(first, n):
            S[0, i] = c[i] / c[i - self.return_period] - 1.0
            S[1, i] = -(c[i] / c[i - self.reversal_period] - 1.0)
            S[2, i] = c[i] / np.max(c[i - self.high_period + 1:i + 1]) - 1.0
            r = c[i - self.vol_period + 1:i + 1] / c[i - self.vol_period:i] - 1.0
            S[3, i] = -float(np.std(r, ddof=1))

        z = np.zeros(4)
        for k in range(4):
            win = S[k, t - self.z_window + 1:t + 1]
            sd = float(np.std(win, ddof=1))
            z[k] = (S[k, t] - float(win.mean())) / sd if sd > 0 else 0.0

        tr = np.arange(t - self.corr_lookback, t - self.horizon + 1)
        y = c[tr + self.horizon] / c[tr] - 1.0
        X = S[:, tr]

        w = np.zeros(4)
        dy = y - y.mean()
        syy = float(np.sum(dy * dy))
        for k in range(4):
            dx = X[k] - X[k].mean()
            sxx = float(np.sum(dx * dx))
            if sxx > 0 and syy > 0:
                w[k] = float(np.sum(dx * dy)) / np.sqrt(sxx * syy)

        if self.weighting == "correlation":
            den = float(np.sum(np.abs(w)))
            out = float(np.sum(w * z)) / den if den > 0 else 0.0
        elif self.weighting == "best":
            a = np.abs(w)
            if not (a > 0).any():
                out = 0.0
            else:
                k = int(np.argmax(a))
                out = float(np.sign(w[k]) * z[k])
        elif self.weighting == "single":
            k = self._SIGNALS.index(self.signal)
            out = float(w[k] * z[k])
        else:
            cols, xt = [], []
            for k in range(4):
                m = float(X[k].mean())
                sd = float(np.std(X[k], ddof=1))
                if sd > 0:
                    cols.append((X[k] - m) / sd)
                    xt.append((S[k, t] - m) / sd)
            if not cols:
                out = 0.0
            else:
                A = np.column_stack([np.ones(len(y))] + cols)
                coef = np.linalg.lstsq(A, y, rcond=None)[0]
                out = 100.0 * float(np.dot(coef[1:], np.array(xt)))

        self._raw_value = float(out)
        self.debug_info = {'weights': w.tolist(), 'z': z.tolist(), 'weighting': self.weighting,
                           'signal': self.signal}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return (max(self.z_window - 1, self.corr_lookback)
                + max(self.return_period, self.reversal_period, self.high_period - 1, self.vol_period) + 1)
```

```python hand
def hand(df, params):
    import math
    p1 = int(params.get("return_period", 28))
    p2 = int(params.get("reversal_period", 1))
    p3 = int(params.get("high_period", 90))
    p4 = int(params.get("vol_period", 30))
    Z = int(params.get("z_window", 365))
    C = int(params.get("corr_lookback", 365))
    h = int(params.get("horizon", 5))
    wt = params.get("weighting", "correlation")
    sig = params.get("signal", "momentum")
    names = ["momentum", "reversal", "high", "volatility"]

    allc = [float(x) for x in list(df["close"])]
    lag = max(p1, p2, p3 - 1, p4)
    need = max(Z - 1, C) + lag + 1
    c = allc[len(allc) - need:]
    for x in c:
        if x != x or not x > 0:
            return float("nan")
    t = len(c) - 1

    def mean(xs):
        s = 0.0
        for x in xs:
            s += x
        return s / len(xs)

    def sd1(xs):
        m = mean(xs)
        s = 0.0
        for x in xs:
            s += (x - m) * (x - m)
        return math.sqrt(s / (len(xs) - 1))

    def value(k, i):
        if k == 0:
            return c[i] / c[i - p1] - 1.0
        if k == 1:
            return -(c[i] / c[i - p2] - 1.0)
        if k == 2:
            hi = c[i]
            for j in range(i - p3 + 1, i + 1):
                if c[j] > hi:
                    hi = c[j]
            return c[i] / hi - 1.0
        rets = []
        for j in range(i - p4 + 1, i + 1):
            rets.append(c[j] / c[j - 1] - 1.0)
        return -sd1(rets)

    z = []
    for k in range(4):
        win = [value(k, i) for i in range(t - Z + 1, t + 1)]
        s = sd1(win)
        z.append((value(k, t) - mean(win)) / s if s > 0 else 0.0)

    rows = list(range(t - C, t - h + 1))
    y = [c[i + h] / c[i] - 1.0 for i in rows]
    xs = [[value(k, i) for i in rows] for k in range(4)]

    my = mean(y)
    syy = 0.0
    for v in y:
        syy += (v - my) * (v - my)
    w = []
    for k in range(4):
        mx = mean(xs[k])
        sxx = 0.0
        sxy = 0.0
        for a, b in zip(xs[k], y):
            sxx += (a - mx) * (a - mx)
            sxy += (a - mx) * (b - my)
        w.append(sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else 0.0)

    if wt == "correlation":
        den = sum(abs(v) for v in w)
        if den <= 0:
            return 0.0
        return sum(w[k] * z[k] for k in range(4)) / den
    if wt == "best":
        best = -1
        for k in range(4):
            if abs(w[k]) > 0 and (best < 0 or abs(w[k]) > abs(w[best])):
                best = k
        if best < 0:
            return 0.0
        sgn = 1.0 if w[best] > 0 else -1.0
        return sgn * z[best]
    if wt == "single":
        k = names.index(sig)
        return w[k] * z[k]

    # regression: normal equations with an intercept, solved by Gaussian elimination
    cols = []
    xt = []
    for k in range(4):
        m = mean(xs[k])
        s = sd1(xs[k])
        if s > 0:
            cols.append([(a - m) / s for a in xs[k]])
            xt.append((value(k, t) - m) / s)
    if not cols:
        return 0.0
    feats = [[1.0] * len(y)] + cols
    p = len(feats)
    M = [[0.0] * (p + 1) for _ in range(p)]
    for r in range(p):
        for q in range(p):
            M[r][q] = sum(feats[r][i] * feats[q][i] for i in range(len(y)))
        M[r][p] = sum(feats[r][i] * y[i] for i in range(len(y)))
    for col in range(p):
        piv = col
        for r in range(col + 1, p):
            if abs(M[r][col]) > abs(M[piv][col]):
                piv = r
        M[col], M[piv] = M[piv], M[col]
        for r in range(p):
            if r != col:
                f = M[r][col] / M[col][col]
                for q in range(col, p + 1):
                    M[r][q] -= f * M[col][q]
    coef = [M[r][p] / M[r][r] for r in range(p)]
    return 100.0 * sum(coef[j + 1] * xt[j] for j in range(len(xt)))
```

checks:
PastPredictivePowerWeightedCompositeComponent: every check passed
the bot's suite: ======= 1579 passed, 16 skipped, 75 deselected, 2244 warnings in 52.10s ========
