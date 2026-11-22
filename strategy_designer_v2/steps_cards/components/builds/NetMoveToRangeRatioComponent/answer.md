# NetMoveToRangeRatioComponent: night4_range_run | 023-03_flatter-range-stronger-reversion_1d | NetMoveToRangeRatio

## attempt 1

answer: built
class: NetMoveToRangeRatioComponent
settings: {"period": 30, "source": "close"}
reason: `NetMoveToRangeRatioComponent` already computes the net move per range, but its range is always max(high) − min(low). The wish divides by the closing range of closes t-29 .. t instead, which differs on real bars. That is the same measure against another base, so the class is rewritten whole with a new `source` setting whose default "high_low" keeps today's output exactly.

table: Regime measures
row: | `NetMoveToRangeRatioComponent` | `period` (30), `source` ("high_low") | abs(close[t] − close[t-`period`]) / (H − L). `source` "high_low": H = max(high[t-`period`+1 .. t]), L = min(low[t-`period`+1 .. t]). `source` "close": H, L = the highest and lowest of close[t-`period`+1 .. t]. 0.0 when H − L is 0 | 0 and up, never negative; no direction; small when the net move is a small part of the range (flat market), 1 when the net move spans the whole range. It is at most 1 whenever close[t-`period`] lies inside [L, H] (as on almost every real bar) and can exceed 1 only when close[t-`period`] lies outside it | regime measure | dimensionless (net move per range) | `period` + 1 (31) | "high_low": close (bars t and t-`period`), high, low (last `period` rows). "close": closes only (last `period` + 1 rows). A NaN in any value read gives NaN. A range of 0 reads 0.0 (`period` identical flat bars for "high_low", `period` equal closes for "close"). These settings raise when the component is built: `period` < 1, `source` other than "high_low" or "close" | stateless; graded, continuous in the prices while the range is above 0. `source` "high_low" (default) is the original output, unchanged. "close" measures the net move against the closing range, the same window and closes as `FlatnessWeightedRangePositionComponent`'s flatness factor (which is 1 minus this). The window's range is bars t-`period`+1 .. t and does not include bar t-`period`, whose close is the base of the move. Not `EfficiencyRatioRegimeComponent`. No `scaling_factor`: scale it with transforms |

```python class
class NetMoveToRangeRatioComponent(SubStrategyComponent):
    """
    The net move over `period` bars per the range of the window, on every bar:

        move = abs(close[t] - close[t - period])
        source = "high_low" (default): H = max(high[t-period+1 .. t]), L = min(low[t-period+1 .. t])
        source = "close":              H = max(close[t-period+1 .. t]), L = min(close[t-period+1 .. t])
        raw_value = move / (H - L), and 0.0 when H - L = 0

    Range & sign: 0 and up, never negative, no direction. It is at most 1 whenever close[t-period] lies inside
    [L, H], as on almost every real bar, and can exceed 1 only when close[t-period] lies outside the window's
    range. Small for a flat market, 1 when the net move spans the whole range. Graded and continuous while the
    range is above 0.
    The default source "high_low" is the original output, unchanged. "close" divides by the closing range instead.
    Warm-up: period + 1 rows, bar t included.

    NaN: a NaN close[t] or close[t-period], or a NaN in the range window (high and low for "high_low", closes for
    "close"), gives NaN. A range of 0 reads 0.0.
    Building the component raises for a period below 1 or a source other than "high_low" or "close".

    WHY THIS CANNOT LEAK: it reads only the rows t-period .. t of the data it is given (the last period + 1 rows,
    bar t being the last row): close[t-period] and close[t], and the high/low or close of the last period rows.
    All of them are known at bar t's close.
    """

    def __init__(self, name="NetMoveToRange", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 30))
        if self.period < 1:
            raise ValueError(f"NetMoveToRangeRatioComponent: period must be >= 1, got {self.period}")
        self.source = self.parameters.get("source", "high_low")
        if self.source not in ("high_low", "close"):
            raise ValueError(
                f"NetMoveToRangeRatioComponent: source must be 'high_low' or 'close', got {self.source!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float)
        c_now = float(close.iloc[-1])
        c_base = float(close.iloc[-(self.period + 1)])
        if self.source == "close":
            win = close.iloc[-self.period:]
            highs = win
            lows = win
        else:
            highs = data["high"].astype(float).iloc[-self.period:]
            lows = data["low"].astype(float).iloc[-self.period:]
        if np.isnan(c_now) or np.isnan(c_base) or highs.isna().any() or lows.isna().any():
            self._raw_value = float("nan")
        else:
            h = float(highs.max())
            l = float(lows.min())
            rng = h - l
            if rng == 0:
                self._raw_value = 0.0
            else:
                self._raw_value = float(abs(c_now - c_base) / rng)
            self.debug_info = {"net_move": abs(c_now - c_base), "range_high": h, "range_low": l,
                               "source": self.source}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period + 1
```

```python hand
def hand(df, params):
    n = int(params.get("period", 30))
    source = params.get("source", "high_low")
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    now = c[last]
    base = c[last - n]
    if source == "close":
        hs = [c[i] for i in range(last - n + 1, last + 1)]
        ls = list(hs)
    else:
        h_all = [float(x) for x in list(df["high"])]
        l_all = [float(x) for x in list(df["low"])]
        hs = [h_all[i] for i in range(last - n + 1, last + 1)]
        ls = [l_all[i] for i in range(last - n + 1, last + 1)]
    for x in [now, base] + hs + ls:
        if x != x:
            return float("nan")
    top = hs[0]
    for x in hs:
        if x > top:
            top = x
    bottom = ls[0]
    for x in ls:
        if x < bottom:
            bottom = x
    width = top - bottom
    if width == 0:
        return 0.0
    move = now - base
    if move < 0:
        move = -move
    return move / width
```

checks:
NetMoveToRangeRatioComponent: every check passed
the bot's suite: == 1612 passed, 16 skipped, 75 deselected, 2244 warnings in 102.62s (0:01:42) ==
