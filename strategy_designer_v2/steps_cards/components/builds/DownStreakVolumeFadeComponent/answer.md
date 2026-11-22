# DownStreakVolumeFadeComponent: night4_exhaustion_run | 024-01_fading-volume-uprun-giveback-size.d2_fading-volume-down-run-rebound_4h | DownStreakVolumeFade

## attempt 1

answer: built
class: DownStreakVolumeFadeComponent
settings: {"side": "down", "statistic": "log_slope"}
reason: `DownStreakVolumeFadeComponent` already measures how volume fades across the current streak, but neither of its statistics is the least-squares slope of ln(volume) on the bar index. "slope" fits volume itself, and "log_ratio" reads only the two end volumes. A fit to the log volumes gives different values on real bars, so it is a new value of the existing `statistic` setting, and the default "slope" keeps today's output unchanged.

table: Directional components
row: | `DownStreakVolumeFadeComponent` | `max_bars` (180), `side` ("down"), `statistic` ("slope") | n = the number of consecutive bars i ending at t with close[i] < close[i-1] (`side` "down") or close[i] > close[i-1] (`side` "up"), capped at `max_bars`. The streak's bars are t-n+1 .. t with volumes v. When n < 2 the output is 0. `statistic` "slope": −b / v̄, where b = Σ(x − x̄)(v − v̄) / Σ(x − x̄)² is the least-squares slope of volume on bar index x = 0 .. n-1 and v̄ = mean(v). `statistic` "log_ratio": ln(volume[t-n+1] / volume[t]), the streak's first-bar volume against its last. `statistic` "log_slope": −c, where c = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)² is the least-squares slope of y = ln(v) on x = 0 .. n-1 | "slope": signed, strictly between −6/(n+1) and +6/(n+1), so within (−2, +2). "log_ratio" and "log_slope": unbounded, signed. All three are 0 when bar t did not move to the counted side or the streak is a single bar. All are positive and grow as volume fades across the streak, and negative when volume rises | graded | "slope": fraction of the streak's mean volume per bar. "log_ratio": natural log of a volume ratio. "log_slope": natural log of volume per bar | `max_bars` + 1 (181) | close, volume. A NaN close in the last `max_bars` + 1 rows gives NaN. With "slope", a NaN volume on a streak bar gives NaN, and so does a mean streak volume not above 0 (never on real bars). With "log_ratio", a NaN volume at the streak's first or last bar gives NaN, and so does a volume not above 0 there (never on real bars). With "log_slope", a NaN volume or a volume not above 0 on any streak bar gives NaN (never on real bars). These settings raise when the component is built: `max_bars` < 2, `side` other than "down" or "up", `statistic` other than "slope", "log_ratio" or "log_slope" | stateless. `side` "down" with `statistic` "slope" (the defaults) is the original output, unchanged. "up" is the volume fade behind an up-run; `negate` on "down" is not it, hence the setting. "log_ratio" reads only the streak's two end volumes. "log_slope" fits every streak volume on a log scale, so it is the per-bar rate of exponential decay, and a single heavy bar weighs less than in "slope". A flat bar (equal close) ends either streak. The output is continuous in the volumes while the streak lasts. It takes its first value when the streak reaches 2 bars and drops to 0 on the first bar that closes on the other side or flat. With n = 2, "log_slope" equals "log_ratio". The cap binds only on a streak longer than `max_bars` bars, which real bars never show. No `scaling_factor`: scale it with transforms |

```python class
class DownStreakVolumeFadeComponent(SubStrategyComponent):
    """
    How volume fades across the current streak of down (or up) closes, on every bar:

        n = the number of consecutive bars i ending at t with close[i] < close[i-1] (side "down")
            or close[i] > close[i-1] (side "up"), capped at max_bars
        v = volume[t-n+1 .. t], x = 0 .. n-1
        n < 2:                          raw_value = 0
        statistic = "slope" (default):  raw_value = -b / mean(v),  b = sum((x-xm)(v-vm)) / sum((x-xm)^2)
        statistic = "log_ratio":        raw_value = ln(v[0] / v[n-1])
        statistic = "log_slope":        raw_value = -c,  c = sum((x-xm)(y-ym)) / sum((x-xm)^2),  y = ln(v)

    The defaults (side "down", statistic "slope") give the original output, unchanged.
    Graded and signed: positive and growing as volume fades across the streak, negative when it rises.
    "slope" lies strictly within (-6/(n+1), +6/(n+1)). "log_ratio" and "log_slope" are unbounded.
    "log_slope" is the per-bar decay rate of the log volume.
    A flat bar (equal close) ends either streak.
    Warm-up: max_bars + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` and `volume` columns of the last max_bars + 1 rows up to and
    including bar t (the last row of data); a bar's close and volume are known at that bar's close.

    NaN: a NaN close in the last max_bars + 1 rows gives NaN. With "slope", a NaN volume on a streak bar or a mean
    streak volume not above 0 gives NaN. With "log_ratio", a NaN volume or a volume not above 0 at the streak's
    first or last bar gives NaN. With "log_slope", a NaN volume or a volume not above 0 on any streak bar gives NaN.
    Building the component raises for max_bars below 2, a side other than "down" or "up", or a statistic other
    than "slope", "log_ratio" or "log_slope".
    """

    def __init__(self, name="DownStreakVolumeFade", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.max_bars = int(self.parameters.get("max_bars", 180))
        if self.max_bars < 2:
            raise ValueError(f"DownStreakVolumeFadeComponent: max_bars must be >= 2, got {self.max_bars}")
        self.side = self.parameters.get("side", "down")
        if self.side not in ("down", "up"):
            raise ValueError(f"DownStreakVolumeFadeComponent: side must be 'down' or 'up', got {self.side!r}")
        self.statistic = self.parameters.get("statistic", "slope")
        if self.statistic not in ("slope", "log_ratio", "log_slope"):
            raise ValueError(
                "DownStreakVolumeFadeComponent: statistic must be 'slope', 'log_ratio' or 'log_slope', "
                f"got {self.statistic!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        m = self.max_bars + 1
        close = data['close'].astype(float).to_numpy()[-m:]
        vol = data['volume'].astype(float).to_numpy()[-m:]
        self.confidence = 1.0
        if np.isnan(close).any():
            self._raw_value = float("nan")
            return
        n = 0
        j = len(close) - 1
        while n < self.max_bars and j >= 1:
            moved = close[j] < close[j - 1] if self.side == "down" else close[j] > close[j - 1]
            if not moved:
                break
            n += 1
            j -= 1
        self.debug_info = {'streak_bars': n, 'side': self.side, 'statistic': self.statistic}
        if n < 2:
            self._raw_value = 0.0
            return
        v = vol[-n:]
        x = np.arange(n, dtype=float)
        xd = x - x.mean()
        sxx = float(np.sum(xd * xd))
        if self.statistic == "slope":
            if np.isnan(v).any():
                self._raw_value = float("nan")
                return
            vm = float(v.mean())
            if not vm > 0:
                self._raw_value = float("nan")
                return
            b = float(np.sum(xd * (v - vm))) / sxx
            self._raw_value = float(-b / vm)
        elif self.statistic == "log_ratio":
            first, last = float(v[0]), float(v[-1])
            if np.isnan(first) or np.isnan(last) or not first > 0 or not last > 0:
                self._raw_value = float("nan")
                return
            self._raw_value = float(np.log(first / last))
        else:
            if np.isnan(v).any() or not (v > 0).all():
                self._raw_value = float("nan")
                return
            y = np.log(v)
            c = float(np.sum(xd * (y - y.mean()))) / sxx
            self._raw_value = float(-c)

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.max_bars + 1
```

```python hand
def hand(df, params):
    import math
    max_bars = int(params.get("max_bars", 180))
    side = params.get("side", "down")
    statistic = params.get("statistic", "slope")
    closes = [float(x) for x in list(df["close"])]
    vols = [float(x) for x in list(df["volume"])]
    last = len(closes) - 1
    first_row = last - max_bars
    for i in range(first_row, last + 1):
        if closes[i] != closes[i]:
            return float("nan")
    n = 0
    i = last
    while n < max_bars:
        if side == "down":
            ok = closes[i] < closes[i - 1]
        else:
            ok = closes[i] > closes[i - 1]
        if not ok:
            break
        n = n + 1
        i = i - 1
    if n < 2:
        return 0.0
    v = vols[last - n + 1: last + 1]
    xs = [float(k) for k in range(n)]
    xbar = sum(xs) / n

    def ls_slope(ys):
        ybar = sum(ys) / n
        num = 0.0
        den = 0.0
        for k in range(n):
            num = num + (xs[k] - xbar) * (ys[k] - ybar)
            den = den + (xs[k] - xbar) * (xs[k] - xbar)
        return num / den

    if statistic == "log_ratio":
        a = v[0]
        z = v[-1]
        if a != a or z != z or not a > 0 or not z > 0:
            return float("nan")
        return math.log(a / z)
    for x in v:
        if x != x:
            return float("nan")
    if statistic == "log_slope":
        for x in v:
            if not x > 0:
                return float("nan")
        return -ls_slope([math.log(x) for x in v])
    vbar = sum(v) / n
    if not vbar > 0:
        return float("nan")
    return -ls_slope(v) / vbar
```

checks:
DownStreakVolumeFadeComponent: every check passed
the bot's suite: == 1611 passed, 16 skipped, 75 deselected, 2244 warnings in 100.93s (0:01:40) ==
