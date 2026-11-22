# FailedBreakoutDepthVolatilityRatioComponent: short_1d_run | 029-02_breakout-volume-trapped-decline.d2_failed-breakout-in-calm-volatility_1d | FailedBreakoutDepthTimesCalmRatio

## attempt 1

answer: built
class: FailedBreakoutDepthVolatilityRatioComponent
settings: {"period": 20, "fail_window": 3, "exclude_current": 1, "vol_period": 20, "base_vol_period": 60}
reason: No component multiplies the failed-breakout depth by a ratio of volatilities. `FailedBreakoutDepthInUsualMovesComponent` divides the depth by s20 only and has no s60 factor, and `RecentToPriorVolatilityRatioComponent` gives the ratio alone, so this combined measure needs one new class.

table: Directional components
row: | `FailedBreakoutDepthVolatilityRatioComponent` | `period` (20), `fail_window` (3), `exclude_current` (1), `vol_period` (20), `base_vol_period` (60) | max(0, H(j) − close[t]) / H(j) x 100 x s_base / s_recent. j is the most recent bar with close[j] > H(j), searched in t-`fail_window` .. t-1 (`exclude_current` 1, bar t excluded) or t-`fail_window`+1 .. t (`exclude_current` 0). H(j) = max(close[j-`period`] .. close[j-1]). s_recent and s_base are the std (ddof 1) of the last `vol_period` and `base_vol_period` one-bar returns close[i] / close[i-1] − 1, both ending at bar t, bar t's return included. 0 when no bar of the window broke out, or when s_recent = 0 | 0 and up, unbounded above, never negative; no direction. It is 0 when no breakout lies in the window or when close[t] is at or above H(j). With `exclude_current` 0 it is also 0 when bar t itself breaks out. It grows linearly as the close sinks under the old high, and as the recent volatility falls below the longer one (the ratio is 1 at equal volatility) | graded | percent of the old high x ratio of volatilities (base over recent) | max(`period` + `fail_window` + `exclude_current`, `vol_period` + 1, `base_vol_period` + 1) (61) | closes only. A NaN close in the last (warmup) rows gives NaN. A close not above 0 there gives NaN, and so does an H(j) not above 0 (never on real bars). s_recent = 0 (a flat return window, never on real bars) gives 0. These settings raise when the component is built: `period` < 1, `fail_window` < 1, `exclude_current` not 0 or 1, `vol_period` < 2, `base_vol_period` < 2 | stateless. The first factor equals `FailedBreakoutDepthComponent` (`period`, `fail_window`, `source` "close", `reference` "prior_high", same `exclude_current`, `lag` 0). The second factor is the inverse of `RecentToPriorVolatilityRatioComponent` (`vol_period`, `base_period` = `base_vol_period`, `base_lag` 0). A breakout needs a strictly higher close, and only the most recent breakout counts. The value is continuous in close[t] while the same breakout stays the most recent, and drops to 0 when that breakout leaves the window. One-sided, a failed-breakout (short-side) reading. No `scaling_factor`: scale it with transforms |

```python class
class FailedBreakoutDepthVolatilityRatioComponent(SubStrategyComponent):
    """
    Depth of a failed closing breakout under the old high, weighted by how calm the recent bars are:

        j = the most recent bar with close[j] > H(j), H(j) = max(close[j-period] .. close[j-1]),
            searched in t-fail_window .. t-1      (exclude_current = 1, default; bar t excluded)
            or in       t-fail_window+1 .. t      (exclude_current = 0)
        depth = max(0, H(j) - close[t]) / H(j) x 100        (0 when no bar of the window broke out)
        r[i] = close[i] / close[i-1] - 1
        s_recent = std (ddof 1) of r[t-vol_period+1 .. t]
        s_base   = std (ddof 1) of r[t-base_vol_period+1 .. t]
        raw_value = depth x s_base / s_recent               (0 when s_recent = 0)

    Range: 0 and up, unbounded above, never negative; no direction. It is 0 with no breakout in the window, or with
    close[t] at or above H(j). It grows as the close sinks under the old high and as the recent volatility falls
    below the longer one.
    Warm-up: max(period + fail_window + exclude_current, vol_period + 1, base_vol_period + 1) rows, bar t included
    (61 at the defaults).
    NaN: a NaN close in those rows gives NaN, and so does a close not above 0 there or an H(j) not above 0 (never on
    real bars). s_recent = 0 (a flat return window, never on real bars) gives 0.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last warm-up rows of data, the last of them being
    bar t; every breakout test, high and return uses closes at or before bar t.
    """

    def __init__(self, name="FailedBreakoutDepthVolRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 20))
        if self.period < 1:
            raise ValueError(f"FailedBreakoutDepthVolatilityRatioComponent: period must be >= 1, got {self.period}")
        self.fail_window = int(self.parameters.get("fail_window", 3))
        if self.fail_window < 1:
            raise ValueError(
                f"FailedBreakoutDepthVolatilityRatioComponent: fail_window must be >= 1, got {self.fail_window}")
        ex = self.parameters.get("exclude_current", 1)
        if isinstance(ex, bool):
            ex = int(ex)
        if ex not in (0, 1):
            raise ValueError(
                f"FailedBreakoutDepthVolatilityRatioComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"FailedBreakoutDepthVolatilityRatioComponent: vol_period must be >= 2, got {self.vol_period}")
        self.base_vol_period = int(self.parameters.get("base_vol_period", 60))
        if self.base_vol_period < 2:
            raise ValueError(
                f"FailedBreakoutDepthVolatilityRatioComponent: base_vol_period must be >= 2, "
                f"got {self.base_vol_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        t = n - 1
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        if self.exclude_current == 1:
            lo, hi = t - self.fail_window, t - 1
        else:
            lo, hi = t - self.fail_window + 1, t
        depth = 0.0
        hj = None
        for j in range(hi, lo - 1, -1):
            h = float(np.max(c[j - self.period:j]))
            if c[j] > h:
                hj = h
                break
        if hj is not None:
            if not hj > 0:
                self._raw_value = float("nan")
                self.confidence = 1.0
                return
            depth = max(0.0, hj - c[t]) / hj * 100.0
        r = c[1:] / c[:-1] - 1.0
        s_recent = float(np.std(r[-self.vol_period:], ddof=1))
        s_base = float(np.std(r[-self.base_vol_period:], ddof=1))
        if s_recent == 0.0:
            value = 0.0
        else:
            value = depth * s_base / s_recent
        self._raw_value = float(value)
        self.confidence = 1.0
        self.debug_info = {'old_high': hj, 'depth_pct': depth, 's_recent': s_recent, 's_base': s_base}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period + self.fail_window + self.exclude_current,
                   self.vol_period + 1, self.base_vol_period + 1)
```

```python hand
def hand(df, params):
    import math
    period = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    ex = int(params.get("exclude_current", 1))
    vp = int(params.get("vol_period", 20))
    bvp = int(params.get("base_vol_period", 60))
    closes = [float(x) for x in list(df["close"])]
    need = max(period + fw + ex, vp + 1, bvp + 1)
    rows = closes[len(closes) - need:]
    for x in rows:
        if x != x or not x > 0:
            return float("nan")
    t = len(closes) - 1

    # breakout search: most recent bar first
    if ex == 1:
        candidates = list(range(t - 1, t - fw - 1, -1))
    else:
        candidates = list(range(t, t - fw, -1))
    old_high = None
    for j in candidates:
        prior = closes[j - period:j]
        top = prior[0]
        for x in prior:
            if x > top:
                top = x
        if closes[j] > top:
            old_high = top
            break
    depth = 0.0
    if old_high is not None:
        if not old_high > 0:
            return float("nan")
        gap = old_high - closes[t]
        if gap < 0:
            gap = 0.0
        depth = gap / old_high * 100.0

    def sample_std(m):
        rets = []
        for i in range(t - m + 1, t + 1):
            rets.append(closes[i] / closes[i - 1] - 1.0)
        mean = sum(rets) / len(rets)
        ss = 0.0
        for x in rets:
            ss += (x - mean) ** 2
        return math.sqrt(ss / (len(rets) - 1))

    s_recent = sample_std(vp)
    s_base = sample_std(bvp)
    if s_recent == 0.0:
        return 0.0
    return depth * s_base / s_recent
```

checks:
FailedBreakoutDepthVolatilityRatioComponent: every check passed
the bot's suite: == 1633 passed, 16 skipped, 75 deselected, 2244 warnings in 79.57s (0:01:19) ===
