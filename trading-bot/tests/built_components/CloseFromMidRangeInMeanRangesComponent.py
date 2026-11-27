"""Spec of CloseFromMidRangeInMeanRangesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'CloseFromMidRangeInMeanRangesComponent'
SETTINGS = [{}, {"base_period": 20}]


def hand(df, params):
    n = int(params.get("base_period", 20))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    c = closes[t]
    if c != c:
        return float("nan")
    total = 0.0
    for k in range(n):
        h = highs[t - k]
        lo = lows[t - k]
        if h != h or lo != lo:
            return float("nan")
        total = total + (h - lo)
    mean_range = total / n
    if mean_range == 0.0:
        return 0.0
    rng = highs[t] - lows[t]
    if rng == 0.0:
        return 0.0
    location = (c - lows[t]) / rng
    return (2.0 * location - 1.0) / 2.0 * (rng / mean_range)
