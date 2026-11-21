"""Spec of MeanAbsScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanAbsScaledReturnComponent'
SETTINGS = [{}, {"period": 24, "window": 720}]


def hand(df, params):
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    first = last - w + 1 - p
    j = first
    while j <= last:
        x = c[j]
        if x != x or not x > 0:
            return float("nan")
        j = j + 1
    total = 0.0
    i = last - w + 1
    while i <= last:
        ri = c[i] / c[i - p] - 1.0
        total = total + (ri if ri >= 0 else -ri)
        i = i + 1
    m = total / w
    ret = c[last] / c[last - p] - 1.0
    if not m > 0:
        return 0.0
    return ret / m
