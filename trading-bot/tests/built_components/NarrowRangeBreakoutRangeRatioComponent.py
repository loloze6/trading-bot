"""Spec of NarrowRangeBreakoutRangeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'NarrowRangeBreakoutRangeRatioComponent'
SETTINGS = [{}, {"period": 12, "base_period": 180, "ratio_long_period": 360, "ratio_short_period": 42}]


def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    lp = int(params.get("ratio_long_period", 360))
    sp = int(params.get("ratio_short_period", 42))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    c = closes[last]
    if c != c:
        return float("nan")

    stretch_h = []
    stretch_l = []
    i = last - p
    while i <= last - 1:
        stretch_h.append(highs[i])
        stretch_l.append(lows[i])
        i = i + 1

    def mean_range(n):
        total = 0.0
        j = last - n + 1
        while j <= last:
            r = highs[j] - lows[j]
            if r != r:
                return float("nan")
            total = total + r
            j = j + 1
        return total / n

    for x in stretch_h + stretch_l:
        if x != x:
            return float("nan")
    B = mean_range(bp)
    L = mean_range(lp)
    Q = mean_range(sp)
    if B != B or L != L or Q != Q:
        return float("nan")
    if not c > 0:
        return float("nan")

    H = stretch_h[0]
    for x in stretch_h:
        if x > H:
            H = x
    lo = stretch_l[0]
    for x in stretch_l:
        if x < lo:
            lo = x
    S = H - lo
    if S <= 0 or Q <= 0:
        return 0.0
    brk = c - H
    if brk < 0:
        brk = 0.0
    return brk / c * 100.0 * (B / S) * (L / Q)
