"""Spec of FallTimesFallComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallTimesFallComponent'
SETTINGS = [{}, {"short_period": 10, "long_period": 60}]


def hand(df, params):
    s = int(params.get("short_period", 10))
    l = int(params.get("long_period", 60))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    now = c[last]
    base_s = c[last - s]
    base_l = c[last - l]
    for x in (now, base_s, base_l):
        if x != x:
            return float("nan")
    if not base_s > 0 or not base_l > 0:
        return float("nan")
    ret_s = (now - base_s) / base_s
    ret_l = (now - base_l) / base_l
    fall_s = -ret_s if ret_s < 0 else 0.0
    fall_l = -ret_l if ret_l < 0 else 0.0
    return fall_s * fall_l * 100.0
