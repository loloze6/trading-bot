"""Spec of IchimokuCloudCrossAgeComponent for the standard checks (component_harness.py), written by the components step: its settings (the defaults first) and a hand computation that uses only the rows up to bar t."""
CLASS = 'IchimokuCloudCrossAgeComponent'
SETTINGS = [{}, {"tenkan_period": 9, "kijun_period": 26, "senkou_period": 52, "displacement": 26, "max_bars": 120, "window": 250}]


def hand(df, params):
    tk = int(params.get("tenkan_period", 9))
    kj = int(params.get("kijun_period", 26))
    sk = int(params.get("senkou_period", 52))
    d = int(params.get("displacement", 26))
    cap = int(params.get("max_bars", 120))
    w = int(params.get("window", 250))
    highs = [float(x) for x in list(df["high"])]
    lows = [float(x) for x in list(df["low"])]
    closes = [float(x) for x in list(df["close"])]
    last = len(closes) - 1

    def is_nan(x):
        return x != x

    def midpoint(end, p):
        hi = None
        lo = None
        k = end - p + 1
        while k <= end:
            if is_nan(highs[k]) or is_nan(lows[k]):
                return float("nan")
            if hi is None or highs[k] > hi:
                hi = highs[k]
            if lo is None or lows[k] < lo:
                lo = lows[k]
            k = k + 1
        return (hi + lo) / 2.0

    # side of each bar from t-w+1 to t, oldest first
    side_list = []
    bar = last - w + 1
    while bar <= last:
        e = bar - d
        span_a = (midpoint(e, tk) + midpoint(e, kj)) / 2.0
        span_b = midpoint(e, sk)
        cl = closes[bar]
        if is_nan(span_a) or is_nan(span_b) or is_nan(cl):
            return float("nan")
        upper = span_a if span_a > span_b else span_b
        lower = span_b if span_a > span_b else span_a
        if cl > upper:
            side_list.append(1)
        elif cl < lower:
            side_list.append(-1)
        else:
            side_list.append(0)
        bar = bar + 1

    current = side_list[len(side_list) - 1]
    if current == 0:
        return 0.0
    run = 0
    pos = len(side_list) - 1
    while pos >= 0 and side_list[pos] == current:
        run = run + 1
        pos = pos - 1
    origin = 0
    while pos >= 0:
        if side_list[pos] != 0:
            origin = side_list[pos]
            break
        pos = pos - 1
    if origin != -current:
        return 0.0
    if run > cap:
        run = cap
    return float(current * run)
