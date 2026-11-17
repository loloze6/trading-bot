# VolatilityScaledReturnComponent: night_run | 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.b1_weekend-move-reverses-three-days_1d | LaggedVolatilityScaledReturnComponent

## attempt 1

answer: built
class: VolatilityScaledReturnComponent
settings: {"period": 1, "vol_period": 20, "lag": 1}
reason: The wished quantity is `VolatilityScaledReturnComponent`'s measure, a move in usual moves, read on bar t-`lag` instead of bar t. No config step shifts a component back in time, so the class is rewritten with a `lag` setting. Its default of 0 keeps today's output exactly, and lag 0, 1 and 2 give the three bars of the weekend move.

table: Directional components
row: | `VolatilityScaledReturnComponent` | `period` (1), `vol_period` (20), `lag` (0) | (close[t-`lag`] / close[t-`lag`-`period`] - 1) / (s x sqrt(`period`)), s being the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1 ending at bar t-`lag`, that bar's included; `lag` 0 is bar t itself | unbounded, signed; about +1 for a rise of one usual move, -2 for a fall of two | graded | usual moves | max(`period`, `vol_period`) + 1 + `lag` (21) | closes. A NaN close among rows t-`lag`-max(`period`, `vol_period`) .. t-`lag` gives NaN; a flat return window (s = 0) gives 0. These settings raise when the component is built: `period` below 1, `vol_period` below 2, `lag` below 0 | stateless. The size of a past bar's move against the coin's usual move at that time. `lag` 0 (default) is the original output, unchanged; with `period` 1 and `lag` 1 it is yesterday's move in usual moves. No `scaling_factor`: scale it with transforms. |

```python class
class VolatilityScaledReturnComponent(SubStrategyComponent):
    """
    The size of a move against the coin's usual move, read on bar u = t - lag:

        r(j) = close[j] / close[j-1] - 1
        s    = std(r(u - vol_period + 1) .. r(u)), ddof 1
        raw_value = (close[u] / close[u - period] - 1) / (s x sqrt(period)),   u = t - lag

    lag 0 (default) gives the move ending at bar t, the original output, unchanged.
    Graded and signed: positive after a rise, negative after a fall, unbounded. A value of +1 is a rise of one
    usual move and -2 a fall of two.
    Warm-up: max(period, vol_period) + 1 + lag rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of rows t - lag - max(period, vol_period) .. t - lag,
    all at or before bar t (the last row of data). Each close is known at its bar's close.

    NaN: a NaN close in those rows gives NaN. A flat return window (s = 0) gives 0.
    Building the component raises for a period below 1, a vol_period below 2, or a lag below 0.
    """

    def __init__(self, name="VolatilityScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 1))
        if self.period < 1:
            raise ValueError(f"VolatilityScaledReturnComponent: period must be >= 1, got {self.period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"VolatilityScaledReturnComponent: vol_period must be >= 2, got {self.vol_period}")
        self.lag = int(self.parameters.get("lag", 0))
        if self.lag < 0:
            raise ValueError(f"VolatilityScaledReturnComponent: lag must be >= 0, got {self.lag}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = max(self.period, self.vol_period) + 1
        close = data["close"].astype(float).to_numpy()
        end = len(close) - self.lag
        win = close[end - n:end]
        if np.isnan(win).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            self.debug_info = {"lag": self.lag, "error": "nan_close"}
            return
        rets = win[1:] / win[:-1] - 1.0
        s = float(np.std(rets[-self.vol_period:], ddof=1))
        move = float(win[-1] / win[-1 - self.period] - 1.0)
        if not s > 0:
            self._raw_value = 0.0
        else:
            self._raw_value = float(move / (s * np.sqrt(self.period)))
        self.confidence = 1.0
        self.debug_info = {"lag": self.lag, "move": move, "usual_move": s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.vol_period) + 1 + self.lag
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 1))
    vp = int(params.get("vol_period", 20))
    lag = int(params.get("lag", 0))
    c = [float(x) for x in list(df["close"])]
    u = len(c) - 1 - lag
    m = p if p > vp else vp
    i = u - m
    while i <= u:
        if c[i] != c[i]:
            return float("nan")
        i = i + 1
    rets = []
    j = u - vp + 1
    while j <= u:
        rets.append(c[j] / c[j - 1] - 1.0)
        j = j + 1
    mean = 0.0
    for r in rets:
        mean = mean + r
    mean = mean / vp
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean) * (r - mean)
    s = math.sqrt(ss / (vp - 1))
    move = c[u] / c[u - p] - 1.0
    if not s > 0:
        return 0.0
    return move / (s * math.sqrt(p))
```

checks:
VolatilityScaledReturnComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1536 passed, 8 skipped, 74 deselected, 2170 warnings in 60.54s (0:01:00) ===
