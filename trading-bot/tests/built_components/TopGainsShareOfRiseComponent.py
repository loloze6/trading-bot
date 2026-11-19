"""Spec of TopGainsShareOfRiseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'TopGainsShareOfRiseComponent'
SETTINGS = [{}, {"period": 72, "k": 3}]


def hand(df, params):
    p = int(params.get("period", 72))
    k = int(params.get("k", 3))
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    window = []
    i = last - p
    while i <= last:
        window.append(closes[i])
        i = i + 1
    for x in window:
        if x != x or not x > 0:
            return float("nan")
    gains = []
    j = 1
    while j < len(window):
        ret = window[j] / window[j - 1] - 1.0
        if ret > 0:
            gains.append(ret)
        j = j + 1
    rise = window[-1] / window[0] - 1.0
    if not rise > 0:
        return 0.0
    gains.sort(reverse=True)
    total = 0.0
    n = 0
    for g in gains:
        if n >= k:
            break
        total = total + g
        n = n + 1
    share = total / rise
    if share > 1.0:
        share = 1.0
    return share
