# PriorDownRunLossOnUpCloseComponent: night9_fallcalmfade_run | 074-01.b1.d2.g1_up-run-break-dip-rebound_1d | PriorUpRunGainOnDownCloseComponent

## attempt 1

answer: built
class: PriorDownRunLossOnUpCloseComponent
settings: {"side": "up", "base": "usual_moves", "window": 30, "exclude_current": 1, "max_bars": 30}
reason: `PriorDownRunLossOnUpCloseComponent` already measures the run that bar t breaks, in usual one-bar moves of the window ending at t-1, but only for a down run broken by an up close. The up run broken by a down close is not its negative, and no config step gives it, so the class needs a `side` setting whose default "down" keeps today's output. `DownStreakLossInUsualMovesComponent` with `side` "up" reads the up run on its own bar, not on the down close that ends it.

table: Regime measures
row: | `PriorDownRunLossOnUpCloseComponent` | `max_bars` (30), `base` ("percent"), `window` (30), `exclude_current` (0), `side` ("down") | `side` "down": when close[t] > close[t-1], n = the number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1], capped at `max_bars`, and M = (close[t-1-n] − close[t-1]) / close[t-1-n] (the run's loss). `side` "up": when close[t] < close[t-1], n = the number of consecutive bars i ending at t-1 with close[i] > close[i-1], capped at `max_bars`, and M = (close[t-1] − close[t-1-n]) / close[t-1-n] (the run's gain). `base` "percent": M x 100. `base` "usual_moves": M / m, m = mean of abs(close[j] / close[j-1] − 1) over j = t-`exclude_current`-`window`+1 .. t-`exclude_current` (`exclude_current` 0: bar t's return included; 1: bars t-`window` .. t-1). `base` "std": M / s, s = std (ddof 1) of the one-bar returns close[j] / close[j-1] − 1 over the same j. The output is 0 when bar t does not close to the breaking side or n = 0, and 0 when m = 0 or s = 0. With `side` "up", "usual_moves", `window` 30, `exclude_current` 1: the gain of the up run ending at t-1 in usual daily moves of the 30 returns ending at t-1, on a down close | "down", "percent": 0 to below 100. "up", "percent": 0 and up, unbounded above. "usual_moves" and "std": 0 and up, unbounded above. Never negative; no direction. "down" is 0 on down and flat bars and on an up bar that follows an up or flat bar. "up" is 0 on up and flat bars and on a down bar that follows a down or flat bar. Both grow with the run's total move | regime measure | "percent": percent of the run's starting close. "usual_moves": usual one-bar moves (mean absolute). "std": one-bar return standard deviations | `max_bars` + 2 (32) with "percent"; max(`max_bars` + 2, `window` + 1 + `exclude_current`) with "usual_moves" or "std" (32 at the wished settings) | Closes only. A NaN close in the last (warmup) rows gives NaN, and so does a close not above 0 there (never on real bars). m = 0 or s = 0 gives 0 (never on real bars). These settings raise when the component is built: `max_bars` < 1, `window` < 1, `window` < 2 with "std", `base` other than "percent", "usual_moves" or "std", `exclude_current` not 0 or 1, `side` other than "down" or "up" | Stateless. `side` "down" (default) with every `base` and `exclude_current` is the original output, unchanged. "up" is the gain of the up run that a down close breaks. `negate` on "down" is not it, and no config step gives it, hence the setting. A flat bar (equal close) ends either run and does not count as the break. The value is nonzero only on the first close that breaks a run and is 0 again on the next bar. It jumps, so it belongs in regime rules, not as a forecast source. The cap binds only on a run longer than `max_bars` bars, which real 1d bars do not show. On 1d bars, `side` "up", "usual_moves", `window` 30 and `exclude_current` 1 give the finished up run's gain in usual daily moves of the 30 days ending yesterday, on the dip day. No `scaling_factor`: scale it with transforms |

```python class
class PriorDownRunLossOnUpCloseComponent(SubStrategyComponent):
    """
    The move of the run that bar t breaks, on the breaking bar only:

        side = "down" (default): when close[t] > close[t-1],
            n = number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1],
                capped at max_bars
            M = (close[t-1-n] - close[t-1]) / close[t-1-n]          (the down run's loss)
        side = "up": when close[t] < close[t-1],
            n = number of consecutive bars i ending at t-1 with close[i] > close[i-1], capped at max_bars
            M = (close[t-1] - close[t-1-n]) / close[t-1-n]          (the up run's gain)
        base = "percent" (default): raw_value = M x 100
        base = "usual_moves":       raw_value = M / m, m = mean(abs(close[j] / close[j-1] - 1)),
                                    j = t-exclude_current-window+1 .. t-exclude_current
        base = "std":               raw_value = M / s, s = std (ddof 1) of close[j] / close[j-1] - 1, same j
        raw_value = 0 when bar t does not close to the breaking side, when n = 0, or when m = 0 / s = 0.

    exclude_current 0 includes bar t's return in the base; 1 uses the window returns ending at t-1.
    side "down" is the original output, unchanged, for every base and exclude_current.
    Range: "down" with "percent" is 0 to below 100; "up" with "percent" is 0 and up; "usual_moves" and
    "std" are 0 and up, unbounded. Never negative, no direction. A flat bar ends either run and is not a break.
    Warm-up: max_bars + 2 rows with "percent"; max(max_bars + 2, window + 1 + exclude_current) otherwise.
    NaN: a NaN close in the last (warm-up) rows gives NaN, and so does a close not above 0 there.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last get_required_periods() rows of data,
    the last of them being bar t; every close read is at or before bar t.
    """

    def __init__(self, name="PriorDownRunLossOnUpClose", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(f"PriorDownRunLossOnUpCloseComponent: max_bars must be >= 1, got {self.max_bars}")
        self.base = self.parameters.get("base", "percent")
        if self.base not in ("percent", "usual_moves", "std"):
            raise ValueError(
                f"PriorDownRunLossOnUpCloseComponent: base must be 'percent', 'usual_moves' or 'std', got {self.base!r}")
        self.window = int(self.parameters.get("window", 30))
        if self.window < 1:
            raise ValueError(f"PriorDownRunLossOnUpCloseComponent: window must be >= 1, got {self.window}")
        if self.base == "std" and self.window < 2:
            raise ValueError("PriorDownRunLossOnUpCloseComponent: window must be >= 2 with base 'std'")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"PriorDownRunLossOnUpCloseComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.side = self.parameters.get("side", "down")
        if self.side not in ("down", "up"):
            raise ValueError(f"PriorDownRunLossOnUpCloseComponent: side must be 'down' or 'up', got {self.side!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data["close"].astype(float).to_numpy()
        need = self.get_required_periods()
        tail = c[-need:]
        self.confidence = 1.0
        if np.isnan(tail).any() or (tail <= 0).any():
            self._raw_value = float("nan")
            return
        t = len(c) - 1
        up = self.side == "up"
        breaks = (c[t] < c[t - 1]) if up else (c[t] > c[t - 1])
        if not breaks:
            return
        n = 0
        while n < self.max_bars:
            i = t - 1 - n
            moved = (c[i] > c[i - 1]) if up else (c[i] < c[i - 1])
            if not moved:
                break
            n += 1
        if n == 0:
            return
        start = c[t - 1 - n]
        if up:
            move = (c[t - 1] - start) / start
        else:
            move = (start - c[t - 1]) / start
        if self.base == "percent":
            value = move * 100.0
        else:
            end = t - self.exclude_current
            rets = np.array([c[j] / c[j - 1] - 1.0 for j in range(end - self.window + 1, end + 1)])
            if self.base == "usual_moves":
                d = float(np.mean(np.abs(rets)))
            else:
                d = float(np.std(rets, ddof=1))
            value = move / d if d > 0 else 0.0
        self._raw_value = float(value)
        self.debug_info = {"run_bars": n, "run_move": float(move), "side": self.side, "base": self.base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "percent":
            return self.max_bars + 2
        return max(self.max_bars + 2, self.window + 1 + self.exclude_current)
```

```python hand
def hand(df, params):
    max_bars = int(params.get("max_bars", 30))
    base = params.get("base", "percent")
    window = int(params.get("window", 30))
    ex = int(params.get("exclude_current", 0))
    side = params.get("side", "down")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    if base == "percent":
        need = max_bars + 2
    else:
        need = max(max_bars + 2, window + 1 + ex)
    for x in c[len(c) - need:]:
        if x != x or not x > 0:
            return float("nan")
    # bar t must break the run: a down close for an up run, an up close for a down run
    if side == "up":
        if not c[t] < c[t - 1]:
            return 0.0
    else:
        if not c[t] > c[t - 1]:
            return 0.0
    # length of the run ending at bar t-1
    n = 0
    i = t - 1
    while n < max_bars:
        if side == "up":
            ok = c[i] > c[i - 1]
        else:
            ok = c[i] < c[i - 1]
        if not ok:
            break
        n = n + 1
        i = i - 1
    if n == 0:
        return 0.0
    first = c[t - 1 - n]
    last = c[t - 1]
    if side == "up":
        move = (last - first) / first
    else:
        move = (first - last) / first
    if base == "percent":
        return move * 100.0
    # one-bar returns of the window ending ex bars before t
    rets = []
    j = t - ex
    for k in range(window):
        rets.append(c[j - k] / c[j - k - 1] - 1.0)
    if base == "usual_moves":
        total = 0.0
        for r in rets:
            total = total + abs(r)
        d = total / window
    else:
        mu = sum(rets) / window
        ss = 0.0
        for r in rets:
            ss = ss + (r - mu) * (r - mu)
        d = (ss / (window - 1)) ** 0.5
    if not d > 0:
        return 0.0
    return move / d
```

checks:
PriorDownRunLossOnUpCloseComponent: every check passed
the bot's suite: == 1678 passed, 16 skipped, 75 deselected, 2244 warnings in 157.68s (0:02:37) ==
