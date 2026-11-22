"""Spec of DonchianBreakoutComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DonchianBreakoutComponent'
SETTINGS = [{}, {"period": 30, "source": "high_low", "scaling_factor": 1.0}]


def hand(df, params):
    n = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    src = params.get("source", "close")
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    first = last - n + 1
    c = closes[last]
    if src == "high_low":
        highs = [float(x) for x in list(df["high"])]
        lows = [float(x) for x in list(df["low"])]
        hs = highs[first:last + 1]
        ls = lows[first:last + 1]
        for x in hs + ls + [c]:
            if x != x:
                return float("nan")
        top = hs[0]
        for x in hs:
            if x > top:
                top = x
        bot = ls[0]
        for x in ls:
            if x < bot:
                bot = x
    else:
        cs = closes[first:last + 1]
        for x in cs:
            if x != x:
                return float("nan")
        top = cs[0]
        bot = cs[0]
        for x in cs:
            if x > top:
                top = x
            if x < bot:
                bot = x
    if top == bot:
        return 0.0
    mid = (top + bot) / 2.0
    half = (top - bot) / 2.0
    return (c - mid) / half * sf
