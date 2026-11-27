"""Spec of CloseOffMidRangeInUsualMovesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'CloseOffMidRangeInUsualMovesComponent'
SETTINGS = [{}, {"vol_period": 30}]


def hand(df, params):
    import math
    n = int(params.get("vol_period", 30))
    c = [float(x) for x in list(df["close"])]
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    h = hi[t]
    l = lo[t]
    used = [c[t - k] for k in range(n + 1)]
    if h != h or l != l:
        return float("nan")
    for x in used:
        if x != x:
            return float("nan")
        if not x > 0:
            return float("nan")
    rets = []
    for j in range(t - n + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    total = 0.0
    for r in rets:
        total += r
    m = total / len(rets)
    ss = 0.0
    for r in rets:
        ss += (r - m) * (r - m)
    s = math.sqrt(ss / (len(rets) - 1))
    if s == 0:
        return 0.0
    mid = (h + l) / 2.0
    return 2.0 * (c[t] - mid) / c[t] / s
