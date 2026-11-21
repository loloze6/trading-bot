"""Spec of HighProximityScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'HighProximityScaledReturnComponent'
SETTINGS = [{}, {"period": 720, "return_period": 24, "window": 720, "power": 2.0}]


def hand(df, params):
    period = int(params.get("period", 720))
    rp = int(params.get("return_period", 24))
    window = int(params.get("window", 720))
    power = float(params.get("power", 2.0))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    need = max(period, window + rp)
    i = last - need + 1
    while i <= last:
        x = c[i]
        if x != x or not x > 0:
            return float("nan")
        i = i + 1
    high = c[last]
    i = last - period + 1
    while i <= last:
        if c[i] > high:
            high = c[i]
        i = i + 1
    d = (high - c[last]) / high * 100.0
    if d < 0:
        d = 0.0
    w = (1.0 / (1.0 + d)) ** power
    total = 0.0
    i = last - window + 1
    while i <= last:
        r = c[i] / c[i - rp] - 1.0
        total = total + (r if r >= 0 else -r)
        i = i + 1
    m = total / window
    if m == 0:
        return 0.0
    ret = c[last] / c[last - rp] - 1.0
    return w * ret / m
