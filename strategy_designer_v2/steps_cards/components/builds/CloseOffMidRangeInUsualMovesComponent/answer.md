# CloseOffMidRangeInUsualMovesComponent: night9_fallcalmwide_run | 077-03_choppy-agitated-close-position-reversal_1d | ScaledCloseOffMidRange

## attempt 1

answer: built
class: CloseOffMidRangeInUsualMovesComponent
settings: {"vol_period": 30}
reason: No component gives the close's signed distance from the bar's mid-range in percent of the close, divided by the std of the recent one-bar returns. It equals `DonchianBreakoutComponent` (`period` 1, `sf` 1, `source` "high_low") x `RangeInReturnStdComponent` (`vol_period` 30), but no config step multiplies two components, so it is a new measure that one new class computes.

table: Directional components
row: | `CloseOffMidRangeInUsualMovesComponent` | `vol_period` (30) | 2 x (close[t] − (high[t] + low[t]) / 2) / close[t] / s, s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included; 0 when s = 0 | unbounded, signed; positive with the close above the bar's mid-range, negative below, 0 at the middle (and for a zero-range bar); on real bars its size is at most (high[t] − low[t]) / close[t] / s, reached with the close at the high or the low | graded | usual one-bar moves | `vol_period` + 1 (31) | high, low of bar t; closes (last `vol_period` + 1 rows). A NaN in any value read gives NaN; a close not above 0 among those read gives NaN (never on real bars). s = 0 (a flat return window, never on real bars) gives 0.0. These settings raise when the component is built: `vol_period` < 2 | stateless. Equals `DonchianBreakoutComponent` (`period` 1, `sf` 1, `source` "high_low") x `RangeInReturnStdComponent` (`vol_period`); no config step multiplies two components. Continuous in the highs, lows and closes. Ignores the open and the volume. Not `VolatilityScaledDistanceFromHighComponent`, which measures from the high. `negate` gives the fade reading. No `scaling_factor`: scale it with transforms |

```python class
class CloseOffMidRangeInUsualMovesComponent(SubStrategyComponent):
    """
    The close's signed distance from the bar's mid-range, in usual one-bar moves:

        mid = (high[t] + low[t]) / 2
        s   = std (ddof 1) of r[j] = close[j] / close[j-1] - 1, j = t-vol_period+1 .. t (bar t's return included)
        raw_value = 2 x (close[t] - mid) / close[t] / s,   0.0 when s = 0

    Range and sign: unbounded, signed. It is positive with the close above the bar's middle, negative below it, and
    0 at the middle (a zero-range bar has close = mid, so it reads 0). On real bars its size is at most
    (high[t] - low[t]) / close[t] / s. It equals the bar's close position (2 x pos - 1) times the bar's range in
    usual one-bar moves.
    Graded and continuous in the highs, lows and closes. negate gives the fade reading.
    Warm-up: vol_period + 1 rows, bar t included.

    NaN: a NaN high or low of bar t, or a NaN close among the last vol_period + 1 rows, gives NaN. A close not above
    0 among those gives NaN (never on real bars). s = 0 (a flat return window, never on real bars) gives 0.0.
    Building the component raises for a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the high and low of bar t (the last row of data) and the closes of the last
    vol_period + 1 rows, bar t included; every one of them is known at bar t's close.
    """

    def __init__(self, name="CloseOffMidRangeInUsualMoves", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 30))
        if self.vol_period < 2:
            raise ValueError(
                f"CloseOffMidRangeInUsualMovesComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.vol_period
        closes = data['close'].astype(float).iloc[-(n + 1):].to_numpy()
        h = float(data['high'].astype(float).iloc[-1])
        l = float(data['low'].astype(float).iloc[-1])
        if np.isnan(closes).any() or np.isnan(h) or np.isnan(l):
            self._raw_value = float("nan")
        elif not (closes > 0).all():
            self._raw_value = float("nan")
        else:
            rets = closes[1:] / closes[:-1] - 1.0
            s = float(np.std(rets, ddof=1))
            c = float(closes[-1])
            if s == 0:
                self._raw_value = 0.0
            else:
                self._raw_value = float(2.0 * (c - (h + l) / 2.0) / c / s)
            self.debug_info = {'std': s, 'mid': (h + l) / 2.0, 'close': c}
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.vol_period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("vol_period", 30))
    c = [float(x) for x in list(df["close"])]
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    h = hi[t]
    l = lo[t]
    used = [c[t - k] for k in range(n + 1)]
    if h != h or l != l:
        return float("nan")
    for x in used:
        if x != x:
            return float("nan")
        if not x > 0:
            return float("nan")
    rets = []
    for j in range(t - n + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    total = 0.0
    for r in rets:
        total += r
    m = total / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - m) * (r - m)
    s = math.sqrt(ss / (len(rets) - 1))
    if s == 0:
        return 0.0
    mid = (h + l) / 2.0
    return 2.0 * (c[t] - mid) / c[t] / s
```

checks:
CloseOffMidRangeInUsualMovesComponent: every check passed
the bot's suite: == 1678 passed, 16 skipped, 75 deselected, 2244 warnings in 128.89s (0:02:08) ==
