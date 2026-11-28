"""Spec of ScaledFallRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ScaledFallRangeMultipleComponent'
SETTINGS = [{}, {"period": 6, "lag": 6, "window": 180}, {"period": 1, "lag": 0, "window": 30, "scale": "std"}, {"period": 1, "lag": 0, "window": 30, "scale": "std", "side": "up"}]


def hand(df, params):
    import math
    p = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    w = int(params.get("window", 180))
    scale = params.get("scale", "mean_abs")
    side = params.get("side", "down")
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    e = len(c) - 1 - lag
    # rows read: closes e-w-p+1 .. e, highs/lows e-w-p+2 .. e
    for j in range(e - w - p + 1, e + 1):
        if c[j] != c[j] or not c[j] > 0:
            return float("nan")
    for j in range(e - w - p + 2, e + 1):
        if h[j] != h[j] or l[j] != l[j]:
            return float("nan")
    rets = []
    ranges = []
    for i in range(e - w + 1, e + 1):
        rets.append(c[i] / c[i - p] - 1.0)
        hi = h[i - p + 1]
        lo = l[i - p + 1]
        for j in range(i - p + 1, i + 1):
            if h[j] > hi:
                hi = h[j]
            if l[j] < lo:
                lo = l[j]
        ranges.append(hi - lo)
    n = len(rets)
    if scale == "std":
        mu = sum(rets) / n
        ss = 0.0
        for x in rets:
            ss += (x - mu) ** 2
        m = math.sqrt(ss / (n - 1))
    else:
        m = sum(abs(x) for x in rets) / n
    B = sum(ranges) / len(ranges)
    if not m > 0 or not B > 0:
        return 0.0
    R = c[e] / c[e - p] - 1.0
    move = -R if side == "down" else R
    if move <= 0:
        return 0.0
    return (move / m) * (ranges[-1] / B)
