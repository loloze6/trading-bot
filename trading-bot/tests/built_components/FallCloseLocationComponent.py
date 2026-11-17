"""Spec of FallCloseLocationComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'FallCloseLocationComponent'
SETTINGS = [{}, {"vol_period": 60}]


def hand(df, params):
    import math
    n = int(params.get("vol_period", 60))
    c = [float(x) for x in list(df["close"])]
    h = float(list(df["high"])[-1])
    l = float(list(df["low"])[-1])
    last = len(c) - 1
    window = []
    i = last - n
    while i <= last:
        window.append(c[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
    if h != h or l != l:
        return float("nan")
    rets = []
    k = 1
    while k < len(window):
        base = window[k - 1]
        if not base > 0:
            return float("nan")
        rets.append(window[k] / base - 1.0)
        k = k + 1
    m = sum(rets) / len(rets)
    ss = 0.0
    for x in rets:
        ss = ss + (x - m) * (x - m)
    s = math.sqrt(ss / (len(rets) - 1))
    today = rets[-1]
    if s > 0:
        fall = -today / s
    else:
        fall = 0.0
    if fall < 0:
        fall = 0.0
    if h == l:
        loc = 0.5
    else:
        loc = (h - c[last]) / (h - l)
    return fall * loc
