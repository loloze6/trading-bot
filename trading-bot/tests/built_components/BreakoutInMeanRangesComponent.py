"""Spec of BreakoutInMeanRangesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutInMeanRangesComponent'
SETTINGS = [{}, {"period": 12, "base_period": 180}, {"period": 12, "base_period": 180, "side": "below"}]


def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    last = len(cl) - 1
    c = cl[last]
    if c != c:
        return float("nan")
    prior_high = None
    i = last - p
    while i <= last - 1:
        if hi[i] != hi[i]:
            return float("nan")
        if prior_high is None or hi[i] > prior_high:
            prior_high = hi[i]
        i = i + 1
    total = 0.0
    i = last - bp + 1
    while i <= last:
        if hi[i] != hi[i] or lo[i] != lo[i]:
            return float("nan")
        total = total + (hi[i] - lo[i])
        i = i + 1
    mean_range = total / bp
    if mean_range == 0:
        return 0.0
    if side == "below":
        dist = prior_high - c
    else:
        dist = c - prior_high
    if dist < 0:
        dist = 0.0
    return dist / mean_range
