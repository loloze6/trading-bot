"""Spec of VolumeWeightedScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'VolumeWeightedScaledReturnComponent'
SETTINGS = [{}, {"vol_period": 20, "volume_period": 30}]


def hand(df, params):
    import math
    m = int(params.get("vol_period", 20))
    n = int(params.get("volume_period", 30))
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    last = len(c) - 1
    closes = []
    i = last - m
    while i <= last:
        closes.append(c[i])
        i = i + 1
    vols = []
    i = last - n + 1
    while i <= last:
        vols.append(v[i])
        i = i + 1
    for x in closes + vols:
        if x != x:
            return float("nan")
    rets = []
    k = 1
    while k < len(closes):
        rets.append(closes[k] / closes[k - 1] - 1.0)
        k = k + 1
    mean_r = 0.0
    for r in rets:
        mean_r = mean_r + r
    mean_r = mean_r / len(rets)
    ss = 0.0
    for r in rets:
        ss = ss + (r - mean_r) * (r - mean_r)
    s = math.sqrt(ss / (len(rets) - 1))
    total = 0.0
    for x in vols:
        total = total + x
    avg = total / n
    if not avg > 0:
        return float("nan")
    ratio = v[last] / avg
    if s == 0:
        z = 0.0
    else:
        z = rets[-1] / s
    return z * ratio
