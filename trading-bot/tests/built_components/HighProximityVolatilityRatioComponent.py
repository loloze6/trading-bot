"""Spec of HighProximityVolatilityRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'HighProximityVolatilityRatioComponent'
SETTINGS = [{}, {"period": 365, "vol_period": 20, "vol_lookback": 365}]


def hand(df, params):
    p = int(params.get("period", 365))
    vp = int(params.get("vol_period", 20))
    lb = int(params.get("vol_lookback", 365))
    c = [float(x) for x in list(df["close"])]
    n = max(p, lb + vp)
    c = c[len(c) - n:]
    for x in c:
        if x != x:
            return float("nan")
    h = c[len(c) - p]
    for x in c[len(c) - p:]:
        if x > h:
            h = x
    if not h > 0:
        return float("nan")
    prox = 100.0 + (c[-1] - h) / h * 100.0
    stds = []
    last = len(c) - 1
    for i in range(last - lb + 1, last + 1):
        rs = []
        for j in range(i - vp + 1, i + 1):
            rs.append(c[j] / c[j - 1] - 1.0)
        m = 0.0
        for r in rs:
            m = m + r
        m = m / vp
        ss = 0.0
        for r in rs:
            ss = ss + (r - m) * (r - m)
        stds.append(pow(ss / (vp - 1), 0.5))
    s_now = stds[-1]
    if not s_now > 0:
        return float("nan")
    tot = 0.0
    for s in stds:
        tot = tot + s
    mean_s = tot / lb
    return prox * mean_s / s_now
