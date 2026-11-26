"""Spec of ReclaimedPriorLowPierceDepthComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'ReclaimedPriorLowPierceDepthComponent'
SETTINGS = [{}, {"period": 30}]


def hand(df, params):
    n = int(params.get("period", 30))
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(lows) - 1
    low_t = lows[t]
    close_t = closes[t]
    if low_t != low_t or close_t != close_t:
        return float("nan")
    L = None
    for i in range(t - n, t):
        x = lows[i]
        if x != x:
            return float("nan")
        if L is None or x < L:
            L = x
    if not L > 0:
        return float("nan")
    if close_t < L:
        return 0.0
    depth = L - low_t
    if depth < 0:
        depth = 0.0
    return depth / L * 100.0
