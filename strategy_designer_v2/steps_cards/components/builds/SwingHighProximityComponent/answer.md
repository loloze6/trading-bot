# SwingHighProximityComponent: night3_levels_run | 020-01_resistance-retest-turns-down_1d | TurnDownLevelProximity

## attempt 1

answer: built
class: SwingHighProximityComponent
settings: {"period": 90, "side": 2, "power": 1.0}
reason: No catalogued class finds swing highs. `DistanceFromHighComponent` only measures the distance from the highest value of its window, not from the nearest pivot level above the close. This new class takes the lowest swing-high price at or above close[t] and measures the close's proximity to it as (1 / (1 + percent gap))^power.

table: Regime measures
row: | `SwingHighProximityComponent` | `period` (90), `side` (2), `power` (1.0) | (1 / (1 + D))^`power`, D = (L - close[t]) / L x 100, L = the lowest swing-high price at or above close[t]. A swing high is a bar i of the last `period` bars (bar t included) whose high[i] is >= the high of each of the `side` bars before it and the `side` bars after it, all of them inside the window, so i runs t-`period`+1+`side` .. t-`side`. Its price is high[i]. The output is 0 when no swing high sits at or above close[t] | 0 to 1, never negative; no direction. It is above 0 and up to 1 when a level exists above the close: it nears 1 as the close rises to the level from below, and is 1 when the close equals it. It is 0 when no swing high is at or above the close | graded | dimensionless (proximity, 0 to 1) | `period` (90) | high (last `period` rows), close (bar t). A NaN high in the window or a NaN close[t] gives NaN; an L not above 0 gives NaN (never on real bars). These settings raise when the component is built: `side` < 1, `period` < 2 x `side` + 1, `power` not above 0 | stateless. A swing high is confirmed only `side` bars after it, using bars up to t. Ties count (>=). The output jumps where the close crosses a level: it goes from 1 to the proximity of the next level up, or to 0 if no level is above. No `scaling_factor`: scale it with transforms |

```python class
class SwingHighProximityComponent(SubStrategyComponent):
    """
    How near the close sits below the nearest swing-high level above it, on every bar:

        W = rows t - period + 1 .. t                                      (bar t included)
        swing high: a bar i of W with i - side and i + side inside W (i = t-period+1+side .. t-side)
                    and high[i] >= high[j] for every j in i-side .. i+side, j != i
        levels = { high[i] : i a swing high }
        A = { L in levels : L >= close[t] }
        A empty:     raw_value = 0.0
        otherwise:   L = min(A), D = (L - close[t]) / L x 100,
                     raw_value = (1 / (1 + D)) ** power

    Range 0 to 1, never negative, no direction. The value is above 0 and up to 1 when a level exists at or above
    the close, nearing 1 as the close rises to that level from below (1 when the close equals it). It is 0 when no
    swing high in the window is at or above the close. Graded in the gap; the value jumps when the close crosses a
    level (to the next level up, or to 0).
    Warm-up: period rows, bar t included.

    WHY THIS CANNOT LEAK: it reads the `high` column of the last `period` rows of data (bar t the last row) and
    close[t]; a swing high at bar i is confirmed with highs up to i + side <= t, so no row after t is read.

    NaN: a NaN high in the window or a NaN close[t] gives NaN; a level L not above 0 gives NaN (never on real bars).
    Building the component raises for side < 1, period < 2 x side + 1, or power not above 0.
    """

    def __init__(self, name="SwingHighProximity", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        self.power = float(self.parameters.get("power", 1.0))
        if self.side < 1:
            raise ValueError(f"SwingHighProximityComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"SwingHighProximityComponent: period must be >= 2 x side + 1, got {self.period}")
        if not self.power > 0:
            raise ValueError(f"SwingHighProximityComponent: power must be above 0, got {self.power}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        highs = data['high'].astype(float).iloc[-self.period:].to_numpy()
        c = float(data['close'].astype(float).iloc[-1])
        if np.isnan(highs).any() or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = len(highs)
        s = self.side
        levels = []
        for j in range(s, n - s):
            neigh = np.concatenate([highs[j - s:j], highs[j + 1:j + s + 1]])
            if highs[j] >= neigh.max():
                levels.append(float(highs[j]))
        above = [lv for lv in levels if lv >= c]
        if not above:
            value = 0.0
            level = float("nan")
        else:
            level = min(above)
            if not level > 0:
                value = float("nan")
            else:
                d = (level - c) / level * 100.0
                value = float((1.0 / (1.0 + d)) ** self.power)
        self._raw_value = value
        self.confidence = 1.0
        self.debug_info = {'level': level, 'n_swing_highs': len(levels), 'close': c}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period
```

```python hand
def hand(df, params):
    n = int(params.get("period", 90))
    s = int(params.get("side", 2))
    p = float(params.get("power", 1.0))
    h_all = [float(x) for x in list(df["high"])]
    c_all = [float(x) for x in list(df["close"])]
    h = h_all[len(h_all) - n:]
    c = c_all[len(c_all) - 1]
    for x in h:
        if x != x:
            return float("nan")
    if c != c:
        return float("nan")
    levels = []
    i = s
    while i <= n - 1 - s:
        ok = True
        j = i - s
        while j <= i + s:
            if j != i and h[j] > h[i]:
                ok = False
            j = j + 1
        if ok:
            levels.append(h[i])
        i = i + 1
    best = None
    for lv in levels:
        if lv >= c:
            if best is None or lv < best:
                best = lv
    if best is None:
        return 0.0
    if not best > 0:
        return float("nan")
    gap = (best - c) / best * 100.0
    return (1.0 / (1.0 + gap)) ** p
```

checks:
SwingHighProximityComponent: every check passed
the bot's suite: ======= 1579 passed, 16 skipped, 75 deselected, 2244 warnings in 57.59s ========
