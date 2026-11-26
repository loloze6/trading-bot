"""Spec of BreakoutInMeanRangesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutInMeanRangesComponent'
SETTINGS = [{}, {"period": 12, "base_period": 180}, {"period": 12, "base_period": 180, "side": "below"}, {"period": 1, "base_period": 20, "side": "below", "high_current": 1, "base_exclude_current": 1}, {"period": 1, "base_period": 30, "side": "below", "high_current": 0, "base_exclude_current": 1, "source": "close"}, {"period": 1, "base_period": 20, "side": "above", "high_current": 1, "base_exclude_current": 0, "source": "high", "extreme": "low"}]


def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hc = int(params.get("high_current", 0))
    bex = int(params.get("base_exclude_current", 0))
    source = params.get("source", "high")
    extreme = params.get("extreme", "high")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    if source == "close":
        x = c
    elif extreme == "high":
        x = h
    else:
        x = l

    # stretch bars
    if hc == 1:
        idx = [t - k for k in range(p)]          # t-p+1 .. t
    else:
        idx = [t - 1 - k for k in range(p)]      # t-p .. t-1
    vals = [x[i] for i in idx]

    # base rows
    last = t - bex
    ranges = []
    for k in range(bp):
        i = last - k
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
        ranges.append(h[i] - l[i])

    for v in vals:
        if v != v:
            return float("nan")
    if c[t] != c[t]:
        return float("nan")

    level = vals[0]
    for v in vals:
        if extreme == "high":
            if v > level:
                level = v
        else:
            if v < level:
                level = v

    total = 0.0
    for r in ranges:
        total = total + r
    mean_range = total / len(ranges)

    if side == "above":
        d = c[t] - level
    else:
        d = level - c[t]
    if d < 0:
        d = 0.0
    if mean_range == 0:
        return 0.0
    return d / mean_range
