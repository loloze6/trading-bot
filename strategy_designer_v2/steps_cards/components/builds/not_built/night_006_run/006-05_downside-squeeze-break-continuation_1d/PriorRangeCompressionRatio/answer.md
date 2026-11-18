# not built: night_006_run | 006-05_downside-squeeze-break-continuation_1d | PriorRangeCompressionRatio

## attempt 1

answer: built
class: RangeCompressionRatioComponent
settings: {"short_period": 20, "long_period": 100, "exclude_current": 1}
reason: `RangeCompressionRatioComponent` already computes this measure (1 minus the short high-low range over the long high-low range), but both of its windows end at bar t inclusive. The wish needs both windows to end at bar t-1, which changes the output on real data on every bar where bar t sets a new high or low. So the class is rewritten with an `exclude_current` setting (the same setting `VolumeRatioComponent` and `DistanceFromHighComponent` use for this purpose), and its default 0 keeps today's output exactly.

table: Regime measures
row: | `RangeCompressionRatioComponent` | `short_period` (20), `long_period` (100), `exclude_current` (0) | 1 − (max(high) − min(low) over the short window) / (max(high) − min(low) over the long window). With `exclude_current` 0, the windows are the last `short_period` and the last `long_period` bars, bar t included. With `exclude_current` 1, they are bars t-`short_period` .. t-1 and t-`long_period` .. t-1, bar t excluded. The value is 0.0 when the long range is 0 | 0 to 1, never negative; no direction; 0 when the short range spans the whole long range, near 1 when the short band is very narrow against the long range | regime measure | dimensionless | `long_period` + `exclude_current` (100) | high, low. A NaN high or low anywhere in the long window gives NaN. These settings raise when the component is built: `short_period` < 1, `short_period` >= `long_period`, `exclude_current` not 0 or 1 | stateless. The short window is inside the long one, so the ratio never exceeds 1. `exclude_current` 1 measures the band before bar t (the prior squeeze), so bar t's own break does not widen it. The default 0 is the original output, unchanged. Graded, for regime rules or as a forecast source after transforms |

```python class
class RangeCompressionRatioComponent(SubStrategyComponent):
    """
    How narrow the recent high-low band is against a longer high-low range, on every bar:

        e = exclude_current (0 or 1); the windows end at bar t - e
        S = max(high) - min(low) over bars t-e-short_period+1 .. t-e
        L = max(high) - min(low) over bars t-e-long_period+1  .. t-e
        raw_value = 1 - S / L      (0.0 when L = 0)

    exclude_current 0 (default): both windows end at bar t inclusive (the original output, unchanged).
    exclude_current 1: both windows end at bar t-1 (bars t-short_period .. t-1 and t-long_period .. t-1),
    which is the band before bar t, so a break on bar t does not widen it.
    Range: 0 to 1, never negative, no direction (the short window lies inside the long one, so S <= L).
    The value is 0 when the short band spans the whole long range, and near 1 when it is very narrow.
    Graded. Warm-up: long_period + exclude_current rows, bar t included.
    NaN: a NaN high or low anywhere in the long window gives NaN. A long range of 0 gives 0.0.
    Building the component raises for short_period < 1, short_period >= long_period, or an
    exclude_current other than 0 or 1.

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the rows up to and including bar t
    (the last row of data), over at most the last long_period + exclude_current rows. With exclude_current 1
    it does not even read bar t.
    """

    def __init__(self, name="RangeCompressionRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 20))
        self.long_period = int(self.parameters.get("long_period", 100))
        if self.short_period < 1:
            raise ValueError(f"RangeCompressionRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                f"RangeCompressionRatioComponent: short_period must be < long_period, got "
                f"{self.short_period} >= {self.long_period}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"RangeCompressionRatioComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data: pd.DataFrame):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        hi = data['high'].astype(float)
        lo = data['low'].astype(float)
        end = len(data) - self.exclude_current
        long_h = hi.iloc[end - self.long_period:end]
        long_l = lo.iloc[end - self.long_period:end]
        short_h = hi.iloc[end - self.short_period:end]
        short_l = lo.iloc[end - self.short_period:end]
        if long_h.isna().any() or long_l.isna().any():
            self._raw_value = float("nan")
        else:
            long_range = float(long_h.max() - long_l.min())
            short_range = float(short_h.max() - short_l.min())
            if not long_range > 0:
                self._raw_value = 0.0
            else:
                self._raw_value = float(1.0 - short_range / long_range)
            self.debug_info = {'short_range': short_range, 'long_range': long_range}
        self.confidence = 1.0

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return self.long_period + self.exclude_current
```

```python hand
def hand(df, params):
    sp = int(params.get("short_period", 20))
    lp = int(params.get("long_period", 100))
    ex = int(params.get("exclude_current", 0))
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    last = len(h) - 1 - ex
    for i in range(last - lp + 1, last + 1):
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
    def band(n):
        top = h[last]
        bot = l[last]
        i = last - n + 1
        while i <= last:
            if h[i] > top:
                top = h[i]
            if l[i] < bot:
                bot = l[i]
            i = i + 1
        return top - bot
    long_range = band(lp)
    short_range = band(sp)
    if not long_range > 0:
        return 0.0
    return 1.0 - short_range / long_range
```

checks:
proof: 590 files compared, 6 differ:
missing in the rerun: XRPUSD/protocol_summary.json.gz
missing in the rerun: XRPUSD/trade_diagnostics.json.gz
missing in the rerun: ZECUSD/protocol_summary.json.gz
missing in the rerun: ZECUSD/trade_diagnostics.json.gz
missing in the rerun: chart_bars.csv.gz
missing in the rerun: chart_trades.csv.gz

## attempt 2

answer: built
class: RangeCompressionRatioComponent
settings: {"short_period": 20, "long_period": 100, "exclude_current": 1}
reason: `RangeCompressionRatioComponent` already computes this measure, but both of its windows always end at bar t. The wish needs both windows to end at bar t-1, which changes the output on real data. So the class is written again with an `exclude_current` setting; its default of 0 gives exactly today's output, warm-up, zero-range value and NaN behaviour.

table: Regime measures
row: | `RangeCompressionRatioComponent` | `short_period` (20), `long_period` (100), `exclude_current` (0) | 1 − (max(high) − min(low) over the last `short_period` bars) / (max(high) − min(low) over the last `long_period` bars). Both windows end at bar t inclusive (`exclude_current` 0) or at bar t-1 with bar t excluded (`exclude_current` 1). 0.0 when the long range is 0 | 0 to 1, never negative; no direction; 0 when the short range spans the whole long range, near 1 when the short band is very narrow against the long range | regime measure | dimensionless | `long_period` + `exclude_current` (100) | high, low. A NaN high or low in the `long_period` rows read gives NaN. These raise when the component is built: `short_period` < 1, `short_period` >= `long_period`, `exclude_current` not 0 or 1 | stateless. The short window sits inside the long one, so the ratio never exceeds 1. With `exclude_current` 1 it is the compression of the band before bar t (bars t-20..t-1 against t-100..t-1), so bar t's own move does not enter it. `exclude_current` 0 (default) is the original output, unchanged |

```python class
class RangeCompressionRatioComponent(SubStrategyComponent):
    """
    How narrow the recent high-low band is against a longer one, on every bar:

        exclude_current = 0 (default): rows read are t - long_period + 1 .. t      (bar t included)
        exclude_current = 1:           rows read are t - long_period .. t - 1      (bar t excluded)
        e = the last row read (t, or t - 1)
        S = max(high[e - short_period + 1 .. e]) - min(low[e - short_period + 1 .. e])
        L = max(high[e - long_period + 1 .. e])  - min(low[e - long_period + 1 .. e])
        raw_value = 1 - S / L        (0.0 when L is 0)

    Range and sign: 0 to 1, never negative, no direction. The short window lies inside the long one, so S <= L.
    The value is 0 when the short band spans the whole long range and near 1 when the short band is very narrow.
    The defaults (exclude_current 0) give the original output, unchanged.
    Warm-up: long_period + exclude_current rows, bar t included.

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the rows up to and including bar t (the last
    row of data). It reads the last long_period rows ending at bar t, or ending at bar t-1 with exclude_current 1.

    NaN: a NaN high or low in the long_period rows read gives NaN. A missing column raises.
    Building the component raises for a short_period below 1, a short_period >= long_period, or an exclude_current
    other than 0 or 1.
    """

    def __init__(self, name="Range compression ratio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 20))
        self.long_period = int(self.parameters.get("long_period", 100))
        if self.short_period < 1:
            raise ValueError(
                f"RangeCompressionRatioComponent: short_period must be >= 1, got {self.short_period}")
        if self.short_period >= self.long_period:
            raise ValueError(
                "RangeCompressionRatioComponent: short_period must be below long_period, got "
                f"{self.short_period} and {self.long_period}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"RangeCompressionRatioComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        end = len(data) - self.exclude_current
        start = end - self.long_period
        hi = data['high'].astype(float).to_numpy()[start:end]
        lo = data['low'].astype(float).to_numpy()[start:end]
        if np.isnan(hi).any() or np.isnan(lo).any():
            self._raw_value = float("nan")
        else:
            long_range = float(hi.max() - lo.min())
            short_range = float(hi[-self.short_period:].max() - lo[-self.short_period:].min())
            if long_range == 0:
                self._raw_value = 0.0
            else:
                self._raw_value = float(1.0 - short_range / long_range)
            self.debug_info = {'short_range': short_range, 'long_range': long_range,
                               'exclude_current': self.exclude_current}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.long_period + self.exclude_current
```

```python hand
def hand(df, params):
    sp = int(params.get("short_period", 20))
    lp = int(params.get("long_period", 100))
    ex = int(params.get("exclude_current", 0))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(highs) - 1
    e = t - ex
    long_h = []
    long_l = []
    i = e - lp + 1
    while i <= e:
        long_h.append(highs[i])
        long_l.append(lows[i])
        i = i + 1
    for x in long_h + long_l:
        if x != x:
            return float("nan")
    short_h = []
    short_l = []
    i = e - sp + 1
    while i <= e:
        short_h.append(highs[i])
        short_l.append(lows[i])
        i = i + 1
    big = long_h[0]
    for x in long_h:
        if x > big:
            big = x
    small = long_l[0]
    for x in long_l:
        if x < small:
            small = x
    long_range = big - small
    big = short_h[0]
    for x in short_h:
        if x > big:
            big = x
    small = short_l[0]
    for x in short_l:
        if x < small:
            small = x
    short_range = big - small
    if long_range == 0:
        return 0.0
    return 1.0 - short_range / long_range
```

checks:
proof: 590 files compared, 14 differ:
missing in the rerun: BTCUSD/protocol_summary.json.gz
missing in the rerun: BTCUSD/trade_diagnostics.json.gz
missing in the rerun: ETHUSD/protocol_summary.json.gz
missing in the rerun: ETHUSD/trade_diagnostics.json.gz
missing in the rerun: LTCUSD/protocol_summary.json.gz
missing in the rerun: LTCUSD/trade_diagnostics.json.gz
missing in the rerun: XMRUSD/protocol_summary.json.gz
missing in the rerun: XMRUSD/trade_diagnostics.json.gz
missing in the rerun: XRPUSD/protocol_summary.json.gz
missing in the rerun: XRPUSD/trade_diagnostics.json.gz
missing in the rerun: ZECUSD/protocol_summary.json.gz
missing in the rerun: ZECUSD/trade_diagnostics.json.gz
missing in the rerun: chart_bars.csv.gz
missing in the rerun: chart_trades.csv.gz

## attempt 3

answer: built
class: RangeCompressionRatioComponent
settings: {"short_period": 20, "long_period": 100, "exclude_current": 1}
reason: `RangeCompressionRatioComponent` measures this band against the long range, but both of its windows end at bar t, and the wish needs both to end at bar t-1. Including bar t's high and low changes the value on real bars, so the class is rewritten with an `exclude_current` setting. Its default of 0 keeps today's output, warm-up, NaN handling and errors unchanged.

table: Regime measures
row: | `RangeCompressionRatioComponent` | `short_period` (20), `long_period` (100), `exclude_current` (0) | 1 − (max(high) − min(low) over the last `short_period` bars) / (max(high) − min(low) over the last `long_period` bars). Both windows end at bar t inclusive (`exclude_current` 0) or at bar t-1 with bar t excluded (`exclude_current` 1: bars t-`short_period` .. t-1 against t-`long_period` .. t-1). 0.0 when the long range is 0 | 0 to 1, never negative; no direction. 0 when the short range spans the whole long range, near 1 when the short band is very narrow against the long range | regime measure | dimensionless | `long_period` + `exclude_current` (100) | high, low. A NaN high or low anywhere in the long window gives NaN. Building raises for `short_period` < 1, `short_period` >= `long_period`, or `exclude_current` not 0 or 1 | stateless. The short window sits inside the long one, so the ratio never exceeds 1. `exclude_current` 1 is the squeeze before bar t, so bar t's own range (a break) does not dilute it. Graded: for regime rules, or as a forecast source after transforms |

```python class
class RangeCompressionRatioComponent(SubStrategyComponent):
    """
    How narrow the recent high-low band is against the longer range, on every bar:

        e = exclude_current (0 or 1); the windows end at bar t - e
        S = max(high[t-e-short_period+1 .. t-e]) - min(low[t-e-short_period+1 .. t-e])
        L = max(high[t-e-long_period+1 .. t-e])  - min(low[t-e-long_period+1 .. t-e])
        raw_value = 1 - S / L        (0.0 when L == 0)

    exclude_current 0 (default) is the original output, unchanged: both windows end at bar t inclusive.
    exclude_current 1 uses bars t-short_period .. t-1 against t-long_period .. t-1, the band before bar t.
    Range: 0 to 1, never negative, no direction. It is 0 when the short range spans the whole long range and
    grows towards 1 as the short band narrows against the long range. Graded.
    Warm-up: long_period + exclude_current rows, bar t included.
    NaN: a NaN high or low anywhere in the long window gives NaN.
    Building raises for a short_period below 1, a short_period >= long_period, or an exclude_current other
    than 0 or 1.

    WHY THIS CANNOT LEAK: it reads only the `high` and `low` columns of the last long_period + exclude_current
    rows of data, whose last row is bar t; no later row exists in data.
    """

    def __init__(self, name="RangeCompressionRatio", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self.short_period = int(self.parameters.get("short_period", 20))
        self.long_period = int(self.parameters.get("long_period", 100))
        if self.short_period < 1 or self.short_period >= self.long_period:
            raise ValueError(
                f"RangeCompressionRatioComponent: need 1 <= short_period < long_period, got "
                f"{self.short_period} and {self.long_period}")
        ex = self.parameters.get("exclude_current", 0)
        if ex not in (0, 1):
            raise ValueError(f"RangeCompressionRatioComponent: exclude_current must be 0 or 1, got {ex!r}")
        self.exclude_current = int(ex)
        self._raw_value = 0.0

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        hi = data['high'].to_numpy(dtype=float)
        lo = data['low'].to_numpy(dtype=float)
        end = len(hi) - self.exclude_current
        h = hi[end - self.long_period:end]
        l = lo[end - self.long_period:end]
        if np.isnan(h).any() or np.isnan(l).any():
            self._raw_value = float("nan")
        else:
            long_range = float(h.max() - l.min())
            short_range = float(h[-self.short_period:].max() - l[-self.short_period:].min())
            if not long_range > 0:
                self._raw_value = 0.0
            else:
                self._raw_value = float(1.0 - short_range / long_range)
            self.debug_info = {'short_range': short_range, 'long_range': long_range}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return self.long_period + self.exclude_current
```

```python hand
def hand(df, params):
    sp = int(params.get("short_period", 20))
    lp = int(params.get("long_period", 100))
    ex = int(params.get("exclude_current", 0))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    last = len(highs) - 1 - ex
    lh = []
    ll = []
    i = last - lp + 1
    while i <= last:
        lh.append(highs[i])
        ll.append(lows[i])
        i = i + 1
    for x in lh + ll:
        if x != x:
            return float("nan")
    sh = lh[len(lh) - sp:]
    sl = ll[len(ll) - sp:]
    top = lh[0]
    for x in lh:
        if x > top:
            top = x
    bottom = ll[0]
    for x in ll:
        if x < bottom:
            bottom = x
    long_range = top - bottom
    stop = sh[0]
    for x in sh:
        if x > stop:
            stop = x
    sbottom = sl[0]
    for x in sl:
        if x < sbottom:
            sbottom = x
    short_range = stop - sbottom
    if not long_range > 0:
        return 0.0
    return 1.0 - short_range / long_range
```

checks:
proof: 590 files compared, 14 differ:
missing in the rerun: BTCUSD/protocol_summary.json.gz
missing in the rerun: BTCUSD/trade_diagnostics.json.gz
missing in the rerun: ETHUSD/protocol_summary.json.gz
missing in the rerun: ETHUSD/trade_diagnostics.json.gz
missing in the rerun: LTCUSD/protocol_summary.json.gz
missing in the rerun: LTCUSD/trade_diagnostics.json.gz
missing in the rerun: XMRUSD/protocol_summary.json.gz
missing in the rerun: XMRUSD/trade_diagnostics.json.gz
missing in the rerun: XRPUSD/protocol_summary.json.gz
missing in the rerun: XRPUSD/trade_diagnostics.json.gz
missing in the rerun: ZECUSD/protocol_summary.json.gz
missing in the rerun: ZECUSD/trade_diagnostics.json.gz
missing in the rerun: chart_bars.csv.gz
missing in the rerun: chart_trades.csv.gz
