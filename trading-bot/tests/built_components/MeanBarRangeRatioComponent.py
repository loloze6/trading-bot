"""Spec of MeanBarRangeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanBarRangeRatioComponent'
SETTINGS = [{}, {"long_period": 360, "short_period": 42}]


def hand(df, params):
    lp = int(params.get("long_period", 360))
    sp = int(params.get("short_period", 42))
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    last = len(h) - 1
    long_sum = 0.0
    i = last - lp + 1
    while i <= last:
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
        long_sum = long_sum + (h[i] - l[i])
        i = i + 1
    short_sum = 0.0
    i = last - sp + 1
    while i <= last:
        short_sum = short_sum + (h[i] - l[i])
        i = i + 1
    L = long_sum / lp
    Q = short_sum / sp
    if not Q > 0:
        return float("nan")
    return L / Q
