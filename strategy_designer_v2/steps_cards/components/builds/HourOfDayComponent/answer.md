# HourOfDayComponent: intraday_1h_run | 017-02_presettle-rise-after-downtrend_1h | HourOfDayComponent

## attempt 1

answer: built
class: HourOfDayComponent
settings: {}
reason: No catalogue component gives the UTC hour 0 to 23 of the coming bar. `HoursToSettlementComponent` reads 8 − (h mod 8), so it cannot tell 06:00 from 14:00 or 22:00, and it is not a mirror (negative or 1 minus) of the hour. The hour of day is a calendar position read from the coin's own `timestamp`, so it is a new measure that one stateless class computes. (If the plan only needs the three pre-settlement pairs together, `HoursToSettlementComponent` `between` 1 and 2 already selects them.)

table: Regime measures
row: | `HourOfDayComponent` | none | h, the UTC hour of the coming bar's start: the current bar's timestamp plus one bar's spacing (timestamp[t] − timestamp[t-1]) | 0 to 23, integers, never negative; no direction; rises by one each hour and wraps from 23 to 0 at midnight UTC | regime measure | hour of day (UTC) | 2 | `timestamp` only. A NaN/NaT timestamp on bar t or t-1 gives NaN; a spacing not above 0 gives NaN (never on real bars) | stateless; a calendar clock known at bar t's close (no lookahead), like `WeekdayComponent`, and not a bet in itself. A rule `between` 21.5 and 23.5 selects coming bars stamped 22:00 and 23:00. On 1d bars (hour 0) it reads 0 on every bar; on 4h bars it reads 0, 4, 8, 12, 16 or 20. Naive timestamps are read as UTC; numeric timestamps are read as epoch seconds, ms, µs or ns by size. Not `HoursToSettlementComponent` (8 − (h mod 8)). No `scaling_factor` |

```python class
class HourOfDayComponent(SubStrategyComponent):
    """
    The UTC hour of the coming bar's start, on every bar:

        spacing   = timestamp[t] - timestamp[t-1]
        coming    = timestamp[t] + spacing
        raw_value = coming.hour  (UTC), an integer 0 .. 23

    Range: 0 to 23, never negative, no direction. It rises by one per hour and wraps from 23 to 0 at
    midnight UTC. On 1d bars stamped at 00:00 it reads 0 on every bar.
    A regime measure (a calendar clock, like WeekdayComponent), not a bet in itself.
    Warm-up: 2 rows (bar t-1 and bar t).

    WHY THIS CANNOT LEAK: it reads only the `timestamp` column of the last two rows of data (bar t-1 and
    bar t). The coming bar's start is bar t's timestamp plus the spacing already observed, so it is known at
    bar t's close. No later row is read.

    NaN: a NaN/NaT timestamp on bar t or t-1 gives NaN, and so does a spacing not above 0 (never on real
    bars). A missing `timestamp` column raises. Naive timestamps are read as UTC, and aware ones are converted
    to UTC. Numeric timestamps are read as epoch seconds (< 1e11), ms (< 1e14), µs (< 1e17) or ns otherwise.
    """

    def __init__(self, name="HourOfDay", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    @staticmethod
    def _to_utc(x):
        if x is None or pd.isna(x):
            return pd.NaT
        if isinstance(x, (int, float, np.integer, np.floating)) and not isinstance(x, bool):
            a = abs(float(x))
            if a < 1e11:
                unit = "s"
            elif a < 1e14:
                unit = "ms"
            elif a < 1e17:
                unit = "us"
            else:
                unit = "ns"
            return pd.to_datetime(x, unit=unit, utc=True)
        ts = pd.Timestamp(x)
        if ts.tzinfo is None:
            return ts.tz_localize("UTC")
        return ts.tz_convert("UTC")

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        col = data['timestamp']
        t0 = self._to_utc(col.iloc[-2])
        t1 = self._to_utc(col.iloc[-1])
        if pd.isna(t0) or pd.isna(t1):
            self._raw_value = float("nan")
        else:
            spacing = t1 - t0
            if not spacing > pd.Timedelta(0):
                self._raw_value = float("nan")
            else:
                coming = t1 + spacing
                self._raw_value = float(coming.hour)
                self.debug_info = {'coming_bar_start_utc': str(coming)}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return 2
```

```python hand
def hand(df, params):
    import math
    ts = list(df["timestamp"])
    a = ts[len(ts) - 2]
    b = ts[len(ts) - 1]

    def to_ns(x):
        if x is None:
            return None
        if isinstance(x, (int, float)) and not isinstance(x, bool):
            if isinstance(x, float) and math.isnan(x):
                return None
            m = abs(float(x))
            if m < 1e11:
                return int(round(float(x) * 1e9))
            if m < 1e14:
                return int(round(float(x))) * 1000000
            if m < 1e17:
                return int(round(float(x))) * 1000
            return int(round(float(x)))
        if hasattr(x, "item") and not hasattr(x, "tzinfo"):
            # numpy scalar (number or datetime64)
            try:
                v = x.item()
                if isinstance(v, (int, float)):
                    return to_ns(v)
            except Exception:
                pass
        t = pd.Timestamp(x)
        if t is pd.NaT or t != t:
            return None
        return int(t.value)  # ns since the epoch, UTC (naive read as UTC)

    n0 = to_ns(a)
    n1 = to_ns(b)
    if n0 is None or n1 is None:
        return float("nan")
    spacing = n1 - n0
    if spacing <= 0:
        return float("nan")
    coming = n1 + spacing
    hour_ns = 3600 * 1000000000
    return float((coming // hour_ns) % 24)
```

checks:
the standard checks:
Traceback (most recent call last):
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 261, in <module>
    main()
    ~~~~^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 243, in main
    fails += check_hand(cls, spec.SETTINGS, spec.hand)
             ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/tests/component_harness.py", line 97, in check_hand
    want = float(hand(rows.copy(), dict(params)))
                 ~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/user/trading-bot/trading-bot/tests/built_components/HourOfDayComponent.py", line 39, in hand
    n0 = to_ns(a)
  File "/home/user/trading-bot/trading-bot/tests/built_components/HourOfDayComponent.py", line 34, in to_ns
    t = pd.Timestamp(x)
        ^^
NameError: name 'pd' is not defined. Did you mean: 'id'?

## attempt 2

answer: built
class: HourOfDayComponent
settings: {}
reason: No component gives the UTC hour of the coming bar. `HoursToSettlementComponent` reads only that hour mod 8, so it cannot tell 22:00 from 06:00 or 14:00, and `WeekdayComponent` reads the day. A new stateless calendar class computes the hour exactly.

table: Regime measures
row: | `HourOfDayComponent` | none | h, the UTC hour (0 to 23) of the coming bar's start: the current bar's timestamp plus one bar's spacing (timestamp[t] − timestamp[t-1]) | 0 to 23, integers, never negative; no direction; rises by one each hour and returns from 23 to 0 at midnight UTC | regime measure | hour of the day (UTC) | 2 | `timestamp` only. A NaN/NaT timestamp on bar t or t-1 gives NaN; a spacing not above 0 gives NaN (never on real bars) | stateless; a calendar clock known at bar t's close (no lookahead), like `WeekdayComponent`, and not a bet in itself. A rule `between` 21.5 and 23.5 selects coming bars stamped 22:00 and 23:00. On 1d bars (hour 0) it reads 0 on every bar. Naive timestamps are read as UTC; numeric timestamps are read as epoch seconds, ms, µs or ns by size. No `scaling_factor` |

```python class
class HourOfDayComponent(SubStrategyComponent):
    """
    The UTC hour of the coming bar's start:

        spacing = timestamp[t] - timestamp[t-1]
        next    = timestamp[t] + spacing
        raw_value = hour of `next` in UTC, 0 .. 23

    Range: integers 0 to 23, never negative. It carries no direction. It rises by one each hour and
    returns from 23 to 0 at midnight UTC. It is a calendar regime measure for a rule such as
    `between` 21.5 and 23.5 (coming bars stamped 22:00 and 23:00). It is not a bet in itself.
    On 1d bars stamped at hour 0 it reads 0 on every bar.
    Warm-up: 2 rows (bars t-1 and t).
    NaN: a NaN/NaT timestamp on bar t or t-1 gives NaN. A spacing not above 0 gives NaN (never on real bars).
    Naive timestamps are read as UTC. Numeric timestamps are read as epoch seconds, ms, µs or ns by size.

    WHY THIS CANNOT LEAK: it reads only the `timestamp` column of the last two rows (bars t-1 and t). Both are
    known at bar t's close, and the coming bar's start is extrapolated from them without reading any later row.
    """

    _NS_PER_HOUR = 3_600_000_000_000

    def __init__(self, name="HourOfDay", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    @staticmethod
    def _to_ns(x):
        if x is None:
            return None
        if isinstance(x, (int, float, np.integer, np.floating)) and not isinstance(x, bool):
            v = float(x)
            if v != v:
                return None
            a = abs(v)
            if a < 1e11:
                return int(round(v * 1e9))
            if a < 1e14:
                return int(round(v * 1e6))
            if a < 1e17:
                return int(round(v * 1e3))
            return int(v)
        ts = pd.Timestamp(x)
        if pd.isna(ts):
            return None
        if ts.tz is None:
            ts = ts.tz_localize("UTC")
        return int(ts.value)

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        n0 = self._to_ns(data['timestamp'].iloc[-2])
        n1 = self._to_ns(data['timestamp'].iloc[-1])
        if n0 is None or n1 is None or not (n1 - n0) > 0:
            self._raw_value = float("nan")
        else:
            nxt = n1 + (n1 - n0)
            self._raw_value = float((nxt // self._NS_PER_HOUR) % 24)
        self.confidence = 1.0
        self.debug_info = {'hour_of_coming_bar': self._raw_value}

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return 2
```

```python hand
def hand(df, params):
    import datetime
    import math

    def to_seconds(x):
        if x is None:
            return None
        if isinstance(x, datetime.datetime):
            if x != x:
                return None
            if x.tzinfo is None:
                x = x.replace(tzinfo=datetime.timezone.utc)
            return x.timestamp()
        try:
            v = float(x)
        except (TypeError, ValueError):
            return None
        if v != v:
            return None
        a = abs(v)
        if a < 1e11:
            return v
        if a < 1e14:
            return v / 1e3
        if a < 1e17:
            return v / 1e6
        return v / 1e9

    ts = list(df["timestamp"])
    s0 = to_seconds(ts[-2])
    s1 = to_seconds(ts[-1])
    if s0 is None or s1 is None:
        return float("nan")
    spacing = s1 - s0
    if not spacing > 0:
        return float("nan")
    nxt = s1 + spacing
    hours_since_epoch = math.floor(nxt / 3600.0)
    return float(hours_since_epoch % 24)
```

checks:
HourOfDayComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1559 passed, 8 skipped, 74 deselected, 2244 warnings in 46.67s ========
