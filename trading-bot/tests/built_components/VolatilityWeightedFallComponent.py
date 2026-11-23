"""Spec of VolatilityWeightedFallComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolatilityWeightedFallComponent'
SETTINGS = [{}, {"vol_period": 20}]


def hand(df, params):
    import math
    n = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    window = c[t - n:t + 1]
    for x in window:
        if x != x or not x > 0:
            return float("nan")
    rets = []
    for j in range(t - n + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean) * (r - mean)
    s = math.sqrt(ss / (len(rets) - 1))
    today = c[t] / c[t - 1] - 1.0
    fall = -today if today < 0 else 0.0
    return fall * 100.0 * s
