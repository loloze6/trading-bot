"""Spec of RsiMidlineAgeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RsiMidlineAgeComponent'
SETTINGS = [{}, {"period": 14, "max_bars": 60, "rsi_window": 100}]


def hand(df, params):
    p = int(params.get("period", 14))
    m = int(params.get("max_bars", 60))
    w = int(params.get("rsi_window", 100))
    c = [float(x) for x in list(df["close"])]
    c = c[-(m + w):]
    for x in c:
        if x != x:
            return float("nan")

    def upper(i):
        # bar i (index into c): the w changes ending at i use closes c[i-w] .. c[i]
        a = 1.0 / p
        G = None
        L = None
        for k in range(i - w + 1, i + 1):
            ch = c[k] - c[k - 1]
            gain = ch if ch > 0 else 0.0
            loss = -ch if ch < 0 else 0.0
            if G is None:
                G, L = gain, loss
            else:
                G = (1.0 - a) * G + a * gain
                L = (1.0 - a) * L + a * loss
        # RSI > 50 is G > L (G + L = 0 is RSI 50, the lower side)
        return G > L

    last = len(c) - 1
    side = upper(last)
    n = 1
    while n < m and upper(last - n) == side:
        n += 1
    return float(n) if side else float(-n)
