# RecentToPriorVolumeScaledReturnComponent: retest_weekend_run | 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h | VolumeRatioWeightedReturnComponent

## attempt 1

answer: built
class: RecentToPriorVolumeScaledReturnComponent
settings: {"period": 48, "window": 720, "base_period": 120}
reason: `ThinVolumeScaledReturnComponent` scales the same return in usual moves by base over recent mean volume, so it grows as volume thins. The wish needs recent over base, which grows as volume gets heavier. That inverse is not a mirror any config step gives, and the two measure opposite things, so it is a new measure in one new class.

table: Directional components
row: | `RecentToPriorVolumeScaledReturnComponent` | `period` (48), `window` (720), `base_period` (120) | (close[t] / close[t-`period`] - 1) / m x (mean(volume[t-`period`+1 .. t]) / mean(volume[t-`period`-`base_period`+1 .. t-`period`])). m = mean over i = t-`window`+1 .. t of abs(close[i] / close[i-`period`] - 1), the overlapping `period`-bar returns ending at each of the last `window` bars, bar t included. The first factor is 0 when m = 0 | unbounded, signed like the `period`-bar return; 0 for a flat move. The size grows with the move in usual `period`-bar moves and with the recent volume against the base just before it. The first factor is at most `window` in size. The volume factor is above 0 and is 1 when the two means are equal. `negate` gives the against-the-move reading | graded | usual `period`-bar moves x volume ratio (recent over prior) | max(`window` + `period`, `period` + `base_period`) (768) | close, volume. A NaN close in the last `window` + `period` rows, or a NaN volume in either volume window, gives NaN. A close not above 0 there gives NaN (never on real bars), and so does a base mean volume not above 0 (never on real bars). m = 0 gives 0 (never on real bars; the return is then 0 too). These settings raise when the component is built: `period` < 1, `window` < 1, `base_period` < 1 | stateless. It equals `MeanAbsScaledReturnComponent` (`period`, `window`) x `VolumeRatioComponent` (`period` = `base_period`, `exclude_current` = `period`, `short_period` = `period`). The volume windows are adjacent and do not overlap: at the defaults, bars t-47 .. t against bars t-167 .. t-48. On 1h bars that is the 48h return in usual 48h moves times the last two days' mean volume over the five days before them. It is not `ThinVolumeScaledReturnComponent`, whose volume factor is the inverse (base over recent). No `scaling_factor`: scale it with transforms |

```python class
class RecentToPriorVolumeScaledReturnComponent(SubStrategyComponent):
    """
    The period-bar return in usual period-bar moves, weighted by recent volume against the volume just before it:

        R      = close[t] / close[t - period] - 1
        m      = mean over i = t-window+1 .. t of abs(close[i] / close[i - period] - 1)
        first  = R / m            (0.0 when m = 0)
        recent = mean(volume[t - period + 1 .. t])
        base   = mean(volume[t - period - base_period + 1 .. t - period])
        raw_value = first * recent / base

    Defaults: period 48, window 720, base_period 120, so the base is bars t-167 .. t-48.
    Range and sign: unbounded and signed like the period-bar return. It is 0 for a flat move. Its size grows
    with the move in usual moves, which is at most `window` because R is one of the averaged returns. It also
    grows with the volume ratio, which is above 0 and is 1 at equal means.
    Warm-up: max(window + period, period + base_period) rows (768 at the defaults), bar t included.
    NaN: a NaN close in the last window + period rows, or a NaN volume in either volume window, gives NaN.
    A close not above 0 there, or a base mean volume not above 0, also gives NaN (never on real bars).
    m = 0 gives 0.
    Building the component raises for period < 1, window < 1 or base_period < 1.

    WHY THIS CANNOT LEAK: it reads only the `close` and `volume` columns of the rows up to and including bar t
    (the last row of data). It reads at most the last max(window + period, period + base_period) rows.
    """

    def __init__(self, name="RecentToPriorVolumeScaledReturn", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 48))
        self.window = int(self.parameters.get("window", 720))
        self.base_period = int(self.parameters.get("base_period", 120))
        if self.period < 1:
            raise ValueError(f"RecentToPriorVolumeScaledReturnComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"RecentToPriorVolumeScaledReturnComponent: window must be >= 1, got {self.window}")
        if self.base_period < 1:
            raise ValueError(
                f"RecentToPriorVolumeScaledReturnComponent: base_period must be >= 1, got {self.base_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        P, W, B = self.period, self.window, self.base_period
        c = data['close'].astype(float).to_numpy()[-(W + P):]
        v = data['volume'].astype(float).to_numpy()
        recent = v[-P:]
        base = v[-(P + B):-P]
        if np.isnan(c).any() or not (c > 0).all() or np.isnan(recent).any() or np.isnan(base).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        base_mean = float(base.mean())
        if not base_mean > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = c[P:] / c[:W] - 1.0
        ret = float(rets[-1])
        m = float(np.abs(rets).mean())
        first = 0.0 if m == 0 else ret / m
        recent_mean = float(recent.mean())
        self._raw_value = float(first * recent_mean / base_mean)
        self.confidence = 1.0
        self.debug_info = {'return': ret, 'mean_abs_return': m, 'recent_volume': recent_mean,
                           'base_volume': base_mean}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.window + self.period, self.period + self.base_period)
```

```python hand
def hand(df, params):
    P = int(params.get("period", 48))
    W = int(params.get("window", 720))
    B = int(params.get("base_period", 120))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    # closes used: bars t-W-P+1 .. t
    for k in range(W + P):
        x = c[t - k]
        if x != x or not x > 0:
            return float("nan")
    recent = [v[t - k] for k in range(P)]             # bars t-P+1 .. t
    base = [v[t - P - k] for k in range(B)]           # bars t-P-B+1 .. t-P
    for x in recent + base:
        if x != x:
            return float("nan")
    base_mean = sum(base) / B
    if not base_mean > 0:
        return float("nan")
    recent_mean = sum(recent) / P
    total = 0.0
    for k in range(W):
        i = t - k
        total += abs(c[i] / c[i - P] - 1.0)
    m = total / W
    ret = c[t] / c[t - P] - 1.0
    first = 0.0 if m == 0 else ret / m
    return first * recent_mean / base_mean
```

checks:
RecentToPriorVolumeScaledReturnComponent: every check passed
the bot's suite: == 1635 passed, 16 skipped, 75 deselected, 2244 warnings in 78.12s (0:01:18) ===
