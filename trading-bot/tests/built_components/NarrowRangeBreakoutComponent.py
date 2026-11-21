"""Spec of NarrowRangeBreakoutComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'NarrowRangeBreakoutComponent'
SETTINGS = [{}, {"period": 12, "base_period": 180}]


def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1
    c = cl[t]
    if c != c:
        return float("nan")
    # prior stretch t-p .. t-1
    top = None
    bottom = None
    j = t - p
    while j <= t - 1:
        if hi[j] != hi[j] or lo[j] != lo[j]:
            return float("nan")
        if top is None or hi[j] > top:
            top = hi[j]
        if bottom is None or lo[j] < bottom:
            bottom = lo[j]
        j = j + 1
    # mean bar range over the last bp bars, bar t included
    total = 0.0
    j = t - bp + 1
    while j <= t:
        if hi[j] != hi[j] or lo[j] != lo[j]:
            return float("nan")
        total = total + (hi[j] - lo[j])
        j = j + 1
    mean_range = total / bp
    if not c > 0:
        return float("nan")
    stretch = top - bottom
    if not stretch > 0:
        return 0.0
    rise = c - top
    if rise < 0:
        rise = 0.0
    return rise / c * 100.0 * (mean_range / stretch)
