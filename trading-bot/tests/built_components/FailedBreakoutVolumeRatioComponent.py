"""Spec of FailedBreakoutVolumeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FailedBreakoutVolumeRatioComponent'
SETTINGS = [{}, {"period": 20, "fail_window": 3, "source": "high", "volume_period": 20}, {"period": 20, "fail_window": 3, "source": "close", "volume_period": 20, "form": "thin"}]


def hand(df, params):
    period = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    vp = int(params.get("volume_period", 20))
    source = params.get("source", "close")
    form = params.get("form", "ratio")
    c = [float(x) for x in list(df["close"])]
    v = [float(x) for x in list(df["volume"])]
    t = len(c) - 1
    if source == "high":
        hi = [float(x) for x in list(df["high"])]
        read = [hi[i] for i in range(t - period - fw + 1, t)] + [c[i] for i in range(t - fw + 1, t + 1)]
        ref = hi
    else:
        read = [c[i] for i in range(t - period - fw + 1, t + 1)]
        ref = c
    for x in read:
        if x != x:
            return float("nan")
    # most recent breakout bar: newest first
    j = -1
    H = None
    k = t
    while k >= t - fw + 1:
        top = ref[k - period]
        for i in range(k - period, k):
            if ref[i] > top:
                top = ref[i]
        if c[k] > top:
            j = k
            H = top
            break
        k = k - 1
    if j < 0:
        return 0.0
    if c[t] >= H:
        return 0.0
    total = 0.0
    for i in range(j - vp + 1, j + 1):
        if v[i] != v[i]:
            return float("nan")
        total = total + v[i]
    mean_v = total / vp
    if not mean_v > 0:
        return float("nan")
    ratio = v[j] / mean_v
    if form == "thin":
        thin = 1.0 - ratio
        return thin if thin > 0.0 else 0.0
    return ratio
