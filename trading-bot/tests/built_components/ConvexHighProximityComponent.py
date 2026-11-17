"""Spec of ConvexHighProximityComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ConvexHighProximityComponent'
SETTINGS = [{}, {"period": 365, "power": 2.0}]


def hand(df, params):
    n = int(params.get("period", 365))
    p = float(params.get("power", 2.0))
    closes = [float(x) for x in list(df["close"])]
    window = closes[-n:]
    for x in window:
        if x != x:
            return float("nan")
    h = window[0]
    for x in window:
        if x > h:
            h = x
    if not h > 0:
        return float("nan")
    c = window[-1]
    depth = (h - c) / h * 100.0
    closeness = 1.0 / (1.0 + depth)
    return pow(closeness, p)
