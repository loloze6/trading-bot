# PriorDownRunOnUpCloseComponent: night8_risingagitated_run | 068-02_falling-agitated-run-break-fade_1d | PriorDownRunOnUpCloseComponent

## attempt 1

answer: built
class: PriorDownRunOnUpCloseComponent
settings: {"max_bars": 30}
reason: No component gives this. `UpCloseStreakLengthComponent` with `side` "down" counts the run ending at bar t, so it reads 0 on an up bar. A `lag` on it would still count the run on down bars, and no config step adds the gate "bar t closed up". This is a measure of its own: the length of the down run that bar t's higher close has just ended. It needs one new class, with a cap that only bounds runs real daily bars do not show.

table: Regime measures
row: | `PriorDownRunOnUpCloseComponent` | `max_bars` (30) | when close[t] > close[t-1]: min(n, `max_bars`), n = the number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1]; 0 when close[t] <= close[t-1] | 0 to `max_bars` (0 to 30), integers, never negative; no direction; 0 on down and flat bars and on an up bar that follows an up or flat bar; grows by one with each further down bar in the run that bar t breaks | regime measure | bars | `max_bars` + 2 (32) | closes only. A NaN close in the last `max_bars` + 2 rows gives NaN. These settings raise when the component is built: `max_bars` < 1 | stateless. A flat bar (equal close) ends the down run and does not count as the bounce. The value is nonzero only on the first up close after a down run, and it is 0 again on the next bar. It jumps, so it belongs in regime rules, not as a forecast source. Not `UpCloseStreakLengthComponent` (`side` "down"), which is 0 on every up bar. The cap binds only on a down run longer than `max_bars` bars, which real 1d bars do not show. No `scaling_factor`: scale it with transforms |

```python class
class PriorDownRunOnUpCloseComponent(SubStrategyComponent):
    """
    Length of the down run that bar t's up close has just ended:

        if close[t] > close[t-1]:
            n = number of consecutive bars i = t-1, t-2, ... with close[i] < close[i-1], capped at max_bars
            raw_value = n
        else:
            raw_value = 0

    Range: 0 to max_bars, integers, never negative, no direction. It is 0 on a down or flat bar t, and 0 on an
    up bar whose previous bar was not a down bar. A flat bar (equal close) ends the down run.
    Warm-up: max_bars + 2 rows, bar t included.
    NaN: a NaN close in the last max_bars + 2 rows gives NaN.
    Building the component raises for a max_bars below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max_bars + 2 rows of data, which end at
    bar t (the last row); a bar's close is known at that bar's close.
    """

    def __init__(self, name="PriorDownRunOnUpClose", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(f"PriorDownRunOnUpCloseComponent: max_bars must be >= 1, got {self.max_bars}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()[-self.get_required_periods():]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = 0
        if c[-1] > c[-2]:
            i = len(c) - 2
            while n < self.max_bars and c[i] < c[i - 1]:
                n += 1
                i -= 1
        self._raw_value = float(n)
        self.confidence = 1.0
        self.debug_info = {'prior_down_run': n, 'up_close': bool(c[-1] > c[-2])}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.max_bars + 2
```

```python hand
def hand(df, params):
    cap = int(params.get("max_bars", 30))
    close = [float(x) for x in list(df["close"])]
    t = len(close) - 1
    # rows read: t-cap-1 .. t
    for k in range(cap + 2):
        x = close[t - k]
        if x != x:
            return float("nan")
    # bar t must close strictly above bar t-1
    if not (close[t] > close[t - 1]):
        return 0.0
    # count the down bars going back from t-1
    count = 0
    j = t - 1
    while count < cap:
        if close[j] < close[j - 1]:
            count = count + 1
            j = j - 1
        else:
            break
    return float(count)
```

checks:
PriorDownRunOnUpCloseComponent: every check passed
the bot's suite: == 1670 passed, 16 skipped, 75 deselected, 2244 warnings in 119.46s (0:01:59) ==
