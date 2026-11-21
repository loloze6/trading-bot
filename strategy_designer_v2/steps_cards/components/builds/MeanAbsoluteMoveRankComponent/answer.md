# MeanAbsoluteMoveRankComponent: intraday_1h_run | 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h | MeanAbsoluteMoveRankComponent

## attempt 1

answer: built
class: MeanAbsoluteMoveRankComponent
settings: {"period": 168, "lookback": 720}
reason: No component ranks the mean absolute one-bar return within its own past. `VolatilityPercentileRegimeComponent` ranks a rolling standard deviation of returns divided by the current close, then smooths the rank and keeps state between bars, and `RankWeightedScaledMoveComponent` only divides by the mean absolute move. This new stateless class computes the wished rank exactly, with `period` 168 and a 720-bar (30-day) lookback.
table: Regime measures
row: | `MeanAbsoluteMoveRankComponent` | `period` (168), `lookback` (720) | (number of bars i in t-`lookback`+1 .. t with m(i) <= m(t)) / `lookback`, m(i) being the mean of abs(close[j] / close[j-1] - 1) over the `period` one-bar returns j = i-`period`+1 .. i, bar i's included | above 0, up to 1 (steps of 1/`lookback`), never negative; no direction; 1 when today's mean absolute move is the highest of the lookback, near 0 when it is the lowest | regime measure | dimensionless (rank) | `period` + `lookback` (888) | closes only. A NaN close in the last `period` + `lookback` rows gives NaN; a close not above 0 there gives NaN (never on real bars). These settings raise when the component is built: `period` < 1, `lookback` < 2 | stateless and unsmoothed; the rank counts m(t) itself, so it is never 0. It grows as the mean absolute move rises above its usual level over the lookback. No `scaling_factor`: scale it with transforms |

```python class
class MeanAbsoluteMoveRankComponent(SubStrategyComponent):
    """
    Rank of the mean absolute one-bar move within its own recent past, on every bar:

        r[j]  = close[j] / close[j-1] - 1
        m(i)  = mean(abs(r[j]) for j = i - period + 1 .. i)        (bar i's return included)
        raw_value = (number of i in t - lookback + 1 .. t with m(i) <= m(t)) / lookback

    Range: above 0, up to 1, in steps of 1/lookback. It is never negative and has no direction. It is 1 when
    today's mean absolute move is the highest of the lookback. It is 1/lookback when it is the lowest, because
    the count includes m(t) itself. It grows as the mean absolute move rises above its usual level. Stateless
    and unsmoothed.
    Warm-up: period + lookback rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last period + lookback rows of data, the last
    of which is bar t; every m(i) ends at a bar i <= t.

    NaN: a NaN close in the last period + lookback rows gives NaN. A close not above 0 there gives NaN (never on
    real bars).
    Building the component raises for a period below 1 or a lookback below 2.
    """

    def __init__(self, name="MeanAbsMoveRank", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.period = int(self.parameters.get("period", 168))
        if self.period < 1:
            raise ValueError(f"MeanAbsoluteMoveRankComponent: period must be >= 1, got {self.period}")
        self.lookback = int(self.parameters.get("lookback", 720))
        if self.lookback < 2:
            raise ValueError(f"MeanAbsoluteMoveRankComponent: lookback must be >= 2, got {self.lookback}")
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).to_numpy()[-n:]
        if np.isnan(c).any() or not (c > 0).all():
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        a = np.abs(c[1:] / c[:-1] - 1.0)          # n - 1 = period + lookback - 1 returns
        m = np.empty(self.lookback)
        for k in range(self.lookback):
            m[k] = float(np.sum(a[k:k + self.period])) / self.period
        cur = m[-1]
        rank = float(np.sum(m <= cur)) / self.lookback
        self._raw_value = float(rank)
        self.confidence = 1.0
        self.debug_info = {'mean_abs_move': float(cur), 'rank': rank}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.period + self.lookback
```

```python hand
def hand(df, params):
    p = int(params.get("period", 168))
    lb = int(params.get("lookback", 720))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    first = last - (p + lb) + 1
    for i in range(first, last + 1):
        if c[i] != c[i] or not c[i] > 0:
            return float("nan")

    def mean_abs_move(i):
        total = 0.0
        for j in range(i - p + 1, i + 1):
            total = total + abs(c[j] / c[j - 1] - 1.0)
        return total / p

    current = mean_abs_move(last)
    count = 0
    for i in range(last - lb + 1, last + 1):
        if mean_abs_move(i) <= current:
            count = count + 1
    return count / lb
```

checks:
MeanAbsoluteMoveRankComponent: every check passed
proof: 288 files compared, identical but for run ids, times and temporary paths; the bot's suite: == 1552 passed, 16 skipped, 74 deselected, 2244 warnings in 63.84s (0:01:03) ===
