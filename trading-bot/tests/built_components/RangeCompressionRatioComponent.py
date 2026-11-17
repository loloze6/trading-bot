"""Spec of RangeCompressionRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RangeCompressionRatioComponent'
SETTINGS = [{}, {"short_period": 20, "long_period": 100}]


def hand(df, params):
    s = params.get("short_period", 20)
    n = params.get("long_period", 100)
    highs = list(df["high"])
    lows = list(df["low"])
    hl = highs[len(highs) - n:]
    ll = lows[len(lows) - n:]
    for x in hl + ll:
        if x != x:
            return float("nan")
    top_long = hl[0]
    bottom_long = ll[0]
    for i in range(n):
        if hl[i] > top_long:
            top_long = hl[i]
        if ll[i] < bottom_long:
            bottom_long = ll[i]
    top_short = hl[n - s]
    bottom_short = ll[n - s]
    for i in range(n - s, n):
        if hl[i] > top_short:
            top_short = hl[i]
        if ll[i] < bottom_short:
            bottom_short = ll[i]
    long_range = top_long - bottom_long
    short_range = top_short - bottom_short
    if long_range == 0:
        return 0.0
    return 1.0 - short_range / long_range
