"""Spec of TouchWeightedSupportBreakDepthComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'TouchWeightedSupportBreakDepthComponent'
SETTINGS = [{}, {"period": 90, "side": 2, "band": 2.0}]


def hand(df, params):
    period = int(params.get("period", 90))
    side = int(params.get("side", 2))
    band = float(params.get("band", 2.0))
    low = [float(x) for x in list(df["low"])]
    close = [float(x) for x in list(df["close"])]
    t = len(close) - 1
    c = close[t]
    if c != c:
        return float("nan")
    first = t - period
    for i in range(first, t):
        if low[i] != low[i]:
            return float("nan")
    levels = []
    i = first + side
    while i <= t - 1 - side:
        is_swing = True
        for k in range(1, side + 1):
            if not low[i] < low[i - k]:
                is_swing = False
            if not low[i] < low[i + k]:
                is_swing = False
        if is_swing:
            levels.append(low[i])
        i = i + 1
    chosen = None
    chosen_count = 0
    for lv in levels:
        if not lv >= c:
            continue
        if not lv > 0:
            return float("nan")
        count = 0
        for other in levels:
            if abs(other - lv) / lv * 100.0 <= band:
                count = count + 1
        if chosen is None or count > chosen_count or (count == chosen_count and lv < chosen):
            chosen = lv
            chosen_count = count
    if chosen is None:
        return 0.0
    return chosen_count * (chosen - c) / chosen * 100.0
