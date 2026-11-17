"""Spec of VolumeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeRatioComponent'
SETTINGS = [{}, {"period": 30}, {"period": 10}, {"period": 2}, {"period": 20, "exclude_current": 1}]


def hand(df, params):
    n = int(params.get("period", 30))
    ex = int(params.get("exclude_current", 0))
    v = [float(x) for x in list(df["volume"])]
    cur = v[-1]
    if ex == 1:
        prior = v[-(n + 1):-1]
    else:
        prior = v[-n:]
    total = 0.0
    for x in prior:
        total = total + x
    mean = total / n
    if mean != mean or not mean > 0:
        return float("nan")
    return cur / mean
