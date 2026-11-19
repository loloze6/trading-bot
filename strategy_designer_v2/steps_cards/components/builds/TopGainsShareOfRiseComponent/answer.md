# TopGainsShareOfRiseComponent: slow_1h_run | 016-01_up-grind-price-continuation_1h | GrindShareOfRise

## attempt 1

answer: built
class: TopGainsShareOfRiseComponent
settings: {"period": 72, "k": 3, "form": "residual"}
reason: `TopGainsShareOfRiseComponent` already computes this measure, min(T / R, 1) over a rising window, and the wish asks for its mirror. That mirror is 1 - min(T / R, 1) while the window rose and 0 otherwise. No config step gives 1 minus a value, so the measure becomes a `form` setting on the same class; its default "share" keeps today's output exactly. `RiseBeyondLargestMovesComponent` is a different measure: it is that residual times the log rise, in log units.

table: Regime measures
row: | `TopGainsShareOfRiseComponent` | `period` (72), `k` (3), `form` ("share") | R = close[t] / close[t-`period`] - 1 is the net simple rise. T is the sum of the `k` largest positive one-bar returns close[j] / close[j-1] - 1, j = t-`period`+1 .. t (all the positive ones if there are fewer than `k`). "share": min(T / R, 1) when R > 0, else 0. "residual": 1 - min(T / R, 1) when R > 0, else 0 | "share": 0 to 1, never negative, no direction. It is near 0 when the rise is a grind of many small up-bars, 1 when the `k` largest up-bars carry all of the rise or more, and 0 when the window did not rise. "residual": 0 to below 1, never negative, no direction. It is 0 when the window did not rise or when its `k` largest up-bars carry all of the rise, and it nears 1 as the rise spreads over many small up-bars | graded | dimensionless (share of the net rise) | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN. A close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `k` >= `period`, `form` other than "share" or "residual" | stateless. `form` "share" (default) is the original output, unchanged. "share" jumps from 1 to 0 where the net return crosses 0. "residual" is 1 minus "share" while the window rose and 0 otherwise. No config step gives 1 minus a value, hence the setting. "residual" is continuous at R = 0, because a tiny positive rise caps T / R at 1. Simple returns, not log returns. Not `RiseBeyondLargestMovesComponent`, which is the residual log rise in log units. No `scaling_factor`: scale it with transforms |

```python class
class TopGainsShareOfRiseComponent(SubStrategyComponent):
    """
    How much of the window's net rise its few largest up-bars carry, on every bar:

        R = close[t] / close[t - period] - 1                       (net simple rise)
        r[j] = close[j] / close[j - 1] - 1,  j = t - period + 1 .. t
        T = sum of the k largest r[j] > 0 (all the positive ones if there are fewer than k)
        share = min(T / R, 1) if R > 0 else 0
        form = "share" (default): raw_value = share
        form = "residual":        raw_value = 1 - share if R > 0 else 0

    The default "share" is the original output, unchanged. It runs 0 to 1, never negative, with no direction.
    It is near 0 for a grind of many small up-bars, 1 when the k largest up-bars carry the whole rise or more,
    and 0 when the window did not rise.
    "residual" runs 0 to below 1, never negative, with no direction. A rise needs at least one positive
    return, so T > 0. It is 0 when the window did not rise or when the top k up-bars carry the whole rise, and
    it grows towards 1 as the rise is spread over many small up-bars. It is continuous in the closes,
    including where R crosses 0.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data, bar t (the
    last row) included; a bar's close is known at that bar's close.

    NaN: a NaN close in the last period + 1 rows gives NaN. A close not above 0 there gives NaN (never on real
    bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, a k >= period, or a form other than
    "share" or "residual".
    """

    def __init__(self, name="TopGainsShareOfRise", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopGainsShareOfRiseComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1:
            raise ValueError(f"TopGainsShareOfRiseComponent: k must be >= 1, got {self.k}")
        if self.k >= self.period:
            raise ValueError(
                f"TopGainsShareOfRiseComponent: k must be below period, got k={self.k}, period={self.period}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "residual"):
            raise ValueError(
                f"TopGainsShareOfRiseComponent: form must be 'share' or 'residual', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rise = float(c[-1] / c[0] - 1.0)
        rets = c[1:] / c[:-1] - 1.0
        pos = np.sort(rets[rets > 0])[::-1][:self.k]
        top = float(pos.sum()) if pos.size else 0.0
        if rise > 0:
            share = min(top / rise, 1.0)
            value = share if self.form == "share" else 1.0 - share
        else:
            share = 0.0
            value = 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'net_rise': rise, 'top_gains': top, 'share': share, 'form': self.form}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
    form = params.get("form", "share")
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    window = []
    i = last - n
    while i <= last:
        window.append(c[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
        if not x > 0:
            return float("nan")
    rise = window[-1] / window[0] - 1.0
    gains = []
    j = 1
    while j < len(window):
        r = window[j] / window[j - 1] - 1.0
        if r > 0:
            gains.append(r)
        j = j + 1
    gains.sort(reverse=True)
    top = 0.0
    m = 0
    while m < k and m < len(gains):
        top = top + gains[m]
        m = m + 1
    if not rise > 0:
        return 0.0
    share = top / rise
    if share > 1.0:
        share = 1.0
    if form == "residual":
        return 1.0 - share
    return share
```

checks:
TopGainsShareOfRiseComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1559 passed, 8 skipped, 74 deselected, 2244 warnings in 56.27s ========
