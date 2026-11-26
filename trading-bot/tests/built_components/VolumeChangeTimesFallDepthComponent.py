"""Spec of VolumeChangeTimesFallDepthComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeChangeTimesFallDepthComponent'
SETTINGS = [{}, {"volume_period": 30, "fall_period": 20}]


def hand(df, params):
    import math
    vp = int(params.get("volume_period", 30))
    fp = int(params.get("fall_period", 20))
    v = [float(x) for x in list(df["volume"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    recent = [v[t - k] for k in range(vp)]
    prior = [v[t - vp - k] for k in range(vp)]
    vals = recent + prior + [c[t], c[t - fp]]
    for x in vals:
        if x != x:
            return float("nan")
    a = sum(recent) / vp
    b = sum(prior) / vp
    if not a > 0 or not b > 0 or not c[t - fp] > 0:
        return float("nan")
    ret = c[t] / c[t - fp] - 1.0
    depth = -ret * 100.0
    if depth < 0.0:
        depth = 0.0
    return math.log(a / b) * depth
