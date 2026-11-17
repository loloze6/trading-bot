"""Spec of HighProximityMomentumComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'HighProximityMomentumComponent'
SETTINGS = [{}, {"period": 365, "power": 2.0, "return_period": 30}]


def hand(df, params):
    n = int(params.get("period", 365))
    p = float(params.get("power", 2.0))
    r = int(params.get("return_period", 30))
    closes = [float(x) for x in list(df["close"])]
    cur = closes[-1]
    window = closes[len(closes) - n:]
    for x in window:
        if x != x:
            return float("nan")
    old = closes[len(closes) - 1 - r]
    if old != old or cur != cur:
        return float("nan")
    high = window[0]
    for x in window:
        if x > high:
            high = x
    if not high > 0 or not old > 0:
        return float("nan")
    depth = (high - cur) / high * 100.0
    closeness = pow(1.0 / (1.0 + depth), p)
    change = (cur - old) / old * 100.0
    return closeness * change
