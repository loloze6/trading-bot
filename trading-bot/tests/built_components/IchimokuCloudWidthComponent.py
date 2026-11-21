"""Spec of IchimokuCloudWidthComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'IchimokuCloudWidthComponent'
SETTINGS = [{}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26}, {"form": "proximity"}]


def hand(df, params):
    tp = int(params.get("tenkan_period", 9))
    kp = int(params.get("kijun_period", 26))
    sp = int(params.get("senkou_period", 52))
    d = int(params.get("displacement", 26))
    form = params.get("form", "width")
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    cl = [float(x) for x in list(df["close"])]
    t = len(cl) - 1
    e = t - d

    def midpoint(p):
        top = None
        bot = None
        j = e - p + 1
        while j <= e:
            h = hi[j]
            l = lo[j]
            if h != h or l != l:
                return float("nan")
            if top is None or h > top:
                top = h
            if bot is None or l < bot:
                bot = l
            j = j + 1
        return (top + bot) / 2.0

    m_t = midpoint(tp)
    m_k = midpoint(kp)
    m_s = midpoint(sp)
    c = cl[t]
    if m_t != m_t or m_k != m_k or m_s != m_s or c != c:
        return float("nan")
    if not c > 0:
        return float("nan")
    span_a = (m_t + m_k) / 2.0
    span_b = m_s
    diff = span_a - span_b
    if diff < 0:
        diff = -diff
    width = diff / c * 100.0
    if form == "proximity":
        return 1.0 / (1.0 + width)
    return width
