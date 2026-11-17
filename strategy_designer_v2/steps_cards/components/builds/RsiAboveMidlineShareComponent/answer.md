# RsiAboveMidlineShareComponent: night_rsi_run | 010-01_rsi-above-share-continuation_1d | RSIShareAboveMidline

## attempt 1

answer: built
class: RsiAboveMidlineShareComponent
settings: {"period": 14, "window": 30, "rsi_window": 100}
reason: No catalogue component counts the bars on which the RSI sat above 50. `RSIPullbackComponent` gives the RSI level of the current bar only, and `RsiChangeFromPriorLowComponent` gives a difference of two RSI values. This new class computes the share of the last `window` bars with RSI above 50, minus 0.5. Each RSI uses a fixed window of `rsi_window` changes, so the value does not depend on how many bars the run has seen.

table: Directional components
row: | `RsiAboveMidlineShareComponent` | `period` (14), `window` (30), `rsi_window` (100) | (number of bars i in t-`window`+1 .. t with RSI(i) > 50) / `window` - 0.5. RSI(i) = 100 x G / (G + L), where G and L are the EWMs (alpha 1/`period`, adjust=False, seeded at the first change) of the gains and losses of the `rsi_window` one-bar close changes ending at bar i. RSI > 50 is G > L; when G + L = 0 the RSI is 50, which is not above 50 | -0.5 to +0.5 in steps of 1/`window`, signed; positive when the RSI was above 50 on more than half of the window, -0.5 when it was always at or below 50, +0.5 when it was always above | graded | share of bars, centred | `window` + `rsi_window` (130) | closes only. A NaN close anywhere in the last `window` + `rsi_window` rows gives NaN. These settings raise when the component is built: `period` < 1, `window` < 1, `rsi_window` < `period` | stateless; how persistently the RSI has held above its midline, not its level. No `scaling_factor`: scale it with transforms |

```python class
class RsiAboveMidlineShareComponent(SubStrategyComponent):
    """
    The share of recent bars on which the Wilder RSI of the closes was above 50, centred on zero:

        raw_value = #{ i in t-window+1 .. t : RSI(i) > 50 } / window - 0.5

    RSI(i) = 100 x G / (G + L). G and L are the EWMs (alpha 1/period, adjust=False, seeded at the first change)
    of the gains max(d, 0) and losses max(-d, 0) of the rsi_window one-bar close changes d ending at bar i.
    RSI(i) > 50 exactly when G > L. When G + L = 0 the RSI is 50, which is not above 50.

    Range: -0.5 (never above 50 in the window) to +0.5 (always above), in steps of 1/window; signed and graded.
    Warm-up: window + rsi_window rows, bar t included.
    NaN: a NaN close anywhere in the last window + rsi_window rows gives NaN.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + rsi_window rows of data, the
    last of which is bar t; each RSI(i) uses closes up to bar i <= t.
    """

    def __init__(self, name="RsiAboveMidlineShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 14))
        self.window = int(self.parameters.get("window", 30))
        self.rsi_window = int(self.parameters.get("rsi_window", 100))
        if self.period < 1:
            raise ValueError(f"RsiAboveMidlineShareComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"RsiAboveMidlineShareComponent: window must be >= 1, got {self.window}")
        if self.rsi_window < self.period:
            raise ValueError(
                f"RsiAboveMidlineShareComponent: rsi_window must be >= period, got {self.rsi_window} < {self.period}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        closes = data['close'].astype(float).iloc[-n:].to_numpy()
        if np.isnan(closes).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        alpha = 1.0 / self.period
        above = 0
        for j in range(self.window):
            seg = closes[j:j + self.rsi_window + 1]
            d = np.diff(seg)
            g = pd.Series(np.where(d > 0, d, 0.0)).ewm(alpha=alpha, adjust=False).mean().iloc[-1]
            l = pd.Series(np.where(d < 0, -d, 0.0)).ewm(alpha=alpha, adjust=False).mean().iloc[-1]
            if g > l:
                above += 1
        self._raw_value = float(above / self.window - 0.5)
        self.confidence = 1.0
        self.debug_info = {'bars_above_50': above, 'window': self.window}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.rsi_window
```

```python hand
def hand(df, params):
    p = int(params.get("period", 14))
    w = int(params.get("window", 30))
    rw = int(params.get("rsi_window", 100))
    c = [float(x) for x in list(df["close"])]
    c = c[-(w + rw):]
    for x in c:
        if x != x:
            return float("nan")
    a = 1.0 / p
    count = 0
    # bar i = t - k, k = w-1 .. 0; its rsi_window changes use closes c[e - rw] .. c[e]
    for k in range(w - 1, -1, -1):
        e = len(c) - 1 - k
        G = None
        L = None
        for m in range(e - rw + 1, e + 1):
            ch = c[m] - c[m - 1]
            gain = ch if ch > 0 else 0.0
            loss = -ch if ch < 0 else 0.0
            if G is None:
                G = gain
                L = loss
            else:
                G = (1 - a) * G + a * gain
                L = (1 - a) * L + a * loss
        if G + L > 0:
            rsi = 100.0 * G / (G + L)
        else:
            rsi = 50.0
        if G > L:
            count = count + 1
    return count / w - 0.5
```

checks:
RsiAboveMidlineShareComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: === 1525 passed, 8 skipped, 74 deselected, 2170 warnings in 61.47s (0:01:01) ===
