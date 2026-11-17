"""Spec of LowerWickPercentComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'LowerWickPercentComponent'
SETTINGS = [{}]


def hand(df, params):
    import math
    o = list(df["open"])[-1]
    l = list(df["low"])[-1]
    c = list(df["close"])[-1]
    if any(isinstance(x, float) and math.isnan(x) for x in (o, l, c)) or c == 0:
        return float("nan")
    body_bottom = o if o < c else c
    return (body_bottom - l) / c * 100.0
