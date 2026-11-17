"""Spec of VolumeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeRatioComponent'
SETTINGS = [{}, {"period": 30}, {"period": 10}, {"period": 2}, {"period": 20, "exclude_current": 1}, {"period": 30, "short_period": 5, "centred": 1}, {"period": 30, "log": 1}]


def hand(df, params):
    import math
    n = int(params.get("period", 30))
    ex = int(params.get("exclude_current", 0))
    s = int(params.get("short_period", 1))
    c = int(params.get("centred", 0))
    lg = int(params.get("log", 0))
    v = [float(x) for x in list(df["volume"])]
    last = len(v) - 1
    recent = []
    i = last - s + 1
    while i <= last:
        recent.append(v[i])
        i = i + 1
    longw = []
    if ex == 1:
        i = last - n
        while i <= last - 1:
            longw.append(v[i])
            i = i + 1
    else:
        i = last - n + 1
        while i <= last:
            longw.append(v[i])
            i = i + 1
    for x in recent + longw:
        if x != x:
            return float("nan")
    total = 0.0
    for x in recent:
        total = total + x
    num = total / s
    total = 0.0
    for x in longw:
        total = total + x
    den = total / n
    if not den > 0:
        return float("nan")
    ratio = num / den
    if lg == 1:
        if not ratio > 0:
            return float("nan")
        return math.log(ratio)
    return ratio - c
