"""Spec of IchimokuCloudPositionComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'IchimokuCloudPositionComponent'
SETTINGS = [{}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "edge": "nearest"}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "edge": "nearest", "base": "close"}]


def hand(df, params):
    tk = int(params.get("tenkan_period", 9))
    kj = int(params.get("kijun_period", 26))
    sk = int(params.get("senkou_period", 52))
    disp = int(params.get("displacement", 26))
    edge = params.get("edge", "top")
    base = params.get("base", "edge")
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    t = len(closes) - 1
    e = t - disp

    def midpoint(p):
        hi = None
        lw = None
        i = e - p + 1
        while i <= e:
            if highs[i] != highs[i] or lows[i] != lows[i]:
                return None
            if hi is None or highs[i] > hi:
                hi = highs[i]
            if lw is None or lows[i] < lw:
                lw = lows[i]
            i = i + 1
        return (hi + lw) / 2.0

    m_tk = midpoint(tk)
    m_kj = midpoint(kj)
    m_sk = midpoint(sk)
    close_t = closes[t]
    if m_tk is None or m_kj is None or m_sk is None or close_t != close_t:
        return float("nan")
    span_a = (m_tk + m_kj) / 2.0
    span_b = m_sk
    top = span_a if span_a > span_b else span_b
    bottom = span_b if span_a > span_b else span_a
    if edge == "top":
        dist = close_t - top
        ref = top
    else:
        if close_t > top:
            dist = close_t - top
            ref = top
        elif close_t < bottom:
            dist = close_t - bottom
            ref = bottom
        else:
            dist = 0.0
            ref = bottom
    divisor = close_t if base == "close" else ref
    if not divisor > 0:
        return float("nan")
    return dist / divisor * 100.0
