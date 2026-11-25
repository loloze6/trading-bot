# MovingAverageDistanceComponent: night8_risingagitated_run | 058-02_agitated-rise-swing-scaled-giveback_1d | MovingAverageDistanceInUsualMovesComponent

## attempt 1

answer: built
class: MovingAverageDistanceComponent
settings: {"period": 20, "average": "sma", "base": "return_std", "vol_period": 20}
reason: `MovingAverageDistanceComponent` already computes this distance of the close from its SMA, but only in percent of the average. Dividing it by the standard deviation of the last 20 one-bar returns is the same measure against another base, and no config step divides by a window's return std. So the class is written again with a `base` setting ("percent" by default, which keeps today's output) and a `vol_period` read only by "return_std".

table: Directional components
row: | `MovingAverageDistanceComponent` | `period` (50), `average` ("sma"), `base` ("percent"), `vol_period` (20) | d = (close[t] − MA) / MA, MA being the simple mean of the last `period` closes including bar t (`average` "sma") or their EMA with `span` = `period`, adjust=False (`average` "ema"). `base` "percent": d x 100. `base` "return_std": d / s, s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included; 0 when s = 0. With `period` 20, "sma", "return_std", `vol_period` 20: (close[t] − SMA20) / SMA20 / s20 | unbounded, signed; positive when the close is above its average, 0 at it, negative below. With "return_std" its size is the distance from the average in usual one-bar moves | graded | "percent": percent. "return_std": usual one-bar moves (fraction of the average over the std of simple returns) | `period` with "percent" (50); max(`period`, `vol_period` + 1) with "return_std" (21 at the wished settings) | closes only. An SMA window holding a NaN close, or a NaN latest close, gives NaN; with "return_std" a NaN close among the last `vol_period` + 1 rows gives NaN, and so does a close not above 0 there or an MA not above 0 (never on real bars). s = 0 (flat return window, never on real bars) gives 0. These settings raise when the component is built: `period` below 2, `average` other than "sma" or "ema", `base` other than "percent" or "return_std", `vol_period` below 2 | stateless; no lag: the average includes the current close. `base` "percent" (default) is the original output, unchanged; `vol_period` is read only by "return_std". "return_std" counts the distance in usual one-bar moves; no config step divides by a window's std, hence the setting. With `average` "ema" and "percent" it equals `MacroTrendFilterComponent` at `scaling_factor` 1. On 1d bars the wished settings give the close's distance above its 20-day SMA in usual 20-day daily moves. No `scaling_factor`: scale it with transforms. Long-only: add a `clip` with `min` 0 |

```python class
class MovingAverageDistanceComponent(SubStrategyComponent):
    """
    Distance of the close from its moving average, on every bar:

        MA = mean(close[t-period+1 .. t])                       (average "sma", default; bar t included)
        MA = EMA of the closes, span = period, adjust=False      (average "ema", over the bar window)
        d  = (close[t] - MA) / MA
        base = "percent" (default):  raw_value = d x 100
        base = "return_std":         raw_value = d / s
            s = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1,
                j = t-vol_period+1 .. t (bar t's return included); raw_value = 0 when s = 0

    base "percent" is the original output, unchanged. With period 20, average "sma", base "return_std" and
    vol_period 20 the output is (close[t] - SMA20) / SMA20 / s20: the close's distance from its 20-bar average in
    usual one-bar moves.
    Range and sign: unbounded, signed; positive when the close is above its average, 0 at it, negative below it.
    Graded and continuous in the closes.
    Warm-up: period rows ("percent"); max(period, vol_period + 1) rows ("return_std"), bar t included.

    NaN: an SMA window holding a NaN close, or a NaN latest close, gives NaN (interior NaN closes are skipped by
    the EWM with "ema"). With "return_std", a NaN close among the last vol_period + 1 rows gives NaN, and so does
    a close not above 0 there or an MA not above 0 (never on real bars). s = 0 (a flat return window, never on
    real bars) gives 0.
    Building the component raises for a period below 2, an average other than "sma" or "ema", a base other than
    "percent" or "return_std", or a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the rows up to and including bar t (the last row of
    data): the last period closes (or the window's EMA up to bar t) and, with "return_std", the last
    vol_period + 1 closes; a bar's close is known at that bar's close.
    """

    def __init__(self, name="MA Distance", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 50))
        if self.period < 2:
            raise ValueError(f"MovingAverageDistanceComponent: period must be >= 2, got {self.period}")
        self.average = self.parameters.get("average", "sma")
        if self.average not in ("sma", "ema"):
            raise ValueError(
                f"MovingAverageDistanceComponent: average must be 'sma' or 'ema', got {self.average!r}")
        self.base = self.parameters.get("base", "percent")
        if self.base not in ("percent", "return_std"):
            raise ValueError(
                f"MovingAverageDistanceComponent: base must be 'percent' or 'return_std', got {self.base!r}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"MovingAverageDistanceComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float)
        last = float(close.iloc[-1])
        if self.average == "sma":
            window = close.iloc[-self.period:]
            ma = float("nan") if window.isna().any() else float(window.mean())
        else:
            ma = float(close.ewm(span=self.period, adjust=False).mean().iloc[-1])
        if np.isnan(last) or np.isnan(ma):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.base == "percent":
            self._raw_value = float((last - ma) / ma * 100.0)
            self.confidence = 1.0
            self.debug_info = {"ma": ma, "base": self.base}
            return
        closes = close.iloc[-(self.vol_period + 1):].to_numpy()
        if np.isnan(closes).any() or not (closes[:-1] > 0).all() or not ma > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = closes[1:] / closes[:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        if s == 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float((last - ma) / ma / s)
        self.confidence = 1.0
        self.debug_info = {"ma": ma, "s": s, "base": self.base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "return_std":
            return max(self.period, self.vol_period + 1)
        return self.period
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("period", 50))
    avg = params.get("average", "sma")
    base = params.get("base", "percent")
    vp = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    def isnan(x):
        return x != x

    last = c[t]
    if avg == "sma":
        win = [c[t - k] for k in range(n)]
        if any(isnan(x) for x in win):
            return float("nan")
        total = 0.0
        for x in win:
            total += x
        ma = total / n
    else:
        alpha = 2.0 / (n + 1.0)
        ma = float("nan")
        old_wt = 1.0
        started = False
        for x in c:
            if not started:
                if not isnan(x):
                    ma = x
                    started = True
                continue
            old_wt *= (1.0 - alpha)
            if not isnan(x):
                ma = (old_wt * ma + alpha * x) / (old_wt + alpha)
                old_wt = 1.0
    if isnan(last) or isnan(ma):
        return float("nan")
    d = (last - ma) / ma
    if base == "percent":
        return d * 100.0
    seg = [c[t - vp + k] for k in range(vp + 1)]
    if any(isnan(x) for x in seg):
        return float("nan")
    if not ma > 0:
        return float("nan")
    for x in seg[:-1]:
        if not x > 0:
            return float("nan")
    rets = []
    for k in range(1, vp + 1):
        rets.append(seg[k] / seg[k - 1] - 1.0)
    m = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var += (r - m) ** 2
    s = math.sqrt(var / (len(rets) - 1))
    if s == 0:
        return 0.0
    return d / s
```

checks:
the bot's suite fails:
ersion of bare integers (e.g. `+ 1`).Please use a specific unit instead.
    return str(pd.Timestamp("2024-04-01") + pd.Timedelta(hours=int(i)))

tests/test_gap_detection_bit_identical.py::test_middle_tier_recovery_after_required_bars
tests/test_gap_detection_bit_identical.py::test_middle_tier_recovery_after_required_bars
tests/test_gap_detection_bit_identical.py::test_middle_tier_recovery_after_required_bars
tests/test_gap_detection_bit_identical.py::test_middle_tier_recovery_after_required_bars
tests/test_gap_detection_bit_identical.py::test_middle_tier_recovery_after_required_bars
tests/test_gap_detection_bit_identical.py::test_middle_tier_recovery_after_required_bars
  /home/user/trading-bot/trading-bot/tests/test_gap_detection_bit_identical.py:239: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. `+ 1`).Please use a specific unit instead.
    pd.Timestamp("2024-01-01 04:00:00") + pd.Timedelta(hours=h) for h in range(1, 7)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================== short test summary info ============================
FAILED tests/test_ma_distance_and_macd_histogram.py::test_distance_bad_params_raise[params0-average must be one of]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
= 1 failed, 977 passed, 8 skipped, 75 deselected, 2124 warnings in 105.25s (0:01:45) =


## attempt 2

answer: built
class: MovingAverageDistanceComponent
settings: {"period": 20, "average": "sma", "base": "usual_moves", "vol_period": 20}
reason: The wished measure is the close's distance from its moving average. `MovingAverageDistanceComponent` computes that distance, but only in percent of the average. Counting it in standard deviations of recent one-bar returns is another base for the same measure, and no config step divides by a current return std. This rewrite adds `base` and `vol_period`; the default keeps today's output, and the original error messages ("period must be >= 2", "average must be one of") are kept word for word.

table: Directional components
row: | `MovingAverageDistanceComponent` | `period` (50), `average` ("sma"), `base` ("percent"), `vol_period` (20) | MA is the simple mean of the last `period` closes, bar t included (`average` "sma"), or their EMA with `span` = `period`, adjust=False (`average` "ema"). `base` "percent": (close[t] − MA) / MA x 100. `base` "usual_moves": (close[t] − MA) / MA / s, where s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included; 0 when s = 0. With `period` 20, "sma", "usual_moves" and `vol_period` 20: (close[t] − SMA20) / SMA20 / s20 | unbounded, signed; positive when the close is above its average, negative below, 0 at it; with "usual_moves" its size is the distance in usual one-bar moves | graded | "percent": percent. "usual_moves": usual one-bar moves | `period` with "percent" (50); max(`period`, `vol_period` + 1) with "usual_moves" (21 at the wished settings) | closes only. An SMA window holding a NaN close, or a NaN latest close, gives NaN; with "usual_moves" a NaN close among the last `vol_period` + 1 rows also gives NaN, and so does a close not above 0 there (never on real bars). s = 0 (flat return window, never on real bars) gives 0. These settings raise when the component is built: `period` below 2, an unknown `average`, `base` other than "percent" or "usual_moves", `vol_period` below 2 | stateless. `base` "percent" (default) is the original output, unchanged. "usual_moves" counts the distance in standard deviations of the recent one-bar returns; no config step divides by a window's std, hence the setting. No lag: the average includes the current close. With `average` "ema" and "percent" it equals `MacroTrendFilterComponent` at `scaling_factor` 1. On 1d bars the wished settings give the distance from the 20-day SMA in usual 20-day daily moves. No `scaling_factor`: scale it with transforms |

```python class
class MovingAverageDistanceComponent(SubStrategyComponent):
    """
    Distance of the close from its moving average, on every bar:

        MA = mean(close[t-period+1 .. t])                     (average "sma", default; bar t included)
        MA = EMA(close, span=period, adjust=False) at bar t   (average "ema")
        base = "percent" (default):  raw_value = (close[t] - MA) / MA x 100
        base = "usual_moves":        raw_value = (close[t] - MA) / MA / s
            s = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1,
                j = t-vol_period+1 .. t (bar t's return included); raw_value = 0 when s = 0

    base "percent" is the original output, unchanged.
    Range & sign: unbounded, signed; positive when the close is above its average, negative below, 0 at it.
    With "usual_moves" the size is the distance counted in usual one-bar moves.
    Warm-up: period rows ("percent"); max(period, vol_period + 1) rows ("usual_moves").

    NaN: an SMA window holding a NaN close, or a NaN latest close, gives NaN (interior NaN closes are skipped
    by the EWM with "ema"). With "usual_moves", a NaN close among the last vol_period + 1 rows, or a close not
    above 0 there, gives NaN; s = 0 (never on real bars) gives 0.
    Building the component raises for a period below 2, an average other than "sma" or "ema", a base other
    than "percent" or "usual_moves", or a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the rows up to and including bar t (the last row
    of data): the last period closes for the SMA (the window's closes up to bar t for the EMA) and the last
    vol_period + 1 closes for s; a bar's close is known at that bar's close.
    """

    def __init__(self, name="MovingAverageDistance", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 50))
        if self.period < 2:
            raise ValueError(f"MovingAverageDistanceComponent: period must be >= 2, got {self.period}")
        self.average = self.parameters.get("average", "sma")
        if self.average not in ("sma", "ema"):
            raise ValueError(
                f"MovingAverageDistanceComponent: average must be one of ('sma', 'ema'), got {self.average!r}")
        self.base = self.parameters.get("base", "percent")
        if self.base not in ("percent", "usual_moves"):
            raise ValueError(
                f"MovingAverageDistanceComponent: base must be one of ('percent', 'usual_moves'), got {self.base!r}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"MovingAverageDistanceComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float)
        c = float(close.iloc[-1])
        if self.average == "sma":
            ma = float(close.iloc[-self.period:].mean(skipna=False))
        else:
            ma = float(close.ewm(span=self.period, adjust=False).mean().iloc[-1])
        if np.isnan(c) or np.isnan(ma) or ma == 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rel = (c - ma) / ma
        if self.base == "percent":
            self._raw_value = float(rel * 100.0)
            s = None
        else:
            w = close.iloc[-(self.vol_period + 1):].to_numpy(dtype=float)
            if np.isnan(w).any() or not (w[:-1] > 0).all():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            rets = w[1:] / w[:-1] - 1.0
            s = float(np.std(rets, ddof=1))
            self._raw_value = 0.0 if s == 0 else float(rel / s)
        self.confidence = 1.0
        self.debug_info = {'close': c, 'ma': ma, 'average': self.average, 'base': self.base, 'std': s}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "usual_moves":
            return max(self.period, self.vol_period + 1)
        return self.period
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("period", 50))
    avg = params.get("average", "sma")
    base = params.get("base", "percent")
    vp = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    last = c[t]
    if last != last:
        return float("nan")
    if avg == "sma":
        total = 0.0
        for k in range(n):
            x = c[t - k]
            if x != x:
                return float("nan")
            total = total + x
        ma = total / n
    else:
        alpha = 2.0 / (n + 1.0)
        e = None
        for x in c:
            if x != x:
                continue
            if e is None:
                e = x
            else:
                e = (1.0 - alpha) * e + alpha * x
        ma = e
    if ma is None or ma == 0:
        return float("nan")
    rel = (last - ma) / ma
    if base == "percent":
        return rel * 100.0
    rets = []
    for j in range(t - vp + 1, t + 1):
        a = c[j - 1]
        b = c[j]
        if a != a or b != b or not a > 0:
            return float("nan")
        rets.append(b / a - 1.0)
    m = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var = var + (r - m) * (r - m)
    s = math.sqrt(var / (len(rets) - 1))
    if s == 0:
        return 0.0
    return rel / s
```

checks:
MovingAverageDistanceComponent: every check passed
the bot's suite: == 1669 passed, 16 skipped, 75 deselected, 2244 warnings in 120.09s (0:02:00) ==
