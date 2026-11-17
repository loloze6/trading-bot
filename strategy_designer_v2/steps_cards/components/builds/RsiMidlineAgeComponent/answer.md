# RsiMidlineAgeComponent: night_rsi_run | 010-04_rsi-below-streak-continuation_1d | RsiMidlineAgeComponent

## attempt 1

answer: built
class: RsiMidlineAgeComponent
settings: {"period": 14, "max_bars": 60, "rsi_window": 100, "tie_side": "above"}
reason: The catalogue's `RsiMidlineAgeComponent` measures this run length, but it counts an RSI of exactly 50 as below (−n), while the wish counts it as above (+n). This rebuild adds a `tie_side` setting. Its default "below" keeps today's output exactly, and "above" puts RSI = 50 on the positive side, as the wish asks.

table: Regime measures
row: | `RsiMidlineAgeComponent` | `period` (14), `max_bars` (60), `rsi_window` (100), `tie_side` ("below") | +n while bar i is on the upper side on each of the last n bars i = t-n+1 .. t, -n while it is on the lower side on each of them, n being the length of the current run (bar t included), capped at `max_bars`. RSI(i) = 100 x G / (G + L), where G and L are the EWMs (alpha 1/`period`, adjust=False, seeded at the first change) of the gains and losses of the `rsi_window` one-bar close changes ending at bar i; G + L = 0 is RSI 50. Upper side: RSI > 50 (G > L) with `tie_side` "below"; RSI >= 50 (G >= L) with `tie_side` "above" | -`max_bars` .. -1 and +1 .. +`max_bars`, integers, never 0; positive on the upper side, negative on the lower; its size grows by one for each further bar on the same side | regime measure | bars | `max_bars` + `rsi_window` (160) | closes only. A NaN close anywhere in the last `max_bars` + `rsi_window` rows gives NaN. These settings raise when the component is built: `period` < 1, `max_bars` < 1, `rsi_window` < `period`, `tie_side` other than "below" or "above" | stateless; how long the RSI has held its side of the midline. `tie_side` only decides where RSI exactly 50 falls ("below": at or below counts negative, today's output; "above": at or above counts positive). It jumps when the RSI crosses 50 (for example from +`max_bars` to -1), so use it in regime rules, not as a forecast source. No `scaling_factor` |

```python class
class RsiMidlineAgeComponent(SubStrategyComponent):
    """
    How long the RSI has held its side of the midline 50, on every bar:

        RSI(i) = 100 x G(i) / (G(i) + L(i)); G(i), L(i) = EWM (alpha 1/period, adjust=False, seeded at the first
        change) of the gains max(d, 0) and losses max(-d, 0) of the `rsi_window` one-bar close changes d ending at
        bar i. G + L = 0 is RSI 50.
        up(i) = G(i) > L(i)    (RSI > 50; tie_side "below", the default: RSI 50 counts on the lower side)
        up(i) = G(i) >= L(i)   (RSI >= 50; tie_side "above": RSI 50 counts on the upper side)
        n = length of the run of bars ending at t with the same up/down side as bar t, capped at max_bars
        raw_value = +n if up(t) else -n

    Range: -max_bars .. -1 and +1 .. +max_bars, integers, never 0. Positive on the upper side, negative on the lower
    side. The size grows by one for each further bar on the same side.
    Warm-up: max_bars + rsi_window rows, bar t included.
    NaN: a NaN close anywhere in the last max_bars + rsi_window rows gives NaN. `period` < 1, `max_bars` < 1,
    `rsi_window` < `period`, or a `tie_side` other than "below"/"above" raises when the component is built.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max_bars + rsi_window rows of data, the last
    being bar t; every RSI it uses ends at a bar i <= t.
    """

    def __init__(self, name="RsiMidlineAge", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 14))
        self.max_bars = int(self.parameters.get("max_bars", 60))
        self.rsi_window = int(self.parameters.get("rsi_window", 100))
        self.tie_side = self.parameters.get("tie_side", "below")
        if self.period < 1:
            raise ValueError(f"RsiMidlineAgeComponent: period must be >= 1, got {self.period}")
        if self.max_bars < 1:
            raise ValueError(f"RsiMidlineAgeComponent: max_bars must be >= 1, got {self.max_bars}")
        if self.rsi_window < self.period:
            raise ValueError(f"RsiMidlineAgeComponent: rsi_window must be >= period, got {self.rsi_window}")
        if self.tie_side not in ("below", "above"):
            raise ValueError(f"RsiMidlineAgeComponent: tie_side must be 'below' or 'above', got {self.tie_side!r}")
        self._raw_value = 0.0

    def _up(self, closes: np.ndarray) -> bool:
        d = np.diff(closes)
        gains = np.where(d > 0, d, 0.0)
        losses = np.where(d < 0, -d, 0.0)
        a = 1.0 / self.period
        g = float(gains[0])
        l = float(losses[0])
        for k in range(1, len(d)):
            g = (1.0 - a) * g + a * float(gains[k])
            l = (1.0 - a) * l + a * float(losses[k])
        if self.tie_side == "above":
            return g >= l
        return g > l

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        need = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-need:]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        sides = []
        for j in range(self.max_bars):
            end = len(c) - j
            sides.append(self._up(c[end - self.rsi_window - 1:end]))
        side = sides[0]
        n = 1
        while n < self.max_bars and sides[n] == side:
            n += 1
        self._raw_value = float(n if side else -n)
        self.confidence = 1.0
        self.debug_info = {'up': bool(side), 'run': n}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.max_bars + self.rsi_window
```

```python hand
def hand(df, params):
    p = int(params.get("period", 14))
    m = int(params.get("max_bars", 60))
    w = int(params.get("rsi_window", 100))
    tie = params.get("tie_side", "below")
    c = [float(x) for x in list(df["close"])]
    c = c[-(m + w):]
    for x in c:
        if x != x:
            return float("nan")

    def upper(i):
        # bar i (index into c): the w changes ending at i use closes c[i-w] .. c[i]
        a = 1.0 / p
        G = None
        L = None
        for k in range(i - w + 1, i + 1):
            ch = c[k] - c[k - 1]
            gain = ch if ch > 0 else 0.0
            loss = -ch if ch < 0 else 0.0
            if G is None:
                G, L = gain, loss
            else:
                G = (1.0 - a) * G + a * gain
                L = (1.0 - a) * L + a * loss
        # RSI > 50 is G > L; RSI >= 50 is G >= L (G + L = 0 is RSI 50)
        if tie == "above":
            return G >= L
        return G > L

    last = len(c) - 1
    side = upper(last)
    n = 1
    while n < m and upper(last - n) == side:
        n += 1
    return float(n) if side else float(-n)
```

checks:
RsiMidlineAgeComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1526 passed, 8 skipped, 74 deselected, 2170 warnings in 62.09s (0:01:02) ===
