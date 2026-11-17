# RsiMidlineAgeComponent: night_rsi_run | 010-03_rsi-above-streak-continuation_1d | RsiMidlineAgeComponent

## attempt 1

answer: built
class: RsiMidlineAgeComponent
settings: {"period": 14, "max_bars": 60, "rsi_window": 100}
reason: No component measures how long the RSI has stayed on one side of 50. `RsiAboveMidlineShareComponent` gives the share of bars above 50, not the current streak, and `MovingAverageAgeComponent` dates the close against its SMA, not the RSI against its midline. This new class computes the RSI's run length on its current side. It uses the same fixed-window Wilder RSI as `RsiAboveMidlineShareComponent`, so it keeps no state between bars.

table: Regime measures
row: | `RsiMidlineAgeComponent` | `period` (14), `max_bars` (60), `rsi_window` (100) | +n while RSI(i) > 50 on each of the last n bars i = t-n+1 .. t, -n while RSI(i) <= 50 on each of them, n being the length of the current run (bar t included), capped at `max_bars`. RSI(i) = 100 x G / (G + L), where G and L are the EWMs (alpha 1/`period`, adjust=False, seeded at the first change) of the gains and losses of the `rsi_window` one-bar close changes ending at bar i. RSI > 50 is G > L; G + L = 0 is RSI 50, which counts as at or below | -`max_bars` .. -1 and +1 .. +`max_bars`, integers, never 0; positive while the RSI is above 50, negative while at or below; its size grows by one for each further bar on the same side | regime measure | bars | `max_bars` + `rsi_window` (160) | closes only. A NaN close anywhere in the last `max_bars` + `rsi_window` rows gives NaN. These settings raise when the component is built: `period` < 1, `max_bars` < 1, `rsi_window` < `period` | stateless; how long the RSI has held its side of the midline. It jumps when the RSI crosses 50 (for example from +`max_bars` to -1), so use it in regime rules (for example `gte` 5: above 50 for at least 5 bars), not as a forecast source. No `scaling_factor` |

```python class
class RsiMidlineAgeComponent(SubStrategyComponent):
    """
    How long the RSI has stayed on its current side of 50, on every bar:

        side(i)   = +1 if RSI(i) > 50 (G_i > L_i), else -1   (RSI at or below 50, including G_i + L_i = 0)
        n         = largest k <= max_bars with side(t-k+1) = ... = side(t) = side(t)
        raw_value = side(t) x n

    RSI(i) = 100 x G_i / (G_i + L_i). G_i and L_i are the EWMs (alpha = 1/period, adjust=False, seeded with the first
    change: G = gain_1, then G = (1 - alpha) x G + alpha x gain_k) of the gains max(d, 0) and losses max(-d, 0) of the
    `rsi_window` one-bar close changes d ending at bar i. They read the closes i-rsi_window .. i. Each RSI uses this
    fixed window, so the value does not depend on how many bars the run has seen.

    Range: integers in -max_bars .. -1 and +1 .. +max_bars, never 0. Positive while the RSI is above 50, negative
    while it is at or below. Its size grows by one per further bar on the same side, up to max_bars.
    Warm-up: max_bars + rsi_window rows, bar t included (max_bars RSI values, each needing rsi_window + 1 closes).

    NaN: a NaN close anywhere in the last max_bars + rsi_window rows gives NaN. A missing `close` column raises.
    period < 1, max_bars < 1 or rsi_window < period raises when the component is built.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max_bars + rsi_window rows of data, which end
    at bar t (the last row). Each RSI(i) reads closes i-rsi_window .. i with i <= t, all known at bar t's close.
    """

    def __init__(self, name="RsiMidlineAge", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 14))
        self.max_bars = int(self.parameters.get("max_bars", 60))
        self.rsi_window = int(self.parameters.get("rsi_window", 100))
        if self.period < 1:
            raise ValueError(f"RsiMidlineAgeComponent: period must be >= 1, got {self.period}")
        if self.max_bars < 1:
            raise ValueError(f"RsiMidlineAgeComponent: max_bars must be >= 1, got {self.max_bars}")
        if self.rsi_window < self.period:
            raise ValueError(
                f"RsiMidlineAgeComponent: rsi_window must be >= period, got {self.rsi_window} < {self.period}")
        self._raw_value = 0.0

    def _side(self, closes: np.ndarray) -> int:
        d = np.diff(closes)
        gains = np.where(d > 0, d, 0.0)
        losses = np.where(d < 0, -d, 0.0)
        a = 1.0 / self.period
        g = float(gains[0])
        l = float(losses[0])
        for k in range(1, len(d)):
            g = (1.0 - a) * g + a * float(gains[k])
            l = (1.0 - a) * l + a * float(losses[k])
        return 1 if g > l else -1

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
            self.debug_info = {'nan_close': True}
            return
        sides = []
        for j in range(self.max_bars):
            end = self.rsi_window + j
            sides.append(self._side(c[end - self.rsi_window:end + 1]))
        current = sides[-1]
        n = 0
        for s in reversed(sides):
            if s != current:
                break
            n += 1
        self._raw_value = float(current * n)
        self.confidence = 1.0
        self.debug_info = {'side': current, 'run_length': n}

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
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    for x in closes[len(closes) - (m + w):]:
        if x != x:
            return float("nan")

    def rsi_above(i):
        seg = closes[i - w:i + 1]
        alpha = 1.0 / p
        g = None
        l = None
        for k in range(1, len(seg)):
            ch = seg[k] - seg[k - 1]
            up = ch if ch > 0 else 0.0
            dn = -ch if ch < 0 else 0.0
            if g is None:
                g = up
                l = dn
            else:
                g = g + alpha * (up - g)
                l = l + alpha * (dn - l)
        if g + l == 0:
            return False
        return 100.0 * g / (g + l) > 50.0

    now = rsi_above(last)
    count = 0
    i = last
    while count < m and rsi_above(i) == now:
        count = count + 1
        i = i - 1
    return float(count) if now else float(-count)
```

checks:
RsiMidlineAgeComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1526 passed, 8 skipped, 74 deselected, 2170 warnings in 56.30s ========
