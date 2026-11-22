# RecentToPriorVolatilityRatioComponent: night4_weekend_run | 026-02_weekend-drop-reverses-early-week.d1_turbulent-weekend-falls-continue.b1_turbulent-weekend-falls-continue_1h | WeekendToPriorWeekVolatilityRatio

## attempt 1

answer: built
class: VolatilityRatioToAverageComponent
settings: {"vol_period": 48, "vol_lookback": 168, "base": "window", "base_lag": 48}
reason: The wish is the same measure as `VolatilityRatioToAverageComponent`: today's return volatility against a base volatility, with another base (the std of a lagged 168-return window instead of the mean of rolling stds). Only `RecentToPriorVolatilityWeightedReturnComponent` holds this ratio, and only multiplied by a return, so the class is rewritten with a `base` setting and a `base_lag` setting, and `vol_lookback` keeps its role as the base's length; the defaults ("average", 0) leave today's output unchanged.

table: Regime measures
row: | `VolatilityRatioToAverageComponent` | `vol_period` (20), `vol_lookback` (60), `base` ("average"), `base_lag` (0) | s(t) / D, where s(i) is the std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1 ending at bar i, that bar's included. With `base` "average", D = mean(s(t-`base_lag`-`vol_lookback`+1) .. s(t-`base_lag`)). With `base` "window", D = the std (ddof 1) of the `vol_lookback` one-bar returns r[j], j = t-`base_lag`-`vol_lookback`+1 .. t-`base_lag`. With `vol_period` 48, `vol_lookback` 168, `base` "window" and `base_lag` 48 it is std(r[t-47..t]) / std(r[t-215..t-48]) | 0 and up, never negative; no direction. It is 1 when today's volatility equals the base, above 1 when it is higher and below 1 when it is lower. With "average" and `base_lag` 0 it is at most `vol_lookback`; otherwise it is unbounded above | regime measure | dimensionless (ratio of volatilities) | "average": `vol_lookback` + `vol_period` + `base_lag` (80). "window": max(`vol_period`, `base_lag` + `vol_lookback`) + 1 | closes only. A NaN close or a close not above 0 (never on real bars) in the rows read gives NaN. A base D of 0 (flat returns, never on real bars) gives NaN. These settings raise when the component is built: `vol_period` < 2, `vol_lookback` < 1 ("average") or < 2 ("window"), `base_lag` < 0, `base` other than "average" or "window" | stateless; graded. `base` "average" with `base_lag` 0 (the defaults) is the original output, unchanged. "window" with 48 / 168 / 48 gives the recent two days against the week before them, the s_recent / s_base factor of `RecentToPriorVolatilityWeightedReturnComponent` on its own (adjacent, non-overlapping windows). It is the inverse of the R factor of `HighProximityVolatilityRatioComponent` at the defaults. No `scaling_factor`: scale it with transforms |

```python class
class VolatilityRatioToAverageComponent(SubStrategyComponent):
    """
    Current return volatility against a base volatility, on every bar:

        r[j] = close[j] / close[j-1] - 1
        s(i) = std (ddof 1) of the vol_period returns r[i-vol_period+1 .. i]   (bar i's return included)
        base = "average" (default): D = mean(s(t-base_lag-vol_lookback+1) .. s(t-base_lag))
        base = "window":            D = std (ddof 1) of r[t-base_lag-vol_lookback+1 .. t-base_lag]
        raw_value = s(t) / D

    With base "average" and base_lag 0 (the defaults) the output is s(t) / mean of s over the last vol_lookback bars,
    the original output, unchanged. With vol_period 48, vol_lookback 168, base "window" and base_lag 48 the output is
    std(r[t-47..t]) / std(r[t-215..t-48]). Those are the last two days against the week before them on 1h bars.
    Range: 0 and up, never negative, no direction. It is 1 when today's volatility equals the base and grows
    continuously as today's volatility rises above it. With "average" and base_lag 0 it is at most vol_lookback;
    otherwise it is unbounded above.
    Warm-up: "average": vol_lookback + vol_period + base_lag rows; "window": max(vol_period, base_lag + vol_lookback)
    + 1 rows, bar t included.
    NaN: a NaN close, or a close not above 0, among the rows read gives NaN; a base D of 0 gives NaN (flat returns,
    never on real bars).
    Building raises for vol_period < 2, vol_lookback < 1 ("average") or < 2 ("window"), base_lag < 0, and a base
    other than "average" or "window".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last get_required_periods() rows of data, the last
    of which is bar t; every return used ends at bar t or earlier.
    """

    def __init__(self, name="VolatilityRatioToAverage", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"VolatilityRatioToAverageComponent: vol_period must be >= 2, got {self.vol_period}")
        self.base = self.parameters.get("base", "average")
        if self.base not in ("average", "window"):
            raise ValueError(f"VolatilityRatioToAverageComponent: base must be 'average' or 'window', got {self.base!r}")
        self.vol_lookback = int(self.parameters.get("vol_lookback", 60))
        min_lb = 2 if self.base == "window" else 1
        if self.vol_lookback < min_lb:
            raise ValueError(
                f"VolatilityRatioToAverageComponent: vol_lookback must be >= {min_lb} with base {self.base!r}, "
                f"got {self.vol_lookback}")
        self.base_lag = int(self.parameters.get("base_lag", 0))
        if self.base_lag < 0:
            raise ValueError(f"VolatilityRatioToAverageComponent: base_lag must be >= 0, got {self.base_lag}")
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
        r = c[1:] / c[:-1] - 1.0
        m = len(r)
        vp = self.vol_period

        def s_at(k):
            # std of the vol_period returns ending at bar t-k
            return float(np.std(r[m - k - vp:m - k], ddof=1))

        num = s_at(0)
        if self.base == "average":
            den = float(np.mean([s_at(self.base_lag + q) for q in range(self.vol_lookback)]))
        else:
            lo = m - self.base_lag - self.vol_lookback
            hi = m - self.base_lag
            den = float(np.std(r[lo:hi], ddof=1))
        if np.isnan(num) or np.isnan(den) or not den > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(num / den)
        self.confidence = 1.0
        self.debug_info = {"recent_vol": num, "base_vol": den, "base": self.base, "base_lag": self.base_lag}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "window":
            return max(self.vol_period, self.base_lag + self.vol_lookback) + 1
        return self.vol_lookback + self.vol_period + self.base_lag
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("vol_period", 20))
    L = int(params.get("vol_lookback", 60))
    base = params.get("base", "average")
    lag = int(params.get("base_lag", 0))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def std1(xs):
        n = len(xs)
        mu = sum(xs) / n
        ss = 0.0
        for x in xs:
            ss += (x - mu) ** 2
        return math.sqrt(ss / (n - 1))

    def closes_ok(lo, hi):
        for j in range(lo, hi + 1):
            x = c[j]
            if x != x or not x > 0:
                return False
        return True

    def s(i):
        return std1([ret(j) for j in range(i - vp + 1, i + 1)])

    if not closes_ok(t - vp, t):
        return float("nan")
    num = s(t)
    if base == "window":
        lo = t - lag - L + 1
        hi = t - lag
        if not closes_ok(lo - 1, hi):
            return float("nan")
        den = std1([ret(j) for j in range(lo, hi + 1)])
    else:
        first = t - lag - L + 1
        if not closes_ok(first - vp, t - lag):
            return float("nan")
        vals = [s(i) for i in range(first, t - lag + 1)]
        den = sum(vals) / len(vals)
    if not den > 0:
        return float("nan")
    return num / den
```

checks:
the bot's suite fails:
gap
tests/test_rolling_buffer_reindex.py::test_rolling_window_correctly_shrinks_across_an_unfilled_large_gap
tests/test_rolling_buffer_reindex.py::test_rolling_window_correctly_shrinks_across_an_unfilled_large_gap
tests/test_rolling_buffer_reindex.py::test_rolling_window_correctly_shrinks_across_an_unfilled_large_gap
tests/test_rolling_buffer_reindex.py::test_rolling_window_correctly_shrinks_across_an_unfilled_large_gap
tests/test_rolling_buffer_reindex.py::test_rolling_window_correctly_shrinks_across_an_unfilled_large_gap
tests/test_rolling_buffer_reindex.py::test_rolling_window_correctly_shrinks_across_an_unfilled_large_gap
  /home/user/trading-bot/trading-bot/tests/test_rolling_buffer_reindex.py:104: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. `+ 1`).Please use a specific unit instead.
    gap_row_positions = [df.index[df["timestamp"] == ts[-1] + pd.Timedelta(hours=h)][0] for h in range(1, 10)]

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_trailing_return_stds.py::test_same_values_every_bar[VolatilityRatioToAverageComponent-params2-<lambda>-mean_std-<lambda>]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
= 1 failed, 1473 passed, 13 skipped, 75 deselected, 2243 warnings in 95.75s (0:01:35) =


## attempt 2

answer: built
class: RecentToPriorVolatilityRatioComponent
settings: {"vol_period": 48, "base_period": 168, "base_lag": 48}
reason: No catalogue component outputs this ratio of return stds by itself. `RecentToPriorVolatilityWeightedReturnComponent` multiplies it by the 48-bar return, and `VolatilityRatioToAverageComponent` divides one std by the mean of a rolling std, which is a different measure. This is a new class, so no existing component's output changes, unlike the earlier attempt that changed `VolatilityRatioToAverageComponent` and failed its test. Its `form` "centred" (ratio minus 1) is a value no config step gives.

table: Regime measures
row: | `RecentToPriorVolatilityRatioComponent` | `vol_period` (48), `base_period` (168), `base_lag` (48), `form` ("ratio") | s_recent / s_base. s_recent = std (ddof 1) of the `vol_period` one-bar returns r[j] = close[j] / close[j-1] - 1, j = t-`vol_period`+1 .. t. s_base = std (ddof 1) of the `base_period` returns r[j], j = t-`base_lag`-`base_period`+1 .. t-`base_lag`. `form` "ratio": the ratio. `form` "centred": the ratio - 1 | "ratio": 0 and up, unbounded above, never negative; no direction; 1 when the recent bars are as volatile as the base, above 1 as they get more turbulent, below 1 as they get quieter. "centred": -1 and up, signed, 0 at equal volatility | regime measure | dimensionless (ratio of volatilities) | max(`vol_period`, `base_lag` + `base_period`) + 1 (217) | closes only. A NaN close among the rows read gives NaN. A close not above 0 there gives NaN (never on real bars). s_base = 0 (flat base returns, never on real bars) gives NaN. These settings raise when the component is built: `vol_period` < 2, `base_period` < 2, `base_lag` < 0, `form` other than "ratio" or "centred" | stateless; graded and continuous in the closes. At the defaults the recent returns (bars t-47 .. t) and the base (bars t-215 .. t-48) are adjacent and do not overlap: on 1h bars, the last two days against the week before them. It is the volatility factor of `RecentToPriorVolatilityWeightedReturnComponent` on its own. No `scaling_factor`: scale it with transforms |

```python class
class RecentToPriorVolatilityRatioComponent(SubStrategyComponent):
    """
    Recent one-bar return volatility against an earlier base, on every bar:

        r[j] = close[j] / close[j-1] - 1
        s_recent = std (ddof 1) of r[j], j = t-vol_period+1 .. t
        s_base   = std (ddof 1) of r[j], j = t-base_lag-base_period+1 .. t-base_lag
        form "ratio" (default): raw_value = s_recent / s_base
        form "centred":         raw_value = s_recent / s_base - 1

    Range and sign: "ratio" is 0 and up, unbounded above, never negative, with no direction. It is 1 when the
    recent bars are as volatile as the base and grows continuously as they get more turbulent. "centred" is -1
    and up, signed, and 0 at equal volatility.
    Warm-up: max(vol_period, base_lag + base_period) + 1 rows, bar t included (217 at the defaults).
    NaN: a NaN close among the rows read gives NaN. A close not above 0 among them gives NaN. s_base = 0 gives NaN.
    Building raises for vol_period < 2, base_period < 2, base_lag < 0, or a form other than "ratio" or "centred".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(vol_period, base_lag + base_period) + 1
    rows of data, the last of which is bar t; no row after bar t is read.
    """

    def __init__(self, name="RecentToPriorVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 48))
        self.base_period = int(self.parameters.get("base_period", 168))
        self.base_lag = int(self.parameters.get("base_lag", 48))
        self.form = self.parameters.get("form", "ratio")
        if self.vol_period < 2:
            raise ValueError(f"RecentToPriorVolatilityRatioComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.base_period < 2:
            raise ValueError(f"RecentToPriorVolatilityRatioComponent: base_period must be >= 2, got {self.base_period}")
        if self.base_lag < 0:
            raise ValueError(f"RecentToPriorVolatilityRatioComponent: base_lag must be >= 0, got {self.base_lag}")
        if self.form not in ("ratio", "centred"):
            raise ValueError(f"RecentToPriorVolatilityRatioComponent: form must be 'ratio' or 'centred', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        last = len(c) - 1  # bar t

        def returns(first_j, last_j):
            prev = c[first_j - 1:last_j]
            cur = c[first_j:last_j + 1]
            if np.isnan(prev).any() or np.isnan(cur).any():
                return None
            if not (prev > 0).all() or not (cur > 0).all():
                return None
            return cur / prev - 1.0

        r_recent = returns(last - self.vol_period + 1, last)
        b_end = last - self.base_lag
        r_base = returns(b_end - self.base_period + 1, b_end)
        if r_recent is None or r_base is None:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        s_recent = float(np.std(r_recent, ddof=1))
        s_base = float(np.std(r_base, ddof=1))
        if not s_base > 0:
            self._raw_value = float("nan")
        else:
            ratio = s_recent / s_base
            self._raw_value = float(ratio - 1.0) if self.form == "centred" else float(ratio)
        self.confidence = 1.0
        self.debug_info = {"s_recent": s_recent, "s_base": s_base, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.vol_period, self.base_lag + self.base_period) + 1
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("vol_period", 48))
    bp = int(params.get("base_period", 168))
    lag = int(params.get("base_lag", 48))
    form = params.get("form", "ratio")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    def ret(j):
        a = c[j - 1]
        b = c[j]
        if a != a or b != b or not a > 0 or not b > 0:
            return None
        return b / a - 1.0

    def sample_std(xs):
        m = 0.0
        for x in xs:
            m += x
        m /= len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) ** 2
        return math.sqrt(ss / (len(xs) - 1))

    recent = []
    for j in range(t - vp + 1, t + 1):
        r = ret(j)
        if r is None:
            return float("nan")
        recent.append(r)
    base = []
    for j in range(t - lag - bp + 1, t - lag + 1):
        r = ret(j)
        if r is None:
            return float("nan")
        base.append(r)
    sr = sample_std(recent)
    sb = sample_std(base)
    if not sb > 0:
        return float("nan")
    ratio = sr / sb
    if form == "centred":
        return ratio - 1.0
    return ratio
```

checks:
RecentToPriorVolatilityRatioComponent: every check passed
the bot's suite: == 1612 passed, 16 skipped, 75 deselected, 2244 warnings in 99.63s (0:01:39) ===
