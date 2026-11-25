# FallCloseLocationComponent: night7_steadydecline_run | 039-02_agitated-range-fall-low-close-rebound_1d | FallInMeanRangesCloseLocationComponent

## attempt 1

answer: built
class: FallCloseLocationComponent
settings: {"vol_period": 30, "base": "mean_bar_range", "exclude_current": 1}
reason: The wish is the day's fall times the close's place in the bar's range, which is the measure `FallCloseLocationComponent` computes, but counted against a different base: the prior 30 days' mean bar range instead of the std of returns ending at bar t. Rule 1 makes that base a setting, so I rewrote the whole class with `base` ("std") and `exclude_current` (0) settings, whose defaults keep today's output unchanged.

table: Directional components
row: | `FallCloseLocationComponent` | `vol_period` (60), `base` ("std"), `exclude_current` (0) | F x (high[t] − close[t]) / (high[t] − low[t]), the location factor 0.5 when high[t] = low[t]. `base` "std": F = max(0, −(close[t] / close[t-1] − 1) / s), s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`exclude_current`-`vol_period`+1 .. t-`exclude_current` (`exclude_current` 0: bar t's return included; 1: bars t-`vol_period` .. t-1); F = 0 when s = 0. `base` "mean_bar_range": F = max(0, close[t-1] − close[t]) / B, B = mean(high[i] − low[i]) over i = t-`exclude_current`-`vol_period`+1 .. t-`exclude_current`; F = 0 when B = 0. With `vol_period` 30, "mean_bar_range", `exclude_current` 1: max(0, close[t-1] − close[t]) / mean(high[i] − low[i], i = t-30 .. t-1) x (high[t] − close[t]) / (high[t] − low[t]) | 0 and up, unbounded above, never negative; no direction; 0 on up bars and flat bars; grows with the depth of today's fall (in usual moves with "std", in mean bar ranges with "mean_bar_range") and as the close nears the bar's low (location 0 to 1 on real bars). With "mean_bar_range" and `exclude_current` 0 the fall factor is at most `vol_period` on real bars | graded | "std": usual moves x share of the bar's range. "mean_bar_range": mean bar ranges x share of the bar's range | "std": `vol_period` + 1 + `exclude_current` (61). "mean_bar_range": max(`vol_period` + `exclude_current`, 2) (31 at the wished settings) | "std": close (the `vol_period` + 1 closes ending at bar t-`exclude_current`, plus close[t-1] and close[t]), high and low of bar t. "mean_bar_range": close[t] and close[t-1], high and low of bar t and of the base rows. A NaN in any value read gives NaN. With "std", a close not above 0 among the return bases or close[t-1] gives NaN (never on real bars). s = 0 or B = 0 gives 0 (never on real bars). These settings raise when the component is built: `vol_period` < 2 with "std", `vol_period` < 1, `base` other than "std" or "mean_bar_range", `exclude_current` not 0 or 1 | stateless. `base` "std" with `exclude_current` 0 (the defaults) is the original output, unchanged. "mean_bar_range" counts the day's close-to-close fall in average bar ranges, the first factor of `BreakoutInMeanRangesComponent` (`period` 1, `side` "below", `high_current` 0, `source` "close", `base_period` = `vol_period`, `base_exclude_current` = `exclude_current`). The location factor is `CloseLocationInRangeComponent` (`reference` "high"). No config step multiplies two components, hence the setting. `exclude_current` 1 keeps bar t's own range or return out of its base. On 1d bars the wished settings give the day's fall in prior 30-day mean daily ranges, times how near the close is to the day's low. Continuous in the prices while the range is above 0, and exactly 0 on every bar that did not close down. One-sided, a rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class FallCloseLocationComponent(SubStrategyComponent):
    """
    The day's fall, scaled by a usual size, times where the close sits in the bar's range:

        loc = (high[t] - close[t]) / (high[t] - low[t])     (0.5 when high[t] = low[t])
        e = exclude_current (0 or 1); the base ends at bar t - e
        base = "std" (default):
            s = std (ddof 1) of the vol_period one-bar returns close[j] / close[j-1] - 1,
                j = t-e-vol_period+1 .. t-e
            F = max(0, -(close[t] / close[t-1] - 1) / s), F = 0 when s = 0
        base = "mean_bar_range":
            B = mean(high[i] - low[i]), i = t-e-vol_period+1 .. t-e
            F = max(0, close[t-1] - close[t]) / B, F = 0 when B = 0
        raw_value = F x loc

    With vol_period 30, base "mean_bar_range" and exclude_current 1 the output is
    max(0, close[t-1] - close[t]) / mean(high[i] - low[i], i = t-30 .. t-1) x (high[t] - close[t]) / (high[t] - low[t]).
    The defaults (base "std", exclude_current 0) are the original output, unchanged.

    Range and sign: 0 and up, unbounded above, never negative; no direction. 0 on up bars and flat bars; grows with
    the fall (in usual moves or in mean bar ranges) and as the close nears the bar's low.
    Warm-up: "std": vol_period + 1 + exclude_current rows; "mean_bar_range": max(vol_period + exclude_current, 2) rows,
    bar t included.
    NaN: a NaN in any value read gives NaN (closes of the return window, close[t-1], close[t], high and low of bar t,
    and with "mean_bar_range" the high and low of the base rows). With "std", a close not above 0 among the return
    bases or close[t-1] gives NaN (never on real bars). s = 0 or B = 0 gives 0 (never on real bars).
    Building the component raises for a vol_period below 2 with "std" (below 1 otherwise), a base other than "std"
    or "mean_bar_range", or an exclude_current other than 0 or 1.

    WHY THIS CANNOT LEAK: it reads only the close, high and low columns of the rows up to and including bar t (the
    last row of data), over at most the last vol_period + 1 + exclude_current rows; every value is known at bar t's
    close.
    """

    def __init__(self, name="FallCloseLocation", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.base = self.parameters.get("base", "std")
        if self.base not in ("std", "mean_bar_range"):
            raise ValueError(
                f"FallCloseLocationComponent: base must be 'std' or 'mean_bar_range', got {self.base!r}")
        self.vol_period = int(self.parameters.get("vol_period", 60))
        if self.base == "std" and self.vol_period < 2:
            raise ValueError(
                f"FallCloseLocationComponent: vol_period must be >= 2 with base 'std', got {self.vol_period}")
        if self.vol_period < 1:
            raise ValueError(f"FallCloseLocationComponent: vol_period must be >= 1, got {self.vol_period}")
        ex = self.parameters.get("exclude_current", 0)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(f"FallCloseLocationComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        close = data["close"].astype(float).to_numpy()
        high = data["high"].astype(float).to_numpy()
        low = data["low"].astype(float).to_numpy()
        n = len(close)
        ex = self.exclude_current
        vp = self.vol_period
        c = close[-1]
        c1 = close[-2]
        h = high[-1]
        lo = low[-1]
        if np.isnan(c) or np.isnan(c1) or np.isnan(h) or np.isnan(lo):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rng = h - lo
        loc = 0.5 if rng == 0 else (h - c) / rng
        if self.base == "std":
            seg = close[n - vp - 1 - ex: n - ex]
            if np.isnan(seg).any() or (seg[:-1] <= 0).any() or not c1 > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            rets = seg[1:] / seg[:-1] - 1.0
            s = float(np.std(rets, ddof=1))
            ret = c / c1 - 1.0
            fall = max(0.0, -ret) / s if s > 0 else 0.0
            scale = s
        else:
            hb = high[n - vp - ex: n - ex]
            lb = low[n - vp - ex: n - ex]
            if np.isnan(hb).any() or np.isnan(lb).any():
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            b = float(np.mean(hb - lb))
            fall = max(0.0, c1 - c) / b if b > 0 else 0.0
            scale = b
        self._raw_value = float(fall * loc)
        self.confidence = 1.0
        self.debug_info = {"fall_factor": fall, "location": loc, "base": self.base, "base_value": scale,
                           "exclude_current": ex}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        if self.base == "std":
            return self.vol_period + 1 + self.exclude_current
        return max(self.vol_period + self.exclude_current, 2)
```

```python hand
def hand(df, params):
    import math
    vp = int(params.get("vol_period", 60))
    base = params.get("base", "std")
    e = int(params.get("exclude_current", 0))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(c) - 1

    def isnan(x):
        return x != x

    if isnan(c[t]) or isnan(c[t - 1]) or isnan(h[t]) or isnan(l[t]):
        return float("nan")
    # where the close sits: 0 at the high, 1 at the low
    if h[t] - l[t] == 0:
        loc = 0.5
    else:
        loc = (h[t] - c[t]) / (h[t] - l[t])

    if base == "std":
        # returns j = t-e-vp+1 .. t-e
        rets = []
        for j in range(t - e - vp + 1, t - e + 1):
            a = c[j - 1]
            b = c[j]
            if isnan(a) or isnan(b):
                return float("nan")
            if not a > 0:
                return float("nan")
            rets.append(b / a - 1.0)
        if not c[t - 1] > 0:
            return float("nan")
        m = sum(rets) / len(rets)
        ss = 0.0
        for r in rets:
            ss += (r - m) * (r - m)
        s = math.sqrt(ss / (len(rets) - 1))
        day_ret = c[t] / c[t - 1] - 1.0
        fall = 0.0
        if s > 0 and day_ret < 0:
            fall = -day_ret / s
    else:
        # mean bar range over i = t-e-vp+1 .. t-e
        total = 0.0
        for i in range(t - e - vp + 1, t - e + 1):
            if isnan(h[i]) or isnan(l[i]):
                return float("nan")
            total += h[i] - l[i]
        mean_range = total / vp
        drop = c[t - 1] - c[t]
        fall = 0.0
        if mean_range > 0 and drop > 0:
            fall = drop / mean_range
    return fall * loc
```

checks:
FallCloseLocationComponent: every check passed
the bot's suite: == 1658 passed, 16 skipped, 75 deselected, 2244 warnings in 120.83s (0:02:00) ==
