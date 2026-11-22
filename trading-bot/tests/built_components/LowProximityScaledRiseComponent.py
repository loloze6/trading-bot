"""Spec of LowProximityScaledRiseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'LowProximityScaledRiseComponent'
SETTINGS = [{}, {"vol_period": 20, "period": 90}]


def hand(df, params):
    import math
    vp = int(params.get("vol_period", 20))
    p = int(params.get("period", 90))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(vp + 1, p)
    for i in range(last - need + 1, last + 1):
        if c[i] != c[i]:
            return float("nan")
    rets = []
    for j in range(last - vp + 1, last + 1):
        if not c[j - 1] > 0:
            return float("nan")
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var = var + (r - mean) * (r - mean)
    var = var / (len(rets) - 1)
    s = math.sqrt(var)
    lo = c[last]
    for i in range(last - p + 1, last + 1):
        if c[i] < lo:
            lo = c[i]
    if not lo > 0:
        return float("nan")
    d = (c[last] - lo) / lo * 100.0
    weight = 1.0 / (1.0 + d)
    today = c[last] / c[last - 1] - 1.0
    if s > 0:
        first = today / s
        if first < 0:
            first = 0.0
    else:
        first = 0.0
    return first * weight
