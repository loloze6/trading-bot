"""Spec of TopGainsShareOfRiseComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'TopGainsShareOfRiseComponent'
SETTINGS = [{}, {"period": 72, "k": 3}, {"period": 72, "k": 3, "form": "residual"}]


def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
    form = params.get("form", "share")
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    window = []
    i = last - n
    while i <= last:
        window.append(c[i])
        i = i + 1
    for x in window:
        if x != x:
            return float("nan")
        if not x > 0:
            return float("nan")
    rise = window[-1] / window[0] - 1.0
    gains = []
    j = 1
    while j < len(window):
        r = window[j] / window[j - 1] - 1.0
        if r > 0:
            gains.append(r)
        j = j + 1
    gains.sort(reverse=True)
    top = 0.0
    m = 0
    while m < k and m < len(gains):
        top = top + gains[m]
        m = m + 1
    if not rise > 0:
        return 0.0
    share = top / rise
    if share > 1.0:
        share = 1.0
    if form == "residual":
        return 1.0 - share
    return share
