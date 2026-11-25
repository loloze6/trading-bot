"""Spec of BarBodySizeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BarBodySizeComponent'
SETTINGS = [{}, {"relative_to": "open"}, {"relative_to": "range", "form": "flatness"}, {"relative_to": "open", "form": "drop"}]


def hand(df, params):
    rel = params.get("relative_to", "open")
    form = params.get("form", "body")
    o = float(list(df["open"])[-1])
    c = float(list(df["close"])[-1])
    if rel == "open":
        if o != o or c != c:
            return float("nan")
        if not o > 0:
            return float("nan")
        if form == "drop":
            fall = o - c
            if fall < 0:
                fall = 0.0
            return fall / o * 100.0
        size = c - o
        if size < 0:
            size = -size
        return size / o * 100.0
    h = float(list(df["high"])[-1])
    l = float(list(df["low"])[-1])
    for x in (o, c, h, l):
        if x != x:
            return float("nan")
    rng = h - l
    size = c - o
    if size < 0:
        size = -size
    if form == "flatness":
        if rng == 0:
            return 1.0
        return 1.0 - size / rng
    if form == "drop":
        if rng == 0:
            return 0.0
        fall = o - c
        if fall < 0:
            fall = 0.0
        return fall / rng
    if rng == 0:
        return 0.0
    return size / rng
