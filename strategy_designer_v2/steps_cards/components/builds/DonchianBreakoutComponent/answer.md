# DonchianBreakoutComponent: night4_range_run | 023-02_flat-range-bottom-reverts-up.d1_flat-range-bottom-turning-up.d1_flat-range-turn-nearing-middle_1d | RangeMidpointProximity

## attempt 1

answer: built
class: DonchianBreakoutComponent
settings: {"period": 30, "source": "high_low", "form": "below_proximity"}
reason: The wish measures where the close sits against the middle of its 30-bar high–low channel, which is the measure `DonchianBreakoutComponent` (`source` "high_low") already computes, here counted in percent of the mid instead of half-ranges and in a bounded below-the-middle proximity form that no config step gives. The class is rewritten whole with a new `form` setting. Its default "position" keeps today's output exactly.

table: Directional components
row: | `DonchianBreakoutComponent` | `period` (48), `scaling_factor` (20.0), `source` ("close"), `form` ("position") | H, L over bars t-`period`+1 .. t (bar t included). `source` "close": H, L = highest and lowest close. `source` "high_low": H = max(high), L = min(low). `form` "position": (2 x pos − 1) x `sf`, pos = (close[t] − L) / (H − L), pos = 0.5 when H = L. `form` "below_proximity": mid = (H + L) / 2, D = (mid − close[t]) / mid x 100; 1 / (1 + D) when close[t] < mid, 0 when close[t] >= mid (`sf` not used) | "position": −`sf` to +`sf`, signed, positive above the window's middle, 0 at the middle or for a zero range. "below_proximity": 0 to below 1, never negative, no direction; 0 at or above the middle (and for a zero range), above 0 below it, rising toward 1 as the close climbs back to the middle from below; it jumps from near 1 to 0 where the close crosses the middle | graded | "position": forecast units (x `sf`). "below_proximity": dimensionless (0 to 1) | `period` (48) | "close": closes only. "high_low": high and low (last `period` rows) and close[t]. A NaN in any value read gives NaN. With "below_proximity", a mid not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `source` other than "close" or "high_low", `form` other than "position" or "below_proximity" | stateless. `form` "position" (default) is the original output, unchanged. "below_proximity" is the nearness of a close below the channel middle to that middle, in percent of the mid; `sf` is ignored there. It is not a breakout event. No config step gives this bounded form, hence the setting |

```python class
class DonchianBreakoutComponent(SubStrategyComponent):
    """
    Where the close sits against its window's channel, on every bar:

        W = bars t-period+1 .. t (bar t included)
        source = "close" (default): H = max(close[W]), L = min(close[W])
        source = "high_low":        H = max(high[W]),  L = min(low[W])
        form = "position" (default):
            pos = (close[t] - L) / (H - L)   (pos = 0.5 when H = L)
            raw_value = (2 x pos - 1) x scaling_factor
        form = "below_proximity":
            mid = (H + L) / 2
            D = (mid - close[t]) / mid x 100
            raw_value = 1 / (1 + D) if close[t] < mid, else 0.0     (scaling_factor not used)

    Range and sign: "position" is -sf to +sf, signed, positive above the middle of the window, 0 at the middle
    or for a zero range. "below_proximity" is 0 to below 1, never negative, with no direction. It is 0 at or above
    the middle (a zero range puts the close on the middle) and rises toward 1 as a close below the middle
    climbs back to it. It jumps from near 1 to 0 where the close crosses the middle.
    The default form "position" is the original output, unchanged.
    Warm-up: period rows, bar t included.
    NaN: a NaN in any value read gives NaN. With "below_proximity", a mid not above 0 gives NaN (never on real bars).
    Building the component raises for a period below 1, a source other than "close" or "high_low", or a
    form other than "position" or "below_proximity".

    WHY THIS CANNOT LEAK: it reads only the last `period` rows of data (bar t is the last row): the closes, or the
    highs and lows plus close[t]; all of them are known at bar t's close.
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
        self.form = self.parameters.get("form", "position")
        if self.form not in ("position", "below_proximity"):
            raise ValueError(
                f"DonchianBreakoutComponent: form must be 'position' or 'below_proximity', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.period
        close = data['close'].astype(float)
        c = float(close.iloc[-1])
        if self.source == "high_low":
            hi = data['high'].astype(float).iloc[-n:]
            lo = data['low'].astype(float).iloc[-n:]
            if hi.isna().any() or lo.isna().any() or np.isnan(c):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            H = float(hi.max())
            L = float(lo.min())
        else:
            win = close.iloc[-n:]
            if win.isna().any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            H = float(win.max())
            L = float(win.min())
        if self.form == "position":
            rng = H - L
            pos = 0.5 if rng == 0 else (c - L) / rng
            self._raw_value = float((2.0 * pos - 1.0) * self.scaling_factor)
        else:
            mid = (H + L) / 2.0
            if not mid > 0:
                self._raw_value = float("nan")
            elif c < mid:
                d = (mid - c) / mid * 100.0
                self._raw_value = float(1.0 / (1.0 + d))
            else:
                self._raw_value = 0.0
        self.confidence = 1.0
        self.debug_info = {'high': H, 'low': L, 'close': c, 'form': self.form, 'source': self.source}

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
    form = params.get("form", "position")
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    c = closes[last]
    if source == "high_low":
        highs = [float(x) for x in list(df["high"])][last - n + 1:last + 1]
        lows = [float(x) for x in list(df["low"])][last - n + 1:last + 1]
        for x in highs + lows + [c]:
            if x != x:
                return float("nan")
        top = highs[0]
        for x in highs:
            if x > top:
                top = x
        bot = lows[0]
        for x in lows:
            if x < bot:
                bot = x
    else:
        win = closes[last - n + 1:last + 1]
        for x in win:
            if x != x:
                return float("nan")
        top = win[0]
        bot = win[0]
        for x in win:
            if x > top:
                top = x
            if x < bot:
                bot = x
    if form == "position":
        if top == bot:
            pos = 0.5
        else:
            pos = (c - bot) / (top - bot)
        return (2.0 * pos - 1.0) * sf
    middle = (top + bot) / 2.0
    if not middle > 0:
        return float("nan")
    if c >= middle:
        return 0.0
    dist_pct = (middle - c) / middle * 100.0
    return 1.0 / (1.0 + dist_pct)
```

checks:
DonchianBreakoutComponent: every check passed
the bot's suite: == 1614 passed, 16 skipped, 75 deselected, 2244 warnings in 102.09s (0:01:42) ==
