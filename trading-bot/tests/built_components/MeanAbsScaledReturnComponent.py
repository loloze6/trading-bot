"""Spec of MeanAbsScaledReturnComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'MeanAbsScaledReturnComponent'
SETTINGS = [{}, {"period": 24, "window": 720}, {"period": 3, "window": 30, "base": "mean_relative_range"}]


def hand(df, params):
    p = int(params.get("period", 24))
    w = int(params.get("window", 720))
    base = params.get("base", "mean_abs_return")
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    def bad(x):
        return x != x or not x > 0

    if base == "mean_relative_range":
        h = [float(x) for x in list(df["high"])]
        lo = [float(x) for x in list(df["low"])]
        total = 0.0
        for i in range(t - w + 1, t + 1):
            if h[i] != h[i] or lo[i] != lo[i] or bad(c[i]):
                return float("nan")
            total = total + (h[i] - lo[i]) / c[i]
        if bad(c[t - p]):
            return float("nan")
        m = total / w
    else:
        for i in range(t - w - p + 1, t + 1):
            if bad(c[i]):
                return float("nan")
        total = 0.0
        for i in range(t - w + 1, t + 1):
            total = total + abs(c[i] / c[i - p] - 1.0)
        m = total / w
    r = c[t] / c[t - p] - 1.0
    if m == 0:
        return 0.0
    return r / m
