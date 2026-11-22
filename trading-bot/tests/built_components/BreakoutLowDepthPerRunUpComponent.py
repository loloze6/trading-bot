"""Spec of BreakoutLowDepthPerRunUpComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutLowDepthPerRunUpComponent'
SETTINGS = [{}, {"period": 20, "fail_window": 3, "rise_period": 20}]


def hand(df, params):
    p = int(params.get("period", 20))
    fw = int(params.get("fail_window", 3))
    rp = int(params.get("rise_period", 20))
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1

    def isnan(x):
        return x != x

    # every high that can enter a prior-high window, every close that can be a breakout close
    for i in range(t - fw - p + 1, t):
        if isnan(hi[i]):
            return float("nan")
    for i in range(t - fw + 1, t + 1):
        if isnan(cl[i]):
            return float("nan")

    # most recent breakout bar, scanning back from bar t
    j = -1
    k = 0
    while k < fw:
        b = t - k
        prior = hi[b - p]
        for i in range(b - p, b):
            if hi[i] > prior:
                prior = hi[i]
        if cl[b] > prior:
            j = b
            break
        k = k + 1
    if j < 0:
        return 0.0

    level = lo[j]
    start = cl[j - rp]
    if isnan(level) or isnan(start) or not level > 0 or not start > 0:
        return float("nan")
    gap = level - cl[t]
    if gap < 0:
        gap = 0.0
    depth = gap / level * 100.0
    run = cl[j] / start - 1.0
    if run < 0:
        run = 0.0
    run = run * 100.0
    return depth / (1.0 + run)
