"""Spec of FallVolumeVolatilityWeightedComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallVolumeVolatilityWeightedComponent'
SETTINGS = [{}, {"volume_period": 20, "vol_period": 20, "base_vol_period": 120}]


def hand(df, params):
    import math
    vp = int(params.get("volume_period", 20))
    sp = int(params.get("vol_period", 20))
    bp = int(params.get("base_vol_period", 120))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    n_ret = max(sp, bp)
    used_c = [c[t - k] for k in range(n_ret + 1)]
    used_v = [v[t]] + [v[t - k] for k in range(1, vp + 1)]
    for x in used_c + used_v:
        if x != x:
            return float("nan")
    for x in used_c:
        if not x > 0:
            return float("nan")

    def ret(j):
        return c[j] / c[j - 1] - 1.0

    def std1(xs):
        m = sum(xs) / len(xs)
        ss = 0.0
        for x in xs:
            ss += (x - m) ** 2
        return math.sqrt(ss / (len(xs) - 1))

    base_vol = [v[t - k] for k in range(1, vp + 1)]
    mean_base = sum(base_vol) / len(base_vol)
    if not mean_base > 0:
        return float("nan")
    s_recent = std1([ret(t - k) for k in range(sp)])
    s_base = std1([ret(t - k) for k in range(bp)])
    if not s_base > 0:
        return float("nan")
    r_t = ret(t)
    fall = -r_t * 100.0 if r_t < 0 else 0.0
    return fall * (v[t] / mean_base) * (s_recent / s_base)
