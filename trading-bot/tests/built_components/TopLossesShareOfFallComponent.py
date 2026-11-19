"""Spec of TopLossesShareOfFallComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'TopLossesShareOfFallComponent'
SETTINGS = [{}, {"period": 72, "k": 3, "form": "share"}]


def hand(df, params):
    p = int(params.get("period", 72))
    k = int(params.get("k", 3))
    form = params.get("form", "share")
    c = [float(x) for x in list(df["close"])]
    w = c[len(c) - p - 1:]
    for x in w:
        if x != x:
            return float("nan")
    start = w[0]
    end = w[len(w) - 1]
    net_fall = start - end
    if not net_fall > 0:
        return 0.0
    drops = []
    j = 1
    while j < len(w):
        change = w[j] - w[j - 1]
        if change < 0:
            drops.append(-change)
        j = j + 1
    drops = sorted(drops, reverse=True)
    t = 0.0
    n = 0
    for x in drops:
        if n >= k:
            break
        t = t + x
        n = n + 1
    share = t / net_fall
    if form == "weighted":
        if not start > 0:
            return float("nan")
        return share * (net_fall / start * 100.0)
    return share
