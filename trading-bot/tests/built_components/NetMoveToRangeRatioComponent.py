"""Spec of NetMoveToRangeRatioComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'NetMoveToRangeRatioComponent'
SETTINGS = [{}, {"period": 30}, {"period": 30, "source": "close"}]


def hand(df, params):
    n = int(params.get("period", 30))
    source = params.get("source", "high_low")
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    now = c[last]
    base = c[last - n]
    if source == "close":
        hs = [c[i] for i in range(last - n + 1, last + 1)]
        ls = list(hs)
    else:
        h_all = [float(x) for x in list(df["high"])]
        l_all = [float(x) for x in list(df["low"])]
        hs = [h_all[i] for i in range(last - n + 1, last + 1)]
        ls = [l_all[i] for i in range(last - n + 1, last + 1)]
    for x in [now, base] + hs + ls:
        if x != x:
            return float("nan")
    top = hs[0]
    for x in hs:
        if x > top:
            top = x
    bottom = ls[0]
    for x in ls:
        if x < bottom:
            bottom = x
    width = top - bottom
    if width == 0:
        return 0.0
    move = now - base
    if move < 0:
        move = -move
    return move / width
