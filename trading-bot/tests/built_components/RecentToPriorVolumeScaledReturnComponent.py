"""Spec of RecentToPriorVolumeScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RecentToPriorVolumeScaledReturnComponent'
SETTINGS = [{}, {"period": 48, "window": 720, "base_period": 120}]


def hand(df, params):
    P = int(params.get("period", 48))
    W = int(params.get("window", 720))
    B = int(params.get("base_period", 120))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    # closes used: bars t-W-P+1 .. t
    for k in range(W + P):
        x = c[t - k]
        if x != x or not x > 0:
            return float("nan")
    recent = [v[t - k] for k in range(P)]             # bars t-P+1 .. t
    base = [v[t - P - k] for k in range(B)]           # bars t-P-B+1 .. t-P
    for x in recent + base:
        if x != x:
            return float("nan")
    base_mean = sum(base) / B
    if not base_mean > 0:
        return float("nan")
    recent_mean = sum(recent) / P
    total = 0.0
    for k in range(W):
        i = t - k
        total += abs(c[i] / c[i - P] - 1.0)
    m = total / W
    ret = c[t] / c[t - P] - 1.0
    first = 0.0 if m == 0 else ret / m
    return first * recent_mean / base_mean
