"""Spec of FallGatedRangeMultipleComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallGatedRangeMultipleComponent'
SETTINGS = [{}, {"period": 6, "base_period": 180, "fall_period": 6}, {"period": 6, "base_period": 180, "fall_period": 6, "lag": 6}]


def hand(df, params):
    p = int(params.get("period", 6))
    bp = int(params.get("base_period", 180))
    fp = int(params.get("fall_period", 6))
    lag = int(params.get("lag", 0))
    high = [float(x) for x in list(df["high"])]
    low = [float(x) for x in list(df["low"])]
    close = [float(x) for x in list(df["close"])]
    e = len(close) - 1 - lag
    # every high and low the ranges read, and the two gate closes
    j = e - bp - p + 2
    while j <= e:
        if high[j] != high[j] or low[j] != low[j]:
            return float("nan")
        j = j + 1
    if close[e] != close[e] or close[e - fp] != close[e - fp]:
        return float("nan")

    def stretch_range(i):
        top = high[i - p + 1]
        bot = low[i - p + 1]
        k = i - p + 1
        while k <= i:
            if high[k] > top:
                top = high[k]
            if low[k] < bot:
                bot = low[k]
            k = k + 1
        return top - bot

    total = 0.0
    i = e - bp + 1
    while i <= e:
        total = total + stretch_range(i)
        i = i + 1
    mean_s = total / bp
    if mean_s == 0:
        return 0.0
    if close[e] < close[e - fp]:
        return stretch_range(e) / mean_s
    return 0.0
