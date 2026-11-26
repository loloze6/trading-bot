"""Spec of VolumeDryUpTimesFallModerationComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeDryUpTimesFallModerationComponent'
SETTINGS = [{}, {"volume_period": 30, "fall_period": 20}]


def hand(df, params):
    import math
    vp = int(params.get("volume_period", 30))
    fp = int(params.get("fall_period", 20))
    v = [float(x) for x in list(df["volume"])]
    c = [float(x) for x in list(df["close"])]
    t = len(v) - 1
    recent = [v[t - k] for k in range(vp)]
    base = [v[t - vp - k] for k in range(vp)]
    for x in recent + base + [c[t], c[t - fp]]:
        if x != x:
            return float("nan")
    s_r = 0.0
    for x in recent:
        s_r += x
    s_b = 0.0
    for x in base:
        s_b += x
    a = s_r / vp
    b = s_b / vp
    if not a > 0 or not b > 0 or not c[t - fp] > 0:
        return float("nan")
    shrink = -math.log(a / b)
    if shrink < 0:
        shrink = 0.0
    fall = (c[t - fp] - c[t]) / c[t - fp] * 100.0
    if fall < 0:
        fall = 0.0
    return shrink * (1.0 / (1.0 + fall))
