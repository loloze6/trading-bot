# HighProximityMomentumComponent: night_013_run | 013-02_follow-through-stronger-near-high_1d | HighAnchoredMomentumComponent

## attempt 1

answer: built
class: HighProximityMomentumComponent
settings: {"period": 365, "power": 1.0, "return_period": 30, "proximity": "ratio"}
reason: `HighProximityMomentumComponent` already measures the `return_period`-bar return weighted by closeness to the `period`-bar closing high, but only with the weight (1 / (1 + D))^`power`. That weight never equals close / H on real bars, so the same measure with another proximity statistic is the same component with a new setting, `proximity` ("convex" by default, which keeps today's output exactly; "ratio" gives (close / H)^`power`).

table: Directional components
row: | `HighProximityMomentumComponent` | `period` (365), `power` (2.0), `return_period` (30), `proximity` ("convex") | P x (close[t] - close[t-`return_period`]) / close[t-`return_period`] x 100, H[t] being the highest of the last `period` closes, bar t included. P = (1 / (1 + D))^`power` with D = (H[t] - close[t]) / H[t] x 100 (`proximity` "convex"), or P = (close[t] / H[t])^`power` (`proximity` "ratio") | unbounded, signed; same sign as the `return_period`-bar return; its size is at most that return's size, equal to it at a new high and shrinking the deeper the close sits below the high ("ratio": proportional to close / H at `power` 1) | graded | percent (proximity-weighted) | max(`period`, `return_period` + 1) (365) | closes only. A NaN close in the last `period` rows or at close[t-`return_period`] gives NaN; a highest close or base close not above 0 gives NaN. These settings raise when the component is built: `period` below 2, `power` not above 0, `return_period` below 1, `proximity` other than "convex" or "ratio" | stateless. "convex" equals `ConvexHighProximityComponent` (same `period` and `power`) times `PriceEvolutionOnPeriodComponent` (`comparison_period` = `return_period`). "ratio" with `power` 1 gives the 30-bar return times close / 365-bar high. No `scaling_factor`: scale it with transforms |

```python class
class HighProximityMomentumComponent(SubStrategyComponent):
    """
    A return weighted by how close the close sits to its recent closing high, on every bar:

        H   = max(close[t - period + 1 .. t])                          (bar t included)
        ret = (close[t] - close[t - return_period]) / close[t - return_period] x 100
        proximity "convex" (default): D = (H - close[t]) / H x 100,  P = (1 / (1 + D)) ** power
        proximity "ratio":                                            P = (close[t] / H) ** power
        raw_value = P x ret

    Graded, signed: same sign as the return_period-bar return. P lies in (0, 1] for positive closes,
    so the size is at most |ret|, equal to it at a new high and smaller the deeper the close is below the high.
    Warm-up: max(period, return_period + 1) rows, bar t included.

    NaN: a NaN close in the last period rows or at close[t - return_period] gives NaN. A highest close or base
    close not above 0 also gives NaN.
    Building the component raises for a period below 2, a power not above 0, a return_period below 1, or a
    proximity other than "convex" or "ratio".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the rows up to and including bar t (the last row of
    data). It uses the last period rows and the row return_period bars before t; each close is known at its bar's close.
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
        prox = self.parameters.get("proximity", "convex")
        if prox not in ("convex", "ratio"):
            raise ValueError(
                f"HighProximityMomentumComponent: proximity must be 'convex' or 'ratio', got {prox!r}")
        self.proximity = prox
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = data['close'].astype(float)
        win = closes.iloc[-self.period:].to_numpy(dtype=float)
        c = float(closes.iloc[-1])
        base = float(closes.iloc[-(self.return_period + 1)])
        if np.isnan(win).any() or np.isnan(base) or np.isnan(c):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        h = float(win.max())
        if not h > 0 or not base > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        ret = (c - base) / base * 100.0
        if self.proximity == "convex":
            d = (h - c) / h * 100.0
            p = float(np.power(1.0 / (1.0 + d), self.power))
        else:
            p = float(np.power(c / h, self.power))
        self._raw_value = float(p * ret)
        self.confidence = 1.0
        self.debug_info = {'highest_close': h, 'return_pct': ret, 'proximity_weight': p}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.return_period + 1)
```

```python hand
def hand(df, params):
    n = int(params.get("period", 365))
    pw = float(params.get("power", 2.0))
    r = int(params.get("return_period", 30))
    mode = params.get("proximity", "convex")
    c = [float(x) for x in list(df["close"])]
    last = c[len(c) - 1]
    base = c[len(c) - 1 - r]
    window = c[len(c) - n:]
    for x in window + [base, last]:
        if x != x:
            return float("nan")
    h = window[0]
    for x in window:
        if x > h:
            h = x
    if not h > 0 or not base > 0:
        return float("nan")
    ret = (last / base - 1.0) * 100.0
    if mode == "convex":
        d = (h - last) / h * 100.0
        w = (1.0 / (1.0 + d)) ** pw
    else:
        w = (last / h) ** pw
    return w * ret
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 251, in <module>
    main()
    ~~~~^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 228, in main
    spec = load_spec(args.spec)
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 210, in load_spec
    spec.loader.exec_module(mod)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^
  File "<frozen importlib._bootstrap_external>", line 1023, in exec_module
  File "<frozen importlib._bootstrap_external>", line 1161, in get_code
  File "<frozen importlib._bootstrap_external>", line 1091, in source_to_code
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/user/trading-bot/trading-bot/tests/built_components/HighProximityMomentumComponent.py", line 27
    w = (1.0 / (1.0 + d))  pw
                           ^^
SyntaxError: invalid syntax

## attempt 2

answer: built
class: HighProximityMomentumComponent
settings: {"period": 365, "power": 1.0, "return_period": 30, "proximity": "ratio"}
reason: `HighProximityMomentumComponent` measures the same thing: the 30-bar return weighted by how close the close is to its 365-bar high. Its weight is (1 / (1 + D))^power, and no `power` makes that equal close[t] / H[t] = 1 - D/100, so it does not give the wished value. A `proximity` setting adds the ratio weight; its default "convex" keeps today's output exactly.

table: Directional components
row: | `HighProximityMomentumComponent` | `period` (365), `power` (2.0), `return_period` (30), `proximity` ("convex") | W x (close[t] - close[t-`return_period`]) / close[t-`return_period`] x 100. With `proximity` "convex", W = (1 / (1 + D))^`power`, D = (H[t] - close[t]) / H[t] x 100. With `proximity` "ratio", W = (close[t] / H[t])^`power`. H[t] is the highest of the last `period` closes, bar t included | unbounded, signed; same sign as the `return_period`-bar return; its size is at most that return's size, equal to it at a new high and shrinking the deeper the close sits below the high (with "ratio", towards 0 far below it) | graded | percent (proximity-weighted) | max(`period`, `return_period` + 1) (365) | closes only. A NaN close in the last `period` rows or at close[t-`return_period`] gives NaN; a highest close or base close not above 0 gives NaN. These settings raise when the component is built: a `period` below 2, a `power` not above 0, a `return_period` below 1, a `proximity` other than "convex" or "ratio" | stateless; with "convex" it equals `ConvexHighProximityComponent` x `PriceEvolutionOnPeriodComponent`. "ratio" with `power` 1 gives return x close / 52-week high. No `scaling_factor`: scale it with transforms |

```python class
class HighProximityMomentumComponent(SubStrategyComponent):
    """
    A return weighted by how close the close is to its recent high, on every bar:

        H[t]  = max(close[t - period + 1 .. t])                      (bar t included)
        R     = (close[t] - close[t - return_period]) / close[t - return_period] x 100
        proximity "convex" (default): W = (1 / (1 + D)) ^ power,  D = (H[t] - close[t]) / H[t] x 100
        proximity "ratio":            W = (close[t] / H[t]) ^ power
        raw_value = W x R

    Range and sign: unbounded and signed, with the same sign as R. Since 0 < W <= 1 for positive closes, its size
    is at most |R|. It equals R at a new high and shrinks the further the close sits below the high. Graded.
    Warm-up: max(period, return_period + 1) rows, bar t included.
    NaN: a NaN close in the last period rows or at close[t - return_period] gives NaN. A highest close or base
    close not above 0 also gives NaN.
    Building the component raises for a period below 2, a power not above 0, a return_period below 1, or a
    proximity other than "convex" or "ratio".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the rows up to and including bar t (the last row of
    data): the last period closes and the close return_period rows before bar t.
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
        self.proximity = self.parameters.get("proximity", "convex")
        if self.proximity not in ("convex", "ratio"):
            raise ValueError(
                f"HighProximityMomentumComponent: proximity must be 'convex' or 'ratio', got {self.proximity!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()
        win = c[-self.period:]
        base = float(c[-(self.return_period + 1)])
        ct = float(c[-1])
        self.confidence = 1.0
        if np.isnan(win).any() or np.isnan(base) or np.isnan(ct):
            self._raw_value = float("nan")
            return
        h = float(np.max(win))
        if not h > 0 or not base > 0:
            self._raw_value = float("nan")
            return
        if self.proximity == "convex":
            d = (h - ct) / h * 100.0
            w = float(np.power(1.0 / (1.0 + d), self.power))
        else:
            w = float(np.power(ct / h, self.power))
        ret = (ct - base) / base * 100.0
        self._raw_value = float(w * ret)
        self.debug_info = {'high': h, 'weight': w, 'return_pct': ret}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return max(self.period, self.return_period + 1)
```

```python hand
def hand(df, params):
    n = int(params.get("period", 365))
    pw = float(params.get("power", 2.0))
    rp = int(params.get("return_period", 30))
    prox = params.get("proximity", "convex")
    c = [float(x) for x in list(df["close"])]
    last = c[len(c) - 1]
    base = c[len(c) - 1 - rp]
    window = c[len(c) - n:]
    for x in window + [base, last]:
        if x != x:
            return float("nan")
    h = window[0]
    for x in window:
        if x > h:
            h = x
    if not h > 0 or not base > 0:
        return float("nan")
    ret = (last / base - 1.0) * 100.0
    if prox == "ratio":
        w = pow(last / h, pw)
    else:
        d = (h - last) / h * 100.0
        w = pow(1.0 / (1.0 + d), pw)
    return w * ret
```

checks:
HighProximityMomentumComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1530 passed, 8 skipped, 74 deselected, 2170 warnings in 64.86s (0:01:04) ===
