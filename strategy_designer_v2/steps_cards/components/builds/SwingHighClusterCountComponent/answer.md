# SwingHighClusterCountComponent: night3_levels_run | 020-04_support-breakdown-continues-down_1d | SupportTouchCount

## attempt 1

answer: built
class: SwingHighClusterCountComponent
settings: {"period": 90, "side": 2, "band": 1.0, "form": "count", "level": "above", "pivot": "low", "exclude_current": 1}
reason: The wish is the measure `SwingHighClusterCountComponent` already computes: the number of swing points banded around the nearest swing level at or above the close. It is wished on swing lows (strictly below their neighbours) and over bars t-90 .. t-1, values that class does not have. So the class is written again with two new settings, `pivot` ("high", or "low" for this wish) and `exclude_current` (0, or 1 for this wish), whose defaults keep today's output exactly.

table: Regime measures
row: | `SwingHighClusterCountComponent` | `period` (90), `side` (2), `band` (2.0), `form` ("count"), `power` (1.0), `level` ("above"), `pivot` ("high"), `exclude_current` (0) | The window W is the last `period` bars ending at bar t (`exclude_current` 0) or at bar t-1 (`exclude_current` 1: bars t-`period` .. t-1). A swing point is a bar i of W with `side` bars of W before it and `side` after it. With `pivot` "high", high[i] is >= each of those highs and its price is high[i]. With `pivot` "low", low[i] is strictly < each of those lows and its price is low[i]. L is the reference price. With `level` "above" it is the lowest swing price at or above close[t]; with "below" it is the highest swing price strictly below close[t]. N = the number of swing points with abs(price[i] - L) / L x 100 <= `band`, L's own included. "count": N. "proximity": N x (1 / (1 + D))^`power`, where D = (L - close[t]) / L x 100 ("above") or (close[t] - L) / L x 100 ("below"). Both forms are 0 when no swing point sits on the chosen side of close[t] | "count": 0, or an integer from 1 to `period` - 2 x `side`. "proximity": 0 to N. Never negative; no direction. Both grow by one with each further turn near the level | graded | swing points (count), or count x proximity | `period` + `exclude_current` (90) | high (`pivot` "high") or low (`pivot` "low") over W; close (bar t). A NaN in W or a NaN close[t] gives NaN; an L not above 0 gives NaN (never on real bars). These settings raise when the component is built: `side` < 1, `period` < 2 x `side` + 1, `band` not above 0, `form` other than "count" or "proximity", `power` not above 0, `level` other than "above" or "below", `pivot` other than "high" or "low", `exclude_current` not 0 or 1 | stateless. The defaults (`pivot` "high", `exclude_current` 0) are the original output, unchanged. `pivot` "low" counts the turn-ups (support touches) near the level. Swing lows need a strictly lower low (ties do not count, so a flat bottom counts none of its bars), while swing highs count ties (>=). A swing point is confirmed only `side` bars after it, inside W. With `exclude_current` 1, bar t's own high or low cannot make or confirm a swing point. The band is in percent of L, and swing points within it on the other side of the close also count. The value jumps where the close crosses a level. No `scaling_factor`: scale it with transforms |

```python class
class SwingHighClusterCountComponent(SubStrategyComponent):
    """
    How many swing turns cluster at the nearest swing level on one side of the close.

        W = the last `period` bars ending at bar t (exclude_current 0)
            or bars t-period .. t-1 (exclude_current 1)
        swing point: a bar i of W with `side` bars of W before it and `side` after it, such that
            pivot "high" (default): high[i] >= each of those highs, price p[i] = high[i]
            pivot "low":            low[i]  <  each of those lows,  price p[i] = low[i]
        level "above" (default): L = min(p[i] for swing points with p[i] >= close[t])
        level "below":           L = max(p[i] for swing points with p[i] <  close[t])
        N = number of swing points with abs(p[i] - L) / L * 100 <= band   (L's own included)
        form "count" (default): raw_value = N
        form "proximity":       raw_value = N * (1 / (1 + D)) ** power,
            D = (L - close[t]) / L * 100 ("above") or (close[t] - L) / L * 100 ("below")
        raw_value = 0.0 when no swing point lies on the chosen side of close[t].

    The defaults (pivot "high", exclude_current 0) give the original output, unchanged. With pivot "low",
    exclude_current 1, period 90 and level "above", the value is the number of swing lows of bars t-90 .. t-1
    within `band` percent of the nearest swing-low level at or above the close: the touch count of the
    support the close sits under.
    Range: "count" gives 0, or an integer from 1 to period - 2*side; "proximity" gives 0 to N. Never negative,
    no direction. Graded: it grows by one with each further turn near the level.
    Warm-up: period + exclude_current rows, bar t included.
    NaN: a NaN high (pivot "high") or low (pivot "low") anywhere in W, or a NaN close[t], gives NaN.
    An L not above 0 gives NaN (never on real bars).
    Building the component raises for side < 1, period < 2*side + 1, band not above 0, an unknown form, power
    not above 0, an unknown level, a pivot other than "high" or "low", or an exclude_current other than 0 or 1.

    WHY THIS CANNOT LEAK: it reads the high or low column of the rows of W only, which are at most the last
    period + exclude_current rows of data and end at bar t or t-1. It also reads close[t], the last row. A swing
    point is confirmed only by bars inside W, all at or before bar t.
    """

    def __init__(self, name="SwingHighClusterCount", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 90))
        self.side = int(self.parameters.get("side", 2))
        if self.side < 1:
            raise ValueError(f"SwingHighClusterCountComponent: side must be >= 1, got {self.side}")
        if self.period < 2 * self.side + 1:
            raise ValueError(
                f"SwingHighClusterCountComponent: period must be >= 2*side+1, got {self.period}")
        self.band = float(self.parameters.get("band", 2.0))
        if not self.band > 0:
            raise ValueError(f"SwingHighClusterCountComponent: band must be > 0, got {self.band}")
        self.form = self.parameters.get("form", "count")
        if self.form not in ("count", "proximity"):
            raise ValueError(
                f"SwingHighClusterCountComponent: form must be 'count' or 'proximity', got {self.form!r}")
        self.power = float(self.parameters.get("power", 1.0))
        if not self.power > 0:
            raise ValueError(f"SwingHighClusterCountComponent: power must be > 0, got {self.power}")
        self.level = self.parameters.get("level", "above")
        if self.level not in ("above", "below"):
            raise ValueError(
                f"SwingHighClusterCountComponent: level must be 'above' or 'below', got {self.level!r}")
        self.pivot = self.parameters.get("pivot", "high")
        if self.pivot not in ("high", "low"):
            raise ValueError(
                f"SwingHighClusterCountComponent: pivot must be 'high' or 'low', got {self.pivot!r}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(
                f"SwingHighClusterCountComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        col = "high" if self.pivot == "high" else "low"
        p = data[col].astype(float).to_numpy()
        end = len(p) - self.exclude_current
        w = p[end - self.period:end]
        close_t = float(data["close"].astype(float).iloc[-1])
        if np.isnan(w).any() or np.isnan(close_t):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        s = self.side
        prices = []
        for j in range(s, self.period - s):
            v = w[j]
            nb = np.concatenate([w[j - s:j], w[j + 1:j + s + 1]])
            if self.pivot == "high":
                ok = bool(np.all(v >= nb))
            else:
                ok = bool(np.all(v < nb))
            if ok:
                prices.append(float(v))
        if self.level == "above":
            cands = [x for x in prices if x >= close_t]
        else:
            cands = [x for x in prices if x < close_t]
        if not cands:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {"swing_points": len(prices), "level": None, "count": 0}
            return
        L = min(cands) if self.level == "above" else max(cands)
        if not L > 0:
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = 0
        for x in prices:
            if abs(x - L) / L * 100.0 <= self.band:
                n += 1
        if self.form == "count":
            val = float(n)
        else:
            if self.level == "above":
                d = (L - close_t) / L * 100.0
            else:
                d = (close_t - L) / L * 100.0
            val = float(n * (1.0 / (1.0 + d)) ** self.power)
        self._raw_value = val
        self.confidence = 1.0
        self.debug_info = {"swing_points": len(prices), "level": L, "count": n}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.exclude_current
```

```python hand
def hand(df, params):
    period = int(params.get("period", 90))
    side = int(params.get("side", 2))
    band = float(params.get("band", 2.0))
    form = params.get("form", "count")
    power = float(params.get("power", 1.0))
    level = params.get("level", "above")
    pivot = params.get("pivot", "high")
    ex = int(params.get("exclude_current", 0))
    col = "high" if pivot == "high" else "low"
    vals = [float(x) for x in list(df[col])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    close_t = closes[t]
    last = t - ex                      # last bar of the window
    first = last - period + 1          # first bar of the window
    for k in range(first, last + 1):
        if vals[k] != vals[k]:
            return float("nan")
    if close_t != close_t:
        return float("nan")
    swings = []
    i = first + side
    while i <= last - side:
        is_swing = True
        for k in range(i - side, i + side + 1):
            if k == i:
                continue
            if pivot == "high":
                if not vals[i] >= vals[k]:
                    is_swing = False
            else:
                if not vals[i] < vals[k]:
                    is_swing = False
        if is_swing:
            swings.append(vals[i])
        i += 1
    L = None
    for x in swings:
        if level == "above":
            if x >= close_t and (L is None or x < L):
                L = x
        else:
            if x < close_t and (L is None or x > L):
                L = x
    if L is None:
        return 0.0
    if not L > 0:
        return float("nan")
    n = 0
    for x in swings:
        if abs(x - L) / L * 100.0 <= band:
            n += 1
    if form == "count":
        return float(n)
    if level == "above":
        d = (L - close_t) / L * 100.0
    else:
        d = (close_t - L) / L * 100.0
    return float(n * (1.0 / (1.0 + d)) ** power)
```

checks:
SwingHighClusterCountComponent: every check passed
the bot's suite: ======= 1582 passed, 16 skipped, 75 deselected, 2244 warnings in 57.27s ========
