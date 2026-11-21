# SwingLowTouchNearnessComponent: night3_levels_run | 020-02_support-retest-bounces-up_1d | SupportTouchCountComponent

## attempt 1

answer: built
class: SwingLowTouchNearnessComponent
settings: {"period": 90, "side": 2, "band": 1.5, "fall_period": 5}
reason: No component in the catalogue measures swing lows near the close. `SwingHighClusterCountComponent` counts swing highs around the nearest level at or above the close, and it weights the whole count by that one level's proximity. This measure is a sum over the swing lows inside a band of the close, each weighted by its own nearness, and it applies only while the close sits below its value `fall_period` bars ago. One new class computes it.

table: Regime measures
row: | `SwingLowTouchNearnessComponent` | `period` (90), `side` (2), `band` (1.5), `fall_period` (5) | G x sum over swing lows i of max(0, 1 - D_i / `band`), D_i = abs(close[t] - low[i]) / close[t] x 100. A swing low is a bar i in t-`period`+1+`side` .. t-`side` whose low[i] is strictly below the low of each of the `side` bars before it and the `side` bars after it, all inside the window. G = 1 when close[t] < close[t-`fall_period`], else 0 | 0 up to the number of swing lows (at most `period` - 2 x `side`), never negative; no direction. It is 0 when no swing low lies within `band` percent of the close, or when the close is not below its value `fall_period` bars ago. Each low adds 1 when the close sits exactly on it and 0 at the band's edge | graded | swing lows (nearness-weighted count) | max(`period`, `fall_period` + 1) (90) | low (last `period` rows), close (bar t and bar t-`fall_period`). A NaN low in the window, or a NaN close[t] or close[t-`fall_period`], gives NaN. A close[t] not above 0 gives NaN (never on real bars). These settings raise when the component is built: `side` < 1, `period` < 2 x `side` + 1, `band` not above 0, `fall_period` < 1 | stateless. A swing low is confirmed only `side` bars after it, using bars up to t. Ties do not count (strictly below), so a flat bottom of equal lows counts none of its bars. The band is in percent of the close, on either side of it. The value is continuous in the closes while the gate is on. It drops to 0 where close[t] crosses close[t-`fall_period`] upward. No `scaling_factor`: scale it with transforms |

```python class
class SwingLowTouchNearnessComponent(SubStrategyComponent):
    """
    Nearness-weighted count of the swing lows close to the current close, while the close is falling:

        swing low: a bar i in t-period+1+side .. t-side whose low[i] < low[j] for every j in
                   i-side .. i-1 and i+1 .. i+side (all inside the last `period` bars, bar t included)
        D_i = abs(close[t] - low[i]) / close[t] x 100                    (percent of the close)
        w_i = max(0, 1 - D_i / band)                                     (1 on the level, 0 at the band's edge)
        G   = 1 if close[t] < close[t - fall_period] else 0
        raw_value = G x sum of w_i over the swing lows

    Range: 0 up to the number of swing lows (at most period - 2 x side). It is never negative and has no
    direction. It is 0 with no swing low within `band` percent of the close, and 0 when the close is not below
    its value fall_period bars ago. It grows continuously with each further nearby swing low and with the
    nearness of the close to each one.
    Warm-up: max(period, fall_period + 1) rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `low` column of the last `period` rows and the `close` of the last
    row (bar t) and of the row fall_period rows before it. A swing low at bar i is confirmed with lows up to
    bar i + side <= t, all known at bar t's close.

    NaN: a NaN low in the window, or a NaN close[t] or close[t - fall_period], gives NaN. A close[t] not above 0
    gives NaN (never on real bars).
    Building the component raises for side < 1, period < 2 x side + 1, band not above 0, or fall_period < 1.
    """

    def __init__(self, name="SwingLowTouchNearness", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        self.band = float(self.parameters.get("band", 1.5))
        self.fall_period = int(self.parameters.get("fall_period", 5))
        if self.side < 1:
            raise ValueError(f"SwingLowTouchNearnessComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"SwingLowTouchNearnessComponent: period must be >= 2 x side + 1, got {self.period}")
        if not self.band > 0:
            raise ValueError(f"SwingLowTouchNearnessComponent: band must be above 0, got {self.band}")
        if self.fall_period < 1:
            raise ValueError(
                f"SwingLowTouchNearnessComponent: fall_period must be >= 1, got {self.fall_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        lows = data['low'].astype(float).iloc[-self.period:].to_numpy()
        closes = data['close'].astype(float)
        c_t = float(closes.iloc[-1])
        c_base = float(closes.iloc[-(self.fall_period + 1)])
        if np.isnan(lows).any() or np.isnan(c_t) or np.isnan(c_base) or not c_t > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        k = self.side
        n = len(lows)
        total = 0.0
        swings = 0
        for i in range(k, n - k):
            neighbours = np.concatenate([lows[i - k:i], lows[i + 1:i + k + 1]])
            if np.all(lows[i] < neighbours):
                swings += 1
                d = abs(c_t - lows[i]) / c_t * 100.0
                w = 1.0 - d / self.band
                if w > 0:
                    total += w
        gate = 1.0 if c_t < c_base else 0.0
        self._raw_value = float(gate * total)
        self.confidence = 1.0
        self.debug_info = {'swing_lows': swings, 'weighted_touches': total, 'falling': bool(gate)}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.fall_period + 1)
```

```python hand
def hand(df, params):
    period = int(params.get("period", 90))
    side = int(params.get("side", 2))
    band = float(params.get("band", 1.5))
    fall_period = int(params.get("fall_period", 5))
    low_all = [float(x) for x in list(df["low"])]
    close_all = [float(x) for x in list(df["close"])]
    last = len(close_all) - 1
    close_t = close_all[last]
    close_before = close_all[last - fall_period]
    window = low_all[len(low_all) - period:]
    for x in window:
        if x != x:
            return float("nan")
    if close_t != close_t or close_before != close_before:
        return float("nan")
    if not close_t > 0:
        return float("nan")
    if not close_t < close_before:
        return 0.0
    result = 0.0
    i = side
    while i <= period - 1 - side:
        is_swing = True
        j = i - side
        while j <= i + side:
            if j != i and not window[i] < window[j]:
                is_swing = False
            j = j + 1
        if is_swing:
            distance_pct = abs(close_t - window[i]) / close_t * 100.0
            nearness = 1.0 - distance_pct / band
            if nearness > 0:
                result = result + nearness
        i = i + 1
    return result
```

checks:
SwingLowTouchNearnessComponent: every check passed
the bot's suite: ======= 1581 passed, 16 skipped, 75 deselected, 2244 warnings in 50.74s ========
