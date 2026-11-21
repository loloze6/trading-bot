# TouchWeightedSupportBreakDepthComponent: night3_levels_run | 020-04_support-breakdown-continues-down_1d | HeldLevelBreakDepth

## attempt 1

answer: built
class: TouchWeightedSupportBreakDepthComponent
settings: {"period": 90, "side": 2, "band": 2.0}
reason: No component gives the percent depth of the close under a support level weighted by that level's touch count. `SwingHighClusterCountComponent` (`pivot` "low", `level` "above", `exclude_current` 1) picks the nearest level rather than the most-touched one, and its "proximity" form shrinks as the close moves away, so it never measures the break's depth. One new class computes the count times the depth, choosing the most-touched swing-low level of bars t-90 .. t-1 among those the close sits at or under.

table: Directional components
row: | `TouchWeightedSupportBreakDepthComponent` | `period` (90), `side` (2), `band` (2.0) | N x (L - close[t]) / L x 100. W = bars t-`period` .. t-1 (bar t excluded). A swing low is a bar i of W with `side` bars of W before it and `side` after it, so i runs t-`period`+`side` .. t-1-`side`, whose low[i] is strictly below the low of each of those bars. For each swing low j, N_j = the number of swing lows i with abs(low[i] - low[j]) / low[j] x 100 <= `band`, j's own included. L = low[j] of the swing low with the largest N_j among those with low[j] >= close[t]; on a tie, the lowest such low[j] (the one nearest the close). N = that N_j. 0 when no swing low is at or above close[t] | 0 and up, never negative, below N x 100; no direction; 0 when the close is above every swing low of W; grows with the close's percent depth under the level and with the level's touch count | graded | touches x percent | `period` + 1 (91) | low (bars t-`period` .. t-1), close (bar t). A NaN low in W or a NaN close[t] gives NaN; an L not above 0 gives NaN (never on real bars). These settings raise when the component is built: `side` < 1, `period` < 2 x `side` + 1, `band` not above 0 | stateless. Bar t's own low cannot make or confirm a swing low. A swing low is confirmed only `side` bars after it, inside W. Ties do not count (strictly lower), so a flat bottom counts none of its bars. The band is in percent of the candidate level, and swing lows within it above or below the level both count. Continuous in close[t] while the chosen level stays the same: it is 0 at the level and grows as the close falls under it. It jumps where the close crosses another swing low and the choice of level changes. No `scaling_factor`: scale it with transforms |

```python class
class TouchWeightedSupportBreakDepthComponent(SubStrategyComponent):
    """
    How far the close sits under the most-touched support level of the prior bars, weighted by that level's
    touch count:

        W = bars t-period .. t-1                                   (bar t excluded)
        swing low: bar i of W, i in t-period+side .. t-1-side, with low[i] < low[i-k] and low[i] < low[i+k]
                   for k = 1 .. side (strictly lower; all those bars inside W)
        N_j = #{swing lows i : abs(low[i] - low[j]) / low[j] x 100 <= band}   (j's own included)
        candidates = swing lows j with low[j] >= close[t]
        L = low[j] of the candidate with the largest N_j (a tie goes to the lowest low[j]); N = that N_j
        raw_value = N x (L - close[t]) / L x 100, or 0.0 when there is no candidate

    Range: 0 and up, never negative, below N x 100. It has no direction. It is 0 when the close is above every
    swing low of W, and it grows with the close's percent depth under the level and with the level's touch count.
    Graded: continuous in close[t] while the chosen level stays the same, and 0 at the level itself. It jumps where
    the close crosses another swing low.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads the `low` column of bars t-period .. t-1 and the `close` of bar t (the last row
    of data), nothing later; a swing low is confirmed only by the side bars after it inside W, all before bar t.

    NaN: a NaN low in W or a NaN close[t] gives NaN; a candidate level not above 0 gives NaN (never on real bars).
    Building the component raises for a side below 1, a period below 2 x side + 1, or a band not above 0.
    """

    def __init__(self, name="TouchWeightedSupportBreakDepth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        self.band = float(self.parameters.get("band", 2.0))
        if self.side < 1:
            raise ValueError(f"TouchWeightedSupportBreakDepthComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"TouchWeightedSupportBreakDepthComponent: period must be >= 2 x side + 1, got {self.period}")
        if not self.band > 0:
            raise ValueError(f"TouchWeightedSupportBreakDepthComponent: band must be above 0, got {self.band}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.period
        lows = data['low'].astype(float).to_numpy()[-(n + 1):-1]
        c = float(data['close'].astype(float).iloc[-1])
        self.confidence = 1.0
        if np.isnan(lows).any() or np.isnan(c):
            self._raw_value = float("nan")
            return
        swings = []
        for i in range(self.side, n - self.side):
            v = lows[i]
            ok = True
            for k in range(1, self.side + 1):
                if not (v < lows[i - k] and v < lows[i + k]):
                    ok = False
                    break
            if ok:
                swings.append(float(v))
        best_n = 0
        best_level = None
        for level in swings:
            if level < c:
                continue
            if not level > 0:
                self._raw_value = float("nan")
                return
            cnt = sum(1 for p in swings if abs(p - level) / level * 100.0 <= self.band)
            if cnt > best_n or (cnt == best_n and best_level is not None and level < best_level):
                best_n = cnt
                best_level = level
        if best_level is None:
            self._raw_value = 0.0
        else:
            self._raw_value = float(best_n * (best_level - c) / best_level * 100.0)
        self.debug_info = {'level': best_level, 'touches': best_n, 'swing_lows': len(swings)}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    period = int(params.get("period", 90))
    side = int(params.get("side", 2))
    band = float(params.get("band", 2.0))
    low = [float(x) for x in list(df["low"])]
    close = [float(x) for x in list(df["close"])]
    t = len(close) - 1
    c = close[t]
    if c != c:
        return float("nan")
    first = t - period
    for i in range(first, t):
        if low[i] != low[i]:
            return float("nan")
    levels = []
    i = first + side
    while i <= t - 1 - side:
        is_swing = True
        for k in range(1, side + 1):
            if not low[i] < low[i - k]:
                is_swing = False
            if not low[i] < low[i + k]:
                is_swing = False
        if is_swing:
            levels.append(low[i])
        i = i + 1
    chosen = None
    chosen_count = 0
    for lv in levels:
        if not lv >= c:
            continue
        if not lv > 0:
            return float("nan")
        count = 0
        for other in levels:
            if abs(other - lv) / lv * 100.0 <= band:
                count = count + 1
        if chosen is None or count > chosen_count or (count == chosen_count and lv < chosen):
            chosen = lv
            chosen_count = count
    if chosen is None:
        return 0.0
    return chosen_count * (chosen - c) / chosen * 100.0
```

checks:
TouchWeightedSupportBreakDepthComponent: every check passed
the bot's suite: ======= 1583 passed, 16 skipped, 75 deselected, 2244 warnings in 52.96s ========
