"""Spec of HoursToSettlementComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'HoursToSettlementComponent'
SETTINGS = [{}]


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
