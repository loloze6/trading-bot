# BarBodySizeComponent: brief_absorption_run | 030-03_heavy-flat-high-close-reverses_1d | BodyFlatnessComponent

## attempt 1

answer: built
class: BarBodySizeComponent
settings: {"relative_to": "range", "form": "flatness"}
reason: `BarBodySizeComponent` with `relative_to` "range" already computes this measure, abs(close − open) / (high − low). The wish asks for its mirror, 1 minus that value, and no config step gives 1 minus a value. So the same class gets a new `form` setting, "flatness", and its default "body" keeps today's output exactly.

table: Hedges and filters
row: | `BarBodySizeComponent` | `relative_to` ("open"), `form` ("body") | B = abs(close[t] − open[t]). `relative_to` "open": B / open[t] x 100. `relative_to` "range": B / (high[t] − low[t]), 0.0 when high[t] = low[t]. `form` "body": that value. `form` "flatness" (only with `relative_to` "range"): 1 − B / (high[t] − low[t]), 1.0 when high[t] = low[t] | "body", "open": 0 and up, never negative. "body", "range": 0 to 1 on real bars, never negative. "flatness": 0 to 1 on real bars, never negative; 1 when the close equals the open (or for a zero range), 0 when the body spans the whole range, rising as the close nears the open. No direction | graded | "open": percent of the open. "range": dimensionless (share of the bar's range); "flatness": 1 minus that share | 1 | "open": open and close of bar t only. "range": also high and low of bar t. A NaN in any value read gives NaN. With "open", an open not above 0 gives NaN (never on real bars). With "range", a zero range reads 0.0 ("body") or 1.0 ("flatness"), because the body is then 0 on real bars. A missing column raises. These settings raise when the component is built: `relative_to` other than "open" or "range", `form` other than "body" or "flatness", `form` "flatness" with `relative_to` "open" | stateless. `form` "body" (default) is the original output, unchanged. "flatness" is 1 minus the body's share of the range, a doji-like bar reading; no config step gives 1 minus a value, hence the setting. It reads only the shape of the current bar, with no lookback, and is continuous in the close while the range is above 0. Not `OpenToLowDropComponent` and not `CloseLocationInRangeComponent`. No `scaling_factor`: scale it with transforms |

```python class
class BarBodySizeComponent(SubStrategyComponent):
    """
    The size of the current bar's body, the net move from its open, on bar t:

        B = abs(close[t] - open[t])
        relative_to = "open" (default):  body = B / open[t] x 100            (percent of the open)
        relative_to = "range":           body = B / (high[t] - low[t])       (0.0 when high[t] = low[t])
        form = "body" (default):         raw_value = body
        form = "flatness" (needs relative_to "range"):
                                         raw_value = 1 - B / (high[t] - low[t])   (1.0 when high[t] = low[t])

    form "body" is the original output, unchanged. form "flatness" is 1 minus the body's share of the range.
    It equals 1 when the close equals the open (or for a zero range) and 0 when the body spans the whole range.
    It grows continuously as the close nears the open. No config step gives 1 minus a value, hence the setting.

    Range & sign: "open" is 0 and up, never negative. "range" is 0 to 1 on real bars, never negative.
    "flatness" is 0 to 1 on real bars, never negative. None of them has a direction.
    Warm-up: 1 row (bar t only).

    NaN: a NaN in any value read gives NaN. With "open", an open not above 0 gives NaN (never on real bars).
    A missing column raises.
    Building the component raises for a relative_to other than "open" or "range", for a form other than "body"
    or "flatness", and for form "flatness" with relative_to "open".

    WHY THIS CANNOT LEAK: it reads only the open, close (and, for "range", the high and low) of the last row of
    data, bar t itself, all known at that bar's close.
    """

    def __init__(self, name="BarBodySize", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.relative_to = self.parameters.get("relative_to", "open")
        if self.relative_to not in ("open", "range"):
            raise ValueError(
                f"BarBodySizeComponent: relative_to must be 'open' or 'range', got {self.relative_to!r}")
        self.form = self.parameters.get("form", "body")
        if self.form not in ("body", "flatness"):
            raise ValueError(f"BarBodySizeComponent: form must be 'body' or 'flatness', got {self.form!r}")
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
        if self.relative_to == "open":
            if np.isnan(o) or np.isnan(c) or not o > 0:
                value = float("nan")
            else:
                value = abs(c - o) / o * 100.0
        else:
            h = float(data["high"].iloc[-1])
            lo = float(data["low"].iloc[-1])
            if np.isnan(o) or np.isnan(c) or np.isnan(h) or np.isnan(lo):
                value = float("nan")
            else:
                rng = h - lo
                share = 0.0 if rng == 0 else abs(c - o) / rng
                value = (1.0 - share) if self.form == "flatness" else share
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"relative_to": self.relative_to, "form": self.form}

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
        return abs(c - o) / o * 100.0
    h = float(list(df["high"])[-1])
    lo = float(list(df["low"])[-1])
    for x in (o, c, h, lo):
        if x != x:
            return float("nan")
    width = h - lo
    if width == 0:
        body_share = 0.0
    else:
        body_share = abs(c - o) / width
    if form == "flatness":
        return 1.0 - body_share
    return body_share
```

checks:
BarBodySizeComponent: every check passed
the bot's suite: == 1636 passed, 16 skipped, 75 deselected, 2244 warnings in 78.64s (0:01:18) ===
