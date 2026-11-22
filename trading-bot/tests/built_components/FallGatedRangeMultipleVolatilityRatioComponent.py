"""Spec of FallGatedRangeMultipleVolatilityRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallGatedRangeMultipleVolatilityRatioComponent'
SETTINGS = [{}, {"period": 6, "base_period": 180, "fall_period": 6, "vol_period": 42, "vol_lookback": 360}]


def hand(df, params):
    import math
    p = int(params.get("period", 6))
    b = int(params.get("base_period", 180))
    f = int(params.get("fall_period", 6))
    v = int(params.get("vol_period", 42))
    L = int(params.get("vol_lookback", 360))
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    nan = float("nan")

    def isnan(x):
        return x != x

    # rows read
    for i in range(t - b - p + 2, t + 1):
        if isnan(h[i]) or isnan(lo[i]):
            return nan
    for i in range(t - L - v + 1, t + 1):
        if isnan(c[i]):
            return nan
        if not c[i] > 0:
            return nan
    if isnan(c[t - f]):
        return nan

    # range multiple
    def stretch_range(i):
        top = h[i - p + 1]
        bottom = lo[i - p + 1]
        for j in range(i - p + 1, i + 1):
            if h[j] > top:
                top = h[j]
            if lo[j] < bottom:
                bottom = lo[j]
        return top - bottom

    total = 0.0
    for i in range(t - b + 1, t + 1):
        total = total + stretch_range(i)
    mean_s = total / b
    if mean_s == 0:
        rm = 0.0
    else:
        rm = stretch_range(t) / mean_s

    # volatility ratio
    def sd(i):
        rets = []
        for j in range(i - v + 1, i + 1):
            rets.append(c[j] / c[j - 1] - 1.0)
        m = sum(rets) / len(rets)
        acc = 0.0
        for r in rets:
            acc = acc + (r - m) * (r - m)
        return math.sqrt(acc / (len(rets) - 1))

    total = 0.0
    for i in range(t - L + 1, t + 1):
        total = total + sd(i)
    mean_sd = total / L
    if not mean_sd > 0:
        return nan
    vr = sd(t) / mean_sd

    g = 1.0 if c[t] < c[t - f] else 0.0
    return g * rm * vr
