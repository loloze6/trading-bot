"""Spec of LowerWickShareComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'LowerWickShareComponent'
SETTINGS = [{}]


def hand(df, params):
    o = list(df["open"])[-1]
    h = list(df["high"])[-1]
    l = list(df["low"])[-1]
    c = list(df["close"])[-1]
    if o != o or h != h or l != l or c != c:
        return float("nan")
    body_bottom = o if o < c else c
    wick = body_bottom - l
    full_range = h - l
    if full_range == 0:
        return 0.0
    return wick / full_range
