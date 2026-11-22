# UpStreakGainTimesDepthBelowAverageComponent: night4_exhaustion_run | 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h | UpStreakGainTimesDepthBelowAverageComponent

## attempt 1

answer: built
class: UpStreakGainTimesDepthBelowAverageComponent
settings: {"window": 180, "max_bars": 180, "ma_period": 180}
reason: No class in the catalogue computes this product. `DownStreakLossInUsualMovesComponent` (`side` "up", `window` 180) gives the first factor, and `MovingAverageDistanceComponent` (`period` 180, `average` "sma"), negated and clipped at 0 and divided by... no, simply negated and clipped at 0, gives the second. No config step multiplies two components, so one new class computes their product.

table: Directional components
row: | `UpStreakGainTimesDepthBelowAverageComponent` | `window` (180), `max_bars` (180), `ma_period` (180) | G x D. G = (close[t] − close[t-n]) / close[t-n] / m, where n is the number of consecutive bars i ending at t with close[i] > close[i-1], capped at `max_bars`. m = mean of abs(close[j] / close[j-1] − 1) over the last `window` one-bar returns, bar t's included. G is 0 when n = 0 or m = 0. D = max(0, (SMA − close[t]) / SMA x 100), where SMA = mean of the last `ma_period` closes, bar t included | 0 and up, unbounded above, never negative; no direction. It is 0 when bar t did not close up, and 0 when the close is at or above its SMA. It grows with the up-streak's gain in usual one-bar moves and with the percent depth below the average | graded | usual one-bar moves x percent | max(`window` + 1, `max_bars` + 1, `ma_period`) (181) | closes only. A NaN close in the last max(`window` + 1, `max_bars` + 1, `ma_period`) rows gives NaN. A close not above 0 there gives NaN (never on real bars). m = 0 gives 0 (never on real bars). These settings raise when the component is built: `window` < 1, `max_bars` < 1, `ma_period` < 2 | stateless. It equals `DownStreakLossInUsualMovesComponent` (`side` "up", `base` "start", same `window`, `max_bars`) x `MovingAverageDistanceComponent` (`period` = `ma_period`, `average` "sma") negated and clipped at 0. It is continuous in the closes while the streak lasts and drops to 0 on the first bar that closes down or flat. The cap binds only on a streak longer than `max_bars` bars, which real bars never show. One-sided; `negate` gives the short forecast. No `scaling_factor`: scale it with transforms |

```python class
class UpStreakGainTimesDepthBelowAverageComponent(SubStrategyComponent):
    """
    The up-streak's gain in usual one-bar moves, times the close's percent depth below its simple average:

        n = number of consecutive bars i ending at t with close[i] > close[i-1], capped at max_bars
        m = mean(abs(close[j] / close[j-1] - 1)) over the last `window` one-bar returns, bar t's included
        G = (close[t] - close[t-n]) / close[t-n] / m        (0 when n = 0 or m = 0)
        SMA = mean(close[t-ma_period+1 .. t])
        D = max(0, (SMA - close[t]) / SMA * 100)
        raw_value = G * D

    Range: 0 and up, unbounded above, never negative, with no direction. It is 0 when bar t did not close up
    or when the close is at or above its SMA. It grows with the streak's gain in usual moves and with the depth
    below the average. `negate` gives the short forecast.
    Warm-up: max(window + 1, max_bars + 1, ma_period) rows, bar t included.
    NaN: a NaN close in those rows gives NaN, and so does a close not above 0 there (never on real bars).
    m = 0 gives 0.
    Building the component raises for a window < 1, a max_bars < 1 or an ma_period < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(window + 1, max_bars + 1, ma_period)
    rows of data, the last being bar t; a close is known at its bar's close.
    """

    def __init__(self, name="UpStreakGainDepth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 180))
        if self.window < 1:
            raise ValueError(f"UpStreakGainTimesDepthBelowAverageComponent: window must be >= 1, got {self.window}")
        self.max_bars = int(self.parameters.get("max_bars", 180))
        if self.max_bars < 1:
            raise ValueError(
                f"UpStreakGainTimesDepthBelowAverageComponent: max_bars must be >= 1, got {self.max_bars}")
        self.ma_period = int(self.parameters.get("ma_period", 180))
        if self.ma_period < 2:
            raise ValueError(
                f"UpStreakGainTimesDepthBelowAverageComponent: ma_period must be >= 2, got {self.ma_period}")
        self._raw_value = 0.0

    def update(self, data):
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
        n = 0
        while n < self.max_bars and c[-1 - n] > c[-2 - n]:
            n += 1
        rets = c[-self.window:] / c[-self.window - 1:-1] - 1.0
        m = float(np.mean(np.abs(rets)))
        if n > 0 and m > 0:
            gain = (c[-1] - c[-1 - n]) / c[-1 - n] / m
        else:
            gain = 0.0
        sma = float(np.mean(c[-self.ma_period:]))
        depth = max(0.0, (sma - c[-1]) / sma * 100.0)
        self._raw_value = float(gain * depth)
        self.confidence = 1.0
        self.debug_info = {'streak': n, 'mean_abs_return': m, 'gain_usual_moves': float(gain),
                           'sma': sma, 'depth_pct': float(depth)}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.window + 1, self.max_bars + 1, self.ma_period)
```

```python hand
def hand(df, params):
    window = int(params.get("window", 180))
    max_bars = int(params.get("max_bars", 180))
    ma_period = int(params.get("ma_period", 180))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(window + 1, max_bars + 1, ma_period)
    for i in range(last - need + 1, last + 1):
        x = c[i]
        if x != x or not x > 0:
            return float("nan")
    # current run of up closes
    n = 0
    while n < max_bars and c[last - n] > c[last - n - 1]:
        n = n + 1
    # usual one-bar move
    total = 0.0
    for j in range(last - window + 1, last + 1):
        total = total + abs(c[j] / c[j - 1] - 1.0)
    m = total / window
    if n > 0 and m > 0:
        start = c[last - n]
        gain = (c[last] - start) / start / m
    else:
        gain = 0.0
    s = 0.0
    for j in range(last - ma_period + 1, last + 1):
        s = s + c[j]
    sma = s / ma_period
    depth = (sma - c[last]) / sma * 100.0
    if depth < 0:
        depth = 0.0
    return gain * depth
```

checks:
UpStreakGainTimesDepthBelowAverageComponent: every check passed
the bot's suite: == 1612 passed, 16 skipped, 75 deselected, 2244 warnings in 95.99s (0:01:35) ===
