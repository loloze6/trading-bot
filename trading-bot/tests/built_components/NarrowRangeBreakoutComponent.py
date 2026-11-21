"""Spec of NarrowRangeBreakoutComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'NarrowRangeBreakoutComponent'
SETTINGS = [{}, {"period": 12, "base_period": 180}, {"period": 12, "base_period": 180, "side": "below"}]


def hand(df, params):
    p = int(params.get("period", 12))
    bp = int(params.get("base_period", 180))
    side = params.get("side", "above")
    hs = [float(x) for x in list(df["high"])]
    ls = [float(x) for x in list(df["low"])]
    cs = [float(x) for x in list(df["close"])]
    t = len(cs) - 1
    c = cs[t]
    # the stretch: bars t-p .. t-1
    st_h = []
    st_l = []
    i = t - p
    while i <= t - 1:
        st_h.append(hs[i])
        st_l.append(ls[i])
        i = i + 1
    # the base: bars t-bp+1 .. t
    ranges = []
    nan_seen = False
    i = t - bp + 1
    while i <= t:
        if hs[i] != hs[i] or ls[i] != ls[i]:
            nan_seen = True
        ranges.append(hs[i] - ls[i])
        i = i + 1
    for x in st_h + st_l:
        if x != x:
            nan_seen = True
    if c != c:
        nan_seen = True
    if nan_seen:
        return float("nan")
    if not c > 0:
        return float("nan")
    top = st_h[0]
    for x in st_h:
        if x > top:
            top = x
    bottom = st_l[0]
    for x in st_l:
        if x < bottom:
            bottom = x
    s = top - bottom
    if s == 0:
        return 0.0
    total = 0.0
    for r in ranges:
        total = total + r
    b = total / len(ranges)
    if side == "below":
        depth = bottom - c
    else:
        depth = c - top
    if depth < 0:
        depth = 0.0
    return depth / c * 100.0 * b / s
