"""Spec of HourOfDayComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'HourOfDayComponent'
SETTINGS = [{}]


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
