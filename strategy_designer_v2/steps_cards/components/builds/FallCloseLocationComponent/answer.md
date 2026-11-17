# FallCloseLocationComponent: night_run | 011-01_weekend-rise-reverses-monday.g1_volatile-day-selloffs-bounce-next.g1_falls-closing-near-low-bounce_1d | DownMoveCloseLocationComponent

## attempt 1

answer: built
class: FallCloseLocationComponent
settings: {"vol_period": 60}
reason: No catalogue class multiplies the fall in usual moves by where the close sits in the bar's range. `VolatilityRankedFallComponent` weights the fall by a volatility rank, and `CloseLocationInRangeComponent` (`reference` "high") only gives the close location. This product is one new measure, so one new class computes it, with the 60-bar return window as a setting.

table: Directional components
row: | `FallCloseLocationComponent` | `vol_period` (60) | max(0, -(close[t] / close[t-1] - 1) / s) x (high[t] - close[t]) / (high[t] - low[t]), s being the standard deviation (ddof 1) of the last `vol_period` one-bar returns close[j] / close[j-1] - 1, bar t's included; the second factor is 0.5 when high[t] = low[t]; the first factor is 0 when s = 0 | 0 and up, unbounded above, never negative; 0 on up bars and flat bars; grows with the depth of today's fall in usual moves and with how near the close is to the bar's low (second factor 0 to 1 on real bars) | graded | usual moves x share of the bar's range | `vol_period` + 1 (61) | close, high, low. A NaN close in the last `vol_period` + 1 rows, or a NaN high or low on bar t, gives NaN; a close not above 0 among the bases gives NaN; a flat return window (s = 0, never on real bars) gives 0. A `vol_period` below 2 raises when the component is built | stateless. Equals `VolatilityScaledReturnComponent` (`period` 1, `vol_period` 60) negated and clipped at 0, times `CloseLocationInRangeComponent` (`reference` "high"). One-sided (a long-only rebound reading). No `scaling_factor`: scale it with transforms |

```python class
class FallCloseLocationComponent(SubStrategyComponent):
    """
    The size of today's fall in usual moves, weighted by how near the close is to the bar's low:

        r(j)  = close[j] / close[j-1] - 1
        s     = std (ddof 1) of r(t - vol_period + 1) .. r(t)          (bar t's return included)
        fall  = max(0, -r(t) / s)                                       (0 when s = 0)
        loc   = (high[t] - close[t]) / (high[t] - low[t])               (0.5 when high[t] = low[t])
        raw_value = fall x loc

    Graded and one-sided. The value is 0 and up, unbounded above and never negative. It is 0 on up bars
    and on flat bars. It grows with the depth of the fall in usual moves and as the close nears the bar's
    low; loc is 0 to 1 on real bars. No direction.
    Warm-up: vol_period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads the `close` column of the last vol_period + 1 rows up to and including bar t
    (the last row of data), and the `high` and `low` of bar t only; all are known at bar t's close.

    NaN: a NaN close in the last vol_period + 1 rows, or a NaN high or low on bar t, gives NaN. A base close
    that is not above 0 also gives NaN. A flat return window (s = 0, never seen on real bars) gives 0.
    Building the component raises for a vol_period below 2.
    """

    def __init__(self, name="FallCloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 60))
        if self.vol_period < 2:
            raise ValueError(f"FallCloseLocationComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float).iloc[-(self.vol_period + 1):].to_numpy()
        high = float(data['high'].iloc[-1])
        low = float(data['low'].iloc[-1])
        if np.isnan(close).any() or np.isnan(high) or np.isnan(low):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        prev = close[:-1]
        if not (prev > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = close[1:] / prev - 1.0
        s = float(np.std(rets, ddof=1))
        r = float(rets[-1])
        z = -r / s if s > 0 else 0.0
        fall = z if z > 0 else 0.0
        rng = high - low
        loc = 0.5 if rng == 0 else (high - float(close[-1])) / rng
        self._raw_value = float(fall * loc)
        self.confidence = 1.0
        self.debug_info = {'return': r, 'std': s, 'fall_usual_moves': fall, 'close_location_from_high': loc}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.vol_period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("vol_period", 60))
    c = [float(x) for x in list(df["close"])]
    h = float(list(df["high"])[-1])
    l = float(list(df["low"])[-1])
    last = len(c) - 1
    window = []
    i = last - n
    while i <= last:
        window.append(c[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
    if h != h or l != l:
        return float("nan")
    rets = []
    k = 1
    while k < len(window):
        base = window[k - 1]
        if not base > 0:
            return float("nan")
        rets.append(window[k] / base - 1.0)
        k = k + 1
    m = sum(rets) / len(rets)
    ss = 0.0
    for x in rets:
        ss = ss + (x - m) * (x - m)
    s = math.sqrt(ss / (len(rets) - 1))
    today = rets[-1]
    if s > 0:
        fall = -today / s
    else:
        fall = 0.0
    if fall < 0:
        fall = 0.0
    if h == l:
        loc = 0.5
    else:
        loc = (h - c[last]) / (h - l)
    return fall * loc
```

checks:
FallCloseLocationComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1535 passed, 8 skipped, 74 deselected, 2170 warnings in 73.20s (0:01:13) ===
