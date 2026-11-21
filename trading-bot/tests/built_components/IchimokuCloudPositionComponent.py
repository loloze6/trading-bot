"""Spec of IchimokuCloudPositionComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'IchimokuCloudPositionComponent'
SETTINGS = [{}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26}]


def hand(df, params):
    tp = int(params.get("tenkan_period", 9))
    kp = int(params.get("kijun_period", 26))
    sp = int(params.get("senkou_period", 52))
    d = int(params.get("displacement", 26))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    e = t - d

    def midpoint(p):
        hi = None
        lo = None
        j = e - p + 1
        while j <= e:
            if highs[j] != highs[j] or lows[j] != lows[j]:
                return float("nan")
            if hi is None or highs[j] > hi:
                hi = highs[j]
            if lo is None or lows[j] < lo:
                lo = lows[j]
            j = j + 1
        return (hi + lo) / 2.0

    tenkan = midpoint(tp)
    kijun = midpoint(kp)
    span_b = midpoint(sp)
    span_a = (tenkan + kijun) / 2.0
    ct = closes[t]
    if span_a != span_a or span_b != span_b or ct != ct:
        return float("nan")
    top = span_a if span_a >= span_b else span_b
    if not top > 0:
        return float("nan")
    return (ct - top) / top * 100.0
