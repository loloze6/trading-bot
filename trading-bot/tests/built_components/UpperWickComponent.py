"""Spec of UpperWickComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'UpperWickComponent'
SETTINGS = [{}, {"relative_to": "mean_range", "base_period": 30, "exclude_current": 0}]


def hand(df, params):
    rel = params.get("relative_to", "range")
    bp = int(params.get("base_period", 30))
    ex = int(params.get("exclude_current", 0))
    opens = [float(x) for x in list(df["open"])]
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    o, h, l, c = opens[t], highs[t], lows[t], closes[t]
    for x in (o, h, l, c):
        if x != x:
            return float("nan")
    top_of_body = o if o > c else c
    shadow = h - top_of_body
    if rel == "range":
        if h - l > 0:
            return shadow / (h - l)
        return 0.0
    if rel == "close":
        if not c > 0:
            return float("nan")
        return shadow / c * 100.0
    # mean_range: bars t-ex-bp+1 .. t-ex
    total = 0.0
    for k in range(bp):
        i = t - ex - k
        hi = highs[i]
        lo = lows[i]
        if hi != hi or lo != lo:
            return float("nan")
        total = total + (hi - lo)
    mean_range = total / bp
    if not mean_range > 0:
        return 0.0
    return shadow / mean_range
