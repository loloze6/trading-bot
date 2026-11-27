"""Spec of CloseLocationInRangeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'CloseLocationInRangeComponent'
SETTINGS = [{}, {"reference": "high"}, {"reference": "low", "lag": 1}]


def hand(df, params):
    ref = params.get("reference", "low")
    lag = int(params.get("lag", 0))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    e = t - lag
    h = highs[e]
    l = lows[e]
    c = closes[e]
    if h != h or l != l or c != c:
        return float("nan")
    width = h - l
    if width == 0:
        return 0.5
    if ref == "high":
        return (h - c) / width
    return (c - l) / width
