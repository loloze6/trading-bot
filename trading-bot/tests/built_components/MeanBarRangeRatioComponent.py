"""Spec of MeanBarRangeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanBarRangeRatioComponent'
SETTINGS = [{}, {"long_period": 360, "short_period": 42}, {"long_period": 365, "short_period": 30, "form": "inverse"}]


def hand(df, params):
    lp = int(params.get("long_period", 360))
    sp = int(params.get("short_period", 42))
    form = params.get("form", "ratio")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(h) - 1
    long_sum = 0.0
    short_sum = 0.0
    for k in range(lp):
        hi = h[t - k]
        lo = l[t - k]
        if hi != hi or lo != lo:
            return float("nan")
        r = hi - lo
        long_sum = long_sum + r
        if k < sp:
            short_sum = short_sum + r
    L = long_sum / lp
    Q = short_sum / sp
    if form == "inverse":
        if L == 0:
            return float("nan")
        return Q / L
    if Q == 0:
        return float("nan")
    return L / Q
