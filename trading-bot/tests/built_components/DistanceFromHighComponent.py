"""Spec of DistanceFromHighComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DistanceFromHighComponent'
SETTINGS = [{}, {"period": 30, "source": "high", "exclude_current": 1}, {"period": 365, "form": "proximity", "power": 2.0}, {"period": 30, "source": "high", "exclude_current": 1, "form": "proximity", "power": 1.5}, {"period": 20, "source": "high", "exclude_current": 1, "form": "percent", "extreme": "low"}]


def hand(df, params):
    n = int(params.get("period", 60))
    source = params.get("source", "close")
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "percent")
    power = float(params.get("power", 1.0))
    extreme = params.get("extreme", "high")
    closes = [float(x) for x in list(df["close"])]
    if source == "close":
        vals = closes
    elif extreme == "low":
        vals = [float(x) for x in list(df["low"])]
    else:
        vals = [float(x) for x in list(df["high"])]
    last = len(closes) - 1
    if ex == 1:
        first, stop = last - n, last - 1
    else:
        first, stop = last - n + 1, last
    window = []
    i = first
    while i <= stop:
        window.append(vals[i])
        i = i + 1
    c = closes[last]
    if c != c:
        return float("nan")
    for x in window:
        if x != x:
            return float("nan")
    ref = window[0]
    for x in window:
        if extreme == "low":
            if x < ref:
                ref = x
        else:
            if x > ref:
                ref = x
    if not ref > 0:
        return float("nan")
    if form == "percent":
        return (c - ref) / ref * 100.0
    if extreme == "low":
        dist = (c - ref) / ref * 100.0
    else:
        dist = (ref - c) / ref * 100.0
    if dist < 0:
        dist = 0.0
    return (1.0 / (1.0 + dist)) ** power
