"""Spec of DonchianBreakoutComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DonchianBreakoutComponent'
SETTINGS = [{}, {"period": 30, "source": "high_low", "scaling_factor": 1.0}, {"period": 30, "source": "high_low", "form": "below_proximity"}]


def hand(df, params):
    n = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    source = params.get("source", "close")
    form = params.get("form", "position")
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    c = closes[last]
    if source == "high_low":
        highs = [float(x) for x in list(df["high"])][last - n + 1:last + 1]
        lows = [float(x) for x in list(df["low"])][last - n + 1:last + 1]
        for x in highs + lows + [c]:
            if x != x:
                return float("nan")
        top = highs[0]
        for x in highs:
            if x > top:
                top = x
        bot = lows[0]
        for x in lows:
            if x < bot:
                bot = x
    else:
        win = closes[last - n + 1:last + 1]
        for x in win:
            if x != x:
                return float("nan")
        top = win[0]
        bot = win[0]
        for x in win:
            if x > top:
                top = x
            if x < bot:
                bot = x
    if form == "position":
        if top == bot:
            pos = 0.5
        else:
            pos = (c - bot) / (top - bot)
        return (2.0 * pos - 1.0) * sf
    middle = (top + bot) / 2.0
    if not middle > 0:
        return float("nan")
    if c >= middle:
        return 0.0
    dist_pct = (middle - c) / middle * 100.0
    return 1.0 / (1.0 + dist_pct)
