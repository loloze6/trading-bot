"""Spec of RsiMidlineAgeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'RsiMidlineAgeComponent'
SETTINGS = [{}, {"period": 14, "max_bars": 60, "rsi_window": 100}]


def hand(df, params):
    p = int(params.get("period", 14))
    m = int(params.get("max_bars", 60))
    w = int(params.get("rsi_window", 100))
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    for x in closes[len(closes) - (m + w):]:
        if x != x:
            return float("nan")

    def rsi_above(i):
        seg = closes[i - w:i + 1]
        alpha = 1.0 / p
        g = None
        l = None
        for k in range(1, len(seg)):
            ch = seg[k] - seg[k - 1]
            up = ch if ch > 0 else 0.0
            dn = -ch if ch < 0 else 0.0
            if g is None:
                g = up
                l = dn
            else:
                g = g + alpha * (up - g)
                l = l + alpha * (dn - l)
        if g + l == 0:
            return False
        return 100.0 * g / (g + l) > 50.0

    now = rsi_above(last)
    count = 0
    i = last
    while count < m and rsi_above(i) == now:
        count = count + 1
        i = i - 1
    return float(count) if now else float(-count)
