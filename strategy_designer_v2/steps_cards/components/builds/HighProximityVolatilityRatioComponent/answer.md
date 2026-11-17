# HighProximityVolatilityRatioComponent: night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d3_nearness-strongest-when-calm_1d | CalmScaledDistanceFromHigh

## attempt 1

answer: built
class: HighProximityVolatilityRatioComponent
settings: {"period": 365, "vol_period": 20, "vol_lookback": 365}
reason: No component multiplies the closeness to the 365-bar closing high by how calm daily moves are against their past year. `ConvexHighProximityComponent` and `HighProximityMomentumComponent` weight by the high, and `VolatilityFromStdDevComponent` and `VolatilityPercentileRegimeComponent` read volatility, but none forms this product, so one new class computes it from closes alone.

table: Directional components
row: | `HighProximityVolatilityRatioComponent` | `period` (365), `vol_period` (20), `vol_lookback` (365) | (100 x close[t] / H[t]) x (mean(s[t-`vol_lookback`+1 .. t]) / s[t]); H[t] = highest of the last `period` closes, bar t included; s[i] = std (ddof 1) of the `vol_period` one-bar returns close[j]/close[j-1] - 1 ending at bar i | above 0, unbounded above; never negative; no direction; 100 at a new high with volatility at its yearly average, larger when calmer, smaller below the high or when more volatile | graded | percent of the high x volatility ratio | max(`period`, `vol_lookback` + `vol_period`) (385) | closes only. A NaN close in the last 385 rows gives NaN; a highest close not above 0 or a current std of 0 gives NaN (20 identical returns, which real bars never show). These settings raise when the component is built: `period` < 2, `vol_period` < 2, `vol_lookback` < 1 | stateless; 100 + (close - H) / H x 100 equals 100 x close / H; the mean of the stds includes s[t]. No `scaling_factor`: scale it with transforms |

```python class
class HighProximityVolatilityRatioComponent(SubStrategyComponent):
    """
    Closeness to the recent closing high, times how calm the recent daily moves are against their own past:

        H[t]  = max(close[t - period + 1 .. t])                        (bar t included)
        P[t]  = 100 + (close[t] - H[t]) / H[t] x 100 = 100 x close[t] / H[t]
        r[j]  = close[j] / close[j - 1] - 1
        s[i]  = std (ddof 1) of r[i - vol_period + 1 .. i]
        V[t]  = mean(s[t - vol_lookback + 1 .. t]) / s[t]
        raw_value = P[t] x V[t]

    Graded, above 0, unbounded above, no direction. It is 100 at a new high with volatility at its average, and
    it grows as the close nears its high and as the current std falls below its mean.
    Warm-up: max(period, vol_lookback + vol_period) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, vol_lookback + vol_period)
    rows of data, the last of which is bar t; every close used is known at or before bar t's close.

    NaN: a NaN close anywhere in those rows gives NaN, and so does a highest close not above 0 or a current std
    of 0. Building the component raises for a period below 2, a vol_period below 2, or a vol_lookback below 1.
    """

    def __init__(self, name="HighProxVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"HighProximityVolatilityRatioComponent: period must be >= 2, got {self.period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"HighProximityVolatilityRatioComponent: vol_period must be >= 2, got {self.vol_period}")
        self.vol_lookback = int(self.parameters.get("vol_lookback", 365))
        if self.vol_lookback < 1:
            raise ValueError(
                f"HighProximityVolatilityRatioComponent: vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).iloc[-n:].to_numpy()
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        h = float(np.max(c[-self.period:]))
        if not h > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        prox = 100.0 * float(c[-1]) / h
        need = self.vol_lookback + self.vol_period
        cc = c[-need:]
        r = cc[1:] / cc[:-1] - 1.0
        s = pd.Series(r).rolling(self.vol_period).std(ddof=1).to_numpy()[-self.vol_lookback:]
        s_now = float(s[-1])
        if np.isnan(s).any() or not s_now > 0:
            self._raw_value = float("nan")
        else:
            ratio = float(np.mean(s)) / s_now
            self._raw_value = float(prox * ratio)
        self.confidence = 1.0
        self.debug_info = {'high': h, 'proximity': prox, 'std_now': s_now}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.vol_lookback + self.vol_period)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 365))
    vp = int(params.get("vol_period", 20))
    vl = int(params.get("vol_lookback", 365))
    c = [float(x) for x in list(df["close"])]
    n = max(p, vl + vp)
    used = c[len(c) - n:]
    for x in used:
        if x != x:
            return float("nan")
    h = c[len(c) - p]
    for x in c[len(c) - p:]:
        if x > h:
            h = x
    if not h > 0:
        return float("nan")
    close_t = c[len(c) - 1]
    prox = 100.0 + (close_t - h) / h * 100.0
    stds = []
    for k in range(vl):
        end = len(c) - 1 - k
        rets = []
        for j in range(end - vp + 1, end + 1):
            rets.append(c[j] / c[j - 1] - 1.0)
        m = 0.0
        for x in rets:
            m = m + x
        m = m / vp
        ss = 0.0
        for x in rets:
            ss = ss + (x - m) * (x - m)
        stds.append((ss / (vp - 1)) ** 0.5)
    s_now = stds[0]
    if not s_now > 0:
        return float("nan")
    tot = 0.0
    for x in stds:
        tot = tot + x
    return prox * ((tot / vl) / s_now)
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 261, in <module>
    main()
    ~~~~^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 238, in main
    spec = load_spec(args.spec)
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 220, in load_spec
    spec.loader.exec_module(mod)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "<frozen importlib._bootstrap_external>", line 1023, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1161, in get_code
  File "<frozen importlib._bootstrap_external>", line 1091, in source_to_code
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/user/trading-bot/trading-bot/tests/built_components/HighProximityVolatilityRatioComponent.py", line 37
    stds.append((ss / (vp - 1))  0.5)
                 ^^^^^^^^^^^^^^^^^^^
SyntaxError: invalid syntax. Perhaps you forgot a comma?

## attempt 2

answer: built
class: HighProximityVolatilityRatioComponent
settings: {"period": 365, "vol_period": 20, "vol_lookback": 365}
reason: No component multiplies closeness to the high close by how calm the current 20-bar return volatility is against its past year. `HighProximityMomentumComponent` weights a return, not a volatility ratio, and `ConvexHighProximityComponent` is a different closeness formula with no volatility term. So one new class computes this combined measure.

table: Directional components
row: | `HighProximityVolatilityRatioComponent` | `period` (365), `vol_period` (20), `vol_lookback` (365) | P x R. P = 100 + (close[t] - H) / H x 100, H being the highest of the last `period` closes, bar t included. R = mean(s(t-`vol_lookback`+1) .. s(t)) / s(t), s(i) being the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1 ending at bar i | 0 and up, unbounded above, never negative (P is 0 to 100 for positive closes, R above 0); no direction; larger near the high and when s(t) is below its past-year mean | graded | percent of the high x volatility ratio | max(`period`, `vol_lookback` + `vol_period`) (385) | closes only. A NaN close in the last 385 rows gives NaN; an H not above 0 gives NaN; a current std s(t) of 0 (20 flat closes, never seen on real bars) gives NaN. `period` < 2, `vol_period` < 2 or `vol_lookback` < 1 raises when the component is built | stateless. Equals 100 x R at a new high. R = 1 when today's 20-bar volatility equals its 365-bar mean. No `scaling_factor`: scale it with transforms |

```python class
class HighProximityVolatilityRatioComponent(SubStrategyComponent):
    """
    Closeness to the high close, times how calm current volatility is against its past:

        H    = max(close[t - period + 1 .. t])
        P    = 100 + (close[t] - H) / H x 100
        r(j) = close[j] / close[j - 1] - 1
        s(i) = std (ddof 1) of r(i - vol_period + 1 .. i)
        R    = mean(s(t - vol_lookback + 1 .. t)) / s(t)
        raw_value = P x R

    Graded, non-negative, unbounded above, no direction. P is 100 at a new high and lower the deeper the close
    sits below it. R is above 1 when today's volatility is below its past mean.
    Warm-up: max(period, vol_lookback + vol_period) rows, bar t included (385 at the defaults).

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, vol_lookback + vol_period)
    rows of data, the last row being bar t; a close is known at its bar's close.

    NaN: a NaN close in those rows gives NaN, and so do an H not above 0 or a current std s(t) of 0.
    Building the component raises for period < 2, vol_period < 2 or vol_lookback < 1.
    """

    def __init__(self, name="HighProximityVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"HighProximityVolatilityRatioComponent: period must be >= 2, got {self.period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"HighProximityVolatilityRatioComponent: vol_period must be >= 2, got {self.vol_period}")
        self.vol_lookback = int(self.parameters.get("vol_lookback", 365))
        if self.vol_lookback < 1:
            raise ValueError(
                f"HighProximityVolatilityRatioComponent: vol_lookback must be >= 1, got {self.vol_lookback}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        high = float(np.max(c[-self.period:]))
        last = float(c[-1])
        if not high > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        prox = 100.0 + (last - high) / high * 100.0
        rets = c[1:] / c[:-1] - 1.0
        stds = pd.Series(rets).rolling(self.vol_period).std(ddof=1).to_numpy()[-self.vol_lookback:]
        s_now = float(stds[-1])
        mean_s = float(np.mean(stds))
        if np.isnan(s_now) or np.isnan(mean_s) or not s_now > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(prox * mean_s / s_now)
        self.confidence = 1.0
        self.debug_info = {'proximity': prox, 'std_now': s_now, 'std_mean': mean_s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.vol_lookback + self.vol_period)
```

```python hand
def hand(df, params):
    p = int(params.get("period", 365))
    vp = int(params.get("vol_period", 20))
    lb = int(params.get("vol_lookback", 365))
    c = [float(x) for x in list(df["close"])]
    n = max(p, lb + vp)
    c = c[len(c) - n:]
    for x in c:
        if x != x:
            return float("nan")
    h = c[len(c) - p]
    for x in c[len(c) - p:]:
        if x > h:
            h = x
    if not h > 0:
        return float("nan")
    prox = 100.0 + (c[-1] - h) / h * 100.0
    stds = []
    last = len(c) - 1
    for i in range(last - lb + 1, last + 1):
        rs = []
        for j in range(i - vp + 1, i + 1):
            rs.append(c[j] / c[j - 1] - 1.0)
        m = 0.0
        for r in rs:
            m = m + r
        m = m / vp
        ss = 0.0
        for r in rs:
            ss = ss + (r - m) * (r - m)
        stds.append(pow(ss / (vp - 1), 0.5))
    s_now = stds[-1]
    if not s_now > 0:
        return float("nan")
    tot = 0.0
    for s in stds:
        tot = tot + s
    mean_s = tot / lb
    return prox * mean_s / s_now
```

checks:
HighProximityVolatilityRatioComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1532 passed, 8 skipped, 74 deselected, 2170 warnings in 68.88s (0:01:08) ===
