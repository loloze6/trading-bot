# OpenRiseGivebackShareComponent: night10_fallagishort_run | 086-02_rejected-rise-share-fall_1d | OpenRiseGivebackShare

## attempt 1

answer: built
class: OpenRiseGivebackShareComponent
settings: {}
reason: No component divides the close's drop from the bar's high by the rise from the open to the high. `UpperWickComponent` measures high − max(open, close), and `CloseLocationInRangeComponent` ("high") divides by high − low, so neither gives (high − close) / (high − open). One new class computes it, with an optional `cap`.

table: Hedges and filters
row: | `OpenRiseGivebackShareComponent` | `cap` (none) | (high[t] − close[t]) / (high[t] − open[t]) when high[t] > open[t], else 0; with `cap` set, min(that, `cap`) | 0 and up, unbounded above, never negative on real bars; no direction. 0 with the close at the high or when the bar never rose above its open. 1 when the close is back at the open. Above 1 when the close ends below the open. With `cap` 1 the range is 0 to 1 | graded | dimensionless (share of the bar's rise above its open given back) | 1 | open, high, close of bar t only. A NaN in any of the three gives NaN. A missing column raises. These settings raise when the component is built: `cap` set and not a number above 0 | stateless; the shape of the current bar only, with no lookback. `cap` none (default) is the full share. A `clip` on the output with `max` 1 gives the same as `cap` 1, so `cap` is a convenience only. It is continuous in the close. It is unbounded as high[t] − open[t] nears 0 with the close below the open, and jumps to 0 at high[t] = open[t] (a bar that opened at its high). It ignores the low and the volume. Not `UpperWickComponent` (measured from the body top) and not `CloseLocationInRangeComponent` "high" (divided by the whole range). No `scaling_factor`: scale it with transforms |

```python class
class OpenRiseGivebackShareComponent(SubStrategyComponent):
    """
    Share of the bar's rise above its open that the close gave back, on every bar:

        rise     = high[t] - open[t]
        giveback = high[t] - close[t]
        x = giveback / rise when rise > 0, else 0.0
        cap None (default): raw_value = x
        cap c > 0:          raw_value = min(x, c)

    Range and sign: 0 and up, never negative on real bars (close <= high); no direction.
    - 0 when the close is at the high, or when the bar never traded above its open.
    - 1 when the close is back at the open.
    - Above 1 when the close ends below the open, unbounded as the rise nears 0.
    - With cap 1 the range is 0 to 1.
    Graded: continuous in the close. It jumps to 0 at high = open.

    Warm-up: 1 row (bar t).

    NaN: a NaN open, high or close on bar t gives NaN. A missing column raises.
    Building the component raises for a cap that is set and not a number above 0.

    WHY THIS CANNOT LEAK: it reads only the open, high and close of the last row of data (bar t). They are known at
    bar t's close.
    """

    def __init__(self, name="OpenRiseGivebackShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        cap = self.parameters.get("cap", None)
        if cap is not None:
            if isinstance(cap, bool):
                raise ValueError(f"OpenRiseGivebackShareComponent: cap must be a number above 0, got {cap!r}")
            try:
                cap = float(cap)
            except (TypeError, ValueError):
                raise ValueError(f"OpenRiseGivebackShareComponent: cap must be a number above 0, got {cap!r}")
            if not cap > 0 or np.isinf(cap):
                raise ValueError(f"OpenRiseGivebackShareComponent: cap must be a number above 0, got {cap!r}")
        self.cap = cap
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        o = float(data["open"].iloc[-1])
        h = float(data["high"].iloc[-1])
        c = float(data["close"].iloc[-1])
        if np.isnan(o) or np.isnan(h) or np.isnan(c):
            self._raw_value = float("nan")
        else:
            rise = h - o
            if rise > 0:
                x = (h - c) / rise
            else:
                x = 0.0
            if self.cap is not None:
                x = min(x, self.cap)
            self._raw_value = float(x)
        self.confidence = 1.0
        self.debug_info = {"open": o, "high": h, "close": c, "cap": self.cap}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 1
```

```python hand
def hand(df, params):
    cap = params.get("cap", None)
    opens = [float(x) for x in list(df["open"])]
    highs = [float(x) for x in list(df["high"])]
    closes = [float(x) for x in list(df["close"])]
    o = opens[-1]
    h = highs[-1]
    c = closes[-1]
    if o != o or h != h or c != c:
        return float("nan")
    # how far the bar rose above its open, and how much of that the close gave back
    rise = h - o
    if not rise > 0:
        value = 0.0
    else:
        value = (h - c) / rise
    if cap is not None:
        cap = float(cap)
        if value > cap:
            value = cap
    return value
```

checks:
OpenRiseGivebackShareComponent: every check passed
the bot's suite: = 1687 passed, 16 skipped, 75 deselected, 95636 warnings in 146.91s (0:02:26) ==
