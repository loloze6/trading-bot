"""Spec of VolatilityScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityScaledReturnComponent'
SETTINGS = [{}, {"period": 1, "vol_period": 20, "lag": 1}]


def hand(df, params):
    import math
    p = int(params.get("period", 1))
    vp = int(params.get("vol_period", 20))
    lag = int(params.get("lag", 0))
    c = [float(x) for x in list(df["close"])]
    u = len(c) - 1 - lag
    m = p if p > vp else vp
    i = u - m
    while i <= u:
        if c[i] != c[i]:
            return float("nan")
        i = i + 1
    rets = []
    j = u - vp + 1
    while j <= u:
        rets.append(c[j] / c[j - 1] - 1.0)
        j = j + 1
    mean = 0.0
    for r in rets:
        mean = mean + r
    mean = mean / vp
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean) * (r - mean)
    s = math.sqrt(ss / (vp - 1))
    move = c[u] / c[u - p] - 1.0
    if not s > 0:
        return 0.0
    return move / (s * math.sqrt(p))
