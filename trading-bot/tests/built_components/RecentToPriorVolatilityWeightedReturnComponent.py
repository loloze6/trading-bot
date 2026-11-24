"""Spec of RecentToPriorVolatilityWeightedReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RecentToPriorVolatilityWeightedReturnComponent'
SETTINGS = [{}, {"period": 48, "vol_period": 48, "base_period": 168, "base_lag": 48}, {"period": 1, "vol_period": 5, "base_period": 30, "base_lag": 0, "return_scale": "base_std"}]


def hand(df, params):
    import math
    p = int(params.get("period", 48))
    vp = int(params.get("vol_period", 48))
    bp = int(params.get("base_period", 168))
    lag = int(params.get("base_lag", 48))
    scale = params.get("return_scale", "percent")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(p, vp, lag + bp) + 1
    for k in range(need):
        x = c[t - k]
        if x != x or not x > 0:
            return float("nan")

    def ret1(j):
        return c[j] / c[j - 1] - 1.0

    def std1(xs):
        n = len(xs)
        m = 0.0
        for x in xs:
            m += x
        m /= n
        ss = 0.0
        for x in xs:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (n - 1))

    recent = [ret1(j) for j in range(t - vp + 1, t + 1)]
    base = [ret1(j) for j in range(t - lag - bp + 1, t - lag + 1)]
    s_recent = std1(recent)
    s_base = std1(base)
    if not s_base > 0:
        return float("nan")
    R = c[t] / c[t - p] - 1.0
    if scale == "base_std":
        return R / s_base * (s_recent / s_base)
    return R * 100.0 * (s_recent / s_base)
