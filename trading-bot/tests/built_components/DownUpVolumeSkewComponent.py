"""Spec of DownUpVolumeSkewComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DownUpVolumeSkewComponent'
SETTINGS = [{}, {"period": 20, "form": "centred"}]


def hand(df, params):
    import math
    n = int(params.get("period", 20))
    form = params.get("form", "centred")
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    # bars i = t-n+1 .. t, each compared with close[i-1]
    for i in range(t - n, t + 1):
        if c[i] != c[i]:
            return float("nan")
    for i in range(t - n + 1, t + 1):
        if v[i] != v[i]:
            return float("nan")
    down_sum, down_cnt, up_sum, up_cnt = 0.0, 0, 0.0, 0
    for i in range(t - n + 1, t + 1):
        if c[i] < c[i - 1]:
            down_sum += v[i]
            down_cnt += 1
        elif c[i] > c[i - 1]:
            up_sum += v[i]
            up_cnt += 1
    if down_cnt == 0 or up_cnt == 0:
        return 0.0
    dm = down_sum / down_cnt
    um = up_sum / up_cnt
    if not um > 0:
        return float("nan")
    r = dm / um
    if form == "log":
        if not r > 0:
            return float("nan")
        return math.log(r)
    return r - 1.0
