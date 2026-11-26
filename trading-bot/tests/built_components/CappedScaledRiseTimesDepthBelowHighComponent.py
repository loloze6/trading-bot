"""Spec of CappedScaledRiseTimesDepthBelowHighComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'CappedScaledRiseTimesDepthBelowHighComponent'
SETTINGS = [{}, {"vol_period": 30, "period": 20, "cap": 1.0}]


def hand(df, params):
    vp = int(params.get("vol_period", 30))
    p = int(params.get("period", 20))
    cap = float(params.get("cap", 1.0))
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(vp + 1, p)
    for k in range(need):
        v = c[t - k]
        if v != v or not v > 0:
            return float("nan")
    # one-bar returns j = t-vp+1 .. t
    rets = []
    for j in range(t - vp + 1, t + 1):
        rets.append(c[j] / c[j - 1] - 1.0)
    total = 0.0
    for v in rets:
        total += v
    mean = total / len(rets)
    ss = 0.0
    for v in rets:
        ss += (v - mean) * (v - mean)
    s = (ss / (len(rets) - 1)) ** 0.5
    rise = c[t] / c[t - 1] - 1.0
    if s > 0:
        x = rise / s
        if x < 0:
            x = 0.0
        if x > cap:
            x = cap
    else:
        x = 0.0
    h = c[t]
    for k in range(p):
        if c[t - k] > h:
            h = c[t - k]
    depth = (h - c[t]) / h * 100.0
    if depth < 0:
        depth = 0.0
    return x * depth
