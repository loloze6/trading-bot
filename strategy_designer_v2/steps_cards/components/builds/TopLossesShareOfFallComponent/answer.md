# TopLossesShareOfFallComponent: slow_1h_run | 016-04_down-jump-price-reversal_1h | FallConcentrationShare

## attempt 1

answer: built
class: TopLossesShareOfFallComponent
settings: {"period": 72, "k": 3, "form": "share"}
reason: No component measures the k largest one-bar losses against the window's net fall, in price changes and uncapped. `TopGainsShareOfRiseComponent` measures the rise side, in simple returns, capped at 1, and `LossShareBeyondLargestComponent` compares losses with their own sum, not with the net fall. So a new class computes it, with a `form` setting ("weighted") for the variant that multiplies the share by the net fall in percent.

table: Directional components
row: | `TopLossesShareOfFallComponent` | `period` (72), `k` (3), `form` ("share") | F = close[t-`period`] - close[t]. T = the sum of the `k` largest one-bar losses close[j-1] - close[j] > 0, j = t-`period`+1 .. t (all of them if there are fewer than `k`). "share": T / F when F > 0, else 0. "weighted": (T / F) x (F / close[t-`period`] x 100), which equals T / close[t-`period`] x 100, when F > 0, else 0 | "share": 0 when the window did not fall; otherwise at least min(`k`, number of losses) / number of losses (at least `k` / `period`), unbounded above; it is 1 or more when at most `k` losses exist or when offsetting gains are present. "weighted": 0 or above 0. Never negative; no direction | graded | "share": dimensionless (top losses over the net fall). "weighted": percent of the window's first close | `period` + 1 (73) | closes only. A NaN close in the last `period` + 1 rows gives NaN. With "weighted", a close[t-`period`] not above 0 gives NaN (never on real bars). These settings raise when the component is built: `period` < 2, `k` < 1, `form` other than "share" or "weighted" | stateless. Continuous while the window fell. It jumps to 0 where the net fall crosses 0, and "share" grows without bound as a falling window's net fall nears 0. Use it with a fall condition. Price changes, not returns. A long-only rebound reading. No `scaling_factor`: scale it with transforms |

```python class
class TopLossesShareOfFallComponent(SubStrategyComponent):
    """
    How much of the window's net fall its k largest one-bar losses make up, on every bar:

        F = close[t - period] - close[t]                                (the net fall, price units)
        losses = close[j-1] - close[j] for j = t-period+1 .. t where that change is > 0
        T = sum of the k largest losses (all of them if there are fewer than k)
        form = "share" (default):  raw_value = T / F                          if F > 0, else 0.0
        form = "weighted":         raw_value = (T / F) * (F / close[t-period] * 100)   if F > 0, else 0.0

    Graded, never negative, no direction (a long-only rebound reading). "share" is near k / period for a fall
    spread evenly over many bars. It reaches 1 or more when a few bars carry the whole fall, or when gains offset
    part of it. It is 0 when the window did not fall, and it grows without bound as a falling window's net fall
    nears 0. "weighted" adds the size of the fall: it is the top losses as a percent of the window's first close.
    Warm-up: period + 1 rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + 1 rows of data (bars t-period .. t),
    the last row being bar t; each close is known at its bar's close.

    NaN: a NaN close in the last period + 1 rows gives NaN. With "weighted", a close[t-period] not above 0 gives NaN
    (never on real bars). A missing `close` column raises.
    Building the component raises for a period below 2, a k below 1, or a form other than "share" or "weighted".
    """

    def __init__(self, name="TopLossesShareOfFall", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 72))
        if self.period < 2:
            raise ValueError(f"TopLossesShareOfFallComponent: period must be >= 2, got {self.period}")
        self.k = int(self.parameters.get("k", 3))
        if self.k < 1:
            raise ValueError(f"TopLossesShareOfFallComponent: k must be >= 1, got {self.k}")
        self.form = self.parameters.get("form", "share")
        if self.form not in ("share", "weighted"):
            raise ValueError(f"TopLossesShareOfFallComponent: form must be 'share' or 'weighted', got {self.form!r}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        c = data['close'].astype(float).to_numpy()[-(self.period + 1):]
        if np.isnan(c).any():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        fall = float(c[0] - c[-1])
        if not fall > 0:
            self._raw_value = 0.0
            self.confidence = 1.0
            self.debug_info = {'net_fall': fall, 'top_losses': 0.0}
            return
        d = np.diff(c)
        losses = -d[d < 0]
        top = float(np.sort(losses)[::-1][:self.k].sum())
        share = top / fall
        if self.form == "weighted":
            if not c[0] > 0:
                self._raw_value = float("nan")
            else:
                self._raw_value = float(share * (fall / c[0] * 100.0))
        else:
            self._raw_value = float(share)
        self.confidence = 1.0
        self.debug_info = {'net_fall': fall, 'top_losses': top, 'share': share}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + 1
```

```python hand
def hand(df, params):
    p = int(params.get("period", 72))
    k = int(params.get("k", 3))
    form = params.get("form", "share")
    c = [float(x) for x in list(df["close"])]
    w = c[len(c) - p - 1:]
    for x in w:
        if x != x:
            return float("nan")
    start = w[0]
    end = w[len(w) - 1]
    net_fall = start - end
    if not net_fall > 0:
        return 0.0
    drops = []
    j = 1
    while j < len(w):
        change = w[j] - w[j - 1]
        if change < 0:
            drops.append(-change)
        j = j + 1
    drops = sorted(drops, reverse=True)
    t = 0.0
    n = 0
    for x in drops:
        if n >= k:
            break
        t = t + x
        n = n + 1
    share = t / net_fall
    if form == "weighted":
        if not start > 0:
            return float("nan")
        return share * (net_fall / start * 100.0)
    return share
```

checks:
TopLossesShareOfFallComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1556 passed, 8 skipped, 74 deselected, 2244 warnings in 47.62s ========
