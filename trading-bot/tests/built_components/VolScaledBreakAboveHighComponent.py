"""Spec of VolScaledBreakAboveHighComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolScaledBreakAboveHighComponent'
SETTINGS = [{}, {"period": 480, "step": 24, "steps": 30}]


def hand(df, params):
    p = int(params.get("period", 480))
    step = int(params.get("step", 24))
    steps = int(params.get("steps", 30))
    hi = [float(x) for x in list(df["high"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1
    c = cl[t]
    if c != c or not c > 0:
        return float("nan")
    h = None
    j = t - p
    while j <= t - 1:
        x = hi[j]
        if x != x:
            return float("nan")
        if h is None or x > h:
            h = x
        j = j + 1
    total = 0.0
    k = 0
    while k < steps:
        a = cl[t - k * step]
        b = cl[t - (k + 1) * step]
        if a != a or b != b or not a > 0 or not b > 0:
            return float("nan")
        r = a / b - 1.0
        if r < 0:
            r = -r
        total = total + r
        k = k + 1
    m = total / steps
    diff = c - h
    if diff < 0:
        diff = 0.0
    if not m > 0:
        return 0.0
    return (diff / c) / m
