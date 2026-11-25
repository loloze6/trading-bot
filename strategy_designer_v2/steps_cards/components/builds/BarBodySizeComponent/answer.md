# BarBodySizeComponent: night7_chopreversal_run | 043-01_falling-agitated-intraday-drop-rebound_1d | OpenToCloseDropComponent

## attempt 1

answer: built
class: BarBodySizeComponent
settings: {"relative_to": "open", "form": "drop"}
reason: The catalogue has two near matches, and neither gives the wished quantity. `BarBodySizeComponent` gives the body abs(close − open) / open x 100, which is positive on up bars too, and `OpenToLowDropComponent` reads the low, not the close. The wish is the downward side of the same body measure against the same base, so it is a new value of the existing `form` setting. The default `form` "body" keeps today's output exactly.

table: Hedges and filters
row: | `BarBodySizeComponent` | `relative_to` ("open"), `form` ("body") | B = abs(close[t] − open[t]). `relative_to` "open": B / open[t] x 100. `relative_to` "range": B / (high[t] − low[t]), 0.0 when high[t] = low[t]. `form` "body": that value. `form` "flatness" (only with `relative_to` "range"): 1 − B / (high[t] − low[t]), 1.0 when high[t] = low[t]. `form` "drop": max(0, open[t] − close[t]) over the same base: "open": max(0, open[t] − close[t]) / open[t] x 100; "range": max(0, open[t] − close[t]) / (high[t] − low[t]), 0.0 when high[t] = low[t] | "body", "open": 0 and up, never negative. "body", "range": 0 to 1 on real bars, never negative. "flatness": 0 to 1 on real bars, never negative; 1 when the close equals the open (or for a zero range), 0 when the body spans the whole range. "drop", "open": 0 to below 100 on real bars, never negative; 0 on bars closing at or above their open, growing linearly with the percent fall from open to close. "drop", "range": 0 to 1 on real bars, never negative; 0 on bars closing at or above their open. No direction | graded | "open": percent of the open. "range": dimensionless (share of the bar's range); "flatness": 1 minus that share; "drop": the downward body only, in the same units | 1 | "open": open and close of bar t only. "range": also high and low of bar t. A NaN in any value read gives NaN. With "open", an open not above 0 gives NaN (never on real bars). With "range", a zero range reads 0.0 ("body", "drop") or 1.0 ("flatness"). A missing column raises. These settings raise when the component is built: `relative_to` other than "open" or "range", `form` other than "body", "flatness" or "drop", `form` "flatness" with `relative_to` "open" | stateless. `form` "body" (default) is the original output, unchanged. "flatness" is 1 minus the body's share of the range, a doji-like bar reading; no config step gives 1 minus a value, hence the setting. "drop" is the open-to-close fall of a down bar, 0 on up and flat bars. It is continuous in the close (it meets 0 where the close crosses the open). No config step gives it: `negate` then `clip` would need a signed body, which no component outputs. It reads only the shape of the current bar, with no lookback. Not `OpenToLowDropComponent`, which reads the low, and not `CloseLocationInRangeComponent`. No `scaling_factor`: scale it with transforms |

```python class
class BarBodySizeComponent(SubStrategyComponent):
    """
    The size of the current bar's body, on every bar:

        B = abs(close[t] - open[t])
        relative_to = "open" (default):
            form = "body" (default): B / open[t] x 100
            form = "drop":           max(0, open[t] - close[t]) / open[t] x 100
        relative_to = "range" (R = high[t] - low[t]):
            form = "body":     B / R                          (0.0 when R = 0)
            form = "flatness": 1 - B / R                      (1.0 when R = 0)
            form = "drop":     max(0, open[t] - close[t]) / R (0.0 when R = 0)

    form "body" is the original output, unchanged. form "drop" is the downward body only: it is 0 on bars closing
    at or above their open and grows linearly with the fall from open to close.
    Range: "body", "open": 0 and up. "body", "range" and "flatness": 0 to 1 on real bars. "drop", "open": 0 to below
    100. "drop", "range": 0 to 1 on real bars. Never negative, no direction.
    Warm-up: 1 row (bar t only).

    WHY THIS CANNOT LEAK: it reads only the open and close (and, with relative_to "range", the high and low) of the
    last row of data, bar t, all known at bar t's close.

    NaN: a NaN in any value read gives NaN. With relative_to "open", an open not above 0 gives NaN (never on real
    bars). A missing column raises. Building the component raises for a relative_to other than "open" or "range",
    a form other than "body", "flatness" or "drop", or form "flatness" with relative_to "open".
    """

    def __init__(self, name="BarBodySize", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.relative_to = self.parameters.get("relative_to", "open")
        if self.relative_to not in ("open", "range"):
            raise ValueError(
                f"BarBodySizeComponent: relative_to must be 'open' or 'range', got {self.relative_to!r}")
        self.form = self.parameters.get("form", "body")
        if self.form not in ("body", "flatness", "drop"):
            raise ValueError(
                f"BarBodySizeComponent: form must be 'body', 'flatness' or 'drop', got {self.form!r}")
        if self.form == "flatness" and self.relative_to != "range":
            raise ValueError("BarBodySizeComponent: form 'flatness' needs relative_to 'range'")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        o = float(data["open"].iloc[-1])
        c = float(data["close"].iloc[-1])
        vals = [o, c]
        h = l = float("nan")
        if self.relative_to == "range":
            h = float(data["high"].iloc[-1])
            l = float(data["low"].iloc[-1])
            vals += [h, l]
        if any(np.isnan(v) for v in vals):
            value = float("nan")
        else:
            body = abs(c - o)
            drop = max(0.0, o - c)
            if self.relative_to == "open":
                if not o > 0:
                    value = float("nan")
                elif self.form == "drop":
                    value = drop / o * 100.0
                else:
                    value = body / o * 100.0
            else:
                r = h - l
                if self.form == "flatness":
                    value = 1.0 if r == 0 else 1.0 - body / r
                elif self.form == "drop":
                    value = 0.0 if r == 0 else drop / r
                else:
                    value = 0.0 if r == 0 else body / r
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"open": o, "close": c, "relative_to": self.relative_to, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return 1
```

```python hand
def hand(df, params):
    rel = params.get("relative_to", "open")
    form = params.get("form", "body")
    o = float(list(df["open"])[-1])
    c = float(list(df["close"])[-1])
    if rel == "open":
        if o != o or c != c:
            return float("nan")
        if not o > 0:
            return float("nan")
        if form == "drop":
            fall = o - c
            if fall < 0:
                fall = 0.0
            return fall / o * 100.0
        size = c - o
        if size < 0:
            size = -size
        return size / o * 100.0
    h = float(list(df["high"])[-1])
    l = float(list(df["low"])[-1])
    for x in (o, c, h, l):
        if x != x:
            return float("nan")
    rng = h - l
    size = c - o
    if size < 0:
        size = -size
    if form == "flatness":
        if rng == 0:
            return 1.0
        return 1.0 - size / rng
    if form == "drop":
        if rng == 0:
            return 0.0
        fall = o - c
        if fall < 0:
            fall = 0.0
        return fall / rng
    if rng == 0:
        return 0.0
    return size / rng
```

checks:
BarBodySizeComponent: every check passed
the bot's suite: == 1657 passed, 16 skipped, 75 deselected, 2244 warnings in 131.08s (0:02:11) ==
