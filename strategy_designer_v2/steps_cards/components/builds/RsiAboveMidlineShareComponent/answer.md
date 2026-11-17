# RsiAboveMidlineShareComponent: night_rsi_run | 010-06_rsi-below-share-reversal_1d | RsiTimeBelowMidlineComponent

## attempt 1

answer: built
class: RsiAboveMidlineShareComponent
settings: {"period": 14, "window": 30, "rsi_window": 100, "side": "below"}
reason: `RsiAboveMidlineShareComponent` measures the share of the last `window` bars on which the Wilder RSI held one side of its midline, but it only counts the upper side. The lower side is not simply its negation, because a bar with RSI exactly 50 (including flat changes, G + L = 0) is neither above nor below. So the same class is written again with a `side` setting: the default "above" keeps today's output, and "below" counts RSI < 50.

table: Directional components
row: | `RsiAboveMidlineShareComponent` | `period` (14), `window` (30), `rsi_window` (100), `side` ("above") | (number of bars i in t-`window`+1 .. t on the counted side) / `window` - 0.5. The counted side is RSI(i) > 50 (G > L) with `side` "above" and RSI(i) < 50 (G < L) with `side` "below". RSI(i) = 100 x G / (G + L), where G and L are the EWMs (alpha 1/`period`, adjust=False, seeded at the first change) of the gains and losses of the `rsi_window` one-bar close changes ending at bar i. When G + L = 0 the RSI is 50, which is on neither side | -0.5 to +0.5 in steps of 1/`window`, signed; positive when the RSI was on the counted side on more than half of the window, -0.5 when it never was, +0.5 when it always was | graded | share of bars, centred | `window` + `rsi_window` (130) | closes only. A NaN close anywhere in the last `window` + `rsi_window` rows gives NaN. These settings raise when the component is built: `period` < 1, `window` < 1, `rsi_window` < `period`, `side` other than "above" or "below" | stateless; how persistently the RSI has held one side of its midline, not its level. `side` "below" is not the negation of "above": bars at RSI exactly 50 count on neither side. No `scaling_factor`: scale it with transforms |

```python class
class RsiAboveMidlineShareComponent(SubStrategyComponent):
    """
    How persistently the RSI has held one side of its midline over the last `window` bars:

        raw_value = (number of bars i in t-window+1 .. t on the counted side) / window - 0.5

        counted side: RSI(i) > 50, i.e. G(i) > L(i)   (side = "above", default, today's output)
                      RSI(i) < 50, i.e. G(i) < L(i)   (side = "below")

        RSI(i) = 100 x G / (G + L). G and L are the EWMs (alpha = 1/period, adjust=False, seeded at the first change)
        of the gains max(d, 0) and losses max(-d, 0) of the rsi_window one-bar close changes d ending at bar i
        (closes i-rsi_window .. i). When G + L = 0 the RSI is 50, which is neither above nor below 50.

    Range: -0.5 to +0.5 in steps of 1/window, signed. It is +0.5 when every bar of the window is on the counted side
    and -0.5 when none is. Graded: it grows by 1/window for each further bar on the counted side.
    Warm-up: window + rsi_window rows, bar t included (the oldest RSI needs rsi_window changes, so rsi_window + 1
    closes).

    NaN: a NaN close anywhere in the last window + rsi_window rows gives NaN. A missing `close` column raises.
    These settings raise when the component is built: period < 1, window < 1, rsi_window < period, and a side other
    than "above" or "below".

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last window + rsi_window rows of data, the last
    row being bar t. Each RSI(i) uses closes up to bar i <= t.
    """

    def __init__(self, name="RsiMidlineShare", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 14))
        self.window = int(self.parameters.get("window", 30))
        self.rsi_window = int(self.parameters.get("rsi_window", 100))
        self.side = self.parameters.get("side", "above")
        if self.period < 1:
            raise ValueError(f"RsiAboveMidlineShareComponent: period must be >= 1, got {self.period}")
        if self.window < 1:
            raise ValueError(f"RsiAboveMidlineShareComponent: window must be >= 1, got {self.window}")
        if self.rsi_window < self.period:
            raise ValueError(
                f"RsiAboveMidlineShareComponent: rsi_window must be >= period, got {self.rsi_window} < {self.period}")
        if self.side not in ("above", "below"):
            raise ValueError(f"RsiAboveMidlineShareComponent: side must be 'above' or 'below', got {self.side!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.window + self.rsi_window
        closes = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(closes).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        alpha = 1.0 / self.period
        count = 0
        for j in range(self.window):
            seg = closes[j:j + self.rsi_window + 1]
            diffs = np.diff(seg)
            gains = np.where(diffs > 0, diffs, 0.0)
            losses = np.where(diffs < 0, -diffs, 0.0)
            g = gains[0]
            l = losses[0]
            for k in range(1, len(diffs)):
                g = (1.0 - alpha) * g + alpha * gains[k]
                l = (1.0 - alpha) * l + alpha * losses[k]
            if self.side == "above":
                if g > l:
                    count += 1
            else:
                if g < l:
                    count += 1
        self._raw_value = float(count) / self.window - 0.5
        self.confidence = 1.0
        self.debug_info = {'bars_on_side': count, 'window': self.window, 'side': self.side}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.window + self.rsi_window
```

```python hand
def hand(df, params):
    period = int(params.get("period", 14))
    window = int(params.get("window", 30))
    rsi_window = int(params.get("rsi_window", 100))
    side = params.get("side", "above")
    c = [float(x) for x in list(df["close"])]
    c = c[-(window + rsi_window):]
    for x in c:
        if x != x:
            return float("nan")
    a = 1.0 / period
    hits = 0
    # bar t is the last element; bar t-m for m = window-1 .. 0
    for m in range(window - 1, -1, -1):
        end = len(c) - 1 - m              # index of bar i in c
        start = end - rsi_window          # rsi_window changes need closes start .. end
        G = None
        L = None
        for k in range(start + 1, end + 1):
            d = c[k] - c[k - 1]
            up = d if d > 0 else 0.0
            dn = -d if d < 0 else 0.0
            if G is None:
                G, L = up, dn
            else:
                G = G + a * (up - G)
                L = L + a * (dn - L)
        if G + L == 0:
            rsi = 50.0
        else:
            rsi = 100.0 * G / (G + L)
        if side == "above" and G > L and rsi > 50.0:
            hits += 1
        elif side == "below" and G < L and rsi < 50.0:
            hits += 1
    return hits / window - 0.5
```

checks:
RsiAboveMidlineShareComponent: every check passed
proof: 588 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1526 passed, 8 skipped, 74 deselected, 2170 warnings in 56.14s ========
