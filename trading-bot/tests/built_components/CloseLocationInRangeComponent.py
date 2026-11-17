"""Spec of CloseLocationInRangeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'CloseLocationInRangeComponent'
SETTINGS = [{}, {"reference": "high"}]


def hand(df, params):
    ref = params.get("reference", "low")
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    h = highs[len(highs) - 1]
    l = lows[len(lows) - 1]
    c = closes[len(closes) - 1]
    if h != h or l != l or c != c:
        return float("nan")
    if h == l:
        return 0.5
    if ref == "high":
        distance = h - c
    else:
        distance = c - l
    return distance / (h - l)
