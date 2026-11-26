"""Spec of ClosingRangeInUsualMovesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ClosingRangeInUsualMovesComponent'
SETTINGS = [{}, {"period": 60, "window": 60, "form": "width"}]


def hand(df, params):
    period = int(params.get("period", 60))
    window = int(params.get("window", 60))
    form = params.get("form", "width")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    first = t - max(period, window)
    for i in range(first, t + 1):
        x = c[i]
        if x != x or not x > 0:
            return float("nan")
    # closing range over bars t-period .. t-1
    hi = c[t - period]
    lo = c[t - period]
    for i in range(t - period, t):
        if c[i] > hi:
            hi = c[i]
        if c[i] < lo:
            lo = c[i]
    # usual one-bar move: returns j = t-window+1 .. t
    total = 0.0
    for j in range(t - window + 1, t + 1):
        r = c[j] / c[j - 1] - 1.0
        total = total + (r if r >= 0 else -r)
    m = total / window
    if m == 0.0:
        w = 0.0
    else:
        w = (hi - lo) / c[t - 1] / m
    if form == "compression":
        return 1.0 / (1.0 + w)
    return w
