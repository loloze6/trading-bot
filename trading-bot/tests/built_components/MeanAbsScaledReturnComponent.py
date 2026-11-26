"""Spec of MeanAbsScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanAbsScaledReturnComponent'
SETTINGS = [{}, {"period": 24, "window": 720}, {"period": 3, "window": 30, "base": "mean_relative_range"}, {"period": 7, "window": 30, "base": "mean_abs_return", "form": "centred"}]


def hand(df, params):
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    base = params.get("base", "mean_abs_return")
    form = params.get("form", "ratio")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    if base == "mean_abs_return":
        # every close used: bars t-w-p+1 .. t
        for k in range(t - w - p + 1, t + 1):
            if c[k] != c[k] or not c[k] > 0:
                return float("nan")
        total = 0.0
        for i in range(t - w + 1, t + 1):
            total += abs(c[i] / c[i - p] - 1.0)
        m = total / w
    else:
        h = [float(x) for x in list(df["high"])]
        lo = [float(x) for x in list(df["low"])]
        if c[t - p] != c[t - p] or not c[t - p] > 0:
            return float("nan")
        total = 0.0
        for i in range(t - w + 1, t + 1):
            if c[i] != c[i] or h[i] != h[i] or lo[i] != lo[i] or not c[i] > 0:
                return float("nan")
            total += (h[i] - lo[i]) / c[i]
        m = total / w
    r = c[t] / c[t - p] - 1.0
    x = 0.0 if m == 0 else r / m
    if form == "centred":
        x -= 1.0
    return x
