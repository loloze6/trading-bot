"""Spec of RangeCompressionRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RangeCompressionRatioComponent'
SETTINGS = [{}, {"short_period": 20, "long_period": 100}, {"short_period": 20, "long_period": 100, "exclude_current": 1}, {"short_period": 20, "long_period": 100, "form": "width"}, {"short_period": 12, "long_period": 180, "exclude_current": 1, "base": "mean_bar_range", "form": "width"}, {"short_period": 12, "long_period": 180, "exclude_current": 2, "form": "compression", "base": "mean_bar_range"}]


def hand(df, params):
    sp = int(params.get("short_period", 20))
    lp = int(params.get("long_period", 100))
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "compression")
    base = params.get("base", "range")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    t = len(h) - 1

    if ex == 1:
        long_idx = list(range(t - lp, t))
        short_idx = list(range(t - sp, t))
    elif ex == 2:
        long_idx = list(range(t - lp + 1, t + 1))
        short_idx = list(range(t - sp, t))
    else:
        long_idx = list(range(t - lp + 1, t + 1))
        short_idx = list(range(t - sp + 1, t + 1))

    for i in long_idx + short_idx:
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")

    top = h[short_idx[0]]
    bottom = l[short_idx[0]]
    for i in short_idx:
        if h[i] > top:
            top = h[i]
        if l[i] < bottom:
            bottom = l[i]
    s_range = top - bottom

    if base == "mean_bar_range":
        total = 0.0
        for i in long_idx:
            total = total + (h[i] - l[i])
        b = total / len(long_idx)
    else:
        top = h[long_idx[0]]
        bottom = l[long_idx[0]]
        for i in long_idx:
            if h[i] > top:
                top = h[i]
            if l[i] < bottom:
                bottom = l[i]
        b = top - bottom

    if b == 0:
        return 0.0 if form == "compression" else 1.0
    ratio = s_range / b
    if form == "compression":
        return 1.0 - ratio
    return ratio
