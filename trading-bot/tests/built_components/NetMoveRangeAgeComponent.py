"""Spec of NetMoveRangeAgeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'NetMoveRangeAgeComponent'
SETTINGS = [{}, {"period": 30, "level": 0.5, "max_bars": 30}]


def hand(df, params):
    p = int(params.get("period", 30))
    level = float(params.get("level", 0.5))
    m = int(params.get("max_bars", 30))
    close = [float(x) for x in list(df["close"])]
    high = [float(x) for x in list(df["high"])]
    low = [float(x) for x in list(df["low"])]
    t = len(close) - 1
    first_close = t - (m + p) + 1
    first_hl = first_close + 1
    for j in range(first_close, t + 1):
        if close[j] != close[j]:
            return float("nan")
    for j in range(first_hl, t + 1):
        if high[j] != high[j] or low[j] != low[j]:
            return float("nan")

    def ratio(i):
        hi = high[i - p + 1]
        lw = low[i - p + 1]
        for j in range(i - p + 1, i + 1):
            if high[j] > hi:
                hi = high[j]
            if low[j] < lw:
                lw = low[j]
        rng = hi - lw
        if rng > 0:
            return abs(close[i] - close[i - p]) / rng
        return 0.0

    n = 0
    i = t
    while n < m and ratio(i) >= level:
        n = n + 1
        i = i - 1
    move = close[t] - close[t - p]
    if move > 0:
        return float(n)
    if move < 0:
        return float(-n)
    return 0.0
