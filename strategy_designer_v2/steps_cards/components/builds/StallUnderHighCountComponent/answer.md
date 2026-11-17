# StallUnderHighCountComponent: night_013_run | 013-05_longer-stall-bigger-breakout_1d | StallUnderHighCountComponent

## attempt 1

answer: built
class: StallUnderHighCountComponent
settings: {"window": 60, "period": 365, "band": 10.0}
reason: No catalogue component counts bars whose close sat below, but within a percent band of, the highest of the closes before them. `DistanceFromHighComponent` (`exclude_current` 1) reads only bar t's distance, not how many of the last 60 bars stalled in that band, so a new class computes this count.

table: Regime measures
row: | `StallUnderHighCountComponent` | `window` (60), `period` (365), `band` (10.0) | the number of bars i in t-`window`+1 .. t with close[i] < H(i) and (H(i) - close[i]) / H(i) x 100 <= `band`, H(i) being the highest of the `period` closes before bar i (bars i-`period` .. i-1, bar i excluded) | 0 to `window` (0 to 60), integers, never negative; no direction; grows by one for each further bar spent just under the prior high | regime measure | bars | `window` + `period` (425) | closes only. A NaN close anywhere in the last `window` + `period` rows gives NaN; an H(i) not above 0 gives NaN (never on real bars). These settings raise when the component is built: `window` < 1, `period` < 2, `band` not above 0 | stateless. A bar that makes a new closing high (close >= H(i)) is not counted, and neither is a bar deeper than `band` percent below H(i). The value counts the bars of the window that stalled in the band, not a consecutive run. No `scaling_factor`: scale it with transforms |

```python class
class StallUnderHighCountComponent(SubStrategyComponent):
    """
    How many of the last `window` bars closed just under their prior high:

        H(i) = max(close[i - period] .. close[i - 1])          (bar i excluded)
        stall(i) = 1 if close[i] < H(i) and (H(i) - close[i]) / H(i) x 100 <= band, else 0
        raw_value = sum of stall(i) for i = t - window + 1 .. t

    Range: 0 to window (integers), never negative, no direction. 0 when no bar of the window sat in the band
    under its prior high, window when every bar did. A bar at or above its prior high (a new closing high) is
    not counted, and neither is a bar more than `band` percent below it.
    Warm-up: window + period rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + period rows of data, the last
    of which is bar t; each H(i) uses the closes strictly before bar i, and i <= t.

    NaN: a NaN close anywhere in the last window + period rows gives NaN; an H(i) not above 0 gives NaN (never on
    real bars). A missing `close` column raises.
    Building the component raises for a window below 1, a period below 2, or a band not above 0.
    """

    def __init__(self, name="StallUnderHighCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.window = int(self.parameters.get("window", 60))
        if self.window < 1:
            raise ValueError(f"StallUnderHighCountComponent: window must be >= 1, got {self.window}")
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"StallUnderHighCountComponent: period must be >= 2, got {self.period}")
        self.band = float(self.parameters.get("band", 10.0))
        if not self.band > 0:
            raise ValueError(f"StallUnderHighCountComponent: band must be above 0, got {self.band}")
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
        count = 0
        for k in range(self.window):
            idx = self.period + k
            h = float(np.max(c[k:idx]))
            if not h > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            x = float(c[idx])
            if x < h and (h - x) / h * 100.0 <= self.band:
                count += 1
        self._raw_value = float(count)
        self.confidence = 1.0
        self.debug_info = {'stall_count': count, 'band': self.band}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.period
```

```python hand
def hand(df, params):
    w = int(params.get("window", 60))
    p = int(params.get("period", 365))
    band = float(params.get("band", 10.0))
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    first_needed = last - w + 1 - p
    j = first_needed
    while j <= last:
        if closes[j] != closes[j]:
            return float("nan")
        j = j + 1
    count = 0
    i = last - w + 1
    while i <= last:
        high = None
        j = i - p
        while j <= i - 1:
            if high is None or closes[j] > high:
                high = closes[j]
            j = j + 1
        if not high > 0:
            return float("nan")
        depth = (high - closes[i]) / high * 100.0
        if closes[i] < high and depth <= band:
            count = count + 1
        i = i + 1
    return float(count)
```

checks:
StallUnderHighCountComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1537 passed, 8 skipped, 74 deselected, 2170 warnings in 58.99s ========
