# HighProximityMomentumComponent: night_013_run | 013-01_nearness-to-high-predicts-gains.d1_gain-concentrated-at-the-high_1d | HighProximityMomentumComponent

## attempt 1

answer: built
class: HighProximityMomentumComponent
settings: {"period": 365, "power": 2.0, "return_period": 30}
reason: No component computes this product. `ConvexHighProximityComponent` gives the convex closeness to the 365-bar high, and `PriceEvolutionComponent` / `PriceEvolutionOnPeriodComponent` give the 30-bar percent return, but the catalogue has them only separately. A measure that combines two others is one new class.

table: Directional components
row: | `HighProximityMomentumComponent` | `period` (365), `power` (2.0), `return_period` (30) | P x R, with P = (1 / (1 + D))^`power`, D = (H[t] - close[t]) / H[t] x 100, H[t] the highest of the last `period` closes (bar t included), and R = (close[t] - close[t-`return_period`]) / close[t-`return_period`] x 100 | unbounded, signed; same sign as the `return_period` return; its size is at most abs(R), equals R at a new high, and shrinks convexly the deeper the close sits below the high | graded | percent (proximity-weighted) | max(`period`, `return_period` + 1) (365) | closes only. A NaN close in the last max(`period`, `return_period` + 1) rows that the value uses gives NaN; a highest close or a base close not above 0 gives NaN; `period` < 2, `power` <= 0 or `return_period` < 1 raises when built | stateless; the momentum counts fully only when the close is pressed against its high. No `scaling_factor`: scale it with transforms |

```python class
class HighProximityMomentumComponent(SubStrategyComponent):
    """
    The recent percent return of the close, weighted by how close the close is to its long high (convex), on every bar:

        H[t] = max(close[t - period + 1 .. t])
        D    = (H[t] - close[t]) / H[t] x 100
        P    = (1 / (1 + D)) ** power
        R    = (close[t] - close[t - return_period]) / close[t - return_period] x 100
        raw_value = P x R

    Graded and signed: it has the sign of the return_period return. abs(value) <= abs(R), and value = R at a new high.
    It shrinks convexly as the close falls below its high. It is large and positive when the close is pressed against
    its high after a strong rise, and near 0 far below the high or after a flat stretch.
    Warm-up: max(period, return_period + 1) rows, bar t included.

    NaN: a NaN close in the high window or at either return close gives NaN. A highest close, or a base close
    (close[t - return_period]), that is not above 0 gives NaN. A period below 2, a power not above 0, or a
    return_period below 1 raises when the component is built.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, return_period + 1) rows of data,
    the last row being bar t. A bar's close is known at that bar's close.
    """

    def __init__(self, name="HighProximityMomentum", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"HighProximityMomentumComponent: period must be >= 2, got {self.period}")
        self.power = float(self.parameters.get("power", 2.0))
        if not self.power > 0:
            raise ValueError(f"HighProximityMomentumComponent: power must be > 0, got {self.power}")
        self.return_period = int(self.parameters.get("return_period", 30))
        if self.return_period < 1:
            raise ValueError(
                f"HighProximityMomentumComponent: return_period must be >= 1, got {self.return_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = data['close'].astype(float).to_numpy()
        window = closes[-self.period:]
        last = float(closes[-1])
        base = float(closes[-(self.return_period + 1)])
        nan = float("nan")
        if np.isnan(window).any() or np.isnan(base) or np.isnan(last):
            self._raw_value = nan
            self.confidence = 1.0
            return
        high = float(np.max(window))
        if not high > 0 or not base > 0:
            self._raw_value = nan
            self.confidence = 1.0
            return
        depth = (high - last) / high * 100.0
        proximity = (1.0 / (1.0 + depth)) ** self.power
        ret = (last - base) / base * 100.0
        self._raw_value = float(proximity * ret)
        self.confidence = 1.0
        self.debug_info = {'high': high, 'depth_pct': depth, 'proximity': proximity, 'return_pct': ret}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.return_period + 1)
```

```python hand
def hand(df, params):
    n = int(params.get("period", 365))
    p = float(params.get("power", 2.0))
    k = int(params.get("return_period", 30))
    c = [float(x) for x in list(df["close"])]
    cur = c[-1]
    base = c[-(k + 1)]
    win = c[-n:]
    for x in win + [base, cur]:
        if x != x:
            return float("nan")
    h = win[0]
    for x in win:
        if x > h:
            h = x
    if not h > 0 or not base > 0:
        return float("nan")
    d = (h - cur) / h * 100.0
    prox = (1.0 / (1.0 + d)) ** p
    r = (cur - base) / base * 100.0
    return prox * r
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 36, in <module>
    import strategies.strategy_components as SC  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/strategies/strategy_components.py", line 2610
    proximity = (1.0 / (1.0 + depth))  self.power
                                       ^^^^
SyntaxError: invalid syntax

## attempt 2

answer: built
class: HighProximityMomentumComponent
settings: {"period": 365, "power": 2.0, "return_period": 30}
reason: No component computes this product. `ConvexHighProximityComponent` gives the convex closeness to the 365-bar closing high, and `PriceEvolutionOnPeriodComponent` gives the 30-bar percent return, so one new class computes their product. The earlier attempt failed on a syntax error where the exponent operator was lost. This version raises to the power with `np.power` in the class and `pow` in the hand computation, so no `**` operator appears.

table: Directional components
row: | `HighProximityMomentumComponent` | `period` (365), `power` (2.0), `return_period` (30) | (1 / (1 + D))^`power` x (close[t] - close[t-`return_period`]) / close[t-`return_period`] x 100, with D = (H[t] - close[t]) / H[t] x 100 and H[t] the highest of the last `period` closes, bar t included | unbounded, signed; same sign as the `return_period`-bar return; its size is at most that return's size, equal to it at a new high and shrinking the deeper the close sits below the high | graded | percent (proximity-weighted) | max(`period`, `return_period` + 1) (365) | closes only. A NaN close in the last `period` rows or at close[t-`return_period`] gives NaN; a highest close or base close not above 0 gives NaN; a `period` below 2, a `power` not above 0 or a `return_period` below 1 raises when the component is built | stateless; it equals `ConvexHighProximityComponent` (same `period` and `power`) times `PriceEvolutionOnPeriodComponent` (`comparison_period` = `return_period`). Large and positive only after a strong rise that ends pressed against the high. No `scaling_factor`: scale it with transforms |

```python class
class HighProximityMomentumComponent(SubStrategyComponent):
    """
    The recent return weighted by how close the close sits to its long closing high, on every bar:

        H[t]  = max(close[t - period + 1 .. t])
        D     = (H[t] - close[t]) / H[t] x 100                      (percent below the high, >= 0)
        prox  = (1 / (1 + D)) raised to the power `power`           (in (0, 1], 1 at a new high)
        ret   = (close[t] - close[t - return_period]) / close[t - return_period] x 100
        raw_value = prox x ret

    Graded and signed. It has the sign of the `return_period`-bar return, and its size is at most abs(ret): equal to it
    at a new high and smaller the deeper the close sits below the high. Unbounded.
    Warm-up: max(period, return_period + 1) rows, bar t included (365 at the defaults).

    NaN: a NaN close among the last `period` rows or at close[t - return_period] gives NaN. A highest close that is
    not above 0, or a base close that is not above 0, gives NaN. Invalid settings raise when the component is built.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(period, return_period + 1) rows of data,
    the last row being bar t. A close is known at its bar's close.
    """

    def __init__(self, name="HighProximityMomentum", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 365))
        if self.period < 2:
            raise ValueError(f"HighProximityMomentumComponent: period must be >= 2, got {self.period}")
        self.power = float(self.parameters.get("power", 2.0))
        if not self.power > 0:
            raise ValueError(f"HighProximityMomentumComponent: power must be > 0, got {self.power}")
        self.return_period = int(self.parameters.get("return_period", 30))
        if self.return_period < 1:
            raise ValueError(
                f"HighProximityMomentumComponent: return_period must be >= 1, got {self.return_period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()
        win = c[-self.period:]
        last = float(c[-1])
        base = float(c[-(self.return_period + 1)])
        if np.isnan(win).any() or np.isnan(base) or np.isnan(last):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        high = float(np.max(win))
        if not high > 0 or not base > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        depth = (high - last) / high * 100.0
        proximity = float(np.power(1.0 / (1.0 + depth), self.power))
        ret = (last - base) / base * 100.0
        self._raw_value = float(proximity * ret)
        self.confidence = 1.0
        self.debug_info = {'high': high, 'depth_pct': depth, 'proximity': proximity, 'return_pct': ret}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.return_period + 1)
```

```python hand
def hand(df, params):
    n = int(params.get("period", 365))
    p = float(params.get("power", 2.0))
    r = int(params.get("return_period", 30))
    closes = [float(x) for x in list(df["close"])]
    cur = closes[-1]
    window = closes[len(closes) - n:]
    for x in window:
        if x != x:
            return float("nan")
    old = closes[len(closes) - 1 - r]
    if old != old or cur != cur:
        return float("nan")
    high = window[0]
    for x in window:
        if x > high:
            high = x
    if not high > 0 or not old > 0:
        return float("nan")
    depth = (high - cur) / high * 100.0
    closeness = pow(1.0 / (1.0 + depth), p)
    change = (cur - old) / old * 100.0
    return closeness * change
```

checks:
HighProximityMomentumComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1529 passed, 8 skipped, 74 deselected, 2170 warnings in 58.13s ========
