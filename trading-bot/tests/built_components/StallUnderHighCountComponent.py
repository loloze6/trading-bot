"""Spec of StallUnderHighCountComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'StallUnderHighCountComponent'
SETTINGS = [{}, {"window": 60, "period": 365, "band": 10.0}]


def hand(df, params):
    w = int(params.get("window", 60))
    p = int(params.get("period", 365))
    band = float(params.get("band", 10.0))
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    first_needed = last - w + 1 - p
    j = first_needed
    while j <= last:
        if closes[j] != closes[j]:
            return float("nan")
        j = j + 1
    count = 0
    i = last - w + 1
    while i <= last:
        high = None
        j = i - p
        while j <= i - 1:
            if high is None or closes[j] > high:
                high = closes[j]
            j = j + 1
        if not high > 0:
            return float("nan")
        depth = (high - closes[i]) / high * 100.0
        if closes[i] < high and depth <= band:
            count = count + 1
        i = i + 1
    return float(count)
