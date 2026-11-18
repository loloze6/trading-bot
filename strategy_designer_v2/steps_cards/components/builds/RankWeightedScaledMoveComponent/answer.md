# RankWeightedScaledMoveComponent: night_005_run | 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d | RankWeightedScaledMoveComponent

## attempt 1

answer: built
class: RankWeightedScaledMoveComponent
settings: {"abs_period": 60, "vol_period": 20, "lookback": 100}
reason: No component in the catalogue computes this measure. The closest is `VolatilityRankedFallComponent`, but it divides by the return standard deviation (not the mean absolute return), keeps only falls (clipped at 0), and weights by the volatility rank itself rather than 1 minus that rank. Nothing in a config gives 1 minus a rank, so a new class computes it.

table: Directional components
row: | `RankWeightedScaledMoveComponent` | `abs_period` (60), `vol_period` (20), `lookback` (100) | (close[t] / close[t-1] - 1) / m x (1 - (number of i in t-`lookback`+1 .. t with s(i) <= s(t)) / `lookback`). m = mean of abs(close[j] / close[j-1] - 1) over the last `abs_period` one-bar returns, bar t's included. s(i) = standard deviation (ddof 1) of the `vol_period` one-bar returns ending at bar i, that bar's included. The first factor is 0 when m = 0 | unbounded in practice, signed like the day's move; at most `abs_period` x (1 - 1/`lookback`) in size (today's return is one of the `abs_period` returns, and the rank counts s(t) itself, so the second factor is 0 to 1 - 1/`lookback`); tends to 0 when today's volatility ranks highest | graded | mean absolute moves x share of bars | max(`lookback` + `vol_period`, `abs_period` + 1) (120) | closes only. A NaN close in the last 120 rows gives NaN; a flat window (m = 0, never on real bars) gives 0. These settings raise when the component is built: `abs_period` < 1, `vol_period` < 2, `lookback` < 2 | stateless. The rank is unsmoothed and counts s(t) itself, so the rank weight is never 1. No `scaling_factor`: scale it with transforms |

```python class
class RankWeightedScaledMoveComponent(SubStrategyComponent):
    """
    The day's move against the coin's mean absolute move, weighted by how low today's volatility ranks:

        r(j)  = close[j] / close[j-1] - 1
        m     = mean(abs(r(j))) over j = t-abs_period+1 .. t
        s(i)  = std (ddof 1) of r(i-vol_period+1) .. r(i)
        rank  = (number of i in t-lookback+1 .. t with s(i) <= s(t)) / lookback
        raw_value = r(t) / m x (1 - rank)        (r(t) / m taken as 0 when m = 0)

    Range and sign: signed like the day's move. Its size is at most abs_period x (1 - 1/lookback), because
    |r(t)| <= abs_period x m and the rank counts s(t) itself. It grows with the move in mean absolute moves and as
    the volatility rank falls; it tends to 0 when today's volatility ranks highest. Graded.
    Warm-up: max(lookback + vol_period, abs_period + 1) rows, bar t included (120 at the defaults).
    NaN: a NaN close in those rows gives NaN. A flat window (m = 0, never seen on real bars) gives 0.
    Building the component raises for abs_period < 1, vol_period < 2 or lookback < 2.

    WHY THIS CANNOT LEAK: it reads only the `close` column of the last max(lookback + vol_period, abs_period + 1)
    rows of data, the last row being bar t; every return used ends at or before bar t.
    """

    def __init__(self, name="RankWeightedScaledMove", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.abs_period = int(self.parameters.get("abs_period", 60))
        if self.abs_period < 1:
            raise ValueError(f"RankWeightedScaledMoveComponent: abs_period must be >= 1, got {self.abs_period}")
        self.vol_period = int(self.parameters.get("vol_period", 20))
        if self.vol_period < 2:
            raise ValueError(f"RankWeightedScaledMoveComponent: vol_period must be >= 2, got {self.vol_period}")
        self.lookback = int(self.parameters.get("lookback", 100))
        if self.lookback < 2:
            raise ValueError(f"RankWeightedScaledMoveComponent: lookback must be >= 2, got {self.lookback}")
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n = self.get_required_periods()
        c = data['close'].astype(float).iloc[-n:].to_numpy()
        self.confidence = 1.0
        if np.isnan(c).any():
            self._raw_value = float("nan")
            return
        r = c[1:] / c[:-1] - 1.0
        if np.isnan(r).any() or np.isinf(r).any():
            self._raw_value = float("nan")
            return
        r_t = float(r[-1])
        m = float(np.mean(np.abs(r[-self.abs_period:])))
        move = 0.0 if m == 0 else r_t / m
        last = len(r) - 1
        stds = []
        for k in range(self.lookback):
            end = last - k
            w = r[end - self.vol_period + 1:end + 1]
            stds.append(float(np.std(w, ddof=1)))
        s_t = stds[0]
        rank = float(sum(1 for s in stds if s <= s_t)) / self.lookback
        self._raw_value = float(move * (1.0 - rank))
        self.debug_info = {'move_in_mean_abs': move, 'mean_abs_return': m, 'std_t': s_t, 'vol_rank': rank}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return max(self.lookback + self.vol_period, self.abs_period + 1)
```

```python hand
def hand(df, params):
    ap = int(params.get("abs_period", 60))
    vp = int(params.get("vol_period", 20))
    lb = int(params.get("lookback", 100))
    closes = [float(x) for x in list(df["close"])]
    need = max(lb + vp, ap + 1)
    window = closes[len(closes) - need:]
    for x in window:
        if x != x:
            return float("nan")
    t = len(closes) - 1

    def ret(j):
        return closes[j] / closes[j - 1] - 1.0

    total = 0.0
    j = t - ap + 1
    while j <= t:
        total = total + abs(ret(j))
        j = j + 1
    m = total / ap
    if m == 0:
        move = 0.0
    else:
        move = ret(t) / m

    def sd(i):
        vals = []
        j = i - vp + 1
        while j <= i:
            vals.append(ret(j))
            j = j + 1
        mu = sum(vals) / len(vals)
        ss = 0.0
        for v in vals:
            ss = ss + (v - mu) * (v - mu)
        return (ss / (len(vals) - 1)) ** 0.5

    s_t = sd(t)
    count = 0
    i = t - lb + 1
    while i <= t:
        if sd(i) <= s_t:
            count = count + 1
        i = i + 1
    rank = count / lb
    return move * (1.0 - rank)
```

checks:
RankWeightedScaledMoveComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1538 passed, 8 skipped, 74 deselected, 2170 warnings in 56.84s ========
