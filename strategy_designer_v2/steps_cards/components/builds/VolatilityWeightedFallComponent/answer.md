# VolatilityWeightedFallComponent: retest_monday_run | 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d2_weekend-fall-after-decline.g1_volatile-weekend-fall-rebound_1d | VolatilityWeightedFallComponent

## attempt 1

answer: built
class: VolatilityWeightedFallComponent
settings: {"vol_period": 20}
reason: No component multiplies bar t's fall by the volatility. `VolatilityRankedFallComponent` and `FallCloseLocationComponent` divide the fall by s, so they read it in usual moves, and no config step multiplies one component by another. This new class computes the product directly from closes.

table: Directional components
row: | `VolatilityWeightedFallComponent` | `vol_period` (20) | max(0, -(close[t] / close[t-1] - 1)) x 100 x s, s being the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] - 1, j = t-`vol_period`+1 .. t, bar t's included | 0 and up, unbounded above, never negative; no direction; 0 on up bars and flat bars; grows with the depth of bar t's fall and with the recent volatility | graded | percent x fraction (fall in percent x std of one-bar simple returns) | `vol_period` + 1 (21) | closes only. A NaN close in the last `vol_period` + 1 rows gives NaN; a close not above 0 there gives NaN (never on real bars). `vol_period` < 2 raises when the component is built | stateless. Continuous in the closes; exactly 0 on every bar that did not close down. Not `VolatilityRankedFallComponent`, which divides the fall by s (usual moves) and weights by a rank: this multiplies by s, so a fall in a volatile market reads larger. One-sided, a long-only rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class VolatilityWeightedFallComponent(SubStrategyComponent):
    """
    Bar t's fall weighted by the coin's recent volatility:

        r[j] = close[j] / close[j-1] - 1,  j = t - vol_period + 1 .. t   (bar t's return included)
        s    = std(r, ddof=1)
        raw_value = max(0, -r[t]) x 100 x s

    Range: 0 and up, unbounded above, never negative, no direction. It is 0 on up bars and flat bars, and it grows
    with the depth of bar t's fall (in percent) and with the volatility s of the last vol_period one-bar returns.
    Graded and continuous in the closes.
    Warm-up: vol_period + 1 rows, bar t included.

    NaN: a NaN close in the last vol_period + 1 rows gives NaN. A close not above 0 there also gives NaN (never on
    real bars). Building the component raises for a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last vol_period + 1 rows of data, bar t (the last
    row) included. Each close is known at its bar's close.
    """

    def __init__(self, name="VolatilityWeightedFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"VolatilityWeightedFallComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = data['close'].astype(float).iloc[-(self.vol_period + 1):].to_numpy()
        if np.isnan(closes).any() or (closes <= 0).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = closes[1:] / closes[:-1] - 1.0
        s = float(np.std(rets, ddof=1))
        fall = max(0.0, -float(rets[-1])) * 100.0
        self._raw_value = float(fall * s)
        self.confidence = 1.0
        self.debug_info = {'fall_pct': fall, 'vol': s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.vol_period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    window = c[t - n:t + 1]
    for x in window:
        if x != x or not x > 0:
            return float("nan")
    rets = []
    for j in range(t - n + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean) * (r - mean)
    s = math.sqrt(ss / (len(rets) - 1))
    today = c[t] / c[t - 1] - 1.0
    fall = -today if today < 0 else 0.0
    return fall * 100.0 * s
```

checks:
VolatilityWeightedFallComponent: every check passed
the bot's suite: == 1635 passed, 16 skipped, 75 deselected, 2244 warnings in 76.39s (0:01:16) ===
