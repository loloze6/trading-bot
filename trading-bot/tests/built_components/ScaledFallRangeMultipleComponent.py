"""Spec of ScaledFallRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ScaledFallRangeMultipleComponent'
SETTINGS = [{}, {"period": 6, "lag": 6, "window": 180}]


def hand(df, params):
    p = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    w = int(params.get("window", 180))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    e = len(c) - 1 - lag
    k = e - w - p + 1
    while k <= e:
        if c[k] != c[k] or not c[k] > 0:
            return float("nan")
        k = k + 1
    k = e - w - p + 2
    while k <= e:
        if h[k] != h[k] or lo[k] != lo[k]:
            return float("nan")
        k = k + 1

    def ret(i):
        return c[i] / c[i - p] - 1.0

    def rng(i):
        top = h[i - p + 1]
        bot = lo[i - p + 1]
        j = i - p + 1
        while j <= i:
            if h[j] > top:
                top = h[j]
            if lo[j] < bot:
                bot = lo[j]
            j = j + 1
        return top - bot

    sum_abs = 0.0
    sum_rng = 0.0
    i = e - w + 1
    while i <= e:
        sum_abs = sum_abs + abs(ret(i))
        sum_rng = sum_rng + rng(i)
        i = i + 1
    m = sum_abs / w
    b = sum_rng / w
    if m == 0 or b == 0:
        return 0.0
    fall = -ret(e) / m
    if fall < 0:
        fall = 0.0
    return fall * rng(e) / b
