"""Spec of FailedBreakoutDepthInUsualMovesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FailedBreakoutDepthInUsualMovesComponent'
SETTINGS = [{}, {"period": 20, "fail_window": 3, "vol_period": 20}, {"period": 20, "fail_window": 3, "vol_period": 20, "exclude_current": 0, "lag": 0}]


def hand(df, params):
    import math
    p = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    vp = int(params.get("vol_period", 20))
    ex = int(params.get("exclude_current", 1))
    lag = int(params.get("lag", 0))
    c = [float(v) for v in list(df["close"])]
    t = len(c) - 1
    e = t - lag
    need = max(p + fw + ex, vp + 1) + lag
    first = t - need + 1
    for i in range(first, e + 1):
        v = c[i]
        if v != v or not v > 0:
            return float("nan")
    # candidate breakout bars, newest first
    if ex == 1:
        cands = list(range(e - 1, e - fw - 1, -1))
    else:
        cands = list(range(e, e - fw, -1))
    old_high = None
    for j in cands:
        hi = c[j - 1]
        for k in range(j - p, j):
            if c[k] > hi:
                hi = c[k]
        if c[j] > hi:
            old_high = hi
            break
    # std (ddof 1) of the vp one-bar returns ending at e
    rets = []
    for i in range(e - vp + 1, e + 1):
        rets.append(c[i] / c[i - 1] - 1.0)
    mu = sum(rets) / len(rets)
    var = 0.0
    for r in rets:
        var += (r - mu) * (r - mu)
    var = var / (len(rets) - 1)
    s = math.sqrt(var)
    if old_high is None or not s > 0:
        return 0.0
    depth = old_high - c[e]
    if depth < 0:
        depth = 0.0
    return depth / old_high / s
