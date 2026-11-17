"""Spec of HighProximityMomentumComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'HighProximityMomentumComponent'
SETTINGS = [{}, {"period": 365, "power": 2.0, "return_period": 30}, {"period": 365, "power": 1.0, "return_period": 30, "proximity": "ratio"}]


def hand(df, params):
    n = int(params.get("period", 365))
    pw = float(params.get("power", 2.0))
    rp = int(params.get("return_period", 30))
    prox = params.get("proximity", "convex")
    c = [float(x) for x in list(df["close"])]
    last = c[len(c) - 1]
    base = c[len(c) - 1 - rp]
    window = c[len(c) - n:]
    for x in window + [base, last]:
        if x != x:
            return float("nan")
    h = window[0]
    for x in window:
        if x > h:
            h = x
    if not h > 0 or not base > 0:
        return float("nan")
    ret = (last / base - 1.0) * 100.0
    if prox == "ratio":
        w = pow(last / h, pw)
    else:
        d = (h - last) / h * 100.0
        w = pow(1.0 / (1.0 + d), pw)
    return w * ret
