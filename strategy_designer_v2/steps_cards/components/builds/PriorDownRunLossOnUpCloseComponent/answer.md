# PriorDownRunLossOnUpCloseComponent: night9_fallcalmfade_run | 070-01.b1.g1_calm-decline-depth-fade_1d | PriorDownRunLossInUsualMovesOnUpClose

## attempt 1

answer: built
class: PriorDownRunLossOnUpCloseComponent
settings: {"base": "usual_moves", "window": 20, "exclude_current": 1}
reason: `PriorDownRunLossOnUpCloseComponent` with `base` "usual_moves" computes this loss on the bounce day, but its usual move m always includes bar t's own return. The wish takes m over the 20 returns ending at t-1, which differs on real data, so the class gains an `exclude_current` setting whose default 0 keeps today's output.

table: Regime measures
row: | `PriorDownRunLossOnUpCloseComponent` | `max_bars` (30), `base` ("percent"), `window` (30), `exclude_current` (0) | when close[t] > close[t-1]: L = (close[t-1-n] − close[t-1]) / close[t-1-n], where n = the number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1], capped at `max_bars`. `base` "percent": L x 100. `base` "usual_moves": L / m, m = mean of abs(close[j] / close[j-1] − 1) over j = t-`exclude_current`-`window`+1 .. t-`exclude_current` (`exclude_current` 0: bar t's return included; 1: bars t-`window` .. t-1). `base` "std": L / s, s = std (ddof 1) of the one-bar returns close[j] / close[j-1] − 1 over the same j. 0 when close[t] <= close[t-1] or n = 0; 0 when m = 0 or s = 0 | "percent": 0 to below 100, never negative. "usual_moves" and "std": 0 and up, unbounded above, never negative. No direction. 0 on down and flat bars and on an up bar that follows an up or flat bar. Grows with the depth of the run's total fall | regime measure | "percent": percent of the run's starting close. "usual_moves": usual one-bar moves (mean absolute). "std": one-bar return standard deviations | `max_bars` + 2 (32) with "percent"; max(`max_bars` + 2, `window` + 1 + `exclude_current`) with "usual_moves" or "std" (32 at the wished settings) | Closes only. A NaN close in the last (warmup) rows gives NaN, and so does a close not above 0 there (never on real bars). m = 0 or s = 0 gives 0 (never on real bars). These settings raise when the component is built: `max_bars` < 1, `window` < 1, `window` < 2 with "std", `base` other than "percent", "usual_moves" or "std", `exclude_current` not 0 or 1 | Stateless. `base` "percent" (default), "usual_moves" and "std" with `exclude_current` 0 (default) are the original outputs, unchanged. `exclude_current` 1 sets the run's loss against the usual move of the `window` days before the bounce day, so the bounce's own return cannot enlarge its base; it is not read by "percent". A flat bar (equal close) ends the down run and does not count as the bounce. The value is nonzero only on the first up close after a down run and is 0 again on the next bar. It jumps, so it belongs in regime rules, not as a forecast source. It is the loss counterpart of `PriorDownRunOnUpCloseComponent`, with the same run n. It is not `DownStreakLossInUsualMovesComponent`, which is 0 on every up bar. The cap binds only on a down run longer than `max_bars` bars, which real 1d bars do not show. On 1d bars, "usual_moves", `window` 20 and `exclude_current` 1 give the finished down run's fall in usual daily moves of the 20 days ending yesterday, on the bounce day. No `scaling_factor`: scale it with transforms |

```python class
class PriorDownRunLossOnUpCloseComponent(SubStrategyComponent):
    """
    The total loss of the down run that bar t breaks, on the bounce bar only:

        when close[t] > close[t-1]:
            n = number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1],
                capped at max_bars
            L = (close[t-1-n] - close[t-1]) / close[t-1-n]
            base = "percent" (default): raw_value = L x 100
            base = "usual_moves":       raw_value = L / m,
                m = mean(abs(close[j] / close[j-1] - 1)), j = t-exclude_current-window+1 .. t-exclude_current
            base = "std":               raw_value = L / s, s = std (ddof 1) of the same one-bar returns
        raw_value = 0 when close[t] <= close[t-1] or n = 0, and 0 when m = 0 or s = 0.

    exclude_current = 0 (default): the base returns end at bar t (bar t's return included), the original output.
    exclude_current = 1: the base returns are j = t-window .. t-1, so the bounce's own return is not in the base.
    exclude_current is not read by base "percent".
    Range: "percent" 0 to below 100; "usual_moves" and "std" 0 and up, unbounded; never negative, no direction.
    Warm-up: max_bars + 2 rows ("percent"); max(max_bars + 2, window + 1 + exclude_current) rows otherwise.
    NaN: a NaN close, or a close not above 0, in the last warm-up rows gives NaN.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last get_required_periods() rows of data, the
    last of which is bar t; no later row exists in the data it is given.

    Building the component raises for max_bars < 1, window < 1, window < 2 with "std", a base other than
    "percent", "usual_moves" or "std", or an exclude_current other than 0 or 1.
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
            raise ValueError(f"PriorDownRunLossOnUpCloseComponent: window must be >= 2 with 'std', got {self.window}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"PriorDownRunLossOnUpCloseComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        req = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-req:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        t = len(c) - 1
        value = 0.0
        n = 0
        if c[t] > c[t - 1]:
            i = t - 1
            while n < self.max_bars and c[i] < c[i - 1]:
                n += 1
                i -= 1
            if n > 0:
                start = c[t - 1 - n]
                loss = (start - c[t - 1]) / start
                if self.base == "percent":
                    value = loss * 100.0
                else:
                    end = t - self.exclude_current
                    js = np.arange(end - self.window + 1, end + 1)
                    rets = c[js] / c[js - 1] - 1.0
                    if self.base == "usual_moves":
                        scale = float(np.mean(np.abs(rets)))
                    else:
                        scale = float(np.std(rets, ddof=1))
                    value = float(loss / scale) if scale > 0 else 0.0
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'run_length': n, 'base': self.base, 'exclude_current': self.exclude_current}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        if self.base == "percent":
            return self.max_bars + 2
        return max(self.max_bars + 2, self.window + 1 + self.exclude_current)
```

```python hand
def hand(df, params):
    import math
    max_bars = int(params.get("max_bars", 30))
    base = params.get("base", "percent")
    window = int(params.get("window", 30))
    ex = int(params.get("exclude_current", 0))
    close = [float(x) for x in list(df["close"])]
    if base == "percent":
        need = max_bars + 2
    else:
        need = max(max_bars + 2, window + 1 + ex)
    last = close[len(close) - need:]
    for x in last:
        if x != x or not x > 0:
            return float("nan")
    t = len(close) - 1
    if not close[t] > close[t - 1]:
        return 0.0
    # length of the down run ending at t-1
    n = 0
    while n < max_bars and close[t - 1 - n] < close[t - 2 - n]:
        n = n + 1
    if n == 0:
        return 0.0
    first = close[t - 1 - n]
    loss = (first - close[t - 1]) / first
    if base == "percent":
        return loss * 100.0
    # one-bar returns of the window ending ex bars before t
    rets = []
    for k in range(window):
        j = t - ex - k
        rets.append(close[j] / close[j - 1] - 1.0)
    if base == "usual_moves":
        total = 0.0
        for r in rets:
            total = total + abs(r)
        scale = total / len(rets)
    else:
        mean = sum(rets) / len(rets)
        sq = 0.0
        for r in rets:
            sq = sq + (r - mean) * (r - mean)
        scale = math.sqrt(sq / (len(rets) - 1))
    if not scale > 0:
        return 0.0
    return loss / scale
```

checks:
PriorDownRunLossOnUpCloseComponent: every check passed
the bot's suite: == 1678 passed, 16 skipped, 75 deselected, 2244 warnings in 144.77s (0:02:24) ==
