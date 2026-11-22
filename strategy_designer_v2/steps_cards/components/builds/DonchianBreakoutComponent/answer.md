# DonchianBreakoutComponent: night4_range_run | 023-02_flat-range-bottom-reverts-up_1d | HighLowRangeMidpointPosition

## attempt 1

answer: exists
class: DonchianBreakoutComponent
settings: {"period": 30, "source": "high_low", "scaling_factor": 1.0}
reason: With `source` "high_low", H = max(high) and L = min(low) over bars t-29 .. t (bar t included), and at `sf` 1 the output is (2 x pos − 1) = (close[t] − (H + L) / 2) / ((H − L) / 2). It runs −1 to +1 and grows more negative the further the close sits below the range's middle, which is exactly the wished measure; a zero range, which the wish leaves undefined, reads 0.

refused: DonchianBreakoutComponent does not take the settings ['source']

## attempt 2

answer: built
class: DonchianBreakoutComponent
settings: {"period": 30, "scaling_factor": 1.0, "source": "high_low"}
reason: The catalogue's `DonchianBreakoutComponent` measures the same thing, where the close sits in its window's range, but it reads only closes and has no `source` setting. It is written again with `source` "high_low", which takes the range from the highest high and the lowest low. The default "close" keeps today's output exactly, and with `scaling_factor` 1 the value is (close[t] − (H + L) / 2) / ((H − L) / 2).

table: Directional components
row: | `DonchianBreakoutComponent` | `period` (48), `scaling_factor` (20.0), `source` ("close") | (2 x pos − 1) x `sf`, pos = (close[t] − L) / (H − L) over bars t-`period`+1 .. t (bar t included). `source` "close": H, L = highest and lowest close. `source` "high_low": H = max(high), L = min(low). pos = 0.5 when H = L. With `source` "high_low" and `sf` 1 it equals (close[t] − (H + L) / 2) / ((H − L) / 2) | −`sf` to +`sf` (−20 to +20 at the default; −1 to +1 at `sf` 1). Bounded on real bars because the close lies inside [L, H]. Signed: positive above the window's middle, negative below it, 0 at the middle or for a zero range | graded | forecast units (x `sf`) | `period` (48) | "close": closes only. "high_low": high and low (last `period` rows) and close[t]. A NaN in any value read gives NaN; a zero range gives 0.0. These settings raise when the component is built: `period` < 1, `source` other than "close" or "high_low" | stateless. `source` "close" (default) is the original output, unchanged. "high_low" is where the close sits in the window's full high–low range, the Donchian channel proper. It is not a breakout event. A negative `sf` or `negate` gives the fade-the-top reading |

```python class
class DonchianBreakoutComponent(SubStrategyComponent):
    """
    Where the close sits inside its recent range, on every bar:

        W = bars t - period + 1 .. t                     (bar t included)
        source = "close" (default): H = max(close[W]), L = min(close[W])
        source = "high_low":        H = max(high[W]),  L = min(low[W])
        pos = (close[t] - L) / (H - L), pos = 0.5 when H = L
        raw_value = (2 x pos - 1) x scaling_factor

    With source "high_low" and scaling_factor 1 this equals
    (close[t] - (H + L) / 2) / ((H - L) / 2).
    Range and sign: -sf to +sf. It is +sf at the top of the range, -sf at the bottom and 0 at the middle (or for a
    zero range). Graded and continuous. It is not a breakout event. source "close" is the original output, unchanged.
    Warm-up: period rows, bar t included.
    NaN: a NaN close[t], or a NaN in the window's values read (closes, or highs and lows), gives NaN.
    Building the component raises for a period below 1 or a source other than "close" or "high_low".

    WHY THIS CANNOT LEAK: it reads only the last `period` rows of data (close, and high and low with "high_low"),
    the last of which is bar t; every value is known at bar t's close.
    """

    def __init__(self, name="DonchianBreakout", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        if self.period < 1:
            raise ValueError(f"DonchianBreakoutComponent: period must be >= 1, got {self.period}")
        self.scaling_factor = float(self.parameters.get("scaling_factor", 20.0))
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high_low"):
            raise ValueError(
                f"DonchianBreakoutComponent: source must be 'close' or 'high_low', got {self.source!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float)
        c = float(close.iloc[-1])
        if self.source == "high_low":
            hi_w = data['high'].astype(float).iloc[-self.period:]
            lo_w = data['low'].astype(float).iloc[-self.period:]
        else:
            hi_w = close.iloc[-self.period:]
            lo_w = hi_w
        if np.isnan(c) or hi_w.isna().any() or lo_w.isna().any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(hi_w.max())
        L = float(lo_w.min())
        rng = H - L
        pos = 0.5 if rng == 0 else (c - L) / rng
        self._raw_value = float((2.0 * pos - 1.0) * self.scaling_factor)
        self.confidence = 1.0
        self.debug_info = {'high': H, 'low': L, 'pos': pos, 'source': self.source}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period
```

```python hand
def hand(df, params):
    n = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    source = params.get("source", "close")
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    c = closes[last]
    if source == "high_low":
        highs_all = [float(x) for x in list(df["high"])]
        lows_all = [float(x) for x in list(df["low"])]
    else:
        highs_all = closes
        lows_all = closes
    tops = []
    bottoms = []
    i = last - n + 1
    while i <= last:
        tops.append(highs_all[i])
        bottoms.append(lows_all[i])
        i = i + 1
    if c != c:
        return float("nan")
    for x in tops + bottoms:
        if x != x:
            return float("nan")
    H = tops[0]
    for x in tops:
        if x > H:
            H = x
    L = bottoms[0]
    for x in bottoms:
        if x < L:
            L = x
    if H == L:
        return 0.0 * sf
    mid = (H + L) / 2.0
    half = (H - L) / 2.0
    return (c - mid) / half * sf
```

checks:
DonchianBreakoutComponent: every check passed
the bot's suite: == 1611 passed, 16 skipped, 75 deselected, 2244 warnings in 102.05s (0:01:42) ==
