"""Spec of IchimokuBelowCloudDistancePerWidthComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'IchimokuBelowCloudDistancePerWidthComponent'
SETTINGS = [{}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26}]


def hand(df, params):
    tp = int(params.get("tenkan_period", 9))
    kp = int(params.get("kijun_period", 26))
    sp = int(params.get("senkou_period", 52))
    disp = int(params.get("displacement", 26))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    e = t - disp

    def mid(p):
        hi = None
        lo = None
        j = e - p + 1
        while j <= e:
            h = highs[j]
            l = lows[j]
            if h != h or l != l:
                return float("nan")
            if hi is None or h > hi:
                hi = h
            if lo is None or l < lo:
                lo = l
            j = j + 1
        return (hi + lo) / 2.0

    a = (mid(tp) + mid(kp)) / 2.0
    b = mid(sp)
    c = closes[t]
    if a != a or b != b or c != c or not c > 0:
        return float("nan")
    bottom = a if a < b else b
    below = bottom - c
    if below < 0:
        below = 0.0
    dist_pct = below / c * 100.0
    width_pct = (a - b if a >= b else b - a) / c * 100.0
    return dist_pct / (1.0 + width_pct)
