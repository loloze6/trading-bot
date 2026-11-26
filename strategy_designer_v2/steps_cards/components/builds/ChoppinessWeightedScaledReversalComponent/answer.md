# ChoppinessWeightedScaledReversalComponent: night7c_chopreversal_run | 032-03_reversal-grows-with-choppiness_1d | ChopWeightedScaledReversal

## attempt 1

answer: built
class: ChoppinessWeightedScaledReversalComponent
settings: {"period": 7, "vol_period": 30, "er_period": 30}
reason: No component computes this product. `VolatilityScaledReturnComponent` (period 7, vol_period 30) negated gives the first factor. 1 − ER30 is not available: `EfficiencyRatioRegimeComponent` is EWM-smoothed and stateful, and no config step gives 1 minus a value, so one new class computes the measure.

table: Directional components
row: | `ChoppinessWeightedScaledReversalComponent` | `period` (7), `vol_period` (30), `er_period` (30) | −(close[t] / close[t-`period`] − 1) / (s x sqrt(`period`)) x (1 − ER). s = std (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included. ER = abs(close[t] − close[t-`er_period`]) / sum of abs(close[j] − close[j-1]) over j = t-`er_period`+1 .. t; ER = 0 when that sum is 0. The first factor is 0 when s = 0 | unbounded, signed against the `period`-bar move: positive after a fall, negative after a rise, 0 for a flat move or a straight-line `er_period`-bar trend (ER = 1). Its size grows with the move in usual swings and as the window gets choppier (the weight 1 − ER is 0 to 1) | graded | usual moves x (1 − efficiency ratio) | max(`period`, `vol_period`, `er_period`) + 1 (31) | closes only. A NaN close in the last (warmup) rows gives NaN, and so does a close not above 0 there (never on real bars). s = 0 (a flat return window, never on real bars) gives 0. These settings raise when the component is built: `period` < 1, `vol_period` < 2, `er_period` < 1 | stateless. Equals −`VolatilityScaledReturnComponent` (`period`, `vol_period`) x (1 − raw unsmoothed Kaufman ER(`er_period`)). It is not `EfficiencyRatioRegimeComponent`, which is smoothed. It is continuous in the closes. On 1d bars the defaults give the 7-day reversal in usual 7-day swings, weighted by the 30-day choppiness. No `scaling_factor`: scale it with transforms |

```python class
class ChoppinessWeightedScaledReversalComponent(SubStrategyComponent):
    """
    A reversal of the period-bar move in usual swings, weighted by the choppiness of the er_period window:

        R  = close[t] / close[t - period] - 1
        s  = std (ddof 1) of r[j] = close[j] / close[j-1] - 1, j = t - vol_period + 1 .. t (bar t's return included)
        ER = abs(close[t] - close[t - er_period]) / sum_{j = t-er_period+1 .. t} abs(close[j] - close[j-1])
             (ER = 0 when that sum is 0)
        raw_value = -R / (s * sqrt(period)) * (1 - ER)      (the first factor is 0 when s = 0)

    Range and sign: unbounded and signed against the move. It is positive after a fall and negative after a
    rise. It is 0 for a flat move or a straight-line trend (ER = 1). The weight 1 - ER lies in [0, 1].
    Warm-up: max(period, vol_period, er_period) + 1 rows, bar t included.
    NaN: a NaN close in those rows gives NaN, and so does a close not above 0 there (never on real bars).
    s = 0 (flat return window, never on real bars) gives 0.
    Building raises for period < 1, vol_period < 2, er_period < 1.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, vol_period, er_period) + 1
    rows of data, the last of which is bar t; a close is known at its bar's close.
    """

    def __init__(self, name="ChopWeightedScaledReversal", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 7))
        self.vol_period = int(self.parameters.get("vol_period", 30))
        self.er_period = int(self.parameters.get("er_period", 30))
        if self.period < 1:
            raise ValueError(f"ChoppinessWeightedScaledReversalComponent: period must be >= 1, got {self.period}")
        if self.vol_period < 2:
            raise ValueError(
                f"ChoppinessWeightedScaledReversalComponent: vol_period must be >= 2, got {self.vol_period}")
        if self.er_period < 1:
            raise ValueError(
                f"ChoppinessWeightedScaledReversalComponent: er_period must be >= 1, got {self.er_period}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data["close"].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        t = n - 1
        p, vp, ep = self.period, self.vol_period, self.er_period
        rets = c[t - vp + 1:t + 1] / c[t - vp:t] - 1.0
        s = float(np.std(rets, ddof=1))
        move = float(c[t] / c[t - p] - 1.0)
        total = float(np.abs(np.diff(c[t - ep:t + 1])).sum())
        er = float(abs(c[t] - c[t - ep]) / total) if total > 0 else 0.0
        scaled = 0.0 if s == 0 else -move / (s * float(np.sqrt(p)))
        self._raw_value = float(scaled * (1.0 - er))
        self.confidence = 1.0
        self.debug_info = {"move": move, "std": s, "er": er, "scaled_reversal": scaled}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.period, self.vol_period, self.er_period) + 1
```

```python hand
def hand(df, params):
    import math
    p = int(params.get("period", 7))
    vp = int(params.get("vol_period", 30))
    ep = int(params.get("er_period", 30))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(p, vp, ep) + 1
    window = c[t - need + 1:t + 1]
    for x in window:
        if x != x or not x > 0:
            return float("nan")
    # usual one-bar swing: std (ddof 1) of the vp returns ending at bar t
    rets = []
    for j in range(t - vp + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - mean) ** 2
    s = math.sqrt(ss / (len(rets) - 1))
    # efficiency ratio over ep bars
    path = 0.0
    for j in range(t - ep + 1, t + 1):
        path += abs(c[j] - c[j - 1])
    er = abs(c[t] - c[t - ep]) / path if path > 0 else 0.0
    # reversal of the p-bar move in usual p-bar swings
    move = c[t] / c[t - p] - 1.0
    if s == 0:
        return 0.0
    return -move / (s * math.sqrt(p)) * (1.0 - er)
```

checks:
ChoppinessWeightedScaledReversalComponent: every check passed
the bot's suite: == 1658 passed, 16 skipped, 75 deselected, 2244 warnings in 137.38s (0:02:17) ==
