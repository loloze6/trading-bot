"""Spec of RiseBeyondLargestMovesComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RiseBeyondLargestMovesComponent'
SETTINGS = [{}, {"period": 72, "k": 3}]


def hand(df, params):
    import math
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
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
    R = math.log(window[-1] / window[0])
    ups = []
    j = 1
    while j < len(window):
        r = math.log(window[j] / window[j - 1])
        if r > 0:
            ups.append(r)
        j = j + 1
    ups.sort(reverse=True)
    T = 0.0
    m = 0
    while m < k and m < len(ups):
        T = T + ups[m]
        m = m + 1
    if R > 0:
        share = T / R
        if share > 1.0:
            share = 1.0
        return R * (1.0 - share)
    return 0.0
