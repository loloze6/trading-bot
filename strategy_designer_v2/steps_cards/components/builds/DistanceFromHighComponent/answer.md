# DistanceFromHighComponent: night_013_run | 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g2_break-of-30-day-high_1d | PriorHighBreakoutDistance

## attempt 1

answer: built
class: DistanceFromHighComponent
settings: {"period": 30, "source": "high", "exclude_current": 1}
reason: `DistanceFromHighComponent` already measures the percent distance of the close from a recent high. It cannot give this wish's value because it uses closes and includes bar t, so it is never positive and cannot show a break. The wish is the same measure with a different base: the highest `high` of the `period` bars before bar t. So the class is rewritten with two new settings, `source` and `exclude_current`, whose defaults ("close", 0) keep today's output exactly.

table: Directional components
row: | `DistanceFromHighComponent` | `period` (60), `source` ("close"), `exclude_current` (0) | (close[t] - H) / H x 100. H is the highest `source` value (the `close` or `high` column) over the last `period` bars with bar t included (`exclude_current` 0), or over bars t-`period` .. t-1 with bar t excluded (`exclude_current` 1) | `exclude_current` 0: 0 to -100, never positive; 0 at a new high, more negative the deeper below it. `exclude_current` 1: -100 and up, unbounded above, signed; positive and growing as the close clears the prior high further, negative below it | graded | percent | `period` + `exclude_current` (60) | `close`, plus `high` with `source` "high". A NaN in the window or a NaN close[t] gives NaN, and so does an H not above 0. These settings raise when the engine starts: `period` below 2, `source` other than "close" or "high", `exclude_current` not 0 or 1 | stateless. With `period` 30, `source` "high" and `exclude_current` 1 it is the distance of the close beyond the prior 30-bar high (a `clip` with `min` 0 keeps only the break). No `scaling_factor`: scale it with transforms. |

```python class
class DistanceFromHighComponent(SubStrategyComponent):
    """
    Percent distance of the close from a recent high, on every bar:

        exclude_current = 0 (default): H = max(src[t - period + 1 .. t])   (bar t included)
        exclude_current = 1:           H = max(src[t - period .. t - 1])   (bar t excluded)
        raw_value = (close[t] - H) / H x 100

    src is the `close` column (source "close", default) or the `high` column (source "high").
    The defaults (source "close", exclude_current 0) give the original output.

    Range and sign:
    - With exclude_current 0 the value is 0 to -100 and never positive: 0 at a new high, more negative the deeper
      below it.
    - With exclude_current 1 the value is -100 and up, unbounded above: positive and growing as the close clears
      the prior high further, negative below it.
    Graded.

    Warm-up: period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column (and the `high` column with source "high") of the rows up
    to and including bar t (the last row of data), over at most the last period + exclude_current rows. A bar's
    close and high are known at that bar's close.

    NaN: a NaN in the window, a NaN close[t], or an H not above 0 gives NaN.
    Building the component raises for a period below 2, a source other than "close" or "high", or an
    exclude_current other than 0 or 1.
    """

    def __init__(self, name="DistanceFromHigh", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 60))
        if self.period < 2:
            raise ValueError(f"DistanceFromHighComponent: period must be >= 2, got {self.period}")
        src = self.parameters.get("source", "close")
        if src not in ("close", "high"):
            raise ValueError(f"DistanceFromHighComponent: source must be 'close' or 'high', got {src!r}")
        self.source = src
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"DistanceFromHighComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data['close'].astype(float)
        src = data[self.source].astype(float)
        if self.exclude_current:
            win = src.iloc[-(self.period + 1):-1]
        else:
            win = src.iloc[-self.period:]
        last = float(close.iloc[-1])
        if bool(win.isna().any()) or np.isnan(last):
            self._raw_value = float("nan")
            h = float("nan")
        else:
            h = float(win.max())
            if not h > 0:
                self._raw_value = float("nan")
            else:
                self._raw_value = float((last - h) / h * 100.0)
        self.confidence = 1.0
        self.debug_info = {'high_level': h, 'close': last}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    n = int(params.get("period", 60))
    src = params.get("source", "close")
    ex = int(params.get("exclude_current", 0))
    closes = [float(x) for x in list(df["close"])]
    vals = [float(x) for x in list(df[src])]
    m = len(vals)
    if ex == 1:
        window = vals[m - n - 1:m - 1]
    else:
        window = vals[m - n:]
    c = closes[-1]
    if c != c:
        return float("nan")
    for x in window:
        if x != x:
            return float("nan")
    h = window[0]
    for x in window:
        if x > h:
            h = x
    if not h > 0:
        return float("nan")
    return (c - h) / h * 100.0
```

checks:
DistanceFromHighComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1530 passed, 8 skipped, 74 deselected, 2170 warnings in 69.25s (0:01:09) ===
