"""Spec of RangeInReturnStdComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RangeInReturnStdComponent'
SETTINGS = [{}, {"vol_period": 30}]


def hand(df, params):
    import math
    n = int(params.get("vol_period", 30))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    hi = h[t]
    lo = l[t]
    if hi != hi or lo != lo:
        return float("nan")
    used = c[t - n:t + 1]
    for x in used:
        if x != x:
            return float("nan")
        if not x > 0:
            return float("nan")
    rets = []
    for j in range(t - n + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - mean) * (r - mean)
    s = math.sqrt(ss / (len(rets) - 1))
    if s == 0.0:
        return 0.0
    return (hi - lo) / c[t] / s
