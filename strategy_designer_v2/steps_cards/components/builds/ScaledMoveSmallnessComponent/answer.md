# ScaledMoveSmallnessComponent: a4_research_run | 060-01.b1.g1_quiet-day-next-fade_1d | ScaledMoveSmallnessComponent

## attempt 1

answer: built
class: VolatilityScaledReturnComponent
settings: {"period": 1, "vol_period": 20, "form": "smallness"}
reason: The catalogue has the day's move in usual moves, (close[t] / close[t-1] - 1) / s20, as `VolatilityScaledReturnComponent` (`period` 1, `vol_period` 20). No config step gives 1 / (1 + abs of a value), so the whole class is written again with a `form` setting, as the "proximity" forms of `IchimokuCloudSlopeComponent` and `DistanceFromHighComponent` were. Its default "return" keeps today's output exactly.

table: Directional components
row: | `VolatilityScaledReturnComponent` | `period` (1), `vol_period` (20), `lag` (0), `vol_lookback` (1), `form` ("return") | x = (close[t-`lag`] / close[t-`lag`-`period`] - 1) / (m x sqrt(`period`)). m = mean(s(t-`lag`-`vol_lookback`+1) .. s(t-`lag`)), and s(i) is the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1 ending at bar i, that bar's included. `vol_lookback` 1 gives m = s(t-`lag`), and `lag` 0 is bar t itself. x = 0 when m = 0. `form` "return": x. `form` "smallness": 1 / (1 + abs(x)). With `period` 1, `vol_period` 20, "smallness": 1 / (1 + abs(close[t] / close[t-1] - 1) / s20) | "return": unbounded, signed; about +1 for a rise of one usual move, -2 for a fall of two. With `vol_lookback` above 1 the usual move is its average over the lookback, so the size also grows when the current volatility sits above that average. "smallness": above 0, up to 1, never negative; no direction; 1 for a zero move, 0.5 for a move of one usual move either way, shrinking toward 0 as the move grows | graded | "return": usual moves. "smallness": dimensionless (0 to 1) | max(`period` + 1, `vol_period` + `vol_lookback`) + `lag` (21) | closes. A NaN close among the last max(`period` + 1, `vol_period` + `vol_lookback`) + `lag` rows gives NaN. m = 0 (flat return windows) gives x = 0, so "smallness" reads 1. These settings raise when the component is built: `period` below 1, `vol_period` below 2, `lag` below 0, `vol_lookback` below 1, `form` other than "return" or "smallness" | stateless. `form` "return" with `vol_lookback` 1 (the defaults) is the original output, unchanged. "smallness" is 1 / (1 + the size of the move in usual moves), which no config step gives, hence the setting. It is continuous in the closes and peaks at a zero move. With `period` 24, `vol_period` 168 and `vol_lookback` 720 "return" equals the 24-bar return in usual moves times s(t) / mean(s over the last 720 bars). On 1d bars the wished settings give the smallness of the day's move against its 20-day swing. No `scaling_factor`: scale it with transforms |

```python class
class VolatilityScaledReturnComponent(SubStrategyComponent):
    """
    A move counted in usual one-bar moves, on every bar:

        e = t - lag
        s(i) = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1, j = i-vol_period+1 .. i
        m = mean(s(e-vol_lookback+1) .. s(e))            (vol_lookback 1: m = s(e))
        x = (close[e] / close[e-period] - 1) / (m * sqrt(period)),  x = 0 when m = 0
        form = "return" (default):  raw_value = x
        form = "smallness":         raw_value = 1 / (1 + abs(x))

    With period 1, vol_period 20, form "smallness":
        1 / (1 + abs(close[t] / close[t-1] - 1) / s20).

    Range: "return" is unbounded and signed, about +1 for a rise of one usual move.
    "smallness" is above 0 and up to 1, never negative, with no direction. It is 1 for a zero move,
    0.5 at one usual move either way, and shrinks toward 0 as the move grows.
    The defaults (form "return", vol_lookback 1) are the original output, unchanged.
    Warm-up: max(period + 1, vol_period + vol_lookback) + lag rows, bar t included.
    NaN: a NaN close among those rows gives NaN. m = 0 gives x = 0 ("smallness" 1).
    Building raises for period < 1, vol_period < 2, lag < 0, vol_lookback < 1,
    or a form other than "return" or "smallness".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last
    max(period + 1, vol_period + vol_lookback) + lag rows of data, the last row being bar t.
    It uses no row after bar t, and none after bar t - lag in the value.
    """

    def __init__(self, name="VolScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 1))
        self.vol_period = int(self.parameters.get("vol_period", 20))
        self.lag = int(self.parameters.get("lag", 0))
        self.vol_lookback = int(self.parameters.get("vol_lookback", 1))
        self.form = self.parameters.get("form", "return")
        if self.period < 1:
            raise ValueError(f"VolatilityScaledReturnComponent: period must be >= 1, got {self.period}")
        if self.vol_period < 2:
            raise ValueError(f"VolatilityScaledReturnComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.lag < 0:
            raise ValueError(f"VolatilityScaledReturnComponent: lag must be >= 0, got {self.lag}")
        if self.vol_lookback < 1:
            raise ValueError(f"VolatilityScaledReturnComponent: vol_lookback must be >= 1, got {self.vol_lookback}")
        if self.form not in ("return", "smallness"):
            raise ValueError(f"VolatilityScaledReturnComponent: form must be 'return' or 'smallness', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-need:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = len(c)
        e = n - 1 - self.lag
        stds = []
        for i in range(e - self.vol_lookback + 1, e + 1):
            seg = c[i - self.vol_period:i + 1]
            r = seg[1:] / seg[:-1] - 1.0
            stds.append(float(np.std(r, ddof=1)))
        m = float(np.mean(stds))
        move = float(c[e] / c[e - self.period] - 1.0)
        if m == 0:
            x = 0.0
        else:
            x = move / (m * float(np.sqrt(self.period)))
        if self.form == "smallness":
            self._raw_value = float(1.0 / (1.0 + abs(x)))
        else:
            self._raw_value = float(x)
        self.confidence = 1.0
        self.debug_info = {"move": move, "mean_std": m, "scaled_move": x, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + 1, self.vol_period + self.vol_lookback) + self.lag
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 1))
    vp = int(params.get("vol_period", 20))
    lag = int(params.get("lag", 0))
    vl = int(params.get("vol_lookback", 1))
    form = params.get("form", "return")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(p + 1, vp + vl) + lag
    for k in range(need):
        if c[t - k] != c[t - k]:
            return float("nan")
    e = t - lag

    def std1(xs):
        mu = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - mu) ** 2
        return math.sqrt(ss / (len(xs) - 1))

    sds = []
    for i in range(e - vl + 1, e + 1):
        rets = []
        for j in range(i - vp + 1, i + 1):
            rets.append(c[j] / c[j - 1] - 1.0)
        sds.append(std1(rets))
    m = sum(sds) / len(sds)
    move = c[e] / c[e - p] - 1.0
    x = 0.0 if m == 0 else move / (m * math.sqrt(p))
    if form == "smallness":
        return 1.0 / (1.0 + abs(x))
    return x
```

checks:
the bot's suite fails:
_gap
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
FAILED tests/test_trailing_return_stds.py::test_same_values_every_bar[VolatilityScaledReturnComponent-params0-<lambda>-mean_std-<lambda>]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
= 1 failed, 1537 passed, 13 skipped, 75 deselected, 2243 warnings in 163.53s (0:02:43) =


## attempt 2

answer: built
class: ScaledMoveSmallnessComponent
settings: {"vol_period": 20}
reason: No component gives the size of the day's move in usual moves turned into a bounded smallness. `VolatilityScaledReturnComponent` is the signed move, and no config step takes its absolute value or 1 / (1 + x). The absolute move is a separate measure from the signed move, as `MeanAbsReturnComponent` is from `PriceEvolutionComponent`, so it is a new class and leaves `VolatilityScaledReturnComponent` untouched.

table: Regime measures
row: | `ScaledMoveSmallnessComponent` | `vol_period` (20) | 1 / (1 + abs(close[t] / close[t-1] − 1) / s), s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included; 1.0 when s = 0 (the move is then 0 too) | above 0, up to 1, never negative; no direction; 1 for a zero move, shrinking toward 0 as the day's move grows in usual one-bar moves, growing smoothly as it shrinks | regime measure | dimensionless (smallness, 0 to 1) | `vol_period` + 1 (21) | closes only (last `vol_period` + 1 rows). A NaN close among them gives NaN; a close not above 0 among the return bases gives NaN (never on real bars). s = 0 (flat return window, never on real bars) gives 1.0. These settings raise when the component is built: `vol_period` < 2 | stateless; graded and continuous in the closes. The scaled move is abs(`VolatilityScaledReturnComponent` (`period` 1, `vol_period`)); no config step gives its absolute value or 1 / (1 + x), hence the class. On 1d bars the defaults give the quietness of the day's move against its 20-day swing. No `scaling_factor`: scale it with transforms |

```python class
class ScaledMoveSmallnessComponent(SubStrategyComponent):
    """
    Smallness of the current bar's move in usual one-bar moves, on every bar:

        r[j] = close[j] / close[j-1] - 1
        s    = std (ddof 1) of r[j], j = t-vol_period+1 .. t   (bar t's return included)
        raw_value = 1 / (1 + abs(r[t]) / s)
        s = 0 (every return of the window is 0, so r[t] = 0 too): raw_value = 1.0

    Range: above 0, up to 1, never negative, no direction. It is 1 for a zero move and shrinks toward 0 as the
    move grows against the usual swing. It grows smoothly as the move shrinks.
    Warm-up: vol_period + 1 rows, bar t included.

    NaN: a NaN close among the last vol_period + 1 rows gives NaN. A close not above 0 among the return bases
    (bars t-vol_period .. t-1) gives NaN (never on real bars).
    Building the component raises for a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last vol_period + 1 rows of data, bar t (the
    last row) included; a bar's close is known at that bar's close.
    """

    def __init__(self, name="ScaledMoveSmallness", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"ScaledMoveSmallnessComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.vol_period
        closes = data['close'].astype(float).to_numpy()[-(n + 1):]
        if np.isnan(closes).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        bases = closes[:-1]
        if not (bases > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = closes[1:] / bases - 1.0
        mean_r = float(np.sum(rets)) / n
        var = float(np.sum((rets - mean_r) ** 2)) / (n - 1)
        s = float(np.sqrt(var)) if var > 0 else 0.0
        r_t = float(rets[-1])
        if s > 0:
            value = 1.0 / (1.0 + abs(r_t) / s)
        else:
            value = 1.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'return': r_t, 'std': s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.vol_period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    # the closes read: bars t-n .. t
    for k in range(n + 1):
        x = c[t - k]
        if x != x:
            return float("nan")
    # one-bar returns j = t-n+1 .. t
    rets = []
    for j in range(t - n + 1, t + 1):
        prev = c[j - 1]
        if not prev > 0:
            return float("nan")
        rets.append(c[j] / prev - 1.0)
    total = 0.0
    for r in rets:
        total = total + r
    mean_r = total / n
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean_r) * (r - mean_r)
    s = math.sqrt(ss / (n - 1))
    move = c[t] / c[t - 1] - 1.0
    if s == 0:
        return 1.0
    return 1.0 / (1.0 + abs(move) / s)
```

checks:
ScaledMoveSmallnessComponent: every check passed
the bot's suite: == 1678 passed, 16 skipped, 75 deselected, 2244 warnings in 163.52s (0:02:43) ==
