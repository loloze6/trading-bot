"""Spec of BreakoutMarginProximityComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutMarginProximityComponent'
SETTINGS = [{}, {"period": 60}]


def hand(df, params):
    p = int(params.get("period", 60))
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    window = [closes[t - k] for k in range(0, p + 1)]
    for x in window:
        if x != x:
            return float("nan")
    c = closes[t]
    h = closes[t - 1]
    for k in range(1, p + 1):
        if closes[t - k] > h:
            h = closes[t - k]
    if not h > 0:
        return float("nan")
    if not c > h:
        return 0.0
    margin = (c - h) / h * 100.0
    return 1.0 / (1.0 + margin)
