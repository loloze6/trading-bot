# DownStreakLossInUsualMovesComponent: night4_exhaustion_run | 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h | DownStreakScaledLoss

## attempt 1

answer: built
class: DownStreakLossInUsualMovesComponent
settings: {"window": 180, "max_bars": 180, "side": "down", "base": "end"}
reason: `DownStreakLossInUsualMovesComponent` already measures the down-streak's loss in usual one-bar moves, but it divides the loss by close[t-n], while the wish's close[t-n] / close[t] - 1 divides it by close[t]. The divisor changes the value on every real streak, so it becomes a setting `base` on the same class; its default "start" keeps today's output exactly.

table: Directional components
row: | `DownStreakLossInUsualMovesComponent` | `window` (180), `max_bars` (180), `side` ("down"), `base` ("start") | `side` "down": (close[t-n] − close[t]) / P / m, n = the number of consecutive bars i ending at t with close[i] < close[i-1]. `side` "up": (close[t] − close[t-n]) / P / m, n = the number of consecutive bars i ending at t with close[i] > close[i-1]. n is capped at `max_bars`. P = close[t-n] (`base` "start") or close[t] (`base` "end"). With `base` "end" and `side` "down", the output is (close[t-n] / close[t] − 1) / m. m = mean of abs(close[j] / close[j-1] − 1) over the last `window` one-bar returns, bar t's included. 0 when n = 0 (bar t did not move to the counted side). 0 when m = 0 | 0 and up, unbounded above, never negative; no direction. "down": 0 when bar t did not close down, grows as the streak's summed loss gets larger against the usual one-bar move. "up": 0 when bar t did not close up, grows as the streak's summed gain gets larger against the usual one-bar move. `base` "end" gives a larger reading than "start" for a down-streak and a smaller one for an up-streak | graded | usual one-bar moves | max(`window`, `max_bars`) + 1 (181) | closes only. A NaN close in the last max(`window`, `max_bars`) + 1 rows gives NaN. A close not above 0 there gives NaN (never on real bars). m = 0 gives 0 (never on real bars). These settings raise when the component is built: `window` < 1, `max_bars` < 1, `side` other than "down" or "up", `base` other than "start" or "end" | stateless. `side` "down" with `base` "start" (the defaults) is the original output, unchanged. "up" is the up-streak gain. No config step gives it, because `negate` on "down" is not it, hence the setting. `base` "end" counts the streak's move against the current close: for "down" that is the rise needed to recover the loss. No config step gives that, hence the setting. The output is continuous in the closes while the streak lasts and drops to 0 on the first bar that closes on the other side or flat. A flat bar (equal close) ends either streak. The cap binds only on a streak longer than `max_bars` bars, which real bars never show. On 4h bars the defaults are 30 days of one-bar moves. One-sided for each side. No `scaling_factor`: scale it with transforms |

```python class
class DownStreakLossInUsualMovesComponent(SubStrategyComponent):
    """
    The move of the current one-sided streak of closes, counted in usual one-bar moves:

        side = "down" (default): n = number of consecutive bars i ending at t with close[i] < close[i-1]
        side = "up":             n = number of consecutive bars i ending at t with close[i] > close[i-1]
        n is capped at max_bars.
        base = "start" (default): P = close[t-n]
        base = "end":             P = close[t]
        m = mean(abs(close[j] / close[j-1] - 1)) over the last `window` one-bar returns, j = t-window+1 .. t
        side "down": raw_value = (close[t-n] - close[t]) / P / m
        side "up":   raw_value = (close[t] - close[t-n]) / P / m
        raw_value = 0.0 when n = 0 (bar t did not move to the counted side), and 0.0 when m = 0.

    With base "end" and side "down" the output is (close[t-n] / close[t] - 1) / m: the rise needed to recover the
    streak's loss, in usual one-bar moves. The defaults (side "down", base "start") are the original output,
    unchanged.
    Range: 0 and up, unbounded above, never negative; no direction. It is graded and continuous in the closes
    while the streak lasts.
    Warm-up: max(window, max_bars) + 1 rows, bar t included.

    NaN: a NaN close in the last max(window, max_bars) + 1 rows gives NaN, and so does a close not above 0 there
    (never on real bars). m = 0 gives 0.0 (never on real bars).
    Building the component raises for a window below 1, a max_bars below 1, a side other than "down" or "up", or a
    base other than "start" or "end".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window, max_bars) + 1 rows of data, the
    last of which is bar t; no row after t is read.
    """

    def __init__(self, name="DownStreakLoss", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 180))
        if self.window < 1:
            raise ValueError(f"DownStreakLossInUsualMovesComponent: window must be >= 1, got {self.window}")
        self.max_bars = int(self.parameters.get("max_bars", 180))
        if self.max_bars < 1:
            raise ValueError(f"DownStreakLossInUsualMovesComponent: max_bars must be >= 1, got {self.max_bars}")
        self.side = self.parameters.get("side", "down")
        if self.side not in ("down", "up"):
            raise ValueError(f"DownStreakLossInUsualMovesComponent: side must be 'down' or 'up', got {self.side!r}")
        self.base = self.parameters.get("base", "start")
        if self.base not in ("start", "end"):
            raise ValueError(f"DownStreakLossInUsualMovesComponent: base must be 'start' or 'end', got {self.base!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        last = len(c) - 1
        rets = c[last - self.window + 1:] / c[last - self.window:last] - 1.0
        m = float(np.mean(np.abs(rets)))
        n = 0
        i = last
        while n < self.max_bars:
            if self.side == "down":
                moved = c[i] < c[i - 1]
            else:
                moved = c[i] > c[i - 1]
            if not moved:
                break
            n += 1
            i -= 1
        if n == 0 or m == 0.0:
            value = 0.0
        else:
            start = float(c[last - n])
            end = float(c[last])
            diff = (start - end) if self.side == "down" else (end - start)
            divisor = start if self.base == "start" else end
            value = diff / divisor / m
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'streak_bars': n, 'mean_abs_return': m, 'side': self.side, 'base': self.base}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.window, self.max_bars) + 1
```

```python hand
def hand(df, params):
    window = int(params.get("window", 180))
    max_bars = int(params.get("max_bars", 180))
    side = params.get("side", "down")
    base = params.get("base", "start")
    closes = [float(x) for x in list(df["close"])]
    need = max(window, max_bars) + 1
    c = closes[len(closes) - need:]
    for x in c:
        if x != x or not x > 0:
            return float("nan")
    t = len(c) - 1
    total = 0.0
    for j in range(t - window + 1, t + 1):
        total += abs(c[j] / c[j - 1] - 1.0)
    m = total / window
    n = 0
    while n < max_bars:
        cur = c[t - n]
        prev = c[t - n - 1]
        if side == "down" and cur < prev:
            n += 1
        elif side == "up" and cur > prev:
            n += 1
        else:
            break
    if n == 0 or m == 0.0:
        return 0.0
    first = c[t - n]
    now = c[t]
    if side == "down":
        if base == "end":
            frac = first / now - 1.0
        else:
            frac = 1.0 - now / first
    else:
        if base == "end":
            frac = 1.0 - first / now
        else:
            frac = now / first - 1.0
    return frac / m
```

checks:
DownStreakLossInUsualMovesComponent: every check passed
the bot's suite: == 1611 passed, 16 skipped, 75 deselected, 2244 warnings in 102.83s (0:01:42) ==
