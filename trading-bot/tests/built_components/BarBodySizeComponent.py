"""Spec of BarBodySizeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BarBodySizeComponent'
SETTINGS = [{}, {"relative_to": "open"}, {"relative_to": "range", "form": "flatness"}]


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
        return abs(c - o) / o * 100.0
    h = float(list(df["high"])[-1])
    lo = float(list(df["low"])[-1])
    for x in (o, c, h, lo):
        if x != x:
            return float("nan")
    width = h - lo
    if width == 0:
        body_share = 0.0
    else:
        body_share = abs(c - o) / width
    if form == "flatness":
        return 1.0 - body_share
    return body_share
