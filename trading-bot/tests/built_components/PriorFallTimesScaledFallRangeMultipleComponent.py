"""Spec of PriorFallTimesScaledFallRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorFallTimesScaledFallRangeMultipleComponent'
SETTINGS = [{}, {"period": 6, "lag": 6, "window": 180, "prior_period": 540}]


def hand(df, params):
    p = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    w = int(params.get("window", 180))
    pp = int(params.get("prior_period", 540))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    t = len(c) - 1
    e = t - lag
    used_c = [c[k] for k in range(e - w - p + 1, e + 1)] + [c[e - p - pp]]
    used_hl = [h[k] for k in range(e - w - p + 2, e + 1)] + [lo[k] for k in range(e - w - p + 2, e + 1)]
    for x in used_c + used_hl:
        if x != x:
            return float("nan")
    for x in used_c:
        if not x > 0:
            return float("nan")
    abs_sum = 0.0
    for i in range(e - w + 1, e + 1):
        abs_sum += abs(c[i] / c[i - p] - 1.0)
    m = abs_sum / w

    def stretch_range(i):
        hi = h[i - p + 1]
        lw = lo[i - p + 1]
        for k in range(i - p + 1, i + 1):
            if h[k] > hi:
                hi = h[k]
            if lo[k] < lw:
                lw = lo[k]
        return hi - lw

    s_sum = 0.0
    for i in range(e - w + 1, e + 1):
        s_sum += stretch_range(i)
    b = s_sum / w
    ret_e = c[e] / c[e - p] - 1.0
    fall = -ret_e if ret_e < 0 else 0.0
    if m == 0 or b == 0:
        f = 0.0
    else:
        f = (fall / m) * (stretch_range(e) / b)
    prior_ret = c[e - p] / c[e - p - pp] - 1.0
    prior = (-prior_ret if prior_ret < 0 else 0.0) * 100.0
    return prior * f
