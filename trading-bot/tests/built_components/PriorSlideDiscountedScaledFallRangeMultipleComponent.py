"""Spec of PriorSlideDiscountedScaledFallRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'PriorSlideDiscountedScaledFallRangeMultipleComponent'
SETTINGS = [{}, {"period": 6, "lag": 6, "window": 180, "prior_period": 42}]


def hand(df, params):
    p = int(params.get("period", 6))
    lag = int(params.get("lag", 6))
    w = int(params.get("window", 180))
    q = int(params.get("prior_period", 42))
    c = [float(x) for x in list(df["close"])]
    h = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    e = len(c) - 1 - lag
    first = e - w + 1
    deepest = p if p > q else q
    for j in range(first - deepest, e + 1):
        if c[j] != c[j] or not c[j] > 0:
            return float("nan")
    for j in range(first - p + 1, e + 1):
        if h[j] != h[j] or lo[j] != lo[j]:
            return float("nan")

    def stretch_range(i):
        top = h[i - p + 1]
        bot = lo[i - p + 1]
        for j in range(i - p + 1, i + 1):
            if h[j] > top:
                top = h[j]
            if lo[j] < bot:
                bot = lo[j]
        return top - bot

    sum_abs_p = 0.0
    sum_abs_q = 0.0
    sum_s = 0.0
    for i in range(first, e + 1):
        sum_abs_p += abs(c[i] / c[i - p] - 1.0)
        sum_abs_q += abs(c[i] / c[i - q] - 1.0)
        sum_s += stretch_range(i)
    m = sum_abs_p / w
    u = sum_abs_q / w
    b = sum_s / w
    move = c[e] / c[e - p] - 1.0
    if m == 0 or b == 0 or not move < 0:
        return 0.0
    f = (-move / m) * (stretch_range(e) / b)
    if not f > 0:
        return 0.0
    prior = c[e] / c[e - q] - 1.0
    if u == 0 or prior >= 0:
        factor = 1.0
    else:
        factor = 1.0 + prior / u
    return f * factor
