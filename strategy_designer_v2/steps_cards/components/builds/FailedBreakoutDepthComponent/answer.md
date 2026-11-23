# FailedBreakoutDepthComponent: short_1d_run | 029-05_failed-breakout-multiday-drift_1d | FailedBreakoutDepthComponent

## attempt 1

answer: built
class: FailedBreakoutDepthComponent
settings: {"period": 20, "fail_window": 3, "exclude_current": 1, "lag": 2, "source": "close", "reference": "prior_high"}
reason: The catalogue's `FailedBreakoutDepthComponent` computes this measure but always reads it at bar t. The wish is that reading taken at bar t-2: a breakout searched in t-5 .. t-3, with the depth of close[t-2] below the old high. No config step delays a value, so the class is rewritten with a `lag` setting whose default 0 keeps today's output exactly.

table: Directional components
row: | `FailedBreakoutDepthComponent` | `period` (20), `fail_window` (3), `source` ("close"), `reference` ("prior_high"), `exclude_current` (0), `lag` (0) | max(0, R − close[e]) / R x 100, with e = t − `lag`. j is the most recent bar with close[j] > H(j). It is searched in e-`fail_window`+1 .. e (`exclude_current` 0, bar e included) or in e-`fail_window` .. e-1 (`exclude_current` 1, bar e excluded). H(j) = max(close[j-`period`] .. close[j-1]) (`source` "close") or max(high[j-`period`] .. high[j-1]) (`source` "high"). R = H(j) (`reference` "prior_high") or low[j] (`reference` "breakout_low"). The output is 0 when no bar of the window broke out | 0 and up, below 100, never negative; no direction. It is 0 when no breakout lies in the window, or when close[e] is at or above R (with `exclude_current` 0 it is 0 when bar e itself breaks out, and "breakout_low" with j = e is 0 too). It grows linearly as the close at bar e sinks below the level | graded | percent of the level (old high, or breakout bar's low) | `period` + `fail_window` + `exclude_current` + `lag` (23) | "close": closes (bars e-`period`-`fail_window`-`exclude_current`+1 .. e). "high": high (bars e-`period`-`fail_window`-`exclude_current`+1 .. e-`exclude_current`-1) and close (bars e-`fail_window`-`exclude_current`+1 .. e). "breakout_low" also reads low[j] of the chosen bar only. A NaN in any of those gives NaN. An R not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `fail_window` < 1, `source` other than "close" or "high", `reference` other than "prior_high" or "breakout_low", `exclude_current` not 0 or 1, `lag` not an integer >= 0 | stateless. `reference` "prior_high" with `exclude_current` 0 and `lag` 0 (the defaults) is the original output, unchanged. "breakout_low" is the close's depth under the low of the breakout bar, and no config step gives it, hence the setting. `exclude_current` 1 looks for the breakout before bar e only, so a breakout on bar e does not hide an earlier one. `lag` delays the whole reading: bars after t-`lag` are not read, so the value at t is the `lag` 0 value at bar t-`lag`. No config step delays a value, hence the setting. On 1d bars, `period` 20, `fail_window` 3, `exclude_current` 1 and `lag` 2 give a breakout 3 to 5 days ago, with the depth of the close 2 days ago below the old high. A breakout needs a strictly higher close; a tie is not a breakout. Only the most recent breakout of the window counts. The value is continuous in close[e] while the same breakout stays the most recent, and drops to 0 when that breakout leaves the window. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class FailedBreakoutDepthComponent(SubStrategyComponent):
    """
    Depth of a close below the level of a recent breakout that failed, read at bar e = t - lag:

        e = t - lag                                   (lag 0, the default: e = t)
        candidates: exclude_current 0 (default): bars e-fail_window+1 .. e   (bar e included)
                    exclude_current 1:           bars e-fail_window .. e-1   (bar e excluded)
        H(j) = max(close[j-period] .. close[j-1])     (source "close", default)
             = max(high[j-period] .. high[j-1])       (source "high")
        j = the most recent candidate with close[j] > H(j)   (strictly higher: a tie is not a breakout)
        R = H(j)     (reference "prior_high", default)
          = low[j]   (reference "breakout_low")
        raw_value = max(0, R - close[e]) / R x 100,  or 0.0 when no candidate broke out

    Range and sign: 0 and up, below 100, never negative; no direction. It is 0 when no breakout lies in the window
    or when close[e] is at or above R. It grows linearly as close[e] sinks below the level.
    The defaults (reference "prior_high", exclude_current 0, lag 0) are the original output, unchanged.
    lag delays the whole reading: the value at t is the lag-0 value at bar t-lag.
    Warm-up: period + fail_window + exclude_current + lag rows, bar t included.

    NaN: source "close" reads closes of bars e-period-fail_window-exclude_current+1 .. e. Source "high" reads highs
    of bars e-period-fail_window-exclude_current+1 .. e-exclude_current-1 and closes of bars
    e-fail_window-exclude_current+1 .. e. reference "breakout_low" also reads low[j]. A NaN in any value read
    gives NaN, and so does an R not above 0 (never on real bars).
    Building the component raises for period < 1, fail_window < 1, a source other than "close" or "high", a
    reference other than "prior_high" or "breakout_low", an exclude_current other than 0 or 1, or a lag that is
    not an integer >= 0.

    WHY THIS CANNOT LEAK: it reads only rows up to bar e = t - lag (the last row of data minus lag), so it reads
    no row after bar t. Every high, low and close it reads is known at that bar's close.
    """

    def __init__(self, name="FailedBreakoutDepth", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutDepthComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(f"FailedBreakoutDepthComponent: fail_window must be >= 1, got {self.fail_window}")
        self.source = self.parameters.get("source", "close")
        if self.source not in ("close", "high"):
            raise ValueError(f"FailedBreakoutDepthComponent: source must be 'close' or 'high', got {self.source!r}")
        self.reference = self.parameters.get("reference", "prior_high")
        if self.reference not in ("prior_high", "breakout_low"):
            raise ValueError(
                f"FailedBreakoutDepthComponent: reference must be 'prior_high' or 'breakout_low', got {self.reference!r}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"FailedBreakoutDepthComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        lag = self.parameters.get("lag", 0)
        if isinstance(lag, bool):
            lag = int(lag)
        try:
            lag_int = int(lag)
        except (TypeError, ValueError):
            raise ValueError(f"FailedBreakoutDepthComponent: lag must be an integer >= 0, got {lag!r}")
        if lag_int != lag or lag_int < 0:
            raise ValueError(f"FailedBreakoutDepthComponent: lag must be an integer >= 0, got {lag!r}")
        self.lag = lag_int
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        p = self.period
        fw = self.fail_window
        ex = self.exclude_current
        n = len(data)
        e = n - 1 - self.lag
        close = data["close"].astype(float).to_numpy()
        first = e - p - fw - ex + 1
        if self.source == "close":
            src = close
            if np.isnan(close[first:e + 1]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        else:
            src = data["high"].astype(float).to_numpy()
            if np.isnan(src[first:e - ex]).any() or np.isnan(close[e - fw - ex + 1:e + 1]).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
        if ex == 0:
            candidates = range(e, e - fw, -1)
        else:
            candidates = range(e - 1, e - fw - 1, -1)
        found = None
        level = None
        for j in candidates:
            hj = float(np.max(src[j - p:j]))
            if close[j] > hj:
                found = j
                level = hj
                break
        if found is None:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {"breakout_bar": None, "e": e}
            return
        if self.reference == "breakout_low":
            r = float(data["low"].astype(float).iloc[found])
        else:
            r = level
        if np.isnan(r) or not r > 0:
            self._raw_value = float("nan")
        else:
            self._raw_value = float(max(0.0, r - close[e]) / r * 100.0)
        self.confidence = 1.0
        self.debug_info = {"breakout_bar": int(found), "e": e, "H": level, "R": r}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.fail_window + self.exclude_current + self.lag
```

```python hand
def hand(df, params):
    p = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    source = params.get("source", "close")
    reference = params.get("reference", "prior_high")
    ex = int(params.get("exclude_current", 0))
    lag = int(params.get("lag", 0))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])] if "high" in df.columns else None
    lo = [float(x) for x in list(df["low"])] if "low" in df.columns else None
    t = len(c) - 1
    e = t - lag

    def isnan(x):
        return x != x

    # every value the measure reads
    if source == "close":
        for i in range(e - p - fw - ex + 1, e + 1):
            if isnan(c[i]):
                return float("nan")
    else:
        for i in range(e - p - fw - ex + 1, e - ex):
            if isnan(h[i]):
                return float("nan")
        for i in range(e - fw - ex + 1, e + 1):
            if isnan(c[i]):
                return float("nan")

    # candidate breakout bars, most recent first
    if ex == 0:
        cands = [e - k for k in range(fw)]
    else:
        cands = [e - 1 - k for k in range(fw)]
    for j in cands:
        best = None
        for i in range(j - p, j):
            v = c[i] if source == "close" else h[i]
            if best is None or v > best:
                best = v
        if c[j] > best:
            R = best if reference == "prior_high" else lo[j]
            if isnan(R) or not R > 0:
                return float("nan")
            d = R - c[e]
            if d < 0:
                d = 0.0
            return d / R * 100.0
    return 0.0
```

checks:
FailedBreakoutDepthComponent: every check passed
the bot's suite: == 1630 passed, 16 skipped, 75 deselected, 2244 warnings in 78.71s (0:01:18) ===
