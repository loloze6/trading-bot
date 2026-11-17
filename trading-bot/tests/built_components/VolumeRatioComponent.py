"""Spec of VolumeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeRatioComponent'
SETTINGS = [{}, {"period": 30}, {"period": 10}, {"period": 2}, {"period": 20, "exclude_current": 1}, {"period": 30, "short_period": 5, "centred": 1}]


def hand(df, params):
    n = int(params.get("period", 30))
    ex = int(params.get("exclude_current", 0))
    s = int(params.get("short_period", 1))
    c = int(params.get("centred", 0))
    v = [float(x) for x in list(df["volume"])]
    recent = v[len(v) - s:]
    if ex == 1:
        longw = v[len(v) - n - 1:len(v) - 1]
    else:
        longw = v[len(v) - n:]
    for x in recent + longw:
        if x != x:
            return float("nan")
    num = 0.0
    for x in recent:
        num = num + x
    num = num / s
    den = 0.0
    for x in longw:
        den = den + x
    den = den / n
    if not den > 0:
        return float("nan")
    return num / den - c
