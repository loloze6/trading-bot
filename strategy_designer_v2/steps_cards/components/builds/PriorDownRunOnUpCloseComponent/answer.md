# PriorDownRunOnUpCloseComponent: night9_fallcalmfade_run | 070-01.g1_calm-decline-long-run-break_1d | DownRunLengthBeyondFirstOnUpCloseComponent

## attempt 1

answer: built
class: PriorDownRunOnUpCloseComponent
settings: {"max_bars": 30, "form": "beyond_first"}
reason: `PriorDownRunOnUpCloseComponent` measures the same thing, the length of the down run that bar t's up close breaks, but counts it from the first down day. The wish counts it from the second day instead, max(0, n − 1), and no config step subtracts a constant (`standardise` does not centre). So this is the same class again with a `form` setting, whose default "count" keeps today's output exactly.

table: Regime measures
row: | `PriorDownRunOnUpCloseComponent` | `max_bars` (30), `form` ("count") | when close[t] > close[t-1]: m = min(n, `max_bars`), n = the number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1]; `form` "count": m; `form` "beyond_first": max(0, m − 1); 0 when close[t] <= close[t-1] | "count": 0 to `max_bars` (0 to 30), integers. "beyond_first": 0 to `max_bars` − 1 (0 to 29), integers. Never negative; no direction. Both are 0 on down and flat bars and on an up bar that follows an up or flat bar. "beyond_first" is also 0 on an up bar after a single down day. Both grow by one with each further down bar in the run that bar t breaks | regime measure | bars | `max_bars` + 2 (32) | closes only. A NaN close in the last `max_bars` + 2 rows gives NaN. These settings raise when the component is built: `max_bars` < 1, `form` other than "count" or "beyond_first" | stateless. `form` "count" (default) is the original output, unchanged. "beyond_first" counts the down days of the broken run beyond the first; no config step subtracts a constant, hence the setting. A flat bar (equal close) ends the down run and does not count as the bounce. The value is nonzero only on the first up close after a down run and is 0 again on the next bar, so it jumps. A forecast use that scales it on up-close bars only is a config matter. The cap binds only on a down run longer than `max_bars` bars, which real 1d bars do not show. No `scaling_factor`: scale it with transforms |

```python class
class PriorDownRunOnUpCloseComponent(SubStrategyComponent):
    """
    The length of the down run that bar t's up close breaks:

        if close[t] > close[t-1]:
            n = number of consecutive bars i ending at t-1 (i = t-1, t-2, ...) with close[i] < close[i-1]
            m = min(n, max_bars)
            form = "count" (default):  raw_value = m
            form = "beyond_first":     raw_value = max(0, m - 1)
        else:
            raw_value = 0

    Range and sign: "count" is 0 .. max_bars and "beyond_first" is 0 .. max_bars - 1, both integers, never
    negative, with no direction. Both are 0 on down and flat bars and on an up bar after an up or flat bar.
    "beyond_first" is also 0 on an up bar after a single down day. Each further down bar of the broken run
    adds one. A flat bar ends the down run and is not a bounce. form "count" is the original output, unchanged.
    Warm-up: max_bars + 2 rows, bar t included.

    NaN: a NaN close anywhere in the last max_bars + 2 rows gives NaN.
    Building the component raises for a max_bars below 1 or a form other than "count" or "beyond_first".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max_bars + 2 rows of data (bars
    t-max_bars-1 .. t), the last row being bar t; a bar's close is known at that bar's close.
    """

    def __init__(self, name="PriorDownRunOnUpClose", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.max_bars = int(self.parameters.get("max_bars", 30))
        if self.max_bars < 1:
            raise ValueError(f"PriorDownRunOnUpCloseComponent: max_bars must be >= 1, got {self.max_bars}")
        self.form = self.parameters.get("form", "count")
        if self.form not in ("count", "beyond_first"):
            raise ValueError(
                f"PriorDownRunOnUpCloseComponent: form must be 'count' or 'beyond_first', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data["close"].astype(float).to_numpy()[-(self.max_bars + 2):]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if not c[-1] > c[-2]:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {"run": 0, "form": self.form}
            return
        n = 0
        i = len(c) - 2
        while n < self.max_bars and c[i] < c[i - 1]:
            n += 1
            i -= 1
        if self.form == "beyond_first":
            value = max(0, n - 1)
        else:
            value = n
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {"run": n, "form": self.form}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.max_bars + 2
```

```python hand
def hand(df, params):
    cap = int(params.get("max_bars", 30))
    form = params.get("form", "count")
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    # rows read: bars t-cap-1 .. t
    for k in range(t - cap - 1, t + 1):
        if closes[k] != closes[k]:
            return float("nan")
    if not closes[t] > closes[t - 1]:
        return 0.0
    # count the down closes ending at t-1, walking back
    run = 0
    j = t - 1
    while True:
        if run >= cap:
            break
        if closes[j] < closes[j - 1]:
            run = run + 1
            j = j - 1
        else:
            break
    if form == "beyond_first":
        if run - 1 > 0:
            return float(run - 1)
        return 0.0
    return float(run)
```

checks:
PriorDownRunOnUpCloseComponent: every check passed
the bot's suite: == 1678 passed, 16 skipped, 75 deselected, 2244 warnings in 142.65s (0:02:22) ==
