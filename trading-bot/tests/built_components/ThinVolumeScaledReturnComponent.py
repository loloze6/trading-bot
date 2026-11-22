"""Spec of ThinVolumeScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ThinVolumeScaledReturnComponent'
SETTINGS = [{}, {"period": 48, "window": 720, "volume_period": 48, "base_near": 49, "base_far": 168}]


def hand(df, params):
    p = int(params.get("period", 48))
    w = int(params.get("window", 720))
    vp = int(params.get("volume_period", 48))
    bn = int(params.get("base_near", 49))
    bf = int(params.get("base_far", 168))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    for j in range(t - w - p + 1, t + 1):
        if c[j] != c[j] or not c[j] > 0:
            return float("nan")
    total = 0.0
    for i in range(t - w + 1, t + 1):
        total += abs(c[i] / c[i - p] - 1.0)
    m = total / w
    ret = c[t] / c[t - p] - 1.0
    rs = 0.0
    for i in range(t - vp + 1, t + 1):
        if v[i] != v[i]:
            return float("nan")
        rs += v[i]
    bs = 0.0
    cnt = 0
    for i in range(t - bf, t - bn + 1):
        if v[i] != v[i]:
            return float("nan")
        bs += v[i]
        cnt += 1
    vr = rs / vp
    vb = bs / cnt
    if not vr > 0:
        return float("nan")
    scaled = 0.0 if m == 0 else ret / m
    return scaled * vb / vr
