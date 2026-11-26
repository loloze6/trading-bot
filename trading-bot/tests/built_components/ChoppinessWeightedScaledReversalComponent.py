"""Spec of ChoppinessWeightedScaledReversalComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ChoppinessWeightedScaledReversalComponent'
SETTINGS = [{}, {"period": 7, "vol_period": 30, "er_period": 30}]


def hand(df, params):
    import math
    p = int(params.get("period", 7))
    vp = int(params.get("vol_period", 30))
    ep = int(params.get("er_period", 30))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(p, vp, ep) + 1
    window = c[t - need + 1:t + 1]
    for x in window:
        if x != x or not x > 0:
            return float("nan")
    # usual one-bar swing: std (ddof 1) of the vp returns ending at bar t
    rets = []
    for j in range(t - vp + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - mean) ** 2
    s = math.sqrt(ss / (len(rets) - 1))
    # efficiency ratio over ep bars
    path = 0.0
    for j in range(t - ep + 1, t + 1):
        path += abs(c[j] - c[j - 1])
    er = abs(c[t] - c[t - ep]) / path if path > 0 else 0.0
    # reversal of the p-bar move in usual p-bar swings
    move = c[t] / c[t - p] - 1.0
    if s == 0:
        return 0.0
    return -move / (s * math.sqrt(p)) * (1.0 - er)
