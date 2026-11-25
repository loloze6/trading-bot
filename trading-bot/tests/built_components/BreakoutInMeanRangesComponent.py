"""Spec of BreakoutInMeanRangesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutInMeanRangesComponent'
SETTINGS = [{}, {"period": 12, "base_period": 180}, {"period": 12, "base_period": 180, "side": "below"}, {"period": 1, "base_period": 20, "side": "below", "high_current": 1, "base_exclude_current": 1}, {"period": 10, "base_period": 30, "side": "below", "extreme": "low"}]


def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hc = int(params.get("high_current", 0))
    be = int(params.get("base_exclude_current", 0))
    extreme = params.get("extreme", "high")
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1

    # the stretch: bars t-p .. t-1 (hc 0) or t-p+1 .. t (hc 1)
    first = t - p + hc
    last = t - 1 + hc
    vals = []
    i = first
    while i <= last:
        vals.append(h[i] if extreme == "high" else l[i])
        i += 1

    # the base: bars t-bp+1 .. t (be 0) or t-bp .. t-1 (be 1)
    ranges = []
    for k in range(bp):
        j = t - be - k
        if h[j] != h[j] or l[j] != l[j]:
            return float("nan")
        ranges.append(h[j] - l[j])

    for v in vals:
        if v != v:
            return float("nan")
    if c[t] != c[t]:
        return float("nan")

    level = vals[0]
    for v in vals:
        if extreme == "high":
            if v > level:
                level = v
        else:
            if v < level:
                level = v

    total = 0.0
    for r in ranges:
        total += r
    B = total / bp
    if B == 0:
        return 0.0

    if side == "above":
        d = c[t] - level
    else:
        d = level - c[t]
    if d < 0:
        d = 0.0
    return d / B
