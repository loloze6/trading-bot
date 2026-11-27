# PriorDownRunOnUpCloseComponent: night9_fallcalmfade_run | 074-01.b1.d1.g1_falling-market-rally-break-rebound_1d | PriorUpRunOnDownCloseComponent

## attempt 1

answer: built
class: PriorDownRunOnUpCloseComponent
settings: {"side": "up"}
reason: The wished count of the up run that a down close breaks is the mirror side of `PriorDownRunOnUpCloseComponent`. `negate` on its "down" count does not give it, and `PriorDownRunLossOnUpCloseComponent` "up" gives the run's gain, not its length, so the class is written again with a `side` setting whose default "down" keeps today's output.

table: Regime measures
row: | `PriorDownRunOnUpCloseComponent` | `max_bars` (30), `form` ("count"), `side` ("down") | `side` "down": when close[t] > close[t-1], m = min(n, `max_bars`), n = the number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1]; 0 when close[t] <= close[t-1]. `side` "up": when close[t] < close[t-1], m = min(n, `max_bars`), n = the number of consecutive bars i ending at t-1 with close[i] > close[i-1]; 0 when close[t] >= close[t-1]. `form` "count": m; `form` "beyond_first": max(0, m − 1) | "count": 0 to `max_bars` (0 to 30), integers. "beyond_first": 0 to `max_bars` − 1 (0 to 29), integers. Never negative; no direction. "down" is 0 on down and flat bars and on an up bar that follows an up or flat bar. "up" is 0 on up and flat bars and on a down bar that follows a down or flat bar. Both grow by one with each further bar in the run that bar t breaks | regime measure | bars | `max_bars` + 2 (32) | closes only. A NaN close in the last `max_bars` + 2 rows gives NaN. These settings raise when the component is built: `max_bars` < 1, `form` other than "count" or "beyond_first", `side` other than "down" or "up" | stateless. `side` "down" (default) with either `form` is the original output, unchanged. "up" counts the up days of the run that a down close breaks; `negate` on "down" is not it, and no config step gives it, hence the setting. A flat bar (equal close) ends either run and does not count as the break. The value is nonzero only on the first close that breaks a run and is 0 again on the next bar, so it jumps. A forecast use that scales it on breaking bars only is a config matter. The cap binds only on a run longer than `max_bars` bars, which real 1d bars do not show. No `scaling_factor`: scale it with transforms |

```python class
class PriorDownRunOnUpCloseComponent(SubStrategyComponent):
    """
    Length of the run that bar t's close breaks, on every bar:

        side = "down" (default): when close[t] > close[t-1],
            n = number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1]
        side = "up": when close[t] < close[t-1],
            n = number of consecutive bars i ending at t-1 with close[i] > close[i-1]
        m = min(n, max_bars); 0 when bar t does not close to the breaking side
        form = "count" (default): raw_value = m
        form = "beyond_first":    raw_value = max(0, m - 1)

    Range: integers 0 .. max_bars ("count") or 0 .. max_bars - 1 ("beyond_first"), never negative, no direction.
    It grows by one with each further bar in the broken run. A flat bar ends either run and is not a break.
    side "down" (default) with either form is the original output, unchanged.
    Warm-up: max_bars + 2 rows, bar t included.

    NaN: a NaN close anywhere in the last max_bars + 2 rows gives NaN.
    Building the component raises for max_bars < 1, a form other than "count" or "beyond_first",
    or a side other than "down" or "up".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max_bars + 2 rows of data, ending at
    bar t (the last row); a close is known at that bar's close.
    """

    def __init__(self, name="PriorRunOnBreakClose", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(f"PriorDownRunOnUpCloseComponent: max_bars must be >= 1, got {self.max_bars}")
        self.form = self.parameters.get("form", "count")
        if self.form not in ("count", "beyond_first"):
            raise ValueError(
                f"PriorDownRunOnUpCloseComponent: form must be 'count' or 'beyond_first', got {self.form!r}")
        self.side = self.parameters.get("side", "down")
        if self.side not in ("down", "up"):
            raise ValueError(f"PriorDownRunOnUpCloseComponent: side must be 'down' or 'up', got {self.side!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).iloc[-(self.max_bars + 2):].to_numpy()
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            self.debug_info = {'nan': True}
            return
        t = len(c) - 1
        if self.side == "down":
            breaks = c[t] > c[t - 1]
        else:
            breaks = c[t] < c[t - 1]
        n = 0
        if breaks:
            i = t - 1
            while i >= 1 and n < self.max_bars:
                moved = (c[i] < c[i - 1]) if self.side == "down" else (c[i] > c[i - 1])
                if not moved:
                    break
                n += 1
                i -= 1
        m = n
        if self.form == "beyond_first":
            m = max(0, m - 1)
        self._raw_value = float(m)
        self.confidence = 1.0
        self.debug_info = {'run_length': n, 'side': self.side, 'form': self.form}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.max_bars + 2
```

```python hand
def hand(df, params):
    max_bars = int(params.get("max_bars", 30))
    form = params.get("form", "count")
    side = params.get("side", "down")
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    # NaN anywhere in the last max_bars + 2 rows gives NaN
    for k in range(max_bars + 2):
        x = closes[t - k]
        if x != x:
            return float("nan")
    # does bar t break a run to the counted side?
    if side == "up":
        if not closes[t] < closes[t - 1]:
            return 0.0
    else:
        if not closes[t] > closes[t - 1]:
            return 0.0
    # length of the run of moving bars ending at t-1
    n = 0
    i = t - 1
    while True:
        if n == max_bars:
            break
        if side == "up":
            moved = closes[i] > closes[i - 1]
        else:
            moved = closes[i] < closes[i - 1]
        if not moved:
            break
        n = n + 1
        i = i - 1
    if form == "beyond_first":
        if n - 1 > 0:
            return float(n - 1)
        return 0.0
    return float(n)
```

checks:
PriorDownRunOnUpCloseComponent: every check passed
the bot's suite: == 1678 passed, 16 skipped, 75 deselected, 2244 warnings in 152.87s (0:02:32) ==
