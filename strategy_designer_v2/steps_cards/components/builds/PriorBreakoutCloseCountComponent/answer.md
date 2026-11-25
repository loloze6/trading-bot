# PriorBreakoutCloseCountComponent: night7_rangefail_run | 033-02.d2_fresh-upside-break-rises_1d | PriorBreakoutCloseCountComponent

## attempt 1

answer: built
class: PriorBreakoutCloseCountComponent
settings: {"window": 20, "period": 20}
reason: No component counts the earlier closes that broke above their prior `period`-close high. `StallUnderHighCountComponent` counts bars just under that high and leaves out the breakouts, and `BarsSinceHighComponent` gives how recent the last new high is, not how many there were. This count is a new measure, read from closes only.

table: Regime measures
row: | `PriorBreakoutCloseCountComponent` | `window` (20), `period` (20) | the number of bars i in t-`window` .. t-1 (bar t excluded) with close[i] > max(close[i-`period`] .. close[i-1]) | 0 to `window` (0 to 20), integers, never negative; no direction; grows by one for each earlier breakout close in the window | regime measure | bars | `window` + `period` + 1 (41) | closes only (bars t-`window`-`period` .. t-1; close[t] is not read). A NaN close in those rows gives NaN. These settings raise when the component is built: `window` < 1, `period` < 1 | stateless. A breakout needs a strictly higher close, so a tie is not a breakout. Bar t is excluded, so bar t's own close cannot add to the count. The value counts the breakout bars of the window, not a consecutive run. It changes by whole steps as breakouts enter or leave the window. No `scaling_factor`: scale it with transforms |

```python class
class PriorBreakoutCloseCountComponent(SubStrategyComponent):
    """
    How many earlier closes broke above their prior closing high, on every bar:

        B(i) = 1 if close[i] > max(close[i-period] .. close[i-1]) else 0   (strictly higher; a tie is not a break)
        raw_value = sum of B(i) over i = t-window .. t-1                    (bar t excluded)

    Range: 0 to window, integers, never negative, no direction. It grows by one for each earlier breakout
    close in the window, so fewer earlier breaks give a smaller value.
    Warm-up: window + period + 1 rows, bar t included (the earliest close read is close[t-window-period]).

    NaN: a NaN close in bars t-window-period .. t-1 gives NaN. close[t] is not read.
    Building the component raises for a window below 1 or a period below 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of rows t-window-period .. t-1, all at or before
    bar t (the last row of data). Each breakout test at bar i uses closes up to bar i only.
    """

    def __init__(self, name="PriorBreakoutCloseCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 20))
        if self.window < 1:
            raise ValueError(f"PriorBreakoutCloseCountComponent: window must be >= 1, got {self.window}")
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"PriorBreakoutCloseCountComponent: period must be >= 1, got {self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()
        t = len(c) - 1
        w, p = self.window, self.period
        seg = c[t - w - p:t]
        if np.isnan(seg).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        count = 0
        for i in range(t - w, t):
            if c[i] > np.max(c[i - p:i]):
                count += 1
        self._raw_value = float(count)
        self.confidence = 1.0
        self.debug_info = {'breakout_count': count, 'window': w, 'period': p}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period + 1
```

```python hand
def hand(df, params):
    w = int(params.get("window", 20))
    p = int(params.get("period", 20))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    # rows read: t-w-p .. t-1
    for k in range(t - w - p, t):
        x = closes[k]
        if x != x:
            return float("nan")
    count = 0
    for i in range(t - w, t):
        highest = closes[i - p]
        for j in range(i - p + 1, i):
            if closes[j] > highest:
                highest = closes[j]
        if closes[i] > highest:
            count = count + 1
    return float(count)
```

checks:
PriorBreakoutCloseCountComponent: every check passed
the bot's suite: == 1658 passed, 16 skipped, 75 deselected, 2244 warnings in 121.51s (0:02:01) ==
