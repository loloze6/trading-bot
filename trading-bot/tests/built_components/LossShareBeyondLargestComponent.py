"""Spec of LossShareBeyondLargestComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'LossShareBeyondLargestComponent'
SETTINGS = [{}, {"period": 72, "k": 3}]


def hand(df, params):
    n = int(params.get("period", 72))
    k = int(params.get("k", 3))
    c = [float(x) for x in list(df["close"])]
    last = len(c) - 1
    w = []
    i = last - n
    while i <= last:
        w.append(c[i])
        i = i + 1
    for x in w:
        if x != x or not x > 0:
            return float("nan")
    losses = []
    j = 1
    while j < len(w):
        ret = w[j] / w[j - 1] - 1.0
        if ret < 0:
            losses.append(-ret)
        j = j + 1
    if len(losses) <= k:
        share = 0.0
    else:
        total = 0.0
        for x in losses:
            total = total + x
        srt = sorted(losses, reverse=True)
        top = 0.0
        m = 0
        while m < k:
            top = top + srt[m]
            m = m + 1
        share = 1.0 - top / total if total > 0 else 0.0
        if share < 0:
            share = 0.0
    net = w[-1] / w[0] - 1.0
    if net > 0:
        return share
    if net < 0:
        return -share
    return 0.0
