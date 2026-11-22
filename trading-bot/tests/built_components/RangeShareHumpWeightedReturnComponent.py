"""Spec of RangeShareHumpWeightedReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RangeShareHumpWeightedReturnComponent'
SETTINGS = [{}, {"period": 30}]


def hand(df, params):
    p = int(params.get("period", 30))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    last = len(c) - 1
    now = c[last]
    base = c[last - p]
    highs = []
    lows = []
    i = last - p + 1
    while i <= last:
        highs.append(h[i])
        lows.append(lo[i])
        i = i + 1
    for x in [now, base] + highs + lows:
        if x != x:
            return float("nan")
    if not base > 0:
        return float("nan")
    top = highs[0]
    for x in highs:
        if x > top:
            top = x
    bottom = lows[0]
    for x in lows:
        if x < bottom:
            bottom = x
    width = top - bottom
    ret = now / base - 1.0
    if width > 0:
        share = abs(now - base) / width
        if share > 1.0:
            share = 1.0
    else:
        share = 0.0
    return ret * share * (1.0 - share)
