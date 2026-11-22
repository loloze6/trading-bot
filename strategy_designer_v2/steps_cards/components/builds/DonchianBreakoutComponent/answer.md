# DonchianBreakoutComponent: night4_range_run | 023-02_flat-range-bottom-reverts-up.d2_flat-range-slide-continues.b2_moderate-flat-range-slide-continues.b1_moderate-flat-range-slide-more-coins_1d | HighLowRangePosition

## attempt 1

answer: exists
class: DonchianBreakoutComponent
settings: {"period": 30, "source": "high_low", "scaling_factor": 1.0}
reason: With `source` "high_low" and `sf` 1, DonchianBreakoutComponent outputs (2 x pos − 1), where pos = (close[t] − L) / (H − L), H = max(high) and L = min(low) over the last `period` bars with bar t included. That equals (close[t] − (H + L) / 2) / ((H − L) / 2) and reads 0 when H = L, exactly the wished measure at `period` 30.

refused: DonchianBreakoutComponent does not take the settings ['source']

## attempt 2

answer: built
class: DonchianBreakoutComponent
settings: {"period": 30, "source": "high_low", "scaling_factor": 1.0}
reason: The wished measure is where the close sits in the window's range. That is the measure `DonchianBreakoutComponent` computes, but today it reads only the closes, and the refused answer shows that the class does not accept `source`. This rewrite of the whole class adds `source` "high_low" (H = max(high), L = min(low)); the default "close" keeps today's output exactly, and at `scaling_factor` 1 the output equals (close[t] − (H + L) / 2) / ((H − L) / 2).

table: Directional components
row: | `DonchianBreakoutComponent` | `period` (48), `scaling_factor` (20.0), `source` ("close") | (2 x pos − 1) x `sf`, pos = (close[t] − L) / (H − L) over bars t-`period`+1 .. t (bar t included). `source` "close": H, L = highest and lowest close. `source` "high_low": H = max(high), L = min(low). pos = 0.5 when H = L. With `source` "high_low" and `sf` 1 it equals (close[t] − (H + L) / 2) / ((H − L) / 2) | −`sf` to +`sf` (−20 to +20 at the default; −1 to +1 at `sf` 1). Bounded on real bars because the close lies inside [L, H]. Signed: positive above the window's middle, negative below it, 0 at the middle or for a zero range | graded | forecast units (x `sf`) | `period` (48) | "close": closes only. "high_low": high and low (last `period` rows) and close[t]. A NaN in any value read gives NaN; a zero range gives 0.0. These settings raise when the component is built: `period` < 1, `source` other than "close" or "high_low" | stateless. `source` "close" (default) is the original output, unchanged. "high_low" is where the close sits in the window's full high–low range, the Donchian channel proper. It is not a breakout event. A negative `sf` or `negate` gives the fade-the-top reading |

```python class
class DonchianBreakoutComponent(SubStrategyComponent):
    """
    Where the close sits inside its recent range, on every bar:

        window = bars t - period + 1 .. t                    (bar t included)
        source = "close" (default): H = max(close[window]), L = min(close[window])
        source = "high_low":        H = max(high[window]),  L = min(low[window])
        pos = (close[t] - L) / (H - L)    (pos = 0.5 when H = L)
        raw_value = (2 x pos - 1) x scaling_factor

    With source "high_low" and scaling_factor 1 this is (close[t] - (H + L) / 2) / ((H - L) / 2).
    Range: -scaling_factor to +scaling_factor, bounded on real bars because the close lies inside [L, H].
    Signed: positive above the window's middle, negative below it, 0 at the middle or for a zero range.
    Graded, not a breakout event. The default source "close" is the original output, unchanged.
    Warm-up: period rows, bar t included.
    NaN: a NaN in any value read (the closes of the window for "close"; the highs and lows of the window and
    close[t] for "high_low") gives NaN. A zero range gives 0.0.
    Building the component raises for a period below 1 or a source other than "close" or "high_low".

    WHY THIS CANNOT LEAK: it reads only the close (and, with "high_low", the high and low) of the last `period`
    rows of data, the last row being bar t; every value is known at bar t's close.
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
        close = data['close'].astype(float).iloc[-self.period:]
        c = float(close.iloc[-1])
        if self.source == "high_low":
            highs = data['high'].astype(float).iloc[-self.period:]
            lows = data['low'].astype(float).iloc[-self.period:]
            if highs.isna().any() or lows.isna().any() or np.isnan(c):
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            h = float(highs.max())
            l = float(lows.min())
        else:
            if close.isna().any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            h = float(close.max())
            l = float(close.min())
        rng = h - l
        pos = 0.5 if rng == 0 else (c - l) / rng
        self._raw_value = float((2.0 * pos - 1.0) * self.scaling_factor)
        self.confidence = 1.0
        self.debug_info = {'high': h, 'low': l, 'pos': pos, 'source': self.source}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period
```

```python hand
def hand(df, params):
    n = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    src = params.get("source", "close")
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    first = last - n + 1
    c = closes[last]
    if src == "high_low":
        highs = [float(x) for x in list(df["high"])]
        lows = [float(x) for x in list(df["low"])]
        hs = highs[first:last + 1]
        ls = lows[first:last + 1]
        for x in hs + ls + [c]:
            if x != x:
                return float("nan")
        top = hs[0]
        for x in hs:
            if x > top:
                top = x
        bot = ls[0]
        for x in ls:
            if x < bot:
                bot = x
    else:
        cs = closes[first:last + 1]
        for x in cs:
            if x != x:
                return float("nan")
        top = cs[0]
        bot = cs[0]
        for x in cs:
            if x > top:
                top = x
            if x < bot:
                bot = x
    if top == bot:
        return 0.0
    mid = (top + bot) / 2.0
    half = (top - bot) / 2.0
    return (c - mid) / half * sf
```

checks:
DonchianBreakoutComponent: every check passed
the bot's suite: == 1612 passed, 16 skipped, 75 deselected, 2244 warnings in 101.84s (0:01:41) ==
