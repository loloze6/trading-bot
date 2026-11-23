"""Spec of BreakoutInMeanRangesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'BreakoutInMeanRangesComponent'
SETTINGS = [{}, {"period": 12, "base_period": 180}, {"period": 12, "base_period": 180, "side": "below"}, {"period": 1, "base_period": 20, "side": "below", "high_current": 1, "base_exclude_current": 1}]


def hand(df, params):
    period = int(params.get("period", 12))
    base_period = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hc = int(params.get("high_current", 0))
    bx = int(params.get("base_exclude_current", 0))
    h = [float(x) for x in list(df["high"])]
    l = [float(x) for x in list(df["low"])]
    c = [float(x) for x in list(df["close"])]
    t = len(c) - 1
    # the high's stretch
    if hc == 1:
        idx = [t - k for k in range(period)]            # t-period+1 .. t
    else:
        idx = [t - 1 - k for k in range(period)]        # t-period .. t-1
    highs = [h[i] for i in idx]
    # the base of mean bar ranges
    end = t - bx
    bidx = [end - k for k in range(base_period)]
    ranges = []
    for i in bidx:
        if h[i] != h[i] or l[i] != l[i]:
            return float("nan")
        ranges.append(h[i] - l[i])
    for x in highs:
        if x != x:
            return float("nan")
    if c[t] != c[t]:
        return float("nan")
    H = highs[0]
    for x in highs:
        if x > H:
            H = x
    total = 0.0
    for r in ranges:
        total += r
    B = total / len(ranges)
    if B == 0:
        return 0.0
    if side == "above":
        d = c[t] - H
    else:
        d = H - c[t]
    if d < 0:
        d = 0.0
    return d / B
