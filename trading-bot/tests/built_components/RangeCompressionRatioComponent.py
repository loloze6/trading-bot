"""Spec of RangeCompressionRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RangeCompressionRatioComponent'
SETTINGS = [{}, {"short_period": 20, "long_period": 100}, {"short_period": 20, "long_period": 100, "exclude_current": 1}, {"short_period": 20, "long_period": 100, "form": "width"}]


def hand(df, params):
    sp = int(params.get("short_period", 20))
    lp = int(params.get("long_period", 100))
    ex = int(params.get("exclude_current", 0))
    form = params.get("form", "compression")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    last = len(h) - 1 - ex
    for i in range(last - lp + 1, last + 1):
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
    hi_l = h[last - lp + 1]
    lo_l = l[last - lp + 1]
    for i in range(last - lp + 1, last + 1):
        if h[i] > hi_l:
            hi_l = h[i]
        if l[i] < lo_l:
            lo_l = l[i]
    hi_s = h[last - sp + 1]
    lo_s = l[last - sp + 1]
    for i in range(last - sp + 1, last + 1):
        if h[i] > hi_s:
            hi_s = h[i]
        if l[i] < lo_s:
            lo_s = l[i]
    long_range = hi_l - lo_l
    short_range = hi_s - lo_s
    if form == "width":
        if not long_range > 0:
            return 1.0
        return short_range / long_range
    if not long_range > 0:
        return 0.0
    return 1.0 - short_range / long_range
