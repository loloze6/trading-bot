# HoursToSettlementComponent: intraday_1h_run | 017-01_presettle-drop-after-uptrend_1h | settlement clock

## attempt 1

answer: built
class: HoursToSettlementComponent
settings: {}
reason: No catalogued component reads the time of day: `WeekdayComponent` measures the weekday of the coming bar, which is a different quantity. This new class computes the hours from the coming bar's start to the next 00:00, 08:00 or 16:00 UTC settlement, 8 − (coming bar's UTC hour mod 8), from the `timestamp` column only.

table: Regime measures
row: | `HoursToSettlementComponent` | none | 8 − (h mod 8), h being the UTC hour of the coming bar: the current bar's timestamp plus one bar's spacing (timestamp[t] − timestamp[t-1]) | 1 to 8, integers on bars starting on the hour; never negative; no direction. 1 = the coming bar starts one hour before a settlement (stamped 07:00, 15:00, 23:00), 8 = it starts at a settlement (00:00, 08:00, 16:00) | regime measure | hours | 2 | `timestamp` only. A NaN/NaT timestamp in the last two rows, or a spacing not above 0, gives NaN; a missing column raises | stateless; known at bar t's close, no lookahead. It grows by one hour per bar going back from a settlement, and it jumps from 1 to 8 when a settlement passes, so it is a calendar regime input, not a forecast source. For example, `between` 1 and 2 selects coming bars stamped 06:00, 07:00, 14:00, 15:00, 22:00, 23:00. The settlement times are fixed at 00:00, 08:00 and 16:00 UTC (8h funding). Numeric timestamps are read as epoch seconds, ms, µs or ns by magnitude |

```python class
class HoursToSettlementComponent(SubStrategyComponent):
    """
    Hours from the coming bar's start to the next funding settlement (00:00, 08:00, 16:00 UTC):

        coming = timestamp[t] + (timestamp[t] - timestamp[t-1])       (the coming bar's start, UTC)
        h      = coming.hour                                           (0 .. 23)
        raw_value = 8 - (h mod 8)

    Range: 1 to 8, integers on bars that start on the hour; never negative, no direction.
    1 = the coming bar starts one hour before a settlement; 8 = it starts at a settlement.
    It grows the further the coming bar is from the next settlement, and it jumps from 1 back to 8 once a
    settlement passes: a calendar regime measure, not a forecast source.
    Warm-up: 2 rows (bar t and bar t-1, for the bar spacing).
    NaN: a NaN/NaT timestamp in the last two rows, or a spacing not above 0, gives NaN. A missing `timestamp`
    column raises. Numeric timestamps are read as epoch seconds, milliseconds, microseconds or nanoseconds
    according to their magnitude; naive datetimes are taken as UTC.

    WHY THIS CANNOT LEAK: it reads only the `timestamp` column of the last two rows (bar t-1 and bar t); the
    coming bar's start is bar t's stamp plus the spacing already seen, known at bar t's close.
    """

    def __init__(self, name="HoursToSettlement", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    @staticmethod
    def _to_utc(v):
        if v is None:
            return pd.NaT
        if isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, bool):
            f = float(v)
            if not np.isfinite(f):
                return pd.NaT
            a = abs(f)
            if a < 1e11:
                unit = "s"
            elif a < 1e14:
                unit = "ms"
            elif a < 1e17:
                unit = "us"
            else:
                unit = "ns"
            return pd.to_datetime(int(round(f)), unit=unit, utc=True)
        ts = pd.Timestamp(v)
        if pd.isna(ts):
            return pd.NaT
        if ts.tzinfo is None:
            return ts.tz_localize("UTC")
        return ts.tz_convert("UTC")

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        stamps = data['timestamp']
        t_prev = self._to_utc(stamps.iloc[-2])
        t_cur = self._to_utc(stamps.iloc[-1])
        if pd.isna(t_prev) or pd.isna(t_cur):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        spacing = t_cur - t_prev
        if not spacing > pd.Timedelta(0):
            self._raw_value = float("nan")
            self.confidence = 1.0
            return
        coming = t_cur + spacing
        h = int(coming.hour)
        self._raw_value = float(8 - (h % 8))
        self.confidence = 1.0
        self.debug_info = {'coming_bar_start_utc': str(coming), 'coming_hour': h}

    def is_ready(self) -> bool:
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self) -> int:
        return 2
```

```python hand
def hand(df, params):
    import math
    stamps = list(df["timestamp"])

    def seconds_of(x):
        if x is None:
            return float("nan")
        if isinstance(x, bool):
            return float("nan")
        try:
            f = float(x)
            is_number = True
        except (TypeError, ValueError):
            is_number = False
        if is_number and not hasattr(x, "tzinfo"):
            if f != f or f in (float("inf"), float("-inf")):
                return float("nan")
            a = abs(f)
            if a < 1e11:
                return f
            if a < 1e14:
                return f / 1e3
            if a < 1e17:
                return f / 1e6
            return f / 1e9
        ts = pd.Timestamp(x)
        if ts is pd.NaT or ts != ts:
            return float("nan")
        # Timestamp.value is nanoseconds since the epoch in UTC (naive taken as UTC)
        return ts.value / 1e9

    s_prev = seconds_of(stamps[-2])
    s_cur = seconds_of(stamps[-1])
    if s_prev != s_prev or s_cur != s_cur:
        return float("nan")
    spacing = s_cur - s_prev
    if not spacing > 0:
        return float("nan")
    coming = s_cur + spacing
    hour_count = int(math.floor(coming / 3600.0 + 1e-9))
    # 24 is a multiple of 8, so the hour of day mod 8 equals the hour count since the epoch mod 8
    return float(8 - (hour_count % 8))
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
  File "/home/user/trading-bot/trading-bot/tests/built_components/HoursToSettlementComponent.py", line 37, in hand
    s_prev = seconds_of(stamps[-2])
  File "/home/user/trading-bot/trading-bot/tests/built_components/HoursToSettlementComponent.py", line 31, in seconds_of
    ts = pd.Timestamp(x)
         ^^
NameError: name 'pd' is not defined. Did you mean: 'id'?

## attempt 2

answer: built
class: HoursToSettlementComponent
settings: {}
reason: No component of the catalogue measures where the coming bar sits on the 8-hour funding clock. `WeekdayComponent` gives only the weekday, and the funding components read the `funding_rate` feed, not the clock. One new class computes 8 − (coming bar's UTC hour mod 8) from the bar's own `timestamp`.

table: Regime measures
row: | `HoursToSettlementComponent` | none | 8 − (h mod 8), h being the UTC hour of the coming bar's start: the current bar's timestamp plus one bar's spacing (timestamp[t] − timestamp[t-1]) | 1 to 8, integers, never negative; no direction; 1 when the coming bar starts one hour before a settlement (00:00, 08:00, 16:00 UTC), 8 when it starts on a settlement | regime measure | hours | 2 | `timestamp` only. A NaN/NaT timestamp on bar t or t-1 gives NaN; a spacing not above 0 gives NaN (never on real bars) | stateless; a calendar clock known at bar t's close (no lookahead), like `WeekdayComponent`, and not a bet in itself. A rule `between` 1 and 2 selects coming bars stamped 22:00, 23:00, 06:00, 07:00, 14:00 and 15:00. On 1d bars (hour 0) it reads 8 on every bar. Naive timestamps are read as UTC; numeric timestamps are read as epoch seconds, ms, µs or ns by size. No `scaling_factor` |

```python class
class HoursToSettlementComponent(SubStrategyComponent):
    """
    The hours from the coming bar's start to the next funding settlement (00:00, 08:00, 16:00 UTC):

        spacing = timestamp[t] - timestamp[t-1]
        coming  = timestamp[t] + spacing                (the start of the coming bar)
        h       = UTC hour of coming
        raw_value = 8 - (h mod 8)

    Range: 1 to 8, integers, never negative, with no direction. It is 1 when the coming bar starts one hour
    before a settlement and 8 when it starts on a settlement. It grows the further the coming bar is from the
    next settlement.
    Warm-up: 2 rows (bar t and bar t-1, for the spacing).
    NaN: a NaN/NaT timestamp on bar t or t-1 gives NaN; a spacing not above 0 gives NaN (never on real bars).
    Naive timestamps are read as UTC. Numeric timestamps are read as epoch seconds, ms, us or ns by their size.

    WHY THIS CANNOT LEAK: it reads only the `timestamp` column of the last two rows (bar t-1 and bar t); the
    coming bar's start is bar t's stamp plus the spacing already seen, known at bar t's close.
    """

    def __init__(self, name="HoursToSettlement", weight=1.0, parameters=None):
        super().__init__(name, weight, parameters or {})
        self._raw_value = 0.0

    @staticmethod
    def _seconds(x):
        if x is None:
            return float("nan")
        if isinstance(x, (bool, np.bool_)):
            return float("nan")
        if isinstance(x, (int, float, np.integer, np.floating)):
            v = float(x)
            if v != v:
                return float("nan")
            a = abs(v)
            if a > 1e17:
                return v / 1e9
            if a > 1e14:
                return v / 1e6
            if a > 1e11:
                return v / 1e3
            return v
        ts = pd.Timestamp(x)
        if pd.isna(ts):
            return float("nan")
        if ts.tzinfo is None:
            ts = ts.tz_localize("UTC")
        else:
            ts = ts.tz_convert("UTC")
        return ts.value / 1e9

    def update(self, data):
        self.data = data
        self._raw_value = 0.0
        self.debug_info = {}
        if not self.is_ready():
            return
        s_prev = self._seconds(data["timestamp"].iloc[-2])
        s_now = self._seconds(data["timestamp"].iloc[-1])
        if np.isnan(s_prev) or np.isnan(s_now) or not (s_now - s_prev) > 0:
            self._raw_value = float("nan")
        else:
            coming = s_now + (s_now - s_prev)
            hour = int(np.floor(coming / 3600.0)) % 24
            self._raw_value = float(8 - (hour % 8))
            self.debug_info = {"coming_hour_utc": hour, "spacing_seconds": s_now - s_prev}
        self.confidence = 1.0

    def is_ready(self):
        return self.data is not None and len(self.data) >= self.get_required_periods()

    def get_required_periods(self):
        return 2
```

```python hand
def hand(df, params):
    import datetime
    import math

    def seconds_of(x):
        if x is None:
            return float("nan")
        try:
            if x != x:
                return float("nan")
        except Exception:
            pass
        if isinstance(x, bool):
            return float("nan")
        if isinstance(x, (int, float)) or type(x).__name__ in ("int64", "int32", "float64", "float32"):
            v = float(x)
            a = abs(v)
            if a > 1e17:
                return v / 1e9
            if a > 1e14:
                return v / 1e6
            if a > 1e11:
                return v / 1e3
            return v
        if isinstance(x, datetime.datetime):
            if x.tzinfo is None:
                return (x - datetime.datetime(1970, 1, 1)).total_seconds()
            return (x - datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)).total_seconds()
        return float("nan")

    stamps = list(df["timestamp"])
    if len(stamps) < 2:
        return float("nan")
    s_prev = seconds_of(stamps[-2])
    s_now = seconds_of(stamps[-1])
    if s_prev != s_prev or s_now != s_now:
        return float("nan")
    spacing = s_now - s_prev
    if not spacing > 0:
        return float("nan")
    coming = s_now + spacing
    hour = int(math.floor(coming / 3600.0)) % 24
    return float(8 - (hour % 8))
```

checks:
HoursToSettlementComponent: every check passed
proof: 576 files compared, identical but for run ids, times and temporary paths; the bot's suite: ======== 1558 passed, 8 skipped, 74 deselected, 2244 warnings in 47.51s ========
