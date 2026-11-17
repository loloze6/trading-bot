"""Spec of RsiAboveMidlineShareComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RsiAboveMidlineShareComponent'
SETTINGS = [{}, {"period": 14, "window": 30, "rsi_window": 100}]


def hand(df, params):
    p = int(params.get("period", 14))
    w = int(params.get("window", 30))
    rw = int(params.get("rsi_window", 100))
    c = [float(x) for x in list(df["close"])]
    c = c[-(w + rw):]
    for x in c:
        if x != x:
            return float("nan")
    a = 1.0 / p
    count = 0
    # bar i = t - k, k = w-1 .. 0; its rsi_window changes use closes c[e - rw] .. c[e]
    for k in range(w - 1, -1, -1):
        e = len(c) - 1 - k
        G = None
        L = None
        for m in range(e - rw + 1, e + 1):
            ch = c[m] - c[m - 1]
            gain = ch if ch > 0 else 0.0
            loss = -ch if ch < 0 else 0.0
            if G is None:
                G = gain
                L = loss
            else:
                G = (1 - a) * G + a * gain
                L = (1 - a) * L + a * loss
        if G + L > 0:
            rsi = 100.0 * G / (G + L)
        else:
            rsi = 50.0
        if G > L:
            count = count + 1
    return count / w - 0.5
