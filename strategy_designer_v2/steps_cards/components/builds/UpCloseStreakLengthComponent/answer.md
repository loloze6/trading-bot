# UpCloseStreakLengthComponent: night6_streak_run | 031-04_down-streak-length-continuation_1d | DownStreakLengthComponent

## attempt 1

answer: built
class: UpCloseStreakLengthComponent
settings: {"side": "down"}
reason: No component gives the length of a down-close streak. `UpCloseStreakLengthComponent` counts the same quantity, a run of consecutive closes on one side, but only for higher closes; `negate` does not give a down-streak count, and `DownStreakLossInUsualMovesComponent` measures the streak's loss in usual moves, not its length. So the measure is a new `side` setting on the streak-length class, and its default "up" keeps today's output.

table: Regime measures
row: | `UpCloseStreakLengthComponent` | `max_bars` (30), `base` ("none"), `base_window` (365), `side` ("up") | A bar i "moves" when close[i] > close[i-1] (`side` "up") or close[i] < close[i-1] (`side` "down"). n = the number of consecutive moving bars ending at t (bar t included), capped at `max_bars`; n is 0 when bar t did not move. A completed streak is a maximal run of moving bars lying in bars t-`base_window`+1 .. t. It counts when the bar before its first bar is in that window and did not move, and the bar after its last bar is at or before t and did not move, so the open streak ending at t is excluded. K is the number of completed streaks; their lengths are uncapped. `base` "none": n. `base` "mean_streak": n / M, M = the mean length of the completed streaks. `base` "rank": (number of completed streaks with length <= n) / K. Every base gives 0 when n = 0 | "none": 0 to `max_bars`, integers, never negative; no direction. "mean_streak": 0 and up, at most `max_bars`, never negative; 1 when the current streak is as long as the usual completed streak. "rank": 0 to 1 in steps of 1/K, never negative | regime measure | "none": bars. "mean_streak": multiples of the mean completed streak length. "rank": share of completed streaks | `max_bars` + 1 (31) with "none"; max(`max_bars`, `base_window`) + 1 (366) with "mean_streak" or "rank" | Closes only. A NaN close in the last (warmup) rows gives NaN. With "mean_streak" or "rank", a window with no completed streak gives NaN while n > 0 (never on real bars). These settings raise when the component is built: `max_bars` < 1, `base` other than "none", "mean_streak" or "rank", `base_window` < 3, `side` other than "up" or "down" | Stateless. `side` "up" (default) is the original output, unchanged. "down" counts the run of lower closes; no config step gives it, because `negate` on "up" is not it, hence the setting. A flat bar (equal close) ends either streak. The cap binds only on a streak longer than `max_bars` bars, which real 1d bars do not show. The value drops to 0 on the first bar that does not move to the counted side. No `scaling_factor`: scale it with transforms |

```python class
class UpCloseStreakLengthComponent(SubStrategyComponent):
    """
    Length of the current streak of closes on one side, optionally against the coin's completed streaks.

        moved(i) = close[i] > close[i-1]   (side "up", default)
        moved(i) = close[i] < close[i-1]   (side "down")
        n = number of consecutive bars i ending at t (bar t included) with moved(i), capped at max_bars;
            n = 0 when bar t did not move to the counted side.
        A completed streak is a maximal run of moved bars inside bars t-base_window+1 .. t. It counts when
        the bar before its first bar is inside that window and did not move, and the bar after its last bar
        is at or before t and did not move, so the open streak ending at t is excluded. K is the number of
        completed streaks; their lengths are uncapped.
        base "none" (default):  raw_value = n
        base "mean_streak":     raw_value = n / mean(completed lengths)
        base "rank":            raw_value = (number of completed lengths <= n) / K
        Every base gives 0 when n = 0.

    Range: "none" 0 .. max_bars, integers; "mean_streak" 0 .. max_bars; "rank" 0 .. 1. Never negative, no direction.
    side "up" with any base is the original output, unchanged. "down" is the run of lower closes.
    A flat bar ends either streak.
    Warm-up: max_bars + 1 rows with "none"; max(max_bars, base_window) + 1 rows with "mean_streak" or "rank".
    NaN: a NaN close in those rows gives NaN. With "mean_streak" or "rank", no completed streak while n > 0
    gives NaN (never on real bars).
    Building the component raises for max_bars < 1, an unknown base, base_window < 3, or a side other than
    "up" or "down".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last (warm-up) rows of data, the last row
    being bar t; no row after t exists in the data it is given.
    """

    def __init__(self, name="Close streak length", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(f"UpCloseStreakLengthComponent: max_bars must be >= 1, got {self.max_bars}")
        self.base = self.parameters.get("base", "none")
        if self.base not in ("none", "mean_streak", "rank"):
            raise ValueError(
                f"UpCloseStreakLengthComponent: base must be 'none', 'mean_streak' or 'rank', got {self.base!r}")
        self.base_window = int(self.parameters.get("base_window", 365))
        if self.base_window < 3:
            raise ValueError(f"UpCloseStreakLengthComponent: base_window must be >= 3, got {self.base_window}")
        self.side = self.parameters.get("side", "up")
        if self.side not in ("up", "down"):
            raise ValueError(f"UpCloseStreakLengthComponent: side must be 'up' or 'down', got {self.side!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        self.confidence = 1.0
        if np.isnan(c).any():
            self._raw_value = float("nan")
            return
        if self.side == "up":
            moved = c[1:] > c[:-1]
        else:
            moved = c[1:] < c[:-1]
        # moved[k] is the move of bar (k+1) of c; moved[-1] is bar t
        n = 0
        k = len(moved) - 1
        while n < self.max_bars and k >= 0 and moved[k]:
            n += 1
            k -= 1
        if self.base == "none":
            self._raw_value = float(n)
            self.debug_info = {'n': n, 'side': self.side}
            return
        if n == 0:
            self._raw_value = 0.0
            self.debug_info = {'n': 0, 'side': self.side}
            return
        w = moved[-self.base_window:]
        m = len(w)
        lengths = []
        a = 0
        while a < m:
            if w[a]:
                b = a
                while b + 1 < m and w[b + 1]:
                    b += 1
                if a >= 1 and b + 1 <= m - 1:
                    lengths.append(b - a + 1)
                a = b + 1
            else:
                a += 1
        if len(lengths) == 0:
            self._raw_value = float("nan")
            return
        lengths = np.asarray(lengths, dtype=float)
        if self.base == "mean_streak":
            self._raw_value = float(n / lengths.mean())
        else:
            self._raw_value = float(np.sum(lengths <= n) / len(lengths))
        self.debug_info = {'n': n, 'side': self.side, 'completed_streaks': int(len(lengths))}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "none":
            return self.max_bars + 1
        return max(self.max_bars, self.base_window) + 1
```

```python hand
def hand(df, params):
    mb = int(params.get("max_bars", 30))
    base = params.get("base", "none")
    bw = int(params.get("base_window", 365))
    side = params.get("side", "up")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    if base == "none":
        need = mb + 1
    else:
        need = max(mb, bw) + 1
    for i in range(t - need + 1, t + 1):
        if c[i] != c[i]:
            return float("nan")

    def mv(i):
        if side == "up":
            return c[i] > c[i - 1]
        return c[i] < c[i - 1]

    n = 0
    i = t
    while n < mb and mv(i):
        n = n + 1
        i = i - 1
    if base == "none":
        return float(n)
    if n == 0:
        return 0.0
    lo = t - bw + 1
    lengths = []
    i = lo
    while i <= t:
        if mv(i):
            j = i
            while j + 1 <= t and mv(j + 1):
                j = j + 1
            before_ok = (i - 1 >= lo) and (not mv(i - 1))
            after_ok = (j + 1 <= t) and (not mv(j + 1))
            if before_ok and after_ok:
                lengths.append(j - i + 1)
            i = j + 1
        else:
            i = i + 1
    if len(lengths) == 0:
        return float("nan")
    if base == "mean_streak":
        total = 0.0
        for L in lengths:
            total = total + L
        return n / (total / len(lengths))
    count = 0
    for L in lengths:
        if L <= n:
            count = count + 1
    return count / len(lengths)
```

checks:
UpCloseStreakLengthComponent: every check passed
the bot's suite: == 1653 passed, 16 skipped, 75 deselected, 2244 warnings in 123.60s (0:02:03) ==
