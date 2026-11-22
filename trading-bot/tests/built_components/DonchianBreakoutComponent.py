"""Spec of DonchianBreakoutComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'DonchianBreakoutComponent'
SETTINGS = [{}, {"period": 30, "source": "high_low", "scaling_factor": 1.0}]


def hand(df, params):
    n = int(params.get("period", 48))
    sf = float(params.get("scaling_factor", 20.0))
    source = params.get("source", "close")
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    c = closes[last]
    if source == "high_low":
        highs_all = [float(x) for x in list(df["high"])]
        lows_all = [float(x) for x in list(df["low"])]
    else:
        highs_all = closes
        lows_all = closes
    tops = []
    bottoms = []
    i = last - n + 1
    while i <= last:
        tops.append(highs_all[i])
        bottoms.append(lows_all[i])
        i = i + 1
    if c != c:
        return float("nan")
    for x in tops + bottoms:
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
    if H == L:
        return 0.0 * sf
    mid = (H + L) / 2.0
    half = (H - L) / 2.0
    return (c - mid) / half * sf
