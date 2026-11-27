"""Spec of ScaledMoveSmallnessComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ScaledMoveSmallnessComponent'
SETTINGS = [{}, {"vol_period": 20}]


def hand(df, params):
    import math
    n = int(params.get("vol_period", 20))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    # the closes read: bars t-n .. t
    for k in range(n + 1):
        x = c[t - k]
        if x != x:
            return float("nan")
    # one-bar returns j = t-n+1 .. t
    rets = []
    for j in range(t - n + 1, t + 1):
        prev = c[j - 1]
        if not prev > 0:
            return float("nan")
        rets.append(c[j] / prev - 1.0)
    total = 0.0
    for r in rets:
        total = total + r
    mean_r = total / n
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean_r) * (r - mean_r)
    s = math.sqrt(ss / (n - 1))
    move = c[t] / c[t - 1] - 1.0
    if s == 0:
        return 1.0
    return 1.0 / (1.0 + abs(move) / s)
