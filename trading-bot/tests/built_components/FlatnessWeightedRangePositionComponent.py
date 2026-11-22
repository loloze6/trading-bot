"""Spec of FlatnessWeightedRangePositionComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FlatnessWeightedRangePositionComponent'
SETTINGS = [{}, {"period": 30}, {"period": 30, "source": "high_low"}]


def hand(df, params):
    p = int(params.get("period", 30))
    source = params.get("source", "close")
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    c_t = c[last]
    c_b = c[last - p]
    if source == "high_low":
        h = [float(x) for x in list(df["high"])]
        l = [float(x) for x in list(df["low"])]
        tops = []
        bottoms = []
        i = last - p + 1
        while i <= last:
            tops.append(h[i])
            bottoms.append(l[i])
            i = i + 1
        for x in tops + bottoms + [c_t, c_b]:
            if x != x:
                return float("nan")
    else:
        tops = []
        i = last - p + 1
        while i <= last:
            tops.append(c[i])
            i = i + 1
        bottoms = list(tops)
        for x in tops + [c_b]:
            if x != x:
                return float("nan")
    H = tops[0]
    for x in tops:
        if x > H:
            H = x
    L = bottoms[0]
    for x in bottoms:
        if x < L:
            L = x
    width = H - L
    if width == 0:
        return 0.0
    position = (c_t - L) / width
    net = c_t - c_b
    if net < 0:
        net = -net
    flatness = 1.0 - net / width
    return (2.0 * position - 1.0) * flatness
