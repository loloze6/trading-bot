# ExcessPowerReversalTimesMaDistanceComponent: retest_learned_run | 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d1_nearness-reversal-in-uptrends_1d | TrendScaledExcessPowerReversal

## attempt 1

answer: built
class: ExcessPowerReversalTimesMaDistanceComponent
settings: {"high_period": 90, "corr_lookback": 365, "horizon": 5, "z_window": 365, "mean_window": 365, "ma_period": 100}
reason: `ExcessPredictivePowerZComponent` (`signal` "high") gives (w − wbar) × z, and `MovingAverageDistanceComponent` (`average` "sma", `period` 100) gives the percent distance from the 100-bar SMA. The wish is the product of the first one negated and clipped at 0 with the second clipped at 0, and no config step multiplies two components, so one new class computes it.

table: Directional components
row: | `ExcessPowerReversalTimesMaDistanceComponent` | `high_period` (90), `corr_lookback` (365), `horizon` (5), `z_window` (365), `mean_window` (365), `ma_period` (100) | max(0, −(w(t) − wbar(t)) x z(t)) x max(0, (close[t] − SMA) / SMA x 100). s(i) = close[i] / max(close[i-`high_period`+1 .. i]) − 1. w(u) = Pearson corr of s(i) with y(i) = close[i+`horizon`] / close[i] − 1 over i = u-`corr_lookback` .. u-`horizon`, 0 when either side is flat. wbar(t) = mean of w(t-`mean_window`) .. w(t-1). z(t) = (s(t) − mean) / std (ddof 1) of s over bars t-`z_window`+1 .. t, 0 when s is flat there. SMA = mean of the last `ma_period` closes, bar t included | 0 and up, unbounded above, never negative; no direction. The first factor is at most about 38.1 at the defaults. The value is 0 unless (w − wbar) x z < 0 (the excess-power reading points to a fall) and the close is above its SMA. Otherwise it grows with both factors | graded | z-score x correlation x percent | max(`mean_window` + `corr_lookback`, `z_window` − 1) + `high_period`, at least `ma_period` (820) | closes only. A NaN close, or a close not above 0, in the last (warmup) rows gives NaN (never on real bars for the second case). These settings raise when the component is built: `high_period` < 2, `horizon` < 1, `corr_lookback` − `horizon` < 2, `z_window` < 2, `mean_window` < 1, `ma_period` < 2 | stateless; every w is recomputed on every bar. Equals max(0, −`ExcessPredictivePowerZComponent` (`signal` "high", same settings)) x max(0, `MovingAverageDistanceComponent` (`period` = `ma_period`, `average` "sma")). The latest forward return used ends at bar t (inside w(t)). Continuous in the closes and exactly 0 on many bars. One-sided, a reversal-in-uptrend (short-side) reading; `negate` gives the short forecast. No `scaling_factor`: scale it with transforms |

```python class
class ExcessPowerReversalTimesMaDistanceComponent(SubStrategyComponent):
    """
    Excess predictive power of the nearness to the high, read as a reversal, times the trend distance:

        s(i)    = close[i] / max(close[i-high_period+1 .. i]) - 1
        y(i)    = close[i+horizon] / close[i] - 1
        w(u)    = Pearson corr of s(i) with y(i) over i = u-corr_lookback .. u-horizon
                  (0 when s or y is flat over those rows)
        wbar(t) = mean of w(t-mean_window) .. w(t-1)
        z(t)    = (s(t) - mean) / std (ddof 1) of s over bars t-z_window+1 .. t   (0 when s is flat there)
        SMA     = mean(close[t-ma_period+1 .. t])
        raw_value = max(0, -(w(t) - wbar(t)) * z(t)) * max(0, (close[t] - SMA) / SMA * 100)

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 unless (w - wbar) * z < 0 and
    close[t] > SMA. Graded: it grows continuously with both factors.
    Warm-up: max(mean_window + corr_lookback, z_window - 1) + high_period rows, at least ma_period (820 at the
    defaults), bar t included.
    NaN: a NaN close, or a close not above 0, in the last (warm-up) rows gives NaN.
    Building raises for high_period < 2, horizon < 1, corr_lookback - horizon < 2, z_window < 2,
    mean_window < 1, ma_period < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last (warm-up) rows up to and including bar t.
    The latest forward return used is y(t-horizon) = close[t] / close[t-horizon] - 1, which ends at bar t.
    """

    def __init__(self, name="ExcessPowerReversalTrend", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        p = self.parameters
        self.high_period = int(p.get("high_period", 90))
        self.corr_lookback = int(p.get("corr_lookback", 365))
        self.horizon = int(p.get("horizon", 5))
        self.z_window = int(p.get("z_window", 365))
        self.mean_window = int(p.get("mean_window", 365))
        self.ma_period = int(p.get("ma_period", 100))
        if self.high_period < 2:
            raise ValueError(f"high_period must be >= 2, got {self.high_period}")
        if self.horizon < 1:
            raise ValueError(f"horizon must be >= 1, got {self.horizon}")
        if self.corr_lookback - self.horizon < 2:
            raise ValueError("corr_lookback - horizon must be >= 2")
        if self.z_window < 2:
            raise ValueError(f"z_window must be >= 2, got {self.z_window}")
        if self.mean_window < 1:
            raise ValueError(f"mean_window must be >= 1, got {self.mean_window}")
        if self.ma_period < 2:
            raise ValueError(f"ma_period must be >= 2, got {self.ma_period}")
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
        T = len(c) - 1
        hp, L, h = self.high_period, self.corr_lookback, self.horizon
        hi = pd.Series(c).rolling(hp, min_periods=hp).max().to_numpy()
        s = c / hi - 1.0
        y = np.full(T + 1, np.nan)
        y[:T + 1 - h] = c[h:] / c[:T + 1 - h] - 1.0

        def corr(u):
            a = s[u - L:u - h + 1]
            b = y[u - L:u - h + 1]
            if a.max() == a.min() or b.max() == b.min():
                return 0.0
            da = a - a.mean()
            db = b - b.mean()
            den = np.sqrt(np.sum(da * da) * np.sum(db * db))
            if not den > 0:
                return 0.0
            return float(np.sum(da * db) / den)

        w_t = corr(T)
        wbar = float(np.mean([corr(T - k) for k in range(1, self.mean_window + 1)]))
        zw = s[T - self.z_window + 1:T + 1]
        if zw.max() == zw.min():
            z = 0.0
        else:
            sd = float(np.std(zw, ddof=1))
            z = float((s[T] - zw.mean()) / sd) if sd > 0 else 0.0
        sma = float(np.mean(c[T - self.ma_period + 1:T + 1]))
        dist = (c[T] - sma) / sma * 100.0
        rev = max(0.0, -(w_t - wbar) * z)
        trend = max(0.0, dist)
        self._raw_value = float(rev * trend)
        self.confidence = 1.0
        self.debug_info = {"w": w_t, "wbar": wbar, "z": z, "ma_distance": dist}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(max(self.mean_window + self.corr_lookback, self.z_window - 1) + self.high_period,
                   self.ma_period)
```

```python hand
def hand(df, params):
    import math
    hp = int(params.get("high_period", 90))
    L = int(params.get("corr_lookback", 365))
    h = int(params.get("horizon", 5))
    zw = int(params.get("z_window", 365))
    mw = int(params.get("mean_window", 365))
    ma = int(params.get("ma_period", 100))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(max(mw + L, zw - 1) + hp, ma)
    for k in range(need):
        x = c[t - k]
        if x != x or not x > 0:
            return float("nan")

    def s(i):
        m = c[i]
        for j in range(i - hp + 1, i + 1):
            if c[j] > m:
                m = c[j]
        return c[i] / m - 1.0

    def y(i):
        return c[i + h] / c[i] - 1.0

    def mean(xs):
        tot = 0.0
        for x in xs:
            tot += x
        return tot / len(xs)

    def flat(xs):
        return max(xs) == min(xs)

    def w(u):
        a = [s(i) for i in range(u - L, u - h + 1)]
        b = [y(i) for i in range(u - L, u - h + 1)]
        if flat(a) or flat(b):
            return 0.0
        ma_, mb_ = mean(a), mean(b)
        sab = saa = sbb = 0.0
        for k in range(len(a)):
            da = a[k] - ma_
            db = b[k] - mb_
            sab += da * db
            saa += da * da
            sbb += db * db
        if not saa * sbb > 0:
            return 0.0
        return sab / math.sqrt(saa * sbb)

    wt = w(t)
    wbar = mean([w(t - k) for k in range(1, mw + 1)])
    sw = [s(i) for i in range(t - zw + 1, t + 1)]
    if flat(sw):
        z = 0.0
    else:
        m = mean(sw)
        var = 0.0
        for x in sw:
            var += (x - m) * (x - m)
        sd = math.sqrt(var / (len(sw) - 1))
        z = (s(t) - m) / sd if sd > 0 else 0.0
    sma = mean([c[i] for i in range(t - ma + 1, t + 1)])
    dist = (c[t] - sma) / sma * 100.0
    return max(0.0, -(wt - wbar) * z) * max(0.0, dist)
```

checks:
ExcessPowerReversalTimesMaDistanceComponent: every check passed
the bot's suite: == 1635 passed, 16 skipped, 75 deselected, 2244 warnings in 90.67s (0:01:30) ===
