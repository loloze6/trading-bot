"""Spec of MeanAbsReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanAbsReturnComponent'
SETTINGS = [{}, {"period": 24, "window": 720}]


def hand(df, params):
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    first = last - w - p + 1
    j = first
    while j <= last:
        x = c[j]
        if x != x or not x > 0:
            return float("nan")
        j = j + 1
    total = 0.0
    i = last - w + 1
    while i <= last:
        move = c[i] / c[i - p] - 1.0
        if move < 0:
            move = -move
        total = total + move
        i = i + 1
    return total / w
