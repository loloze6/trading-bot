"""Spec of FlatnessWeightedRangePositionComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FlatnessWeightedRangePositionComponent'
SETTINGS = [{}, {"period": 30}]


def hand(df, params):
    n = int(params.get("period", 30))
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    used = []
    i = last - n
    while i <= last:
        used.append(closes[i])
        i = i + 1
    for x in used:
        if x != x:
            return float("nan")
    base = closes[last - n]
    now = closes[last]
    hi = closes[last - n + 1]
    lo = closes[last - n + 1]
    i = last - n + 1
    while i <= last:
        if closes[i] > hi:
            hi = closes[i]
        if closes[i] < lo:
            lo = closes[i]
        i = i + 1
    width = hi - lo
    if width <= 0:
        return 0.0
    position = (now - lo) / width
    move = now - base
    if move < 0:
        move = -move
    flatness = 1.0 - move / width
    return (2.0 * position - 1.0) * flatness
