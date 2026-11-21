"""Spec of VolatilityScaledDistanceFromHighComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityScaledDistanceFromHighComponent'
SETTINGS = [{}, {"period": 20, "vol_period": 20}]


def hand(df, params):
    import math
    p = int(params.get("period", 20))
    vp = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(p, vp) + 1
    i = last - need + 1
    while i <= last:
        if c[i] != c[i]:
            return float("nan")
        i = i + 1
    h = c[last - p]
    i = last - p
    while i <= last - 1:
        if c[i] > h:
            h = c[i]
        i = i + 1
    if not h > 0:
        return float("nan")
    rets = []
    j = last - vp + 1
    while j <= last:
        if not c[j - 1] > 0:
            return float("nan")
        rets.append(c[j] / c[j - 1] - 1.0)
        j = j + 1
    total = 0.0
    for r in rets:
        total = total + r
    mean = total / len(rets)
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean) * (r - mean)
    s = math.sqrt(ss / (len(rets) - 1))
    if s == 0:
        return 0.0
    return (c[last] - h) / h / s
