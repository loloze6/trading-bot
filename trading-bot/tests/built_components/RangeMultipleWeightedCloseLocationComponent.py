"""Spec of RangeMultipleWeightedCloseLocationComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RangeMultipleWeightedCloseLocationComponent'
SETTINGS = [{}, {"period": 20}]


def hand(df, params):
    p = int(params.get("period", 20))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    c = closes[t]
    h = highs[t]
    lo = lows[t]
    if c != c or h != h or lo != lo:
        return float("nan")
    total = 0.0
    for i in range(t - p, t):
        hi_i = highs[i]
        lo_i = lows[i]
        if hi_i != hi_i or lo_i != lo_i:
            return float("nan")
        total = total + (hi_i - lo_i)
    mean_range = total / p
    if not mean_range > 0:
        return float("nan")
    width = h - lo
    if width > 0:
        location = 2.0 * (c - lo) / width - 1.0
    else:
        location = 0.0
    return location * (width / mean_range)
