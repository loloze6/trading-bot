"""Spec of IchimokuCloudSlopeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'IchimokuCloudSlopeComponent'
SETTINGS = [{}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "lookback": 26}]


def hand(df, params):
    tk = int(params.get("tenkan_period", 9))
    kj = int(params.get("kijun_period", 26))
    sk = int(params.get("senkou_period", 52))
    d = int(params.get("displacement", 26))
    lb = int(params.get("lookback", 26))
    hi = [float(x) for x in list(df["high"])]
    lo = [float(x) for x in list(df["low"])]
    last = len(hi) - 1

    def midpoint(e, p):
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

    def level(i):
        e = i - d
        span_a = (midpoint(e, tk) + midpoint(e, kj)) / 2.0
        span_b = midpoint(e, sk)
        return (span_a + span_b) / 2.0

    now = level(last)
    then = level(last - lb)
    if now != now or then != then:
        return float("nan")
    if not then > 0:
        return float("nan")
    return (now - then) / then * 100.0
