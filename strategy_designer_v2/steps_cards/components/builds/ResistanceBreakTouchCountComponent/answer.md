# ResistanceBreakTouchCountComponent: night3_levels_run | 020-03_resistance-breakout-continues-up_1d | ResistanceBreakTouchCountComponent

## attempt 1

answer: built
class: ResistanceBreakTouchCountComponent
settings: {"period": 90, "side": 2, "band": 2.0, "cross_period": 1}
reason: No catalogue component measures a break above a resistance level. `SwingHighClusterCountComponent` counts touches of the nearest swing-high level still above the close, built on highs; nothing reads the level just crossed below the close, weighted by its touch count and the margin of the break. This new class computes it exactly from closes: the touches of the highest swing-close level the close has crossed within `cross_period` bars, times the percent margin above it.

table: Directional components
row: | `ResistanceBreakTouchCountComponent` | `period` (90), `side` (2), `band` (2.0), `cross_period` (1) | N x (close[t] - L) / L x 100. A swing high is a bar i in t-`period`+1+`side` .. t-`side` whose close[i] is >= each of the `side` closes before it and > each of the `side` closes after it (a fall follows), all inside the window. L = the highest swing-high close with close[t-`cross_period`] <= L < close[t]. N = the number of swing highs with abs(close[i] - L) / L x 100 <= `band`, L's own included. 0 when no swing high satisfies close[t-`cross_period`] <= L < close[t] | 0 and up, unbounded above, never negative; no direction; 0 when no level was crossed upward within `cross_period` bars; grows with the touch count of the crossed level and the close's percent margin above it | graded | touches x percent | max(`period`, `cross_period` + 1) (90) | closes only. A NaN close in the last max(`period`, `cross_period` + 1) rows gives NaN; an L not above 0 gives NaN (never on real bars). These settings raise when the component is built: `side` < 1, `period` < 2 x `side` + 1, `band` not above 0, `cross_period` < 1 | stateless. A swing high is confirmed only `side` bars after it, using bars up to t. Levels are band groups around the crossed swing-high close, so swing highs within `band` of L above or below it count. The value is continuous in close[t] (it nears 0 as the close falls back to L). It drops to 0, or to the reading of a lower level, once close[t-`cross_period`] rises above L: the break is "recent" for `cross_period` bars. No `scaling_factor`: scale it with transforms |

```python class
class ResistanceBreakTouchCountComponent(SubStrategyComponent):
    """
    The touch count of the resistance level the close has just broken, times the margin of the break, on every bar:

        W = close[t - period + 1 .. t]                                  (bar t included)
        swing high: bar i in t - period + 1 + side .. t - side with
                    close[i] >= close[j] for j = i - side .. i - 1 and
                    close[i] >  close[j] for j = i + 1 .. i + side        (all inside W)
        L = the highest swing-high close with close[t - cross_period] <= L < close[t]
        N = the number of swing highs i with abs(close[i] - L) / L x 100 <= band (L's own included)
        raw_value = N x (close[t] - L) / L x 100,   0.0 when no swing high satisfies the crossing condition

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 when no level was crossed upward
    within the last cross_period bars, and it grows with the level's touch count and with the close's percent
    distance above it.
    Warm-up: max(period, cross_period + 1) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, cross_period + 1) rows of data,
    bar t (the last row) included. A swing high at bar i is confirmed by the closes of bars i+1 .. i+side, which all
    lie at or before bar t.

    NaN: a NaN close in the last max(period, cross_period + 1) rows gives NaN. An L not above 0 gives NaN (never on
    real bars). A missing `close` column raises.
    Building the component raises for a side below 1, a period below 2 x side + 1, a band not above 0, or a
    cross_period below 1.
    """

    def __init__(self, name="ResistanceBreakTouchCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        self.band = float(self.parameters.get("band", 2.0))
        self.cross_period = int(self.parameters.get("cross_period", 1))
        if self.side < 1:
            raise ValueError(f"ResistanceBreakTouchCountComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"ResistanceBreakTouchCountComponent: period must be >= 2 x side + 1, got {self.period}")
        if not self.band > 0:
            raise ValueError(f"ResistanceBreakTouchCountComponent: band must be above 0, got {self.band}")
        if self.cross_period < 1:
            raise ValueError(
                f"ResistanceBreakTouchCountComponent: cross_period must be >= 1, got {self.cross_period}")
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
        w = c[-self.period:]
        s = self.side
        highs = []
        for k in range(s, self.period - s):
            v = w[k]
            if np.all(v >= w[k - s:k]) and np.all(v > w[k + 1:k + s + 1]):
                highs.append(float(v))
        c_now = float(c[-1])
        c_before = float(c[-1 - self.cross_period])
        crossed = [h for h in highs if c_before <= h < c_now]
        if not crossed:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {'swing_highs': len(highs), 'level': None, 'touches': 0}
            return
        level = max(crossed)
        if not level > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        touches = sum(1 for h in highs if abs(h - level) / level * 100.0 <= self.band)
        self._raw_value = float(touches * (c_now - level) / level * 100.0)
        self.confidence = 1.0
        self.debug_info = {'swing_highs': len(highs), 'level': level, 'touches': touches}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.cross_period + 1)
```

```python hand
def hand(df, params):
    period = int(params.get("period", 90))
    side = int(params.get("side", 2))
    band = float(params.get("band", 2.0))
    cross = int(params.get("cross_period", 1))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    need = max(period, cross + 1)
    j = t - need + 1
    while j <= t:
        if closes[j] != closes[j]:
            return float("nan")
        j = j + 1
    first = t - period + 1
    swing = []
    i = first + side
    while i <= t - side:
        ok = True
        j = i - side
        while j < i:
            if not closes[i] >= closes[j]:
                ok = False
            j = j + 1
        j = i + 1
        while j <= i + side:
            if not closes[i] > closes[j]:
                ok = False
            j = j + 1
        if ok:
            swing.append(closes[i])
        i = i + 1
    now = closes[t]
    before = closes[t - cross]
    level = None
    for h in swing:
        if before <= h and h < now:
            if level is None or h > level:
                level = h
    if level is None:
        return 0.0
    if not level > 0:
        return float("nan")
    count = 0
    for h in swing:
        if abs(h - level) / level * 100.0 <= band:
            count = count + 1
    return count * (now - level) / level * 100.0
```

checks:
ResistanceBreakTouchCountComponent: every check passed
the bot's suite: ======= 1582 passed, 16 skipped, 75 deselected, 2244 warnings in 54.84s ========
