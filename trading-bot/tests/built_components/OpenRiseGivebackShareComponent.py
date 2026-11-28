"""Spec of OpenRiseGivebackShareComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'OpenRiseGivebackShareComponent'
SETTINGS = [{}]


def hand(df, params):
    cap = params.get("cap", None)
    opens = [float(x) for x in list(df["open"])]
    highs = [float(x) for x in list(df["high"])]
    closes = [float(x) for x in list(df["close"])]
    o = opens[-1]
    h = highs[-1]
    c = closes[-1]
    if o != o or h != h or c != c:
        return float("nan")
    # how far the bar rose above its open, and how much of that the close gave back
    rise = h - o
    if not rise > 0:
        value = 0.0
    else:
        value = (h - c) / rise
    if cap is not None:
        cap = float(cap)
        if value > cap:
            value = cap
    return value
