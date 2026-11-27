# CloseFromMidRangeInMeanRangesComponent: night9_chopstretch_run | 076-01.b1.b1.b1_falling-agitated-wide-close-fade_1d | CloseAboveMidRangeInMeanRanges

## attempt 1

answer: built
class: CloseFromMidRangeInMeanRangesComponent
settings: {"base_period": 20}
reason: No component gives the close's signed distance from the middle of bar t's range in mean bar ranges. `BreakoutInMeanRangesComponent` (`extreme` "low", `high_current` 1, `period` 1) measures from the low and is clipped at 0, and `DonchianBreakoutComponent` (`period` 1) has no range multiple. No config step subtracts one component from another, so one new class computes it.

table: Directional components
row: | `CloseFromMidRangeInMeanRangesComponent` | `base_period` (20) | (close[t] − (high[t] + low[t]) / 2) / B, B = mean(high[i] − low[i]) over i = t-`base_period`+1 .. t, bar t included; 0.0 when B = 0. Equal to (2 x loc − 1) / 2 x (high[t] − low[t]) / B, loc = (close[t] − low[t]) / (high[t] − low[t]) | signed, −`base_period`/2 to +`base_period`/2 on real bars (−10 to +10 at the default; the mean includes bar t's range). Positive when the close is above the middle of the day's range, negative below it, 0 at the middle or for a zero-range bar. Its size grows linearly with the close's distance from the middle and as the day's range widens against its mean | graded | mean bar ranges | `base_period` (20) | high, low (last `base_period` rows), close (bar t). A NaN in any value read gives NaN. B = 0 (`base_period` zero-range bars in a row, never on real bars) gives 0.0, because the distance is then 0 too. These settings raise when the component is built: `base_period` not an integer >= 1 | stateless; continuous in the prices. At the default on 1d bars it is the close's height above the day's mid-range in 20-day mean daily ranges. Not `BreakoutInMeanRangesComponent`, which measures from a window extreme and is one-sided. It ignores the open and the volume. `negate` gives the fade reading. No `scaling_factor`: scale it with transforms |

```python class
class CloseFromMidRangeInMeanRangesComponent(SubStrategyComponent):
    """
    The close's signed distance from the middle of the current bar's range, in mean bar ranges:

        mid = (high[t] + low[t]) / 2
        B   = mean(high[i] - low[i]) over i = t - base_period + 1 .. t   (bar t included)
        raw_value = (close[t] - mid) / B          (0.0 when B = 0)

    This equals (2 x loc - 1) / 2 x (high[t] - low[t]) / B, with loc = (close[t] - low[t]) / (high[t] - low[t]).
    Range and sign: signed. On real bars it runs from -base_period/2 to +base_period/2, because the mean includes
    bar t's own range. It is positive above the middle of the day's range, negative below it, and 0 at the middle
    or for a zero-range bar. Graded: it grows linearly with the distance from the middle and with the day's range
    against its mean.
    Warm-up: base_period rows, bar t included.
    NaN: a NaN high or low in the last base_period rows, or a NaN close[t], gives NaN. B = 0 (base_period
    zero-range bars in a row, never seen on real bars) gives 0.0, because the distance is then 0 too.
    Building the component raises for a base_period that is not an integer >= 1.

    WHY THIS CANNOT LEAK: it reads only the high and low of the last base_period rows of data and the close of
    the last row (bar t); every one of them is known at bar t's close.
    """

    def __init__(self, name="CloseFromMidRangeInMeanRanges", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        bp = self.parameters.get("base_period", 20)
        if isinstance(bp, bool):
            raise ValueError(f"CloseFromMidRangeInMeanRangesComponent: base_period must be an integer >= 1, got {bp!r}")
        try:
            bp_int = int(bp)
        except (TypeError, ValueError):
            raise ValueError(f"CloseFromMidRangeInMeanRangesComponent: base_period must be an integer >= 1, got {bp!r}")
        if bp_int != bp or bp_int < 1:
            raise ValueError(f"CloseFromMidRangeInMeanRangesComponent: base_period must be an integer >= 1, got {bp!r}")
        self.base_period = bp_int
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.base_period
        high = data['high'].astype(float).iloc[-n:].to_numpy()
        low = data['low'].astype(float).iloc[-n:].to_numpy()
        close_t = float(data['close'].astype(float).iloc[-1])
        if np.isnan(high).any() or np.isnan(low).any() or np.isnan(close_t):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        base = float(np.mean(high - low))
        mid = (float(high[-1]) + float(low[-1])) / 2.0
        if base == 0.0:
            self._raw_value = 0.0
        else:
            self._raw_value = float((close_t - mid) / base)
        self.confidence = 1.0
        self.debug_info = {'mid_range': mid, 'mean_bar_range': base, 'close': close_t}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.base_period
```

```python hand
def hand(df, params):
    n = int(params.get("base_period", 20))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    c = closes[t]
    if c != c:
        return float("nan")
    total = 0.0
    for k in range(n):
        h = highs[t - k]
        lo = lows[t - k]
        if h != h or lo != lo:
            return float("nan")
        total = total + (h - lo)
    mean_range = total / n
    if mean_range == 0.0:
        return 0.0
    rng = highs[t] - lows[t]
    if rng == 0.0:
        return 0.0
    location = (c - lows[t]) / rng
    return (2.0 * location - 1.0) / 2.0 * (rng / mean_range)
```

checks:
CloseFromMidRangeInMeanRangesComponent: every check passed
the bot's suite: == 1678 passed, 16 skipped, 75 deselected, 2244 warnings in 124.46s (0:02:04) ==
