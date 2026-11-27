"""Spec of ScaledFallTimesBrokenDownRunComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ScaledFallTimesBrokenDownRunComponent'
SETTINGS = [{}, {"period": 20, "vol_period": 20, "max_bars": 30}]


def hand(df, params):
    import math
    p = int(params.get("period", 20))
    vp = int(params.get("vol_period", 20))
    mb = int(params.get("max_bars", 30))
    need = max(mb + 2, p + 1, vp + 1)
    c = [float(x) for x in list(df["close"])][-need:]
    for x in c:
        if x != x or not x > 0:
            return float("nan")
    t = len(c) - 1
    if not c[t] > c[t - 1]:
        return 0.0
    # length of the run of lower closes ending at bar t-1
    n = 0
    i = t - 1
    while n < mb and c[i] < c[i - 1]:
        n = n + 1
        i = i - 1
    if n == 0:
        return 0.0
    run = [c[k] for k in range(t - n, t)]
    hi = max(run)
    lo = min(run)
    d = (c[t - 1] - lo) / (hi - lo) if hi > lo else 0.0
    # std (ddof 1) of the vp one-bar returns ending at bar t
    rets = []
    for j in range(t - vp + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    mean = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var = var + (r - mean) * (r - mean)
    s = math.sqrt(var / (len(rets) - 1))
    if not s > 0:
        return 0.0
    ret = c[t] / c[t - p] - 1.0
    fall = -ret / (s * math.sqrt(p))
    if fall < 0:
        fall = 0.0
    return fall * (n - 1 + d)
