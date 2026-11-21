"""Spec of IchimokuCloudSlopeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'IchimokuCloudSlopeComponent'
SETTINGS = [{}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "lookback": 26}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "lookback": 26, "form": "proximity"}]


def hand(df, params):
    tp = int(params.get("tenkan_period", 9))
    kp = int(params.get("kijun_period", 26))
    sp = int(params.get("senkou_period", 52))
    disp = int(params.get("displacement", 26))
    lb = int(params.get("lookback", 26))
    form = params.get("form", "percent")
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    t = len(highs) - 1

    def midpoint(end, p):
        top = None
        bot = None
        j = end - p + 1
        while j <= end:
            h = highs[j]
            l = lows[j]
            if h != h or l != l:
                return float("nan")
            if top is None or h > top:
                top = h
            if bot is None or l < bot:
                bot = l
            j = j + 1
        return (top + bot) / 2.0

    def cloud_level(bar):
        end = bar - disp
        span_a = (midpoint(end, tp) + midpoint(end, kp)) / 2.0
        span_b = midpoint(end, sp)
        return (span_a + span_b) / 2.0

    now = cloud_level(t)
    then = cloud_level(t - lb)
    if now != now or then != then:
        return float("nan")
    if not then > 0:
        return float("nan")
    slope = (now - then) / then * 100.0
    if form == "proximity":
        fall = -slope
        if fall < 0:
            fall = 0.0
        return 1.0 / (1.0 + fall)
    return slope
