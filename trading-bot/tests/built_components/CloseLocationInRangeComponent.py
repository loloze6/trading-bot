"""Spec of CloseLocationInRangeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'CloseLocationInRangeComponent'
SETTINGS = [{}]


def hand(df, params):
    h = list(df["high"])[-1]
    l = list(df["low"])[-1]
    c = list(df["close"])[-1]
    if h != h or l != l or c != c:
        return float("nan")
    if h == l:
        return 0.5
    return (c - l) / (h - l)
