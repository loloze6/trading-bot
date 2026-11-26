# DonchianBreakoutComponent: night8_choppycalm_run | 058-02_calm-range-bottom-drifts-up_1d | HighLowRangePosition

## attempt 1

answer: exists
class: DonchianBreakoutComponent
settings: {"period": 20, "scaling_factor": 1.0, "source": "high_low"}
reason: With `source` "high_low", `period` 20 and `sf` 1, the output is 2 x (close[t] − min(low[t-19..t])) / (max(high[t-19..t]) − min(low[t-19..t])) − 1, the wished centred position (0 for a zero range). Its negation, which grows as the close nears the range's bottom, is given exactly by the `negate` config step.

refused: DonchianBreakoutComponent does not take the settings ['source']

## attempt 2

answer: built
class: DonchianBreakoutComponent
settings: {"period": 20, "scaling_factor": 1.0, "source": "high_low"}
reason: `DonchianBreakoutComponent` measures the close's position in its window, but only against the highest and lowest close. The wish needs the same position against the bars' full high-low range, which no config step gives. So the class is written again with a `source` setting whose default "close" keeps today's output exactly, and `negate` then gives the reading that grows near the range's bottom.

table: Directional components
row: | `DonchianBreakoutComponent` | `period` (48), `scaling_factor` (20.0), `source` ("close") | (2 x pos − 1) x `sf`, pos = (close[t] − L) / (H − L) over bars t-`period`+1 .. t (bar t included), pos = 0.5 when H = L. `source` "close": H, L = highest and lowest close. `source` "high_low": H = max(high), L = min(low). With `period` 20, `sf` 1, "high_low": 2 x (close[t] − min(low[t-19..t])) / (max(high[t-19..t]) − min(low[t-19..t])) − 1 | −`sf` to +`sf`, signed; positive above the window's middle, 0 at the middle or for a zero range; +`sf` at the window's top, −`sf` at its bottom | graded | forecast units (x `sf`) | `period` (48) | "close": closes only. "high_low": high and low (last `period` rows) and close[t]. A NaN in any value read gives NaN. These settings raise when the component is built: `period` < 1, `source` other than "close" or "high_low" | stateless. `source` "close" (default) is the original output, unchanged. "high_low" measures the close against the bars' full high-low range, which no config step gives, hence the setting. It is not a breakout event. `negate` gives the near-the-bottom reading |

```python class
class DonchianBreakoutComponent(SubStrategyComponent):
    """
    Where the close sits inside its recent range, on every bar:

        window = bars t-period+1 .. t (bar t included)
        source = "close" (default): H = max(close[window]), L = min(close[window])
        source = "high_low":        H = max(high[window]),  L = min(low[window])
        pos = (close[t] - L) / (H - L), pos = 0.5 when H == L
        raw_value = (2 x pos - 1) x scaling_factor

    With period 20, scaling_factor 1 and source "high_low":
        2 x (close[t] - min(low[t-19..t])) / (max(high[t-19..t]) - min(low[t-19..t])) - 1.
    The defaults (source "close") give the original output, unchanged.
    Range: -scaling_factor to +scaling_factor, signed. It is positive above the window's middle,
    0 at the middle or for a zero range, +sf at the window's top and -sf at its bottom.
    Graded and continuous in the prices while the range is above 0. It is not a breakout event.
    Warm-up: period rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the last `period` rows of data (bar t is the last row).
    "close" reads closes only. "high_low" reads high and low of those rows and close[t].

    NaN: a NaN in any value read gives NaN.
    Building the component raises for a period below 1 or a source other than "close" or "high_low".
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

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        close = data["close"].astype(float)
        c = float(close.iloc[-1])
        if self.source == "close":
            hi = close.iloc[-p:]
            lo = hi
        else:
            hi = data["high"].astype(float).iloc[-p:]
            lo = data["low"].astype(float).iloc[-p:]
        if np.isnan(c) or hi.isna().any() or lo.isna().any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        H = float(hi.max())
        L = float(lo.min())
        if H == L:
            pos = 0.5
        else:
            pos = (c - L) / (H - L)
        self._raw_value = float((2.0 * pos - 1.0) * self.scaling_factor)
        self.confidence = 1.0
        self.debug_info = {"high": H, "low": L, "pos": pos, "source": self.source}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.period
```

```python hand
def hand(df, params):
    p = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    src = params.get("source", "close")
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    c = closes[t]
    if src == "close":
        highs = [closes[t - k] for k in range(p)]
        lows = list(highs)
    else:
        hs = [float(x) for x in list(df["high"])]
        ls = [float(x) for x in list(df["low"])]
        highs = [hs[t - k] for k in range(p)]
        lows = [ls[t - k] for k in range(p)]
    for x in [c] + highs + lows:
        if x != x:
            return float("nan")
    H = highs[0]
    for x in highs:
        if x > H:
            H = x
    L = lows[0]
    for x in lows:
        if x < L:
            L = x
    if H == L:
        pos = 0.5
    else:
        pos = (c - L) / (H - L)
    return (2.0 * pos - 1.0) * sf
```

checks:
DonchianBreakoutComponent: every check passed
the bot's suite: == 1668 passed, 16 skipped, 75 deselected, 2244 warnings in 98.95s (0:01:38) ===

## Note (session E, 2026-11-25 22:50 UTC): the class in force is the one before these builds

The two builds above were asked by a fault, not by a gap: the catalogue's component row for this class was the old one
(`period`, `scaling_factor`), because a night-7 build had written the full row over the class's line in the misleading
names table (`with_row` replaced the first line starting with the class's name). The settings check read the old row and
refused `source`, which the class already had; the rebuild then dropped `form` and `exclude_current`, used by the brief
030 books. Fixed: `with_row` replaces a row only in the component rows (test `test_row_replaced_only_in_the_component_rows`);
the class and its spec are back to the commit before the night (16237e486e), the catalogue's two lines back in their tables.
Proof: on 19 coins' last 400 daily bars, the class before and the class built here give the same value on every bar
(7600 of 7600) for {"period": 20, "scaling_factor": 1.0, "source": "high_low"}, {} and {"period": 20, "scaling_factor": 1.0}.
