"""Spec of FallGatedRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallGatedRangeMultipleComponent'
SETTINGS = [{}, {"period": 6, "base_period": 180, "fall_period": 6}]


def hand(df, params):
    p = int(params.get("period", 6))
    bp = int(params.get("base_period", 180))
    fp = int(params.get("fall_period", 6))
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    first = t - (bp + p - 1) + 1
    j = first
    while j <= t:
        if h[j] != h[j] or l[j] != l[j]:
            return float("nan")
        j = j + 1
    if c[t] != c[t] or c[t - fp] != c[t - fp]:
        return float("nan")

    def stretch(i):
        top = h[i - p + 1]
        bot = l[i - p + 1]
        k = i - p + 1
        while k <= i:
            if h[k] > top:
                top = h[k]
            if l[k] < bot:
                bot = l[k]
            k = k + 1
        return top - bot

    total = 0.0
    i = t - bp + 1
    while i <= t:
        total = total + stretch(i)
        i = i + 1
    mean = total / bp
    if not c[t] < c[t - fp]:
        return 0.0
    if not mean > 0:
        return 0.0
    return stretch(t) / mean
