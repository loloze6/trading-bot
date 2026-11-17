# RsiChangeFromPriorLowComponent: night_005_run | 005-02_bullish-rsi-divergence-rebound_1d | RsiLowDivergence

## attempt 1

answer: built
class: RsiChangeFromPriorLowComponent
settings: {"rsi_period": 14, "lookback": 30, "exclude": 3, "rsi_window": 100}
reason: No catalogue class compares the RSI now with the RSI at an earlier closing low. `RSIPullbackComponent` reads only the current RSI, and its value depends on how long the window is. This new class computes RSI(14) at bar t minus RSI(14) at the lowest close of bars t-30 to t-4, each RSI over a fixed 100-change window. The wish's condition "while price is at or below that low" is not built in, because gating on it would make the output on/off. It needs a separate price measure in a regime rule.

table: Directional components
row: | `RsiChangeFromPriorLowComponent` | `rsi_period` (14), `lookback` (30), `exclude` (3), `rsi_window` (100) | RSI(t) - RSI(s), s being the bar of the lowest close among bars t-`lookback` .. t-`exclude`-1 (the most recent one on a tie); RSI(i) = 100 x G / (G + L), G and L being the EWM (alpha 1/`rsi_period`, adjust=False, seeded at the first change) of the gains and losses of the `rsi_window` one-bar close changes ending at bar i; RSI = 50 when G + L = 0 | -100 to +100, signed; positive when the RSI now is above the RSI at the earlier closing low | graded | RSI points | `lookback` + `rsi_window` + 1 (131) | closes only. A NaN close anywhere in the last `lookback` + `rsi_window` + 1 rows gives NaN; `lookback` < 2, `exclude` < 0, `exclude` >= `lookback` - 0 leaving no candidate, `rsi_period` < 1 or `rsi_window` < `rsi_period` raises | stateless; each RSI uses a fixed window of `rsi_window` changes, so the value does not depend on how many bars the run has seen. It does not check that the close is at or below the earlier low: pair it with a price-position measure in a regime rule for the divergence condition |

```python class
class RsiChangeFromPriorLowComponent(SubStrategyComponent):
    """
    The RSI now against the RSI at the earlier lowest close, on every bar:

        s = bar of the lowest close among bars t-lookback .. t-exclude-1 (the most recent such bar on a tie)
        raw_value = RSI(t) - RSI(s)

        RSI(i) = 100 x G / (G + L)   (50 when G + L = 0, no movement at all)
        G, L   = EWM (alpha = 1/rsi_period, adjust=False, seeded with the first value) of the gains max(d, 0) and the
                 losses max(-d, 0) of the rsi_window one-bar close changes d ending at bar i (closes i-rsi_window .. i)

    Range -100 to +100, signed: positive when the RSI now is above the RSI at the earlier closing low (the momentum
    side of a bullish divergence), negative when it is below. Graded in RSI points. It does not test whether the close is
    at or below that low. Warm-up: lookback + rsi_window + 1 rows (131 at the defaults).

    NaN: a NaN close anywhere in the last lookback + rsi_window + 1 rows gives NaN. Nonsensical settings raise at
    construction.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last lookback + rsi_window + 1 rows, the last of
    which is bar t; every RSI is computed from closes at or before its own bar.
    """

    def __init__(self, name="RsiChangeFromPriorLow", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.rsi_period = int(self.parameters.get("rsi_period", 14))
        self.lookback = int(self.parameters.get("lookback", 30))
        self.exclude = int(self.parameters.get("exclude", 3))
        self.rsi_window = int(self.parameters.get("rsi_window", 100))
        if self.rsi_period < 1:
            raise ValueError(f"RsiChangeFromPriorLowComponent: rsi_period must be >= 1, got {self.rsi_period}")
        if self.lookback < 2:
            raise ValueError(f"RsiChangeFromPriorLowComponent: lookback must be >= 2, got {self.lookback}")
        if self.exclude < 0 or self.exclude >= self.lookback:
            raise ValueError(
                f"RsiChangeFromPriorLowComponent: exclude must be in [0, lookback), got {self.exclude}")
        if self.rsi_window < self.rsi_period:
            raise ValueError(
                f"RsiChangeFromPriorLowComponent: rsi_window must be >= rsi_period, got {self.rsi_window}")
        self._raw_value = 0.0

    def _rsi(self, closes, i):
        alpha = 1.0 / self.rsi_period
        seg = closes[i - self.rsi_window:i + 1]
        d = np.diff(seg)
        gains = np.where(d > 0, d, 0.0)
        losses = np.where(d < 0, -d, 0.0)
        g = gains[0]
        l = losses[0]
        for k in range(1, len(d)):
            g = (1.0 - alpha) * g + alpha * gains[k]
            l = (1.0 - alpha) * l + alpha * losses[k]
        if g + l == 0:
            return 50.0
        return 100.0 * g / (g + l)

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        closes = data['close'].iloc[-self.get_required_periods():].astype(float).to_numpy()
        if np.isnan(closes).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        n = len(closes)
        t = n - 1
        s = t - self.lookback
        for i in range(t - self.lookback, t - self.exclude):
            if closes[i] <= closes[s]:
                s = i
        rsi_now = self._rsi(closes, t)
        rsi_low = self._rsi(closes, s)
        self._raw_value = float(rsi_now - rsi_low)
        self.confidence = 1.0
        self.debug_info = {'rsi_now': rsi_now, 'rsi_at_low': rsi_low, 'bars_since_low': t - s,
                           'low_close': float(closes[s])}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.lookback + self.rsi_window + 1
```

```python hand
def hand(df, params):
    p = params.get("rsi_period", 14)
    lb = params.get("lookback", 30)
    ex = params.get("exclude", 3)
    w = params.get("rsi_window", 100)
    c = list(df["close"])
    t = len(c) - 1
    if any(x != x for x in c[t - lb - w:]):
        return float("nan")

    def rsi(i):
        a = 1.0 / p
        g = l = None
        for k in range(i - w + 1, i + 1):
            d = c[k] - c[k - 1]
            up = d if d > 0 else 0.0
            dn = -d if d < 0 else 0.0
            if g is None:
                g, l = up, dn
            else:
                g = (1 - a) * g + a * up
                l = (1 - a) * l + a * dn
        return 50.0 if g + l == 0 else 100.0 * g / (g + l)

    candidates = list(range(t - lb, t - ex))
    low = min(c[i] for i in candidates)
    s = max(i for i in candidates if c[i] == low)
    return rsi(t) - rsi(s)
```

checks:
RsiChangeFromPriorLowComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1519 passed, 8 skipped, 74 deselected, 2170 warnings in 52.43s ========
