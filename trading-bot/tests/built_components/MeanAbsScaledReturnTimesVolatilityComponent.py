"""Spec of MeanAbsScaledReturnTimesVolatilityComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanAbsScaledReturnTimesVolatilityComponent'
SETTINGS = [{}, {"period": 24, "window": 720, "vol_period": 720}, {"period": 24, "window": 720, "vol_period": 720, "cap": 2.0}]


def hand(df, params):
    import math
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    vp = int(params.get("vol_period", 720))
    cap = params.get("cap", None)
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    need = max(w + p, vp + 1)
    for k in range(need):
        x = c[t - k]
        if x != x or not x > 0:
            return float("nan")
    # usual period-bar move: mean abs of the overlapping returns ending at t-w+1 .. t
    total = 0.0
    for i in range(t - w + 1, t + 1):
        total += abs(c[i] / c[i - p] - 1.0)
    m = total / w
    if m > 0:
        x = (c[t] / c[t - p] - 1.0) / m
    else:
        x = 0.0
    if cap is not None:
        cap = float(cap)
        if x > cap:
            x = cap
        if x < -cap:
            x = -cap
    # ddof-1 std of the last vp one-bar returns
    r = []
    for j in range(t - vp + 1, t + 1):
        r.append(c[j] / c[j - 1] - 1.0)
    mean_r = sum(r) / len(r)
    ss = 0.0
    for v in r:
        ss += (v - mean_r) ** 2
    s = math.sqrt(ss / (len(r) - 1))
    return x * s
