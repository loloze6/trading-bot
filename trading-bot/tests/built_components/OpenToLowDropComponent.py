"""Spec of OpenToLowDropComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'OpenToLowDropComponent'
SETTINGS = [{}]


def hand(df, params):
    opens = [float(x) for x in list(df["open"])]
    lows = [float(x) for x in list(df["low"])]
    o = opens[-1]
    lo = lows[-1]
    if o != o or lo != lo or not o > 0:
        return float("nan")
    drop = o - lo
    return drop / o * 100.0
