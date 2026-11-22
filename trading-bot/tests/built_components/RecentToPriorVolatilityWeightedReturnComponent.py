"""Spec of RecentToPriorVolatilityWeightedReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RecentToPriorVolatilityWeightedReturnComponent'
SETTINGS = [{}, {"period": 48, "vol_period": 48, "base_period": 168, "base_lag": 48}]


def hand(df, params):
    import math
    p = int(params.get("period", 48))
    vp = int(params.get("vol_period", 48))
    bp = int(params.get("base_period", 168))
    lag = int(params.get("base_lag", 48))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    first = t - max(p, vp, lag + bp)
    for i in range(first, t + 1):
        x = c[i]
        if x != x or not x > 0:
            return float("nan")

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def sd(xs):
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) ** 2
        return math.sqrt(ss / (len(xs) - 1))

    recent = [ret(j) for j in range(t - vp + 1, t + 1)]
    base = [ret(j) for j in range(t - lag - bp + 1, t - lag + 1)]
    s_recent = sd(recent)
    s_base = sd(base)
    if not s_base > 0:
        return float("nan")
    move = (c[t] / c[t - p] - 1.0) * 100.0
    return move * s_recent / s_base
