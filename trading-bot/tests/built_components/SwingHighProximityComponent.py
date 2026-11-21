"""Spec of SwingHighProximityComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'SwingHighProximityComponent'
SETTINGS = [{}, {"period": 90, "side": 2, "power": 1.0}]


def hand(df, params):
    n = int(params.get("period", 90))
    s = int(params.get("side", 2))
    p = float(params.get("power", 1.0))
    h_all = [float(x) for x in list(df["high"])]
    c_all = [float(x) for x in list(df["close"])]
    h = h_all[len(h_all) - n:]
    c = c_all[len(c_all) - 1]
    for x in h:
        if x != x:
            return float("nan")
    if c != c:
        return float("nan")
    levels = []
    i = s
    while i <= n - 1 - s:
        ok = True
        j = i - s
        while j <= i + s:
            if j != i and h[j] > h[i]:
                ok = False
            j = j + 1
        if ok:
            levels.append(h[i])
        i = i + 1
    best = None
    for lv in levels:
        if lv >= c:
            if best is None or lv < best:
                best = lv
    if best is None:
        return 0.0
    if not best > 0:
        return float("nan")
    gap = (best - c) / best * 100.0
    return (1.0 / (1.0 + gap)) ** p
