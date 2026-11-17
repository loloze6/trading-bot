"""Spec of DistanceFromHighComponent for the standard checks (component_harness.py), written by the components step (form "proximity" merged from ConvexHighProximityComponent, 2026-11-17): its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DistanceFromHighComponent'
SETTINGS = [{}, {"period": 30, "source": "high", "exclude_current": 1}, {"period": 365, "form": "proximity", "power": 2.0},
            {"period": 30, "source": "high", "exclude_current": 1, "form": "proximity", "power": 1.5}]


def hand(df, params):
    n = int(params.get("period", 60))
    src = params.get("source", "close")
    ex = int(params.get("exclude_current", 0))
    closes = [float(x) for x in list(df["close"])]
    vals = [float(x) for x in list(df[src])]
    m = len(vals)
    if ex == 1:
        window = vals[m - n - 1:m - 1]
    else:
        window = vals[m - n:]
    c = closes[-1]
    if c != c:
        return float("nan")
    for x in window:
        if x != x:
            return float("nan")
    h = window[0]
    for x in window:
        if x > h:
            h = x
    if not h > 0:
        return float("nan")
    if params.get("form", "percent") == "proximity":
        depth = (h - c) / h * 100.0
        if depth < 0:
            depth = 0.0
        return pow(1.0 / (1.0 + depth), float(params.get("power", 1.0)))
    return (c - h) / h * 100.0
