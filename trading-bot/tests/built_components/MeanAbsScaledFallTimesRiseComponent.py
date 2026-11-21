"""Spec of MeanAbsScaledFallTimesRiseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanAbsScaledFallTimesRiseComponent'
SETTINGS = [{}, {"fall_period": 24, "window": 720, "rise_period": 720}]


def hand(df, params):
    p = int(params.get("fall_period", 24))
    w = int(params.get("window", 720))
    q = int(params.get("rise_period", 720))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(w + p, q + 1)
    first = last - need + 1
    j = first
    while j <= last:
        x = c[j]
        if x != x or not x > 0:
            return float("nan")
        j = j + 1
    total = 0.0
    i = last - w + 1
    while i <= last:
        ret = c[i] / c[i - p] - 1.0
        if ret < 0:
            ret = -ret
        total = total + ret
        i = i + 1
    m = total / w
    today = c[last] / c[last - p] - 1.0
    if m == 0:
        fall = 0.0
    else:
        fall = -today / m
        if fall < 0:
            fall = 0.0
    rise = c[last] / c[last - q] - 1.0
    if rise < 0:
        rise = 0.0
    return fall * rise * 100.0
