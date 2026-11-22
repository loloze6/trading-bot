"""Spec of RecentToPriorVolatilityRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RecentToPriorVolatilityRatioComponent'
SETTINGS = [{}, {"vol_period": 48, "base_period": 168, "base_lag": 48}]


def hand(df, params):
    import math
    vp = int(params.get("vol_period", 48))
    bp = int(params.get("base_period", 168))
    lag = int(params.get("base_lag", 48))
    form = params.get("form", "ratio")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    def ret(j):
        a = c[j - 1]
        b = c[j]
        if a != a or b != b or not a > 0 or not b > 0:
            return None
        return b / a - 1.0

    def sample_std(xs):
        m = 0.0
        for x in xs:
            m += x
        m /= len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) ** 2
        return math.sqrt(ss / (len(xs) - 1))

    recent = []
    for j in range(t - vp + 1, t + 1):
        r = ret(j)
        if r is None:
            return float("nan")
        recent.append(r)
    base = []
    for j in range(t - lag - bp + 1, t - lag + 1):
        r = ret(j)
        if r is None:
            return float("nan")
        base.append(r)
    sr = sample_std(recent)
    sb = sample_std(base)
    if not sb > 0:
        return float("nan")
    ratio = sr / sb
    if form == "centred":
        return ratio - 1.0
    return ratio
