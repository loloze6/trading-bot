"""Spec of IchimokuCloudWidthComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'IchimokuCloudWidthComponent'
SETTINGS = [{}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26}]


def hand(df, params):
    tk = int(params.get("tenkan_period", 9))
    kj = int(params.get("kijun_period", 26))
    sk = int(params.get("senkou_period", 52))
    d = int(params.get("displacement", 26))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1
    e = last - d

    def midpoint(p):
        hi = None
        lo = None
        j = e - p + 1
        while j <= e:
            h = highs[j]
            l = lows[j]
            if h != h or l != l:
                return float("nan")
            if hi is None or h > hi:
                hi = h
            if lo is None or l < lo:
                lo = l
            j = j + 1
        return (hi + lo) / 2.0

    m_tk = midpoint(tk)
    m_kj = midpoint(kj)
    m_sk = midpoint(sk)
    if m_tk != m_tk or m_kj != m_kj or m_sk != m_sk:
        return float("nan")
    span_a = (m_tk + m_kj) / 2.0
    span_b = m_sk
    c = closes[last]
    if c != c or not c > 0:
        return float("nan")
    width = span_a - span_b
    if width < 0:
        width = -width
    return width / c * 100.0
