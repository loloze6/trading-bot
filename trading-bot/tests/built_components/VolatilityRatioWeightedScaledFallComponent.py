"""Spec of VolatilityRatioWeightedScaledFallComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityRatioWeightedScaledFallComponent'
SETTINGS = [{}, {"vol_period": 10, "base_vol_period": 60}]


def hand(df, params):
    import math
    vp = int(params.get("vol_period", 10))
    bp = int(params.get("base_vol_period", 60))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    n = max(vp, bp)
    used = closes[t - n: t + 1]
    for x in used:
        if x != x or not x > 0:
            return float("nan")

    def ret(j):
        return closes[j] / closes[j - 1] - 1.0

    def std_ddof1(xs):
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) * (x - m)
        return math.sqrt(ss / (len(xs) - 1))

    recent = [ret(j) for j in range(t - vp + 1, t + 1)]
    base = [ret(j) for j in range(t - bp + 1, t + 1)]
    s_recent = std_ddof1(recent)
    s_base = std_ddof1(base)
    fall = -ret(t)
    if fall < 0:
        fall = 0.0
    if not s_base > 0:
        return 0.0
    return (fall / s_base) * (s_recent / s_base)
