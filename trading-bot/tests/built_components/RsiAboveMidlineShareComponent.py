"""Spec of RsiAboveMidlineShareComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RsiAboveMidlineShareComponent'
SETTINGS = [{}, {"period": 14, "window": 30, "rsi_window": 100}, {"period": 14, "window": 30, "rsi_window": 100, "side": "below"}]


def hand(df, params):
    period = int(params.get("period", 14))
    window = int(params.get("window", 30))
    rsi_window = int(params.get("rsi_window", 100))
    side = params.get("side", "above")
    c = [float(x) for x in list(df["close"])]
    c = c[-(window + rsi_window):]
    for x in c:
        if x != x:
            return float("nan")
    a = 1.0 / period
    hits = 0
    # bar t is the last element; bar t-m for m = window-1 .. 0
    for m in range(window - 1, -1, -1):
        end = len(c) - 1 - m              # index of bar i in c
        start = end - rsi_window          # rsi_window changes need closes start .. end
        G = None
        L = None
        for k in range(start + 1, end + 1):
            d = c[k] - c[k - 1]
            up = d if d > 0 else 0.0
            dn = -d if d < 0 else 0.0
            if G is None:
                G, L = up, dn
            else:
                G = G + a * (up - G)
                L = L + a * (dn - L)
        if G + L == 0:
            rsi = 50.0
        else:
            rsi = 100.0 * G / (G + L)
        if side == "above" and G > L and rsi > 50.0:
            hits += 1
        elif side == "below" and G < L and rsi < 50.0:
            hits += 1
    return hits / window - 0.5
