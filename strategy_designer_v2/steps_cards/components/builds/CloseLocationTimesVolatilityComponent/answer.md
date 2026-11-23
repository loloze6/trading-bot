# CloseLocationTimesVolatilityComponent: brief_absorption_run | 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.g2_low-close-rebound-in-volatility_1d | CloseLocationTimesVolatilityComponent

## attempt 1

answer: built
class: CloseLocationTimesVolatilityComponent
settings: {"vol_period": 20}
reason: No component of the catalogue gives the close's location under the bar's high times the plain 20-bar return standard deviation. `FallCloseLocationComponent` divides a fall by that standard deviation instead, `VolumeWeightedCloseLocationVolatilityRatioComponent` adds a volume ratio and uses a volatility ratio rather than the level, and `VolatilityFromStdDevComponent` is a ddof-0 standard deviation of `vol_period − 1` returns based on the current close. A new class computes this product directly.

table: Directional components
row: | `CloseLocationTimesVolatilityComponent` | `vol_period` (20) | (high[t] − close[t]) / (high[t] − low[t]) x s, s being the standard deviation (ddof 1) of the `vol_period` one-bar returns close[j] / close[j-1] − 1, j = t-`vol_period`+1 .. t, bar t's included; the location factor is 0.5 when high[t] = low[t] | 0 and up, never negative on real bars (location 0 to 1); no direction; 0 with the close at the bar's high, growing as the close nears the low and as s rises; at most s | graded | share of the bar's range x fraction of price (std of simple returns) | `vol_period` + 1 (21) | high, low of bar t; closes (last `vol_period` + 1 rows). A NaN in any value read gives NaN; a close not above 0 among the return bases gives NaN (never on real bars). A zero range gives a location of 0.5. These settings raise when the component is built: `vol_period` < 2 | stateless. Equals `CloseLocationInRangeComponent` (`reference` "high") x the ddof-1 standard deviation of the last `vol_period` one-bar returns. Continuous in the close, the highs and lows while the range is above 0. Ignores the open and the volume. One-sided, a low-close-in-volatility (rebound) reading. No `scaling_factor`: scale it with transforms |

```python class
class CloseLocationTimesVolatilityComponent(SubStrategyComponent):
    """
    The close's location under the bar's high times the recent volatility, on every bar:

        loc = (high[t] - close[t]) / (high[t] - low[t])        (0.5 when high[t] = low[t])
        r[j] = close[j] / close[j-1] - 1,  j = t - vol_period + 1 .. t   (bar t's return included)
        s = standard deviation (ddof 1) of those vol_period returns
        raw_value = loc x s

    Range and sign: 0 and up, never negative on real bars (the close lies inside [low, high], so loc is 0 to 1).
    It has no direction. It is 0 with the close at the bar's high, and it grows as the close nears the bar's low
    and as s rises. It is at most s.
    Warm-up: vol_period + 1 rows, bar t included (21 at the default).
    NaN: a NaN high[t], low[t] or a NaN close among the last vol_period + 1 rows gives NaN. A close not above 0
    among the return bases gives NaN (never on real bars). A zero range gives loc = 0.5.
    Building the component raises for a vol_period below 2.

    WHY THIS CANNOT LEAK: it reads high[t], low[t] and the closes of the last vol_period + 1 rows of data, bar t
    (the last row) included and nothing after it; each value is known at its bar's close.
    """

    def __init__(self, name="CloseLocationTimesVolatility", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(
                f"CloseLocationTimesVolatilityComponent: vol_period must be >= 2, got {self.vol_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.vol_period
        closes = data['close'].astype(float).to_numpy()[-(n + 1):]
        h = float(data['high'].iloc[-1])
        l = float(data['low'].iloc[-1])
        c = float(closes[-1])
        if np.isnan(closes).any() or np.isnan(h) or np.isnan(l):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        bases = closes[:-1]
        if not (bases > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        rets = closes[1:] / bases - 1.0
        s = float(np.std(rets, ddof=1))
        rng = h - l
        loc = 0.5 if rng == 0 else (h - c) / rng
        self._raw_value = float(loc * s)
        self.confidence = 1.0
        self.debug_info = {'location': loc, 'volatility': s}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.vol_period + 1
```

```python hand
def hand(df, params):
    import math
    n = int(params.get("vol_period", 20))
    closes = [float(x) for x in list(df["close"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(closes) - 1
    h = highs[t]
    l = lows[t]
    c = closes[t]
    used = [closes[t - k] for k in range(n + 1)]
    for x in used + [h, l]:
        if x != x:
            return float("nan")
    # one-bar returns of bars t-n+1 .. t
    rets = []
    for j in range(t - n + 1, t + 1):
        base = closes[j - 1]
        if not base > 0:
            return float("nan")
        rets.append(closes[j] / base - 1.0)
    total = 0.0
    for r in rets:
        total += r
    mean = total / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - mean) * (r - mean)
    s = math.sqrt(ss / (len(rets) - 1))
    if h == l:
        loc = 0.5
    else:
        loc = (h - c) / (h - l)
    return loc * s
```

checks:
CloseLocationTimesVolatilityComponent: every check passed
the bot's suite: == 1640 passed, 16 skipped, 75 deselected, 2244 warnings in 79.07s (0:01:19) ===
