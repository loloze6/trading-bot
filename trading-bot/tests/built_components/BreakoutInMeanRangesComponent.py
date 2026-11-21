"""Spec of BreakoutInMeanRangesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutInMeanRangesComponent'
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
    # prior high over bars t-p .. t-1
    prior = None
    j = t - p
    while j <= t - 1:
        x = hi[j]
        if x != x:
            return float("nan")
        if prior is None or x > prior:
            prior = x
        j = j + 1
    # mean bar range over bars t-bp+1 .. t
    total = 0.0
    j = t - bp + 1
    while j <= t:
        a = hi[j]
        b = lo[j]
        if a != a or b != b:
            return float("nan")
        total = total + (a - b)
        j = j + 1
    mean_range = total / bp
    brk = c - prior
    if brk < 0:
        brk = 0.0
    if not mean_range > 0:
        return 0.0
    return brk / mean_range
